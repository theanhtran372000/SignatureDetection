import re
import os


def linux_to_pdf(in_path, out_dir):
    filename = '.'.join(in_path.split(os.path.sep)[-1].split('.')[:-1]) + ".pdf"
    os.system('libreoffice --headless --convert-to pdf:writer_pdf_Export "{}" --outdir {}'.format(in_path, out_dir))
    return os.path.join(out_dir, filename)

def linux_to_docx(in_path, out_dir):
    filename = '.'.join(in_path.split(os.path.sep)[-1].split('.')[:-1]) + ".docx"
    os.system('libreoffice --headless --convert-to docx "{}" --outdir {}'.format(in_path, out_dir))
    return os.path.join(out_dir, filename)

if __name__ == '__main__':
    doc_to_docx(
        'D:\Workplaces\Python\ComputerVision\PdfAutoSign\docs\To trinh test VBNB 2 PB trinh xin phe duyet 1 LD.doc')
