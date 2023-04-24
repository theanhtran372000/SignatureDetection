import re
from docx import Document

def docx_replace_regex(doc, regex, replace):

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_regex(cell, regex, replace)
                
    for p in doc.paragraphs:
        if (regex.search(p.text)):
            print(regex.search(p.text))
            # text = regex.sub(replace, p.text, count = 0)
            text = re.sub(regex.search(p.text).string, replace, p.text, 1)
            p.text = text
            break
                
    return doc


def docx_replace_date(doc, regex, replace):

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_date(cell, regex, replace)

    for p in doc.paragraphs:
        if (regex.search(p.text)):
            # text = regex.sub(replace, p.text)
            text = re.sub(regex.search(p.text).string, replace, p.text, 1)
            p.text = text
            break 
                
    return doc


def remove_datetime(doc):
    regex = re.compile(r".{0,20}, ngày.{0,10}tháng.{0,10}năm.{0,10}")
    replace = " " * 10
    doc = docx_replace_date(doc, regex, replace)
    return doc


def remove_docnum(doc):
    regex = re.compile(r"Số:.{0,20}/[^\s\n\t]{2,15}")
    replace = " " * 10
    doc = docx_replace_regex(doc, regex, replace)
    return doc


def preprocess_doc(in_path, out_path, del_num=True, del_date=True):
    print("Preprocess")
    doc = Document(in_path)
    
    if del_date:
        doc = remove_datetime(doc)    
    
    if del_num:
        doc = remove_docnum(doc)

    doc.save(out_path)
    return out_path
