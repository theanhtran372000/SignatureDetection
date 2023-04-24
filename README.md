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
"doc_file"              : <File doc/docx>
"nguoi_ky_chinh"        : "Tên người ký chính"
"nguoi_ky_dong_trinh"   : "Người ký đồng trình"
                          "Ngăn cách bởi dấu phẩy"
                          "Nếu không có có thể bỏ trường này hoặc để chuỗi rỗng"
"so_ky_nhay"            : "Số lượng ký nháy"
"so_ky_trinh"           : "Số lượng ký trình"
```

**Định dạng phản hồi**

```
{
    "results": {
        "dong_dau": {
            "height": 10,
            "page_height": 841.889763779528,
            "page_num": 0,
            "width": 10,
            "x": 376.4,
            "y": 392.170763779528
        },
        "ky_chinh": {
            "height": 10,
            "page_height": 841.889763779528,
            "page_num": 0,
            "width": 10,
            "x": 396.4,
            "y": 392.170763779528
        },
        "ky_dong_trinh": {
            "Lê Minh Hoàng": {
                "height": 10,
                "page_height": 841.889763779528,
                "page_num": 0,
                "width": 10,
                "x": 212.2,
                "y": 392.170763779528
            }
        },
        "ky_nhay": [
            {
                "height": 10,
                "page_height": 841.889763779528,
                "page_num": 0,
                "width": 10,
                "x": 231.1125,
                "y": 304.85076377952805
            },
            {
                "height": 10,
                "page_height": 841.889763779528,
                "page_num": 0,
                "width": 10,
                "x": 241.1125,
                "y": 304.85076377952805
            }
        ],
        "ky_trinh": [
            {
                "height": 10,
                "page_height": 841.889763779528,
                "page_num": 0,
                "width": 10,
                "x": 536.2339999999999,
                "y": 392.170763779528
            },
            {
                "height": 10,
                "page_height": 841.889763779528,
                "page_num": 0,
                "width": 10,
                "x": 546.2339999999999,
                "y": 392.170763779528
            },
            {
                "height": 10,
                "page_height": 841.889763779528,
                "page_num": 0,
                "width": 10,
                "x": 556.2339999999999,
                "y": 392.170763779528
            }
        ],
        "ngay_thang": {
            "height": 10,
            "page_height": 841.889763779528,
            "page_num": 0,
            "width": 10,
            "x": 334.1,
            "y": 90.92176377952808
        },
        "so_hieu": {
            "height": 10,
            "page_height": 841.889763779528,
            "page_num": 0,
            "width": 10,
            "x": 94.7,
            "y": 90.90876377952804
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
"xoa_so": 0 hoặc 1
"xoa_ngay": 0 hoặc 1
```

**Định dạng phản hồi**

Trả về file PDF đã được xóa vị trí ngày tháng và số hiệu văn bản

### 3. Xem trước vị trí ký

**Định dạng yêu cầu**

- API: /get_sign_position
- Method: POST
- Content-Type: form-data

```
"doc_file"              : <File doc/docx>
"nguoi_ky_chinh"        : "Tên người ký chính"
"nguoi_ky_dong_trinh"   : "Người ký đồng trình"
                          "Ngăn cách bởi dấu phẩy"
                          "Nếu không có có thể bỏ trường này hoặc để chuỗi rỗng"
"so_ky_nhay"            : "Số lượng ký nháy"
"so_ky_trinh"           : "Số lượng ký trình"
```
**Định dạng phản hồi**

Trả về file PDF đã được đánh dấu vị trí ký