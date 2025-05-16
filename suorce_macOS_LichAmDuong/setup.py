from setuptools import setup

APP = ['LichAmDuong.py']
DATA_FILES = [
    ('fonts', ['fonts/arial.ttf']),
+   ('icons', ['icon.icns', 'icon.ico'])  # Thêm icons
]

OPTIONS = {
-    'argv_emulation': True,
+    'argv_emulation': False,  # Tắt cho ứng dụng GUI
     'iconfile': 'icon.icns',
+    'packages': ['pystray', 'PIL', 'lunarcalendar'],  # Thêm packages
     'includes': [
         'pystray',
-        'requests',
-        'PIL',
-        'packaging',
-        'lunarcalendar', 
-        'tkinter',
-        'calendar',
-        'threading',
-        'webbrowser',
-        'time',
-        'datetime',
-        'io',
-        'sys',
+        'pystray._darwin',  # Quan trọng cho macOS
+        'PIL.Image',
+        'PIL.ImageTk',
+        'lunarcalendar.convert',
+        'lunarcalendar.solarterm'
     ],
-    'resources': ['fonts/arial.ttf'],
+    'resources': ['fonts', 'icons'],  # Thêm toàn bộ thư mục
+    'plist': {
+        'CFBundleName': 'LichAmDuong',
+        'CFBundleDisplayName': "Lịch Âm Dương",
+        'CFBundleIdentifier': "com.nhuantin.LichAmDuong",
+        'NSRequiresAquaSystemAppearance': False  # Dark mode support
+    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
+    version='1.0.1',  # Thêm version
+    name='LichAmDuong'
)