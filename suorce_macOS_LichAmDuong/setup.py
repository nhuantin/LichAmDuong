from setuptools import setup

APP = ['LichAmDuong.py']
DATA_FILES = [
    ('fonts', ['fonts/arial.ttf']),
    ('icons', ['icon.icns', 'icon.ico'])
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'icon.icns',
    'packages': ['pystray', 'PIL', 'lunarcalendar'],
    'includes': [
        'pystray',
        'pystray._darwin',
        'PIL.Image',
        'PIL.ImageTk',
        'lunarcalendar.convert',
        'lunarcalendar.solarterm'
    ],
    'resources': ['fonts', 'icons'],
    'plist': {
        'CFBundleName': 'LichAmDuong',
        'CFBundleDisplayName': u"Lịch Âm Dương",
        'CFBundleIdentifier': "com.nhuantin.LichAmDuong",
        'NSRequiresAquaSystemAppearance': False
    }
}

setup(
    name='LichAmDuong',
    version='1.0.1',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
