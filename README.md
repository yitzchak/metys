# Metys

Metys is scientific report generator and a literate programming tool similar to
knitr or Pweave. Like Pweave, Metys uses the Jupyter protocol to run code
embedded in the source document. Unlike Pweave, Metys can access multiple
Jupyter kernels within the same source document and can also create multiple
separate sessions of the same kernel.

Metys is currently alpha level software.

## Processing Metys Documents

Metys is currently run from the command line by using the following.

```sh
metys foo.tmt
```

There are many command line options available. A short description will be shown
with the following.

```sh
metys --help
```

## Input Formats

Metys can parse source documents in noweb, Markdown or Metys format. The format
of the source document will be determined by the file extension or by the
`--parser` command line option if specified. Source documents with a file
extension ending with `nw` are assumed to be noweb documents. Those with a file
extension ending with `md` are assumed to be Markdown documents. All other files
are assumed to be in Metys format.

Parsing the source document results in a series of logical chunks. These chunks
are either text, code or group chunks. Text chunks contain text which is copied
verbatim to the output document. Code chunks are evaluated by a Jupyter kernel
and the results are formatted in the output document as per the local and global
options specified. Group chunks are used to set options for a collection of
chunks or to include subfiles which contain more text, code and group chunks.

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

### Markdown Format

Source documents in the Markdown format can contain text or code chunks, but not
group chunks. Code chunks are delimited by a pair of single back-ticks or by a
pair of triple back-ticks. This is the same delimiters that plain Markdown uses
to indicate code, the difference being that Metys expects a set of key/value
options surrounded by curly braces or a set of empty curly braces.

The following sample document accomplishes the same tasks as the previous noweb
example. Unlike noweb document key value options without a value are assumed
to be a kernel name, not a chunk name.

````Markdown
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

Documents in Metys format can contain text, code or group chunks. Like Markdown
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

Please note that kernels and sessions are local to the innermost enclosing
group chunk.

## Chunk Options

Chunk options may be specified in all input formats as a list of key/value pairs
separated by commas. Each key/value pair consists of a name followed by an
equals sign and a value. The absence of an equals sign and a value is treated as
a value to be assigned to a default key. The default key for noweb format is
`name`. For all other formats the default key is `kernel`.

The key name may contain any combination of letters and underscores, along with
a single period used to specify sub-options. For example, the following
specifies a Maxima kernel, with a LaTeX code environment of `Verbatim` and
`frame=single` as a verbatim environment option.

```
<|maxima, code_env=Verbatim, code_env_options.frame=single:
solve(x^3+x+1=0,x);
|>
```

The table below lists the chunk options available along with a short summary of
each option.

| Name               | Type                         | Default    | Description                                    |
|:-------------------|:-----------------------------|:-----------|:-----------------------------------------------|
| code_echo          | boolean                      | `true`     | Enable echo of code input.                     |
| code_env           | string                       | `verbatim` | Code environment for LaTeX.                    |
| code_env_options   | string/sub-option            | None       | Code environment options for LaTeX.            |
| evaluate           | boolean                      | `true`     | Enable evaluation of code input.               |
| expand_options     | boolean                      | `false`    | Enable option expansion in code input.         |
| figure_caption     | string                       | None       | Figure caption.                                |
| figure_env         | string                       | `figure`   | Figure environment for LaTeX.                  |
| figure_path        | string                       | `figure`   | Figure directory.                              |
| figure_env_options | string/sub-option            | None       | Figure environment options for LaTeX.          |
| figure_prefix      | string                       | `fig:`     | Figure label prefix for LaTeX.                 |
| format             | `latex`, `markdown`          | None       | Format of output file.                         |
| graphics_options   | string/sub-option            | None       | Graphics options for LaTeX.                    |
| inline             | boolean                      | None       | Enable inline output format.                   |
| input              | string                       | None       | Path of input file for chunk.                  |
| kernel             | string                       | None       | Jupyter kernel.                                |
| math_env           | string                       | `equation` | Display math environment for LaTeX.            |
| math_prefix        | string                       | `eq:`      | Mathematics label prefix for LaTeX.            |
| name               | string                       | None       | Chunk name. Used for file names and labels.    |
| output             | string                       | None       | Path of output file for chunk.                 |
| parser             | `markdown`, `metys`, `noweb` | None       | Parser to use for input file.                  |
| results            | boolean                      | `true`     | Enable output of code results.                 |
| session            | string                       | None       | Unique identifier for specific kernel session. |
| stderr_echo        | boolean                      | `true`     | Enable echo of stderr.                         |
| stderr_env         | string                       | `verbatim` | stderr environment for LaTeX.                  |
| stderr_env_options | string/sub-option            | None       | stderr environment options for LaTeX.          |
| stdout_echo        | boolean                      | `false     | Enable echo of stdout.                         |
| stdout_env         | string                       | `verbatim` | stdout environment for LaTeX.                  |
| stdout_env_options | string/sub-option            | None       | stdout environment options for LaTeX.          |
| wrap_math          | boolean                      | `true`     | Enabling wrapping of math results.             |

Please not that some options are automatically deduced or may have special
behavior. For instance,

- The `format` option is automatically set if not specified. If `parser` is
  set to `markdown` then the `format` is also. Otherwise `format` is set to
  `latex`.

- The `inline` option is automatically set for Markdown and Metys documents, but
  not for noweb documents.

- The `input` option has a different behavior for text/code chunks versus group
  chunks. For group chunks the chunks contents are replaced with the contents
  of the file specified by `input` after it has been parsed. For text or code
  chunks the contents of the file is included without any parsing.

- The `kernel` option is not set by default but will be set to `python` for
  input files with an extension of `.Pmd` and set to `r` for input files with an
  extension of `.Rmd`.

- The `output` option will write any chunk output to the file specified by the
  option versus writing the output to main output document.

- The `session` option will allow multiple separate sessions of the same kernel
  to exist. For example, the following document will have two separate Python
  kernels active. In the default session `x` has a value of 3, while in the
  `foo` session `x` has a value of 4.

  ```
  Wibble <|python|x=3|>, wibble <|python,session=foo|x=4|>, quux <|python|x|>.
  ```
