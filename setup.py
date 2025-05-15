from setuptools import setup

APP = ['LichAmDuong.py']
DATA_FILES = [('fonts', ['fonts/arial.ttf'])]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'includes': [
        'pystray',
        'requests',
        'PIL',
        'packaging',
        'lunarcalendar', 
        'tkinter',
        'calendar',
        'threading',
        'webbrowser',
        'time',
        'datetime',
        'io',
        'sys',
    ],
    'resources': ['fonts/arial.ttf'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
