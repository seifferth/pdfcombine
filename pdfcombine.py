#!/usr/bin/env python3

import sys
import re
from PyPDF2 import PdfFileMerger

def combine(*input_pdfs) -> PdfFileMerger:
    merger = PdfFileMerger()
    for pdf in input_pdfs:
        filename, *pages = pdf.rsplit(':', 1)
        if not pages: merger.append(filename); continue
        if not re.fullmatch('[0-9,-]+', pages[0]):
            raise Exception(
                f"Error: Invalid page range: '{pages}'"
            )
        for pagerange in pages[0].split(','):
            if '-' in pagerange:
                first, last = pagerange.split('-', 1)
                merger.append(filename, pages=(int(first)-1, int(last)),
                              import_outline=False)
            else:
                merger.append(filename,
                              pages=(int(pagerange)-1, int(pagerange)),
                              import_outline=False)
    return merger

_cli_help = """
Usage: pdfcombine INFILE[:PAGES] [INFILE[:PAGES]]... OUTFILE
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
