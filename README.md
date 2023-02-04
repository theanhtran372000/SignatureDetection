# Tìm vị trí ký tự động cho văn bản

## Hướng dẫn triển khai

1. Thiết lập môi trường

```
pip install -r requirements.txt
```

2. Chạy server

```
python -m main \
    --port=[Cổng chạy server] \
    --save_dir[Đường dẫn tới thư mục lưu trữ]
```

## Tìm vị trí ký

**Định dạng yêu cầu**

- API: /get_sign_position
- Method: POST
- Content-Type: form-data

```
"file": <File doc/docx>
"path": "Đường dẫn tới file",
"sign_type": "Loại ký (van_thu, ky_chinh, ky_nhay)",
"sign_name": "Tên người cần tìm (nếu cần)"
```

**Định dạng phản hồi**

```
// Ví dụ cho phản hồi của kiểu ký van_thu
// Với kiểu ky_chinh va ky_nhay, định dang data tương tự
{
    "results": {                       # Trả về danh sách vị trí
        "dong_dau": {                  # Vị trí đóng dấu
            "coords": [                # Tọa độ
                158.3,
                433.05608000000007
            ],
            "page_num": 0              # Số trang (bắt đầu từ 0)
        },
        "ngay_thang": {                # Vị trí ngày tháng
            "coords": [
                334.07,
                98.58575999999994
            ],
            "page_num": 0
        },
        "so_hieu": {
            "coords": [
                94.624,
                98.59871999999996
            ],
            "page_num": 0
        }
    },
    "state": "success"
}
```

## Chuyển đổi file

**Định dạng yêu cầu**

- API: /convert
- Method: POST
- Content-Type: form-data

```
"file": <File doc/docx>
```

**Định dạng phản hồi**

Trả về file PDF đã được xóa vị trí ngày tháng và số hiệu văn bản
