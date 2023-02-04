import re
from docx import Document


def docx_replace_regex(doc, regex, replace):

    for p in doc.paragraphs:
        if regex.search(p.text):
            text = regex.sub(replace, p.text)
            p.text = text

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_regex(cell, regex, replace)

    return doc


def remove_datetime(doc):
    regex = re.compile(r"Hà Nội.{0,10}ngày.{0,10}tháng.{0,10}năm")
    replace = " " * 10
    doc = docx_replace_regex(doc, regex, replace)
    return doc


def remove_docnum(doc):
    regex = re.compile(r"Số:.{0,20}/[^\s\n\t]{2,15}")
    replace = " " * 10
    doc = docx_replace_regex(doc, regex, replace)
    return doc


def preprocess_doc(in_path, out_path):
    doc = Document(in_path)

    doc = remove_datetime(doc)
    doc = remove_docnum(doc)

    doc.save(out_path)
    return out_path
