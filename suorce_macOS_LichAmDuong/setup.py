from setuptools import setup

APP = ['LichAmDuong.py']
DATA_FILES = [
    ('fonts', ['fonts/arial.ttf']),
    # Thêm các thư mục/resources khác nếu có
]

OPTIONS = {
    'argv_emulation': False,  # Nên tắt nếu ứng dụng không xử lý argument
    'iconfile': 'icon.icns',
    'packages': [  # Thêm các package cần thiết
        'pystray',
        'requests',
        'PIL',
        'packaging',
        'lunarcalendar',
        'tkinter'
    ],
    'includes': [  # Các module cần include thủ công
        'lunarcalendar.convert',
        'lunarcalendar.solarterm',
        'PIL.Image',
        'PIL.ImageTk',
        'pystray._darwin'
    ],
    'excludes': ['PyQt5', 'PySide2'],  # Loại bỏ package không dùng
    'resources': ['fonts/arial.ttf'],
    'plist': {
        'CFBundleName': 'LichAmDuong',
        'CFBundleShortVersionString': '1.0.1',
        'CFBundleVersion': '1.0.1',
        'NSHumanReadableCopyright': 'Copyright © 2023 Your Name'
    }
}

setup(
    name="LichAmDuong",
    version="1.0.1",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
