import re
import os
# import pythoncom
# from docx2pdf import convert
# import win32com.client as win32
# from win32com.client import constants


# def doc_to_docx(path):
#     # Opening MS Word
#     word = win32.gencache.EnsureDispatch(
#         'Word.Application', pythoncom.CoInitialize())
#     doc = word.Documents.Open(path)
#     doc.Activate()

#     # Rename path with .docx
#     new_file_abs = os.path.abspath(path)
#     new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

#     # Save and Close
#     word.ActiveDocument.SaveAs(
#         new_file_abs, FileFormat=constants.wdFormatXMLDocument
#     )
#     doc.Close(False)
#     os.remove(path)
#     print('Saved file to {}!'.format(new_file_abs))
#     return new_file_abs


# def docx_to_pdf(in_path, out_path):
#     if os.path.exists(out_path):
#         os.remove(out_path)
#     convert(in_path, out_path, pythoncom.CoInitialize())
#     print('Saved file to {}!'.format(out_path))
#     return out_path

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
