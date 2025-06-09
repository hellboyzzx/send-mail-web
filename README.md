# 📧 Web App Gửi Email bằng Microsoft Graph API – by @hellboyzzx

Ứng dụng web đơn giản dùng **Flask + Graph API** cho phép gửi email HTML có đính kèm file, dùng access token từ Microsoft 365 Developer E5.

## 🚀 Tính năng

- Nhập địa chỉ người nhận, tiêu đề, nội dung HTML
- Đính kèm file PDF / hình ảnh
- Gửi email qua Microsoft Graph API

## 🧰 Hướng dẫn sử dụng

### 1. Cài đặt

```bash
pip install -r requirements.txt
```

### 2. Tạo file `.env`:

```
ACCESS_TOKEN=eyJ0eXAiOiJKV1QiLCJub25...
```

### 3. Chạy ứng dụng

```bash
python app.py
```

Truy cập: `http://localhost:5000`

---

**Lưu ý:** Access token hết hạn sau 1 giờ. Lấy token mới từ [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)

© 2025 by @hellboyzzx ❤️
