import flet as ft
from flet_gui import main
import os
import re
from tkinter import messagebox
from i18n.languages import LanguageManager
import flet_gui
import file_operations

if __name__ == "__main__":
    ft.app(target=main, view=ft.FLET_APP)