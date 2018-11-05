from ..Chunk import Chunk
from jupyter_client import KernelManager


class Kernel(object):
    def __init__(self, kernel_name):
        self.kernel = KernelManager(kernel_name=kernel_name)

    def start(self):
        self.kernel.start_kernel()
        self.client = self.kernel.client()
        self.client.start_channels()
        try:
            self.client.wait_for_ready()
        except RuntimeError:
            print("[metys] Unable to start kernel.")
            self.close()
            raise
        info = self.client.kernel_info(reply=True)
        if info and "content" in info and "language_info" in info["content"]:
            self.language_info = info["content"]["language_info"]

    def shutdown(self):
        self.client.shutdown()

    def is_complete(self, code):
        return self.client.is_complete(code)

    def execute_chunk(self, chunk):
        chunk.messages = []
        if hasattr(self, "language_info"):
            chunk.language_info = self.language_info
        input = (
            chunk.input.format(**chunk.options)
            if chunk.options["expand_options"]
            else chunk.input
        )

        if "code_template" in chunk.options:
            input = chunk.options["code_template"].format(input, **chunk.options)

        def output_hook(msg):
            return (
                chunk.messages.append(msg)
                if msg["msg_type"] in ("display_data", "execute_result", "stream")
                else None
            )

        chunk.reply = self.client.execute_interactive(
            input, store_history=False, allow_stdin=False, output_hook=output_hook
        )


class EvaluateCode(object):
    def __init__(self, root):
        self.kernels = {}
        self.root = root

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for kernel_id, kernel in self.kernels.items():
            kernel.shutdown()

    def apply(self):
        chunks = []

        for chunk in self.root.chunks:
            if chunk.type == "group":
                chunks.append(chunk)
                with EvaluateCode(chunk) as p:
                    p.apply()
            elif chunk.type == "code" and chunk.options["evaluate"]:
                if chunk.options["restart"]:
                    self.shutdown_kernel(chunk)
                kernel = self.get_kernel(chunk)
                if chunk.options["split"]:
                    input = ""
                    num = 0
                    for line in chunk.input.strip("\n").splitlines(True):
                        input += line
                        if kernel.is_complete(input):
                            ch = Chunk("code", input, chunk.options)
                            num += 1
                            ch.options["name"] = chunk.options["name"] + "-" + str(num)
                            kernel.execute_chunk(ch)
                            chunks.append(ch)
                            chunks.append(Chunk("text", "\n", chunk.options))
                            input = ""
                else:
                    chunks.append(chunk)
                    kernel.execute_chunk(chunk)
            else:
                chunks.append(chunk)
        self.root.chunks = chunks

    def execute_chunk(self, chunk):
        kernel = self.get_kernel(chunk)
        kernel.execute_chunk(chunk)

    def shutdown_kernel(self, chunk):
        kernel_name = chunk.options["kernel"]
        kernel_id = (
            (kernel_name + "|" + chunk.options["session"])
            if "session" in chunk.options
            else kernel_name
        )
        if kernel_id in self.kernels:
            self.kernels[kernel_id].shutdown()
            del self.kernels[kernel_id]

    def get_kernel(self, chunk):
        kernel_name = chunk.options["kernel"]
        kernel_id = (
            (kernel_name + "|" + chunk.options["session"])
            if "session" in chunk.options
            else kernel_name
        )
        if kernel_id in self.kernels:
            return self.kernels[kernel_id]

        kernel = Kernel(kernel_name)
        self.kernels[kernel_id] = kernel
        kernel.start()

        return kernel
