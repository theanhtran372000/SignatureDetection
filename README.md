# Tìm vị trí ký tự động cho văn bản

## Hướng dẫn triển khai

1. Thiết lập môi trường

```
pip install -r requirements.txt
```

2. Chạy server

```
python -m main --port=[Cổng chạy server]
```

# Định dạng yêu cầu

```
{
    "path": "Đường dẫn tới file",
    "sign_type": "Loại ký (van_thu, ky_chinh, ky_nhay)",
    "sign_name": "Tên người cần tìm (nếu cần)"
}
```

# Định dạng phản hồi

```
{
    "results": {
        "ky_chinh": {       # Loại ký
            "coords": [     # Tọa độ
                380.11,
                334.05608
            ],
            "page_num": 1   # Trang
        }
    },
    "state": "success"
}
```
