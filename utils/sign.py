# Hiệu chỉnh tọa độ
from .pdfutils import find_coordinates
from .draw import draw_rect
import time
from datetime import timedelta


# Lấy tọa độ cho văn thư
def van_thu(file_path, nguoi_ky_chinh):
    print('=== Lấy vị trí ký cho văn thư ===')

    results = {}
    start = time.time()

    # 1. Số hiệu văn bản
    print('1. Tìm số hiệu văn bản')
    keywords = ['Số:', '/']
    ans = find_coordinates(file_path, keywords)
    if len(ans) == 0:
        return "doc_number_error"
     
    # Lấy kết quả đầu tìm được
    ans = ans[0]   

    results['so_hieu'] = {
        "x": ans['coords'][0] - 5,
        "y": ans['coords'][1] - 2,
        "width": 150,
        "height": 30,
        "page_num": ans['page_num'],
        "page_height": ans['page_height']
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
        return "doc_date_error"

    # Lấy kết quả đầu tiên tìm được
    ans = ans[0]

    results['ngay_thang'] = {
        "x": ans['coords'][0] - 5,
        "y": ans['coords'][1] - 2,
        "width": 200,
        "height": 30,
        "page_num": ans['page_num'],
        "page_height": ans['page_height']
    }

    # 3. Vị trí đóng dấu
    print('3. Tìm vị trí đóng dấu')
    keywords = [
        nguoi_ky_chinh
    ]
    ans = find_coordinates(file_path, keywords)
    if len(ans) == 0:
        return 'doc_name_error'

    # Lấy kết quả cuối tìm được
    ans = ans[-1]

    results['dong_dau'] = {
        "x": ans['coords'][0] - 30,
        "y": ans['coords'][1] - 120,
        "width": 120,
        "height": 120,
        "page_num": ans['page_num'],
        "page_height": ans['page_height']
    }

    print('Hoàn thành sau {}s!'.format(
        timedelta(seconds=int(time.time() - start))))
    
    return results


# Lấy tọa độ cho ký nháy
def ky_nhay(file_path, so_ky_nhay):
    print('=== Lấy vị trí ký nháy ===')

    results = {}
    start = time.time()

    # 1. Số hiệu văn bản
    print('1. Tìm vị trí ký nháy')
    keywords = ['/.']
    ans = find_coordinates(file_path, keywords, 'r')
    if len(ans) == 0:
        return 'doc_end_error'

    # Lấy kết quả cuối tìm được
    ans = ans[-1]
    x = ans['coords'][0] + 15
    y = ans['coords'][1] - 5
    w = 35
    h = 35

    results['ky_nhay'] = []
    for i in range(so_ky_nhay):
        results['ky_nhay'].append({
            "x": x + i * (w + 2),
            "y": y,
            "width": w,
            "height": h,
            "page_num": ans['page_num'],
            "page_height": ans['page_height']
        })

    print('Hoàn thành sau {}s!'.format(
        timedelta(seconds=int(time.time() - start))))
    
    return results

# Lấy tọa độ cho ký trình
def ky_trinh(file_path, nguoi_ky_chinh, so_ky_trinh):
    print('=== Lấy vị trí ký trình ===')

    results = {}
    start = time.time()

    # 1. Số hiệu văn bản
    print('1. Tìm vị trí ký trình')
    keywords = [nguoi_ky_chinh]
    ans = find_coordinates(file_path, keywords, 'r')
    if len(ans) == 0:
        return 'doc_name_error'

    # Lấy kết quả cuối tìm được
    ans = ans[-1]
    x = ans['coords'][0]
    y = ans['coords'][1] - 150
    w = 35
    h = 35

    results['ky_trinh'] = []
    for i in range(so_ky_trinh):
        results['ky_trinh'].append({
            "x": x + i * (w + 2),
            "y": y,
            "width": w,
            "height": h,
            "page_num": ans['page_num'],
            "page_height": ans['page_height']
        })

    print('Hoàn thành sau {}s!'.format(
        timedelta(seconds=int(time.time() - start))))
    
    return results

# Lấy tọa độ ký chính
def ky_chinh(file_path, nguoi_ky_chinh, nguoi_ky_dong_trinh):
    print('=== Lấy vị trí ký ===')

    results = {}
    start = time.time()

    # 1. Tìm vị trí ký chính
    print('1. Tìm vị trí ký chính')
    keywords = [nguoi_ky_chinh]
    ans = find_coordinates(file_path, keywords)
    if len(ans) == 0:
        return 'doc_name_error'

    # Lấy kết quả cuối tìm được
    ans = ans[-1]

    results['ky_chinh'] = {
        "x": ans['coords'][0],
        "y": ans['coords'][1] - 90,
        "width": 120,
        "height": 80,
        "page_num": ans['page_num'],
        "page_height": ans['page_height']
    }
    
    # Tìm vị trí ký đồng trình
    print('2. Tìm vị trí ký đồng trình')
    results ['ky_dong_trinh'] = {}
    
    for name in nguoi_ky_dong_trinh:
        keywords = [name]
        ans = find_coordinates(file_path, keywords)
        if len(ans) == 0:
            return 'doc_name_error'

        # Lấy kết quả cuối cùng tìm được
        ans = ans[-1]

        results['ky_dong_trinh'][name] = {
            "x": ans['coords'][0],
            "y": ans['coords'][1] - 90,
            "width": 120,
            "height": 80,
            "page_num": ans['page_num'],
            "page_height": ans['page_height']
        }

    print('Hoàn thành sau {}s!'.format(
        timedelta(seconds=int(time.time() - start))))

    return results


def tim_vi_tri(
    file_path,
    nguoi_ky_chinh,
    nguoi_ky_dong_trinh,
    so_ky_nhay,
    so_ky_trinh
):
    vt = van_thu(file_path, nguoi_ky_chinh)
    if type(vt) == str:
        return vt
    
    kn = ky_nhay(file_path, so_ky_nhay)
    if type(kn) == str:
        return kn
    
    kt = ky_trinh(file_path, nguoi_ky_chinh, so_ky_trinh)
    if type(kt) == str:
        return kt
    
    kc = ky_chinh(file_path, nguoi_ky_chinh, nguoi_ky_dong_trinh)
    if type(kc) == str:
        return kc
    
    vt.update(kn)
    vt.update(kt)
    vt.update(kc)
    
    return vt