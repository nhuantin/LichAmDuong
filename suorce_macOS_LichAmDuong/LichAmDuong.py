import os
import sys
import time
import pystray
import calendar
import requests
import threading
import webbrowser
import tkinter as tk
from io import BytesIO
from PIL import ImageDraw
from packaging import version
from tkinter import messagebox
from PIL import Image, ImageTk
from pystray import MenuItem as item
from datetime import datetime, timedelta
from tkinter import ttk, font, messagebox
from lunarcalendar import Converter, Solar, Lunar, DateNotExist

def check_update():
    current_version = "1.0.1"
    try:
        # Thêm xác thực SSL và kiểm tra hash
        version_url = "https://raw.githubusercontent.com/nhuantin/LichAmDuong/main/version.json" 
        response = requests.get(version_url, verify=True)  # Bật xác thực SSL
        if response.status_code != 200:
            return
        
        data = response.json()
        if version.parse(data["version"]) > version.parse(current_version):
            # Hiển thị thông báo cho người dùng thay vì tự động tải
            user_choice = messagebox.askyesno(
                "Cập nhật", 
                f"Phiên bản mới {data['version']} đã có. Bạn có muốn tải về không?"
            )
            if user_choice:
                os_name = platform.system()
                url = data.get("exe_url") if os_name == "Windows" else data.get("dmg_url")
                if url:
                    webbrowser.open(url)
                else:
                    print("Không tìm thấy URL tải về.")
    except Exception as e:
        print(f"Lỗi cập nhật: {str(e)}")
if __name__ == "__main__":
    check_update()

def resource_path(relative_path):
    """Get absolute path to resource với fallback"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)
    
    if not os.path.exists(full_path):
        print(f"Warning: Resource not found at {full_path}")
        return relative_path  # Fallback về đường dẫn tương đối
    
    return full_path
    
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

class VietnameseCalendarApp:
    def __init__(self, root):
        self.root = root
        self.buddha_images = {}
        self.cal_type = tk.StringVar(value="solar")
        self.show_grid = True
        self.compact_footer = False
        self.initialize_app()
        self.root.after(100, self.set_window_position)

    def preload_buddha_images(self):
        """Chỉ tải ảnh Phật giáo nếu hôm nay là ngày lễ, và chưa có trong cache."""
        def fetch_image(event_key, url):
            if event_key in self.buddha_images:
                print(f"✓ Đã có ảnh cho {event_key} trong cache")
                return

            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    print(f"Lỗi tải ảnh: {response.status_code} - {url}")
                    return

                image = Image.open(BytesIO(response.content))

                # Resize ảnh theo kích thước giao diện
                try:
                    self.root.update_idletasks()
                    grid_width = self.grid_frame.winfo_width()
                    if grid_width < 10:
                        grid_width = 300
                    image = image.resize((grid_width, 200), Image.Resampling.LANCZOS)
                except:
                    image = image.resize((300, 200), Image.LANCZOS)

                # Đưa vào cache
                photo = ImageTk.PhotoImage(image)
                self.buddha_images[event_key] = photo
                print(f"✓ Đã tải ảnh cho {event_key}")
            except Exception as e:
                print(f"Lỗi xử lý ảnh {url}: {e}")

        # Lấy ngày âm hiện tại
        try:
            d = self.displayed_date
            lunar = Converter.Solar2Lunar(Solar(d.year, d.month, d.day))
            key = (lunar.day, lunar.month)

            if key in phat_giao_events and key not in self.buddha_images:
                print(f"Đang tải ảnh cho sự kiện hôm nay: {phat_giao_events[key][0]}")
                url = phat_giao_events[key][1]
                fetch_image(key, url)
        except Exception as e:
            print(f"Lỗi lấy ngày âm hoặc tải ảnh: {e}")


        # Xác định ngày hiện tại và tháng âm lịch hiện tại
        current_day = self.displayed_date.day
        current_month = self.displayed_date.month
        current_year = self.displayed_date.year
        
        # Xác định ngày âm lịch hiện tại
        current_lunar_date = Converter.Solar2Lunar(
            Solar(current_year, current_month, current_day)
        )
        current_lunar_day = current_lunar_date.day
        current_lunar_month = current_lunar_date.month
        
        # Kiểm tra xem ngày hiện tại có phải ngày lễ Phật giáo không
        current_buddha_key = (current_lunar_day, current_lunar_month)
        
        # Tải ảnh cho ngày hiện tại nếu là ngày lễ
        if current_buddha_key in phat_giao_events:
            event_name, url = phat_giao_events[current_buddha_key]
            print(f"Ưu tiên tải ảnh cho ngày hiện tại: {event_name} - {current_buddha_key}")
            
            if url.startswith(('http://', 'https://')):
                # Tải đồng bộ để đảm bảo hiển thị ngay
                fetch_image(current_buddha_key, url)
        
    def check_buddha_event(self):
        """Kiểm tra và hiển thị sự kiện Phật giáo nếu có"""
        try:
            # Chuyển ngày hiện tại sang âm lịch
            solar_date = Solar(self.displayed_date.year, self.displayed_date.month, self.displayed_date.day)
            lunar_date = Converter.Solar2Lunar(solar_date)
            current_key = (lunar_date.day, lunar_date.month)
        
            # Kiểm tra xem có phải ngày lễ Phật giáo không
            if current_key in phat_giao_events:
                event_name, image_url = phat_giao_events[current_key]

                if current_key in self.buddha_images:
                    img = self.buddha_images[current_key]
                    self.buddha_frame.pack_forget()

                    # Hiển thị ảnh đè lên grid
                    self.overlay_image_label.config(image=img)
                    self.overlay_image_label.image = img
                    self.overlay_image_label.lift()

                    # Xóa label cũ nếu có
                    if hasattr(self, 'event_name_labels'):
                        for lbl in self.event_name_labels:
                            lbl.destroy()

                    # Tạo viền chữ bằng nhiều label đen
                    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    self.event_name_labels = []
                    for dx, dy in offsets:
                        shadow = tk.Label(
                            self.grid_frame,
                            text=event_name,
                            font=("Arial", 11, "bold"),
                            fg="black",
                            bg=self.grid_frame.cget("bg"),  # gần giống trong suốt
                        )
                        shadow.place(relx=0.5, rely=0.92, anchor="center", x=dx, y=dy)
                        self.event_name_labels.append(shadow)

                    # Label chính màu trắng
                    main_label = tk.Label(
                        self.grid_frame,
                        text=event_name,
                        font=("Arial", 11, "bold"),
                        fg="white",
                        bg=self.grid_frame.cget("bg"),
                    )
                    main_label.place(relx=0.5, rely=0.92, anchor="center")
                    self.event_name_labels.append(main_label)

                else:
                    # Ẩn nếu chưa tải ảnh
                    self.buddha_frame.pack_forget()
                    self.overlay_image_label.config(image="")
                    if hasattr(self, 'event_name_label'):
                        self.event_name_label.config(text="")
                    self.preload_buddha_images()
            
        except Exception as e:
            print(f"Lỗi kiểm tra sự kiện Phật giáo: {str(e)}")
            self.buddha_frame.pack_forget()
    
    def initialize_app(self):
        # Cấu hình cơ bản
        self.root.title("")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
    
        # Khởi tạo biến trạng thái TRƯỚC
        self.current_date = datetime.now()
        self.displayed_date = self.current_date
        self.leap_month_data = {}
        self.buddha_photo = None
        self.current_buddha_day = None
    
        # Tải ảnh trước (không chặn GUI)
        self.preload_buddha_images()
    
        # Thiết lập font chữ
        self.bold_font = font.Font(family="Arial", size=18, weight="bold")
        self.normal_font = font.Font(family="Arial", size=16)
        self.small_font = font.Font(family="Arial", size=8)
    
        # Vô hiệu hóa padding mặc định
        self.root.option_add('*padY', 0)
        self.root.option_add('*pady', 0)
        self.root.option_add('*padX', 0)
        self.root.option_add('*padx', 0)
    
        # Thiết lập giao diện
        self.setup_icon()
        self.set_window_position()
        self.create_widgets()
        self.update_calendar()
        self.update_time()
        self.adjust_window_size()

    def create_widgets(self):
        """Tạo các thành phần giao diện"""
        # Frame trên cùng chứa toàn bộ giao diện trừ footer
        self.top_frame = tk.Frame(self.root, bd=0)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Footer sát đáy
        self.footer_frame = tk.Frame(self.root, bd=0)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Thêm các thành phần vào top_frame
        self.create_date_search()
        self.create_header()
        self.create_calendar_grid()
        self.create_footer()

    def create_header(self):
        """Tạo phần header"""
        header_container = tk.Frame(
            self.top_frame, 
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        header_container.pack(fill=tk.X, pady=0, padx=0)

        header_center = tk.Frame(
            header_container,
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        header_center.pack(expand=True, anchor="n", pady=0, padx=0)

        self.date_label = tk.Label(
            header_center, 
            font=self.bold_font, 
            fg='#2986cc', 
            bd=0,
            pady=0
        )
        self.date_label.pack(anchor="n", pady=0, padx=0)

        info_frame = tk.Frame(header_center, bd=0, highlightthickness=0)
        info_frame.pack(pady=1)

        self.prefix_label = tk.Label(info_frame, font=self.normal_font, fg='#8fce00', bd=0)
        self.prefix_label.pack(side=tk.LEFT, padx=0)

        self.lunar_month_label = tk.Label(info_frame, font=self.normal_font, fg='#8fce00', bd=0)
        self.lunar_month_label.pack(side=tk.LEFT, padx=0)

        self.lunar_year_label = tk.Label(info_frame, font=self.normal_font, fg='#8fce00', bd=0)
        self.lunar_year_label.pack(side=tk.LEFT, padx=(12, 0))

        self.leap_symbol = tk.Label(info_frame, font=("Arial", 12), fg="red", bd=0)
        self.leap_symbol.place(in_=self.lunar_month_label, relx=1.25, rely=-0.1, anchor="ne")

        self.leap_month_indicator = tk.Label(info_frame, font=("Arial", 8), fg="red", bd=0)
        self.leap_month_indicator.place(
            in_=self.lunar_month_label, relx=1.25, rely=0.1, anchor="se"
        )

        row_frame = tk.Frame(
            header_center,
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        row_frame.pack(fill=tk.X, pady=0, padx=0)

        self.phat_lich_label = tk.Label(
            row_frame, 
            font=("Arial", 14, "bold"), 
            fg='red',
            bd=0,
            padx=0,
            pady=0
        )
        self.phat_lich_label.pack(side=tk.LEFT, anchor='w', padx=0, pady=0)

        self.time_label = tk.Label(
            row_frame, 
            font=("Arial", 14, "bold"), 
            fg='#0539f5',
            bd=0,
            padx=0,
            pady=0
        )
        self.time_label.pack(side=tk.RIGHT, anchor='e', padx=0, pady=0)

        # Phần Buddha frame
        self.buddha_frame = tk.Frame(
            header_center,
            height=0,
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        self.buddha_frame.pack(fill=tk.X, pady=0, padx=0)
        self.buddha_label = tk.Label(self.buddha_frame, bd=0, pady=0, padx=0)
        self.buddha_label.pack(pady=0, padx=0)
    
    # Phần chức năng
    def update_time(self):
        """Cập nhật thời gian thực"""
        self.time_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(500, self.update_time)  # Giảm thời gian cập nhật xuống 500ms

    def update_calendar(self):
        """Cập nhật toàn bộ giao diện lịch"""
        self.update_date_display()
        self.update_lunar_info()
        self.check_buddha_event()
        self.fill_calendar_grid()

    def update_date_display(self):
        """Cập nhật hiển thị ngày tháng"""
        weekday = self.displayed_date.weekday()
        day_name = self.get_vietnamese_weekday(weekday)
        self.date_label.config(text=f"{day_name} {self.displayed_date.strftime('%d/%m/%Y')}")

    def get_vietnamese_weekday(self, weekday):
        """Lấy tên thứ tiếng Việt"""
        weekdays = {
            0: "Thứ hai", 1: "Thứ ba", 2: "Thứ tư",
            3: "Thứ năm", 4: "Thứ sáu", 5: "Thứ bảy",
            6: "Chủ nhật"
        }
        return weekdays.get(weekday, "")

    def update_lunar_info(self):
        """Cập nhật thông tin âm lịch chính xác cho Việt Nam"""
        try:
            # Điều chỉnh múi giờ Việt Nam (UTC+7)
            local_date = self.displayed_date + timedelta(hours=7)
            solar_date = Solar(self.displayed_date.year, self.displayed_date.month, self.displayed_date.day)
            lunar_date = Converter.Solar2Lunar(solar_date)

            lunar_day = lunar_date.day
            lunar_month = lunar_date.month
            lunar_year = lunar_date.year
            is_leap_month = lunar_date.isleap

            # Xác định số ngày trong tháng âm
            try:
                next_month = lunar_month + 1 if lunar_month < 12 else 1
                next_year = lunar_year if lunar_month < 12 else lunar_year + 1
                next_month_start = Converter.Lunar2Solar(Lunar(next_year, next_month, 1)).to_date()
                current_month_start = Converter.Lunar2Solar(Lunar(lunar_year, lunar_month, 1)).to_date()
                num_lunar_days = (next_month_start - current_month_start).days
            except DateNotExist:
                num_lunar_days = 30

            # Tạo danh sách ngày chay động
            base_days = [1, 8, 14, 15, 18, 23, 24, 28, 29]
        
            # Thêm ngày 30 nếu tháng đủ, hoặc 27 nếu tháng thiếu
            if num_lunar_days == 30:
                ngay_chay = base_days + [30]
            else:
                ngay_chay = base_days + [27]

            # Kiểm tra ngày chay
            self.prefix_label.config(text="Ngày chay " if lunar_day in ngay_chay else "Âm lịch ")

            # Xác định ngày trong tháng âm
            month_display = f"{lunar_day}/{lunar_month}"
            self.lunar_month_label.config(text=month_display)

            # Xác định ký hiệu T/Đ
            leap_symbol = "Đ" if num_lunar_days == 30 else "T"
            self.leap_symbol.config(text=leap_symbol)
            
            # Cập nhật hiển thị "N" cho tháng nhuận
            self.leap_month_indicator.config(text="N" if is_leap_month else "")
            
            # danh sách Can-Chi
            can_chi = ["Giáp Tý", "Ất Sửu", "Bính Dần", "Đinh Mão", "Mậu Thìn", 
                       "Kỷ Tỵ", "Canh Ngọ", "Tân Mùi", "Nhâm Thân", "Quý Dậu", 
                       "Giáp Tuất", "Ất Hợi", "Bính Tý", "Đinh Sửu", "Mậu Dần", 
                       "Kỷ Mão", "Canh Thìn", "Tân Tỵ", "Nhâm Ngọ", "Quý Mùi", 
                       "Giáp Thân", "Ất Dậu", "Bính Tuất", "Đinh Hợi", "Mậu Tý", 
                       "Kỷ Sửu", "Canh Dần", "Tân Mão", "Nhâm Thìn", "Quý Tỵ", 
                       "Giáp Ngọ", "Ất Mùi", "Bính Thân", "Đinh Dậu", "Mậu Tuất", 
                       "Kỷ Hợi", "Canh Tý", "Tân Sửu", "Nhâm Dần", "Quý Mão", 
                       "Giáp Thìn", "Ất Tỵ", "Bính Ngọ", "Đinh Mùi", "Mậu Thân", 
                       "Kỷ Dậu", "Canh Tuất", "Tân Hợi", "Nhâm Tý", "Quý Sửu", 
                       "Giáp Dần", "Ất Mão", "Bính Thìn", "Đinh Tỵ", "Mậu Ngọ", 
                       "Kỷ Mùi", "Canh Thân", "Tân Dậu", "Nhâm Tuất", "Quý Hợi"]
            index = (lunar_year - 1984) % 60
            self.lunar_year_label.config(text=can_chi[index])
            
            # PL: luôn hiển thị mỗi ngày, nhưng dựa trên năm âm lịch
            phat_lich = lunar_year + 544
            self.phat_lich_label.config(text=f"PL: {phat_lich}")
            
        except Exception as e:
            print(f"Lỗi cập nhật lịch âm: {str(e)}")
        
    def create_date_search(self):
        """Tạo phần tìm kiếm với lựa chọn loại lịch"""
        search_frame = tk.Frame(self.top_frame)
        search_frame.pack(fill=tk.X, padx=0, pady=0)

        # Ô nhập liệu
        input_frame = tk.Frame(search_frame)
        input_frame.pack(side=tk.LEFT, padx=10)

        # Phần nhập liệu (bên trái)
        input_frame = tk.Frame(search_frame)
        input_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        tk.Label(input_frame,
                text="Tìm ngày:",
                font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=0, anchor='w')

        # Tạo các ô nhập liệu
        self.day_entry = tk.Entry(input_frame, width=3, font=self.small_font)
        self.day_entry.pack(side=tk.LEFT, padx=0)
        tk.Label(input_frame, text="/").pack(side=tk.LEFT)

        self.month_entry = tk.Entry(input_frame, width=3, font=self.small_font)
        self.month_entry.pack(side=tk.LEFT, padx=0)
        tk.Label(input_frame, text="/").pack(side=tk.LEFT)

        self.year_entry = tk.Entry(input_frame, width=5, font=self.small_font)
        self.year_entry.pack(side=tk.LEFT, padx=0)

        # Phần nút bấm (bên phải)
        button_frame = tk.Frame(search_frame)
        button_frame.pack(side=tk.RIGHT)

        # Nút chức năng
        ttk.Button(button_frame,
                text="Xem",
                width=4,
                command=self.search_date).pack(side=tk.LEFT, padx=0)
        ttk.Button(button_frame,
                text="Hôm nay",
                width=10,
                command=self.show_current_date).pack(side=tk.LEFT, padx=5)

    def search_date(self):
        """Tìm kiếm ngày theo lịch Dương"""
        try:
            day = int(self.day_entry.get())
            month = int(self.month_entry.get())
            year = int(self.year_entry.get())

            # Kiểm tra tính hợp lệ của ngày
            if month < 1 or month > 12:
                raise ValueError("Tháng phải từ 1-12")
            
            max_day = calendar.monthrange(year, month)[1]
            if day < 1 or day > max_day:
                raise ValueError(f"Ngày phải từ 1-{max_day}")

            self.displayed_date = datetime(year, month, day)
            self.update_calendar()

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {str(e)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi hệ thống: {str(e)}")
    
    def create_entry(self, parent, default_value, width):
        """Tạo ô nhập liệu"""
        entry = tk.Entry(parent, width=width, font=self.small_font, bd=1)
        entry.insert(0, default_value)
        entry.pack(side=tk.LEFT, padx=0, ipady=0)
        return entry

    def fill_calendar_grid(self):
        """Điền các ngày vào lưới lịch"""
        try:
            year = self.displayed_date.year
            month = self.displayed_date.month
            first_day = datetime(year, month, 1)
            weekday = first_day.weekday()
            num_days = calendar.monthrange(year, month)[1]

            # Lấy ngày hiện tại một lần
            current_date = datetime.now()
            current_day = current_date.day
            current_month = current_date.month
            current_year = current_date.year

            # Reset grid
            for row in self.day_labels:
                for cell in row:
                    solar_label, lunar_label, cell_frame = cell
                    solar_label.config(text="", fg="black")
                    lunar_label.config(text="", fg="blue")
                    cell_frame.config(bg="white")

            # Điền ngày mới
            day_count = 1
            for row in range(5):
                for col in range(7):
                    if (row == 0 and col < weekday) or day_count > num_days:
                        continue
                    
                    solar_label, lunar_label, cell_frame = self.day_labels[row][col]
                    
                    if col == 6:
                        solar_label.config(fg="red")
                        lunar_label.config(fg="red")

                    # Hiển thị ngày dương
                    solar_label.config(text=str(day_count))

                    # Chuyển đổi sang âm lịch
                    try:
                        solar_day = Solar(year, month, day_count)
                        lunar_date = Converter.Solar2Lunar(solar_day)
                        lunar_text = f"{lunar_date.day}/{lunar_date.month}"
                        event_key = (lunar_date.day, lunar_date.month)
                    except DateNotExist:
                        lunar_text = ""
                        event_key = (0, 0)

                    lunar_label.config(text=lunar_text)

                    # Hiển thị ảnh Phật nếu có
                    if event_key in phat_giao_events:
                        if event_key in self.buddha_images:
                            img = self.buddha_images[event_key]
                            img_label = tk.Label(cell_frame, image=img, bg="white")
                            img_label.place(relx=0.5, rely=0.75, anchor="center")

                    # Đánh dấu ngày hiện tại
                    is_today = (
                        day_count == current_day and
                        month == current_month and
                        year == current_year
                    )
                    if is_today:
                        cell_frame.config(bg="#bce4fa")
                        solar_label.config(bg="#bce4fa")
                        lunar_label.config(bg="#bce4fa")

                    day_count += 1
                
        except Exception as e:
            print(f"Lỗi điền lịch: {str(e)}")
    
    def create_calendar_grid(self):
        """Tạo lưới lịch tích hợp header"""
        self.grid_frame = tk.Frame(
            self.top_frame,
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        self.grid_frame.pack(padx=0, pady=0, anchor="n", fill=tk.BOTH, expand=True)

        self.overlay_image_label = tk.Label(self.grid_frame, bd=0, bg='white')
        self.overlay_image_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay_image_label.lower()

        weekdays = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        for col, day in enumerate(weekdays):
            header_cell = tk.Frame(self.grid_frame, width=40, height=25, bd=1, relief="groove", bg="#f0f0f0")
            header_cell.grid(row=0, column=col, sticky="nsew", padx=0, pady=0)
            label = tk.Label(header_cell, text=day, font=self.small_font, fg="red" if col == 6 else "black", bg="#f0f0f0")
            label.place(relx=0.5, rely=0.5, anchor="center")

        self.day_labels = []
        for row in range(1, 6):
            row_labels = []
            for col in range(7):
                cell = self.create_calendar_cell(row, col)
                row_labels.append(cell)
            self.day_labels.append(row_labels)

    def create_header_cell(self, col):
        """Tạo ô header tích hợp"""
        weekdays = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        cell_frame = tk.Frame(
            self.grid_frame,
            width=27,
            height=25,  # Giảm chiều cao header
            bd=1,
            relief="groove",
            bg="#f0f0f0"
        )
        cell_frame.grid(row=0, column=col, sticky="nsew", padx=0, pady=0)
    
        label = tk.Label(
            cell_frame,
            text=weekdays[col],
            font=self.small_font,
            fg="red" if col == 6 else "black",
            bg="#f0f0f0"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        return (None, None, cell_frame)  # Không dùng solar/lunar label ở header

    def create_calendar_cell(self, row, col):
        """Tạo ô lịch với kích thước tối ưu"""
        cell_frame = tk.Frame(
            self.grid_frame,
            width=27,
            height=31,  # Giảm kích thước ô
            bd=1,
            relief="groove",
            bg="white"
        )
        cell_frame.grid(row=row, column=col, sticky="nsew", padx=0, pady=0)
    
        # Label ngày dương
        solar_label = tk.Label(
            cell_frame,
            font=self.small_font,
            bg="white"
        )
        solar_label.place(relx=0.5, rely=0.3, anchor="center")  # Điều chỉnh vị trí

        # Label ngày âm
        lunar_label = tk.Label(
            cell_frame,
            font=("Arial", 7),
            fg="blue",
            bg="white"
        )
        lunar_label.place(relx=0.5, rely=0.7, anchor="center")  # Điều chỉnh vị trí

        return (solar_label, lunar_label, cell_frame)
    
    def toggle_grid(self, icon=None, item=None):
        """Chuyển đổi chế độ hiển thị lưới lịch"""
        self.show_grid = not self.show_grid
        if self.show_grid:
            self.grid_frame.pack(padx=0, pady=0, anchor="n")
        else:
            self.grid_frame.pack_forget()
        self.adjust_window_size()

    def update_grid_visibility(self):
        """Cập nhật trạng thái hiển thị của lưới"""
        if self.show_grid:
            self.grid_frame.pack(padx=0, pady=0, anchor="n")
        else:
            self.grid_frame.pack_forget()

    def adjust_window_size(self):
        """Điều chỉnh kích thước cửa sổ"""
        if self.show_grid:
            self.root.geometry("280x310")
        else:
            self.root.geometry("280x130")
        self.set_window_position()
    
    def create_footer(self):
        footer_frame = self.footer_frame
        footer_frame.configure(pady=0)
    
        # Tác giả
        author = tk.Label(footer_frame, text="© Nhuận Tín", font=self.small_font, fg='blue', cursor="hand2")
        author.pack(side=tk.LEFT, padx=0, pady=0, anchor="e")
        author.bind("<Button-1>", lambda e: webbrowser.open("https://hocphat8.blogspot.com/"))

        # Label "Thoát"
        quit_label = tk.Label(footer_frame, text="Thoát", font=self.small_font, fg='blue', cursor="hand2")
        quit_label.pack(side=tk.RIGHT, padx=0, pady=0, anchor="e")
        quit_label.bind("<Button-1>", lambda e: self.quit_window())
    
    def show_current_date(self):
        """Hiển thị ngày hiện tại"""
        self.displayed_date = datetime.now()
        self.update_calendar()
        
    def show_window(self):
        """Hiển thị cửa sổ"""
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.update()
        self.root.attributes('-topmost', False)
        
    def setup_icon(self):
        """Thiết lập biểu tượng ứng dụng"""
        try:
            icon_path = self.get_icon_path()
            self.root.iconbitmap(icon_path)
            self.create_system_tray(icon_path)
        except Exception as e:
            print(f"Lỗi thiết lập icon: {e}")

    def get_icon_path(self):
        path = resource_path("icon.ico")
        if not os.path.exists(path):
            print(f"Cảnh báo: Không tìm thấy icon tại {path}")
        return path

    def create_system_tray(self, icon_path):
        try:
            image = Image.open(icon_path)
        except Exception as e:
            image = Image.new('RGB', (16, 16), color='blue')
            draw = ImageDraw.Draw(image)
            draw.text((3, 2), "L", fill='white')
    
        separator = item('', None, enabled=False)
        
        menu = (
            item('Hiện lịch', self.toggle_grid, checked=lambda item: self.show_grid),
            item('Ẩn lịch', self.toggle_grid, checked=lambda item: not self.show_grid),
            
            item('Mở', self.show_window),
            item('Thoát', self.quit_window)
        )

        self.tray_icon = pystray.Icon("Lịch Việt", image, "Lịch Âm Dương", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def set_window_position(self):
        self.root.update_idletasks()  # Cập nhật kích thước thực tế
        screen_width = self.root.winfo_screenwidth()
        window_width = self.root.winfo_width()
        x = screen_width - window_width - 0  # Thêm khoảng cách 10px từ lề phải
        self.root.geometry(f"+{x}+0")  # Đặt vị trí Y ở 10px từ top
        
    def quit_window(self):
        """Thoát ứng dụng"""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = VietnameseCalendarApp(root)
    root.mainloop()