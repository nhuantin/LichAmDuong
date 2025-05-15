from django.shortcuts import render
from datetime import date, timedelta, datetime
from .utils import convert_to_lunar, get_buddhist_year, get_can_chi, get_buddha_event

def get_vietnamese_weekday(weekday):
    """Chuyển đổi ngày trong tuần từ tiếng Anh sang tiếng Việt"""
    weekdays = {
        "Monday": "Thứ Hai",
        "Tuesday": "Thứ Ba",
        "Wednesday": "Thứ Tư",
        "Thursday": "Thứ Năm",
        "Friday": "Thứ Sáu",
        "Saturday": "Thứ Bảy",
        "Sunday": "Chủ Nhật",
    }
    return weekdays.get(weekday, "")

def calendar_view(request):
    # Lấy ngày từ request hoặc dùng ngày hiện tại
    try:
        day = int(request.GET.get('day', datetime.now().day))
        month = int(request.GET.get('month', datetime.now().month))
        year = int(request.GET.get('year', datetime.now().year))
        current_date = date(year, month, day)
    except ValueError:
        current_date = datetime.now().date()
    
    # Chuyển đổi ngày dương sang âm lịch
    lunar_date = convert_to_lunar(current_date)

    # Tính toán dữ liệu lịch
    start_date = current_date.replace(day=1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Thông tin tháng âm lịch
    lunar_month_info = None
    if lunar_date:
        lunar_month_info = {
            "days_in_month": lunar_date["days_in_month"],  # Số ngày trong tháng âm lịch
            "leap_month": lunar_date["leap"],  # Tháng nhuận hay không
        }
    
    # Tạo danh sách 35 ngày (5 tuần)
    days = []
    temp_date = start_date - timedelta(days=start_date.weekday())  # Bắt đầu từ Thứ 2 đầu tiên
    
    for _ in range(35):
        lunar_temp_date = convert_to_lunar(temp_date) if start_date <= temp_date <= end_date else None
        days.append({
            "solar_day": temp_date.day if start_date <= temp_date <= end_date else "",
            "lunar_day": lunar_temp_date["day"] if lunar_temp_date else "",
            "lunar_month": lunar_temp_date["month"] if lunar_temp_date else "",
            "lunar_year": lunar_temp_date["year"] if lunar_temp_date else "",
            "is_today": temp_date == datetime.now().date(),
        })
        temp_date += timedelta(days=1)
    
    # Chia thành các tuần
    weeks = [days[i:i+7] for i in range(0, 35, 7)]
    
    # Thông tin header và context
    context = {
        "weeks": weeks,
        "header": ["T2", "T3", "T4", "T5", "T6", "T7", "CN"],
        "info": {
            "weekday": get_vietnamese_weekday(current_date.strftime("%A")),
            "solar_day": current_date.day,
            "solar_month": current_date.month,
            "solar_year": current_date.year,
            "lunar_day": lunar_date["day"] if lunar_date else "",
            "lunar_month": lunar_date["month"] if lunar_date else "",
            "lunar_year": get_can_chi(lunar_date["year"]) if lunar_date else "",
            "pl": get_buddhist_year(current_date),
        },
        "lunar_month_info": lunar_month_info,  # Thông tin về tháng âm lịch
    }
    return render(request, "index.html", context)
