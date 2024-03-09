# pdfcombine

Pdfcombine is a small command line utility that allows you to merge
arbitrary PDF pages from one or more input files into an output file.
It is basically like pdfunite, but with improved support for specifying
page ranges.

```
Usage: pdfcombine INFILE[:PAGES] [INFILE[:PAGES]]... OUTFILE

PAGES is a comma-separated list of either single page numbers or page
ranges separated by a single dash character '-'. The last page in a
file can alternatively be referred to as 'n', 'N', '$' or as the empty
string. All the following examples show valid page specifications:

    file.pdf:1-n
    file.pdf:1,2,5,10
    file.pdf:1,2,5-N,20
    file.pdf:2,5,10-,20
    file.pdf:5-$,10,1-5
```

## Dependencies

* python3
* PyPDF2 (available as python3-pypdf2 on debian)

## License

Pdfcombine is licensed under the terms of the GNU General Public License,
version 3 or later. A copy of this license is included in the repository
as `license.txt`.
