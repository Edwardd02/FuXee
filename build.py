import PyInstaller.__main__
import os

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',  # Main entry point
    '--name=Fuxee',
    '--onefile',
    '--windowed',  # Use windowed mode to prevent console from showing
    f'--icon={os.path.join(current_dir, "assets", "Fuxee.ico")}',
    '--add-data=assets;assets',
    '--add-data=i18n;i18n',
    f'--additional-hooks-dir={current_dir}',
    '--clean',
    '--noconfirm'
])