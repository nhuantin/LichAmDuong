import lunardate
from datetime import date
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image
from lunarcalendar import Converter, Solar, Lunar

# Dữ liệu các ngày lễ Phật giáo
phat_giao_events = {
    (1, 1): ("Vía Đức Phật Di Lặc", "https://i.imgur.com/4MEN4gS.png"),
    (8, 2): ("Vía Bồ Tát Hộ Minh xuất gia", "https://i.imgur.com/QrZ1nCI.png"),
    (15, 2): ("Vía Phật Thích Ca nhập diệt", "https://i.imgur.com/N0TpLyc.png"),
    (19, 2): ("Vía Đức Quán Thế Âm đản sinh", "https://i.imgur.com/q4nZAnN.png"),
    (21, 2): ("Vía Đức Phổ Hiền Bồ Tát", "https://i.imgur.com/6QjkiSc.png"),
    (6, 3): ("Vía tôn giả Ca Diếp", "https://i.imgur.com/ndI1LoC.png"),
    (16, 3): ("Vía Phật Mẫu chuẩn đề", "https://i.imgur.com/UwgTPAZ.png"),
    (4, 4): ("Vía Văn Thù Bồ tát đản sinh", "https://i.imgur.com/9Vs47CJ.png"),
    (8, 4): ("Vía Bồ Tát Hộ Minh đản sinh", "https://i.imgur.com/pAPFBJH.png"),
    (15, 4): ("Đại lễ Tam hợp (Vesak)", "https://i.imgur.com/rCfHThn.png"),
    (20, 4): ("Vía Bồ tát Quảng Đức thiêu thân", "https://i.imgur.com/JWCzlcx.png"),
    (23, 4): ("Vía Phổ Hiền thành đạo", "https://i.imgur.com/6QjkiSc.png"),
    (28, 4): ("Vía Đức Dược Sư đản sinh", "https://i.imgur.com/QrS7Jiw.png"),
    (13, 5): ("Vía Già Lam Thánh Chúng", "https://i.imgur.com/wnxZRAg.png"),
    (3, 6): ("Vía Vi Đà Hộ Pháp", "https://i.imgur.com/xS1QLbl.png"),
    (15, 6): ("Đức Phật chuyển pháp luân tại vườn Lộc Uyển", "https://i.imgur.com/poPafbb.png"),
    (19, 6): ("Vía Đức Quán Thế Âm thành đạo", "https://i.imgur.com/Wtg4aFH.png"),
    (13, 7): ("Vía Đức Đại Thế Chí Bồ tát đản sinh", "https://i.imgur.com/TBTHB2a.png"),
    (15, 7): ("Lễ Vu Lan Báo Hiếu", "https://i.imgur.com/jODUGtD.png"),
    (30, 7): ("Vía Đức Địa Tạng Bồ Tát", "https://i.imgur.com/zTTgmAs.png"),
    (1, 8): ("Vía Huệ Viễn Tuệ Sư Sơ Tổ Tịnh Độ Tông", "https://i.imgur.com/9Q1xIAx.png"),
    (3, 8): ("Vía Đức Lục Tổ Huệ Năng", "https://i.imgur.com/cBp6Tfh.png"),
    (8, 8): ("Vía Tôn giả A Nan Đà", "https://i.imgur.com/AO5JlTY.png"),
    (22, 8): ("Vía Đức Nhiên Đăng đản sinh", "https://i.imgur.com/F7Anq8z.png"),
    (15, 9): ("Ngày Tăng Bảo", "https://i.imgur.com/zDGmCfC.png"),
    (19, 9): ("Vía Quan Âm Bồ Tát xuất gia", "https://i.imgur.com/WRJj3OW.png"),
    (30, 9): ("Vía Đức Phật Dược Sư Lưu Ly thành đạo", "https://i.imgur.com/jBgkTiy.png"),
    (5, 10): ("Vía Đức Bồ Đề Đạt Ma (Sư tổ thiền tông)", "https://i.imgur.com/3jObxBy.png"),
    (17, 11): ("Vía Đức Phật A Di Đà", "https://i.imgur.com/vvBws0J.png"),
    (8, 12): ("Vía Đức Phật Thích Ca Thành Đạo", "https://i.imgur.com/alVJ3N0.png"),
}

def convert_to_lunar(solar_date):
    """Chuyển đổi ngày dương sang âm lịch (trả về dict)"""
    try:
        # Chuyển đổi ngày dương sang ngày âm
        solar = Solar(solar_date.year, solar_date.month, solar_date.day)
        lunar = Converter.Solar2Lunar(solar)
        
        # Số ngày trong tháng âm lịch (giả định 30 ngày nếu không có thông tin)
        days_in_month = 30 if lunar.day <= 15 else 29

        return {
            "day": lunar.day,
            "month": lunar.month,
            "year": lunar.year,
            "leap": lunar.isleap,
            "days_in_month": days_in_month,  # Số ngày trong tháng
            "str_date": f"{lunar.day}/{lunar.month}"  # Chuỗi hiển thị
        }
    except Exception as e:
        print(f"Lỗi chuyển đổi: {e}")
        return None

def get_can_chi(lunar_year):
    """Tính Can Chi dựa trên năm âm lịch"""
    CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    can = CAN[(lunar_year - 4) % 10]  # Điều chỉnh từ -3 thành -4
    chi = CHI[(lunar_year - 4) % 12]
    return f"{can} {chi}"

def get_buddhist_year(solar_date):
    """
    Tính năm Phật lịch.
    Phật lịch tăng 1 năm vào ngày 15/4 âm lịch.
    """
    lunar_date = convert_to_lunar(solar_date)
    if lunar_date:
        # Nếu đã qua ngày 15/4 âm lịch, tăng năm Phật lịch
        if (lunar_date["month"] > 4) or (lunar_date["month"] == 4 and lunar_date["day"] >= 15):
            return solar_date.year + 544  # Phật lịch = Dương lịch + 544
    return solar_date.year + 543  # Phật lịch mặc định

def get_buddha_event(lunar_day, lunar_month):
    """Kiểm tra sự kiện Phật giáo theo ngày âm lịch."""
    return phat_giao_events.get((lunar_day, lunar_month))

def preload_buddha_images():
    """Tải trước hình ảnh sự kiện Phật giáo."""
    images = {}
    for key, (_, url) in phat_giao_events.items():
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            if "image" in response.headers["Content-Type"]:
                image = Image.open(BytesIO(response.content))
                images[key] = image
            else:
                print(f"URL {url} không phải là hình ảnh")
        except Exception as e:
            print(f"Lỗi tải hình ảnh {url}: {e}")
        finally:
            if 'response' in locals():
                response.close()  # Đóng kết nối
    return images
