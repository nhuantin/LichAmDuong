from django.db import models

class CalendarEntry(models.Model):
    solar_date = models.DateField("Ngày dương lịch")
    lunar_date = models.CharField("Ngày âm lịch", max_length=20)
    pl_time = models.CharField("Giờ PL", max_length=20, blank=True)  # Ví dụ: "2569 05:04:56"

    def __str__(self):
        return f"{self.solar_date} - {self.lunar_date}"