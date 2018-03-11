from jupyter_client import KernelManager
from queue import Empty
import copy
import io


class Kernel(object):
    def __init__(self, kernel_name):
        self.kernel = KernelManager(kernel_name = kernel_name)

    def start(self):
        self.kernel.start_kernel()
        self.client = self.kernel.client()
        self.client.start_channels()
        try:
            self.client.wait_for_ready()
        except RuntimeError:
            print("Unable to start kernel.")
            this.close()
            raise

    def close(self):
        self.client.stop_channels()
        self.kernel.shutdown_kernel()

    def execute_chunk(self, chunk):
        chunk['messages'] = []
        self.client.execute_interactive(chunk['input'], store_history=False,
            allow_stdin=False, output_hook=lambda msg: chunk['messages'].append(msg) if msg['msg_type'] in ('display_data', 'execute_result', 'stream') else None)


class Jupyter(object):
    def __init__(self):
        self.kernels = {}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        for kernel_id, kernel in self.kernels.items():
            kernel.close()

    def apply(self, chunks):
        for chunk in chunks:
            if (chunk['type'] == 'code'):
                self.execute_chunk(chunk)

    def execute_chunk(self, chunk):
        kernel = self.get_kernel(chunk)
        kernel.execute_chunk(chunk)

    def get_kernel(self, chunk):
        kernel_name = chunk['options']['kernel']
        kernel_id = (kernel_name + '|' + chunk['options']['session']) if 'session' in chunk['options'] else kernel_name
        if kernel_id in self.kernels:
            return self.kernels[kernel_id]

        kernel = Kernel(kernel_name)
        self.kernels[kernel_id] = kernel
        kernel.start()

        return kernel
