import argparse

from flask import Flask, request
from flask_cors import CORS

from utils import doc_to_docx, docx_to_pdf
from utils import preprocess_doc
from utils import tim_vi_tri
from utils import VAN_THU, KY_CHINH, KY_NHAY

# Flask init
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/get_sign_position', methods=['POST'])
def get_sign_position():

    # Get request body data
    content = request.get_json()
    # TODO: Get file from request and save to local ...

    # Extract info from request
    doc_path = content['path']
    sign_type = content['sign_type']
    sign_name = content['sign_name']

    print('Get request:')
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
        }

    # Convert from doc to docx
    if ext == 'doc':
        print('= Convert file to docx')
        doc_path = doc_to_docx(doc_path)

    # Convert from docx to pdf
    print('= Convert file to pdf')
    origin_pdf_path = doc_path.replace('.docx', '_origin.pdf')
    docx_to_pdf(doc_path, origin_pdf_path)

    # Remove redundant words in word
    print('= Remove redundant words')
    process_doc_path = doc_path.replace('.docx', '_process.docx')
    preprocess_doc(doc_path, process_doc_path)
    process_pdf_path = doc_path.replace('.docx', '_process.pdf')
    process_pdf_path = docx_to_pdf(process_doc_path, process_pdf_path)

    # Find coord on origin doc
    sign_map = {
        'van_thu': VAN_THU,
        'ky_nhay': KY_NHAY,
        'ky_chinh': KY_CHINH
    }

    print('= Find sign position')
    results = tim_vi_tri(origin_pdf_path, sign_map[sign_type], sign_name)

    # TODO: Return pdf file...

    # Remove all file
    # os.remove(doc_path)
    # os.remove(origin_pdf_path)
    # os.remove(process_doc_path)
    # os.remove(process_pdf_path)
    # print('Removed all files!')

    return {
        "state": "success",
        "results": results
    }


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--port', type=int, default=2000,
                        help='Listening port')

    return parser


def main(args):

    # Run app
    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    # Parse CLI args
    parser = get_parser()
    args = parser.parse_args()

    main(args)
