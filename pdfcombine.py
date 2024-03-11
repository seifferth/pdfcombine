#!/usr/bin/env python3

import sys
import re
from PyPDF2 import PdfFileMerger
from PyPDF2.pagerange import PageRange

def combine(*input_pdfs) -> PdfFileMerger:
    merger = PdfFileMerger()
    for pdf in input_pdfs:
        filename, *pages = pdf.rsplit(':', 1)
        if not pages: merger.append(filename); continue
        if not re.fullmatch('[0-9,-nN$]+', pages[0]):
            raise Exception(
                f"Error: Invalid page range: '{pages[0]}'"
            )
        for pagerange in pages[0].split(','):
            if '-' in pagerange:
                first, last = pagerange.split('-', 1)
                if not re.fullmatch('[0-9]+', first):
                    raise Exception(
                        f"Error: Invalid page range: '{first}-{last}'"
                    )
                if not re.fullmatch('([0-9]+|[nN$]|)', last):
                    raise Exception(
                        f"Error: Invalid page range: '{first}-{last}'"
                    )
                if not int(first) >= 1:
                    raise Exception(
                        f"Error: Page number is too small: '{first}'"
                    )
                if last in ['n', 'N', '$', '']: last = ''
                pages = PageRange('{}:{}'.format(int(first)-1, last))
            elif pagerange in ['n', 'N', '$']:
                pages = PageRange('-1:')
            else:
                if not re.fullmatch('[0-9]+', last):
                    raise Exception(
                        f"Error: Invalid page range: '{pagerange}'"
                    )
                if not int(pagerange) >= 1:
                    raise Exception(
                        f"Error: Page number is too small: '{first}'"
                    )
                pages = PageRange('{}'.format(int(pagerange)-1))
            merger.append(filename, pages=pages, import_outline=False)
    return merger

_cli_help = """
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
""".lstrip()

if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print(_cli_help); exit(0)
    if len(sys.argv) < 3:
        print('At least two command line arguments are required',
              file=sys.stderr); exit(1)
    input_pdfs = sys.argv[1:-1]
    output_pdf = sys.argv[-1]
    combine(*input_pdfs).write(output_pdf)
