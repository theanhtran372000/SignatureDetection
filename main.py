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


@app.route('/get_sign_position', methods=['POST'])
def get_sign_position():

    # Extract info from request
    file = request.files['file']
    file.save(os.path.join(args.save_dir, file.filename))
    doc_path = os.path.join(os.getcwd(), args.save_dir, file.filename)

    content = request.form
    sign_type = content['sign_type']
    sign_name = content['sign_name']

    print('Get request:')
    print('- File: ', file.filename)
    print('- Doc path: {}'.format(doc_path))
    print('- Sign type: {}'.format(sign_type))
    print('- Sign name: {}'.format(sign_name))
    print()

    print('Process')

    print('= Validate file extention')
    ext = doc_path.split('.')[-1]
    if ext not in ['doc', 'docx']:
        print("{} not supported!".format(ext))
        return {
            "state": 'error',
            "message": "{} not supported!".format(ext)
        }, 400

    # # Convert from doc to docx
    # if ext == 'doc':
    #     print('= Convert file to docx')
    #     doc_path = doc_to_docx(doc_path)

    # # Convert from docx to pdf
    # print('= Convert file to pdf')
    # origin_pdf_path = doc_path.replace('.docx', '_origin.pdf')
    # docx_to_pdf(doc_path, origin_pdf_path)
    print('= Convert file to pdf')
    origin_pdf_path = linux_to_pdf(doc_path, args.save_dir)

    # Find coord on origin doc
    # sign_map = {
    #     'van_thu': VAN_THU,
    #     'ky_nhay': KY_NHAY,
    #     'ky_chinh': KY_CHINH
    # }

    print('= Find sign position')
    results = tim_vi_tri(origin_pdf_path, sign_type, sign_name)
    if type(results) == str:
        msg = "Lỗi không xác định!"
        if results == 'doc_number_error':
            msg = "Không tìm thấy số hiệu văn bản!"
        elif results == 'doc_date_error':
            msg = "Không tìm thấy ngày tháng năm!"
        elif results == 'doc_name_error':
            msg = "Không tìm thấy {}".format(sign_name)
        elif results == 'sign_type_error':
            msg = "Loại ký {} không hợp lệ!".format(sign_type)
        
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

    # Extract info from request
    file = request.files['file']
    file.save(os.path.join(args.save_dir, file.filename))
    doc_path = os.path.join(os.getcwd(), args.save_dir, file.filename)

    content = request.form
    sign_type = content['sign_type']
    sign_name = content['sign_name']

    print('Get request:')
    print('- File: ', file.filename)
    print('- Doc path: {}'.format(doc_path))
    print('- Sign type: {}'.format(sign_type))
    print('- Sign name: {}'.format(sign_name))
    print()

    print('Process')

    print('= Validate file extention')
    ext = doc_path.split('.')[-1]
    if ext not in ['doc', 'docx']:
        print("{} not supported!".format(ext))
        return {
            "state": 'error',
            "message": "{} not supported!".format(ext)
        }, 400

    # # Convert from doc to docx
    # if ext == 'doc':
    #     print('= Convert file to docx')
    #     doc_path = doc_to_docx(doc_path)

    # # Convert from docx to pdf
    # print('= Convert file to pdf')
    # origin_pdf_path = doc_path.replace('.docx', '_origin.pdf')
    # docx_to_pdf(doc_path, origin_pdf_path)
    print('= Convert file to pdf')
    origin_pdf_path = linux_to_pdf(doc_path, args.save_dir)

    # Find coord on origin doc
    print('= Find sign position')
    results = tim_vi_tri(origin_pdf_path, sign_type, sign_name)
    if type(results) == str:
        msg = "Lỗi không xác định!"
        if results == 'doc_number_error':
            msg = "Không tìm thấy số hiệu văn bản!"
        elif results == 'doc_date_error':
            msg = "Không tìm thấy ngày tháng năm!"
        elif results == 'doc_name_error':
            msg = "Không tìm thấy {}".format(sign_name)
        elif results == 'sign_type_error':
            msg = "Loại ký {} không hợp lệ!".format(sign_type)
        
        return {
            "state": 'error',
            "message": msg
        }, 400
    
    coords = list(results.values())
    dest_path = os.path.join(args.save_dir, 'result.pdf')
    
    # Preview
    print("= Draw coordinates")
    draw_rect(origin_pdf_path, coords, dest_path)
    
    # Remove all file
    os.remove(doc_path)
    os.remove(origin_pdf_path)
    print('Removed all files!')

    return send_file(dest_path), 200

@app.route('/convert', methods=["POST"])
def to_pdf():
    # Extract info from request
    file = request.files['file']
    file.save(os.path.join(args.save_dir, file.filename))
    doc_path = os.path.join(os.getcwd(), args.save_dir, file.filename)

    print('Get request:')
    print('- File: ', file.filename)
    print()

    # Convert doc to docx
    ext = file.filename.split('.')[-1]
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
    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    # Parse CLI args
    parser = get_parser()
    args = parser.parse_args()

    main(args)
