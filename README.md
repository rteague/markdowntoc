# markdowntoc

## Usage
```bash
Generates a 'Table of Contents' for Markdown files.

usage: mdtoc.py [-h] [--root ROOT] path

Generates a table of contents section for your *.md files

positional arguments:
  path

optional arguments:
    -h, --help   show this help message and exit
    --root ROOT  the starting depth, example 2 = ##

by Rashaud Teague
```

## Examples
**Run mdtoc.py on test.md**
```bash
python mdtoc.py test.md
```
**Begin at header 2 '##' (double-pound)**
```bash
python mdtoc.py --root=2 test.md
```


