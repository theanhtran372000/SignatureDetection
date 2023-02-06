from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator


def get_top_right(page, coords):
    return (coords[2], page.mediabox[3] - coords[3])  # (x, y)


def get_top_left(page, coords):
    return (coords[0], page.mediabox[3] - coords[3])  # (x, y)


def find_coordinates(file_path, textlist, side='l'):
    # Open file
    fp = open(file_path, 'rb')

    # Init PDF reader
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    # Loop through pages
    results = []
    for i, page in enumerate(pages):
        # print('Processing page: {}'.format(i))
        interpreter.process_page(page)
        layout = device.get_result()

        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                for line in lobj:
                    coords, text = list(line.bbox[:4]), line.get_text()
                    if all([t in text for t in textlist]):
                        # print('Found at page %d %r: %s' % (i, coords, text))

                        temp = coords[0]
                        for char in line:
                            if char.get_text() != ' ':
                                temp = char.bbox[0]
                                break

                        coords[0] = temp

                        results.append({
                            "page_num": i,
                            "page_height": page.mediabox[3],
                            "coords": get_top_left(page, coords) if side == 'l' else get_top_right(page, coords),
                            "text": text
                        })

    fp.close()

    return results
