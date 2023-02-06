# Tìm vị trí ký tự động cho văn bản

## Hướng dẫn triển khai

1. Thiết lập môi trường

```
sudo apt install libreoffice -y

pip install -U pip setuptools
pip install -r requirements.txt
```

2. Chạy server

```
python main.py \
    --port=[Cổng chạy server] \
    --save_dir[Đường dẫn tới thư mục lưu trữ]
```

## Hướng dẫn sử dụng
### 1. Tìm vị trí ký

**Định dạng yêu cầu**

- API: /get_sign_position
- Method: POST
- Content-Type: form-data

```
"file": <File doc/docx>
"sign_type": "Loại ký (van_thu, ky_chinh, ky_nhay, toan_bo)"
"sign_name": "Tên người cần tìm phân tách bởi dấu phẩy "," (nếu cần)"
             "Tên người ký chính ở đầu, phía sau là người ký đồng trình"
```

**Định dạng phản hồi**

```
// Ví dụ cho phản hồi của kiểu ký toan_bo
// Với kiểu ky_chinh, ky_nhay và van_thu, định dang data tương tự
{
    "results": {
        "dong_dau": {
            "coords": [
                376.4,
                392.170763779528
            ],
            "page_num": 0
        },
        "ky_chinh": {
            "coords": [
                396.4,
                392.170763779528
            ],
            "page_num": 0
        },
        "ky_dong_trinh": {
            "Lê Minh Hoàng": {
                "coords": [
                    212.2,
                    392.170763779528
                ],
                "page_num": 0
            }
        },
        "ky_nhay": {
            "coords": [
                231.1125,
                304.85076377952805
            ],
            "page_num": 0
        },
        "ngay_thang": {
            "coords": [
                334.1,
                90.92176377952808
            ],
            "page_num": 0
        },
        "so_hieu": {
            "coords": [
                94.7,
                90.90876377952804
            ],
            "page_num": 0
        }
    },
    "state": "success"
}
```

### 2. Chuyển đổi file

**Định dạng yêu cầu**

- API: /convert
- Method: POST
- Content-Type: form-data

```
"file": <File doc/docx>
```

**Định dạng phản hồi**

Trả về file PDF đã được xóa vị trí ngày tháng và số hiệu văn bản

### 3. Xem trước vị trí ký

**Định dạng yêu cầu**

- API: /get_sign_position
- Method: POST
- Content-Type: form-data

```
"file": <File doc/docx>
"sign_type": "Loại ký (van_thu, ky_chinh, ky_nhay, toan_bo)"
"sign_name": "Tên người cần tìm phân tách bởi dấu phẩy "," (nếu cần)"
             "Tên người ký chính ở đầu, phía sau là người ký đồng trình"
```
**Định dạng phản hồi**

Trả về file PDF đã được đánh dấu vị trí ký