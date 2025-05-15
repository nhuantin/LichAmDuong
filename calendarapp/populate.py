import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
import django
django.setup()
from calendarapp.models import CalendarEntry
from datetime import date, timedelta
from .utils import convert_to_lunar  # Thêm dòng này

def populate():
    start_date = date(2025, 5, 1)
    for day in range(31):
        current_date = start_date + timedelta(days=day)
        lunar_date = convert_to_lunar(current_date)  # Định dạng mới
        CalendarEntry.objects.create(
            solar_date=current_date,
            lunar_date=lunar_date,
            pl_time="00:00:00"
        )

if __name__ == '__main__':
    populate()