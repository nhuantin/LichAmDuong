from django.urls import path
from .views import calendar_view  # Import trực tiếp hàm view

urlpatterns = [
    path("", calendar_view, name="calendar"),  # Định nghĩa URL pattern
]