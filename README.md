# Metys

Metys is scientific report generator and a literate programming tool similar to
knitr or Pweave. Like Pweave, Metys uses the Jupyter protocol to run code
embedded in the source document. Unlike Pweave, Metys can access multiple
Jupyter kernels within the same source document and can also create multiple
separate sesssions of the same kernel.

Metys is currently alpha level software.

## Processing Metys Documents

Metys is currently run from the command line by using the following.

```sh
python cli/main.py foo.tmt
```

There are many command line options available. A short description will be shown
with the following.

```sh
python cli/main.py --help
```

## Input Formats

Metys can parse source documents in noweb, MarkDown or Metys format. The format
of the source document will be determined by the file extension or by the
`--parser` command line option if specified. Source documents with a file
extension ending with `nw` are assumed to be noweb documents. Those with a file
extension ending with `md` are assumed to be MarkDown documents. All other files
are assumed to be in Metys format.

Parsing the source document results in a series of logical chunks. These chunks
are either text, code or group chunks. Text chunks contain text which is copied
verbatim to the output document. Code chunks are evaluated by a Jupyter kernel
and the results are formatted in the output document as per the local and global
options specified. Group chunks are used to set options for a collection of
chunks or to include subfiles.

### noweb Format

A document in the noweb format can contain text or code chunks, but not group
chunks. Text chunks are preceded by a line containing only an `@`. Code chunks
are preceded by a line containing `<<...>>=`, where `...` represents a list of
key/value options. Both text and code chunks are terminated by a marker starting
a new chunk. The first chunk in a noweb document is assumed to be a text chunk.

In the sample document below a Maxima kernel is asked to solve a cubic equation,
some code is sent to Python and then Maxima is asked to plot a function. Please
note that key value options that are missing a value are assumed to a chunk name.
In other words `<<foo,kernel=python>>=` is equivalent to
`<<name=foo,kernel=python>>=`.

```
Let's ask Maxima to solve a cubic equation.
<<kernel=maxima>>=
solve(x^3+x+1=0,x);
@
Next let Python say hello and have Maxima plot a hyperbolic paraboloid.
<<kernel=python>>=
print('Hello world!')
<<foo, kernel=maxima>>=
plot3d (u^2 - v^2, [u, -2, 2], [v, -3, 3], [grid, 100, 100],
  [mesh_lines_color, false], [svg_plot, "m.svg"]);
@
That's all for now.
```

### MarkDown Format

Source documents in the MarkDown format can contain text or code chunks, but not
group chunks. Code chunks are delimited by a pair of single back-ticks or by a
pair of triple back-ticks. This is the same delimiters that plain MarkDown uses
to indicate code, the difference being that Metys expects a set of key/value
options surrounded by curly braces or a set of empty curly braces.

The following sample document accomplishes the same tasks as the previous noweb
example. Unlike noweb document key value options without a value are assumed
to be a kernel name, not a chunk name.

````MarkDown
Let's ask Maxima to solve a cubic equation.

```{maxima}
solve(x^3+x+1=0,x);
```

Next let Python say hello and have Maxima plot a hyperbolic paraboloid.
`{python} print('Hello world!')`

```{maxima, name=foo}
plot3d (u^2 - v^2, [u, -2, 2], [v, -3, 3], [grid, 100, 100],
  [mesh_lines_color, false], [svg_plot, "m.svg"]);
```
That's all for now.
````

### Metys Format

Documents in Metys format can contain text, code or group chunks. Like MarkDown
the entire document is assumed to be in text mode, so only code and group chunks
have delimiters. Both code and group chunks are started by `<|` and terminated
by `|>`. After the opening delimiter key/value options may be specified until a
chunk separator is received. The remainder of the chunk is then either code or
group data. The chunk separators are `:`, `|` or `@`. The `:` separator is used
for code blocks, the `|` separator is used for inline code, and the `@`
separator is used for group chunks. For example, the following using a group to
declare Maxima as the default kernel before making calls to a Maxima kernel and
a Python kernel.

```
<|maxima@
Let's ask Maxima to solve a cubic equation.

<|:solve(x^3+x+1=0,x);|>

Next let Python say hello and have Maxima plot a hyperbolic paraboloid.
<|python|print('Hello world!')|>

<|name=foo:
plot3d (u^2 - v^2, [u, -2, 2], [v, -3, 3], [grid, 100, 100],
  [mesh_lines_color, false], [svg_plot, "m.svg"]);
|>
That's all for now.
|>
```
