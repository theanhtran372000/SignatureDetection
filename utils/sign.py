# Hiệu chỉnh tọa độ
from .pdfutils import find_coordinates
from .draw import draw_rect
import time
from datetime import timedelta

VAN_THU = 0
KY_NHAY = 1
KY_CHINH = 2


# Lấy tọa độ cho văn thư
def van_thu(file_path, name):
    print('=== Lấy vị trí ký cho văn thư ===')

    results = {}
    start = time.time()

    # 1. Số hiệu văn bản
    print('1. Tìm số hiệu văn bản')
    keywords = ['Số:', '/']
    ans = find_coordinates(file_path, keywords)
    if len(ans) == 0:
        raise Exception('Không tìm thấy {}!'.format(keywords))

    # Hiệu chỉnh tọa độ
    coords = ans[0]['coords']
    coords = (
        coords[0] - 5,
        coords[1] - 5
    )

    results['so_hieu'] = {
        "coords": coords,
        "page_num": ans[0]['page_num']
    }

    # 2. Ngày tháng năm
    print('2. Tìm ngày tháng năm')
    keywords = [
        'ngày',
        'tháng',
        'năm'
    ]
    ans = find_coordinates(file_path, keywords)
    if len(ans) == 0:
        raise Exception('Không tìm thấy {}!'.format(keywords))

    # Hiệu chỉnh tọa độ
    coords = ans[0]['coords']
    coords = (
        coords[0] - 5,
        coords[1] - 5
    )

    results['ngay_thang'] = {
        "coords": coords,
        "page_num": ans[0]['page_num']
    }

    # 3. Vị trí đóng dấu
    print('2. Tìm vị trí đóng dấu')
    keywords = [
        name
    ]
    ans = find_coordinates(file_path, keywords)
    if len(ans) == 0:
        raise Exception('Không tìm thấy {}!'.format(keywords))

    # Hiệu chỉnh tọa độ
    coords = ans[0]['coords']
    coords = (
        coords[0],
        coords[1] - 110
    )

    results['dong_dau'] = {
        "coords": coords,
        "page_num": ans[0]['page_num']
    }

    print('Hoàn thành sau {}s!'.format(
        timedelta(seconds=int(time.time() - start))))
    return results


# Lấy tọa độ cho ký nháy
def ky_nhay(file_path):
    print('=== Lấy vị trí ký nháy ===')

    results = {}
    start = time.time()

    # 1. Số hiệu văn bản
    print('1. Tìm vị trí ký nháy')
    keywords = ['/.']
    ans = find_coordinates(file_path, keywords, 'r')
    if len(ans) == 0:
        raise Exception('Không tìm thấy {}!'.format(keywords))

    # Hiệu chỉnh tọa độ
    coords = ans[0]['coords']
    coords = (
        coords[0] + 15,
        coords[1] - 5
    )

    results['ky_nhay'] = {
        "coords": coords,
        "page_num": ans[0]['page_num']
    }

    print('Hoàn thành sau {}s!'.format(
        timedelta(seconds=int(time.time() - start))))
    return results


# Lấy tọa độ ký chính
def ky_chinh(file_path, name):
    print('=== Lấy vị trí ký chính ===')

    results = {}
    start = time.time()

    # 1. Số hiệu văn bản
    print('1. Tìm vị trí ký chính')
    keywords = [name]
    ans = find_coordinates(file_path, keywords)
    if len(ans) == 0:
        raise Exception('Không tìm thấy {}!'.format(keywords))

    # Hiệu chỉnh tọa độ
    coords = ans[0]['coords']
    coords = (
        coords[0],
        coords[1] - 110
    )

    results['ky_chinh'] = {
        "coords": coords,
        "page_num": ans[0]['page_num']
    }

    print('Hoàn thành sau {}s!'.format(
        timedelta(seconds=int(time.time() - start))))
    return results


def tim_vi_tri(file_path, sign_type, sign_name):
    if sign_type == VAN_THU:
        return van_thu(file_path, sign_name)

    elif sign_type == KY_NHAY:
        return ky_nhay(file_path)

    elif sign_type == KY_CHINH:
        return ky_chinh(file_path, sign_name)

    else:
        print('Không tồn tại loại ký {}!'.format(sign_type))
        return


if __name__ == '__main__':
    file_path = r'D:\Workplaces\Python\ComputerVision\PdfAutoSign\pdfs\result2.pdf'
    name = 'Lê Minh Hoàng'
    results = ky_chinh(file_path, name)
    draw_rect(file_path, results.values(), 'result.pdf')
