import os
import argparse

from flask import Flask, request, send_file
from flask_cors import CORS

# from utils import doc_to_docx, docx_to_pdf
from utils import linux_to_pdf, linux_to_docx
from utils import preprocess_doc
from utils import tim_vi_tri
# from utils import VAN_THU, KY_CHINH, KY_NHAY
from utils import draw_rect

# Flask init
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Lấy tất cả vị trí trong văn bản
@app.route('/get_sign_position', methods=['POST'])
def get_sign_position():

    # Extract info from request #
    # Files
    file = request.files['doc_file']
    file.save(os.path.join(args.save_dir, file.filename))
    doc_path = os.path.join(os.getcwd(), args.save_dir, file.filename)

    # Query
    content = request.form
    nguoi_ky_chinh          = content['nguoi_ky_chinh']
    so_ky_nhay              = int(content['so_ky_nhay'])
    so_ky_trinh             = int(content['so_ky_trinh'])
    if 'nguoi_ky_dong_trinh' in content:
        if content['nguoi_ky_dong_trinh'] != '':
            nguoi_ky_dong_trinh     = content['nguoi_ky_dong_trinh']
            nguoi_ky_dong_trinh     = [name.strip() for name in nguoi_ky_dong_trinh.split(',')]
        else:
            nguoi_ky_dong_trinh = []
    else:
        nguoi_ky_dong_trinh = []

    print('Get request:')
    print('- File: ', file.filename)
    print('- Đường dẫn tới file doc: {}'.format(doc_path))
    print('- Người ký chính: {}'.format(nguoi_ky_chinh))
    print('- Người ký đồng trình: {}'.format(nguoi_ky_dong_trinh))
    print('- Số lượng ký nháy: {}'.format(so_ky_nhay))
    print('- Số lượng ký trình: {}'.format(so_ky_trinh))
    print()

    # Check extension
    print('Process')
    print('= Validate file extention')
    ext = doc_path.split('.')[-1]
    if ext not in ['doc', 'docx']:
        print("{} not supported!".format(ext))
        return {
            "state": 'error',
            "message": "{} not supported!".format(ext)
        }, 400

    print('= Convert file to pdf')
    origin_pdf_path = linux_to_pdf(doc_path, args.save_dir)
    
    print('= Find sign position')
    results = tim_vi_tri(
        origin_pdf_path,
        nguoi_ky_chinh,
        nguoi_ky_dong_trinh,
        so_ky_nhay,
        so_ky_trinh
    )
    
    if type(results) == str:
        
        msg = "Lỗi không xác định!"
        
        if results == 'doc_number_error':
            msg = "Không tìm thấy số hiệu văn bản!"
        elif results == 'doc_date_error':
            msg = "Không tìm thấy ngày tháng năm!"
        elif results == 'doc_end_error':
            msg = "Không tìm thấy vị trí kết thúc văn bản!"
        elif results == 'doc_name_error':
            msg = "Không tìm thấy tên người {} {}".format(nguoi_ky_chinh, nguoi_ky_dong_trinh)
        
        return {
            "state": 'error',
            "message": msg
        }, 400
        
    # Remove all file
    os.remove(doc_path)
    os.remove(origin_pdf_path)
    print('Removed all files!')

    return {
        "state": "success",
        "results": results,
    }

@app.route('/preview_sign_position', methods=['POST'])
def preview_sign_position():

    # Extract info from request #
    # Files
    file = request.files['doc_file']
    file.save(os.path.join(args.save_dir, file.filename))
    doc_path = os.path.join(os.getcwd(), args.save_dir, file.filename)

    # Query
    content = request.form
    nguoi_ky_chinh          = content['nguoi_ky_chinh']
    so_ky_nhay              = int(content['so_ky_nhay'])
    so_ky_trinh             = int(content['so_ky_trinh'])
    if 'nguoi_ky_dong_trinh' in content:
        if content['nguoi_ky_dong_trinh'] != '':
            nguoi_ky_dong_trinh     = content['nguoi_ky_dong_trinh']
            nguoi_ky_dong_trinh     = [name.strip() for name in nguoi_ky_dong_trinh.split(',')]
        else:
            nguoi_ky_dong_trinh = []
    else:
        nguoi_ky_dong_trinh = []

    print('Get request:')
    print('- File: ', file.filename)
    print('- Đường dẫn tới file doc: {}'.format(doc_path))
    print('- Người ký chính: {}'.format(nguoi_ky_chinh))
    print('- Người ký đồng trình: {}'.format(nguoi_ky_dong_trinh))
    print('- Số lượng ký nháy: {}'.format(so_ky_nhay))
    print('- Số lượng ký trình: {}'.format(so_ky_trinh))
    print()

    # Check extension
    print('Process')
    print('= Validate file extention')
    ext = doc_path.split('.')[-1]
    if ext not in ['doc', 'docx']:
        print("{} not supported!".format(ext))
        return {
            "state": 'error',
            "message": "{} not supported!".format(ext)
        }, 400

    print('= Convert file to pdf')
    origin_pdf_path = linux_to_pdf(doc_path, args.save_dir)
    
    print('= Find sign position')
    results = tim_vi_tri(
        origin_pdf_path,
        nguoi_ky_chinh,
        nguoi_ky_dong_trinh,
        so_ky_nhay,
        so_ky_trinh
    )
    
    if type(results) == str:
        
        msg = "Lỗi không xác định!"
        
        if results == 'doc_number_error':
            msg = "Không tìm thấy số hiệu văn bản!"
        elif results == 'doc_date_error':
            msg = "Không tìm thấy ngày tháng năm!"
        elif results == 'doc_end_error':
            msg = "Không tìm thấy vị trí kết thúc văn bản!"
        elif results == 'doc_name_error':
            msg = "Không tìm thấy tên người {} {}".format(nguoi_ky_chinh, nguoi_ky_dong_trinh)
        
        return {
            "state": 'error',
            "message": msg
        }, 400

    placeholders = []
    for e in list(results.values()):
        if 'x' in e:
            placeholders.append(e)
        else:
            if type(e) == dict:
                for _e in list(e.values()):
                    if 'x' in _e:
                        placeholders.append(_e)
            else:
                placeholders.extend(e)
    
    dest_path = os.path.join(args.save_dir, 'result.pdf')
    
    # Preview
    print("= Draw coordinates")
    draw_rect(origin_pdf_path, placeholders, dest_path)
    
    # Remove all file
    os.remove(doc_path)
    os.remove(origin_pdf_path)
    print('Removed all files!')

    return send_file(dest_path), 200


# Convert file doc/docx to PDF and remove datetime, docnum
@app.route('/convert', methods=["POST"])
def to_pdf():
    # Extract info from request
    file = request.files['doc_file']
    file.save(os.path.join(args.save_dir, file.filename))
    doc_path = os.path.join(os.getcwd(), args.save_dir, file.filename)

    print('Get request:')
    print('- File: ', file.filename)
    print()

    # Convert doc to docx
    ext = file.filename.split('.')[-1]
    if ext not in ['doc', 'docx']:
        print("{} not supported!".format(ext))
        return {
            "state": 'error',
            "message": "{} not supported!".format(ext)
        }, 400
    
    if ext == 'doc':
        print('= Convert to docx')
        doc_path = linux_to_docx(doc_path, args.save_dir)
    
    # Preprocess file
    print('= Remove redundant words')
    process_doc_path = doc_path.replace('.docx', '_process.docx')
    preprocess_doc(doc_path, process_doc_path)

    # Convert to pdf
    print('= Convert to PDF')
    # process_pdf_path = doc_path.replace('.docx', '_process.pdf')
    # process_pdf_path = docx_to_pdf(process_doc_path, process_pdf_path)
    process_pdf_path = linux_to_pdf(process_doc_path, args.save_dir)

    # Remove all file
    os.remove(doc_path)
    os.remove(process_doc_path)
    print('Removed all files!')

    return send_file(process_pdf_path), 200


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--port', type=int, default=2000,
                        help='Listening port')
    parser.add_argument('--save_dir', type=str,
                        default='saved', help='Saving directory')

    return parser


def main(args):

    # Make save dir
    os.makedirs(args.save_dir, exist_ok=True)

    # Run app
    app.run(host='0.0.0.0', port=args.port, threaded=True)


if __name__ == '__main__':
    # Parse CLI args
    parser = get_parser()
    args = parser.parse_args()

    main(args)
