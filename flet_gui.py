# 版权所有 @renxuanyao@formail.com 侵权必究
# Copyright @renxuanyao@formail.com . All rights reserved. Unauthorized use is strictly prohibited.
import flet as ft
from file_operations import rename_files_and_folders, capitalize_names
from i18n.languages import LanguageManager
import sys
import os

class PrintLogger:
    """Redirects print statements to a Text widget."""
    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, text):
        if self.text_area.page:  # Only update if the control is added to the page
            current = self.text_area.value or ""
            self.text_area.value = current + text
            self.text_area.update()

    def flush(self):
        pass


class RenameApp:
    # Initialization
    def __init__(self, page: ft.Page):
        self.page = page
        self.lang = LanguageManager()
        self.setup_page()
        self.create_widgets()
        self.setup_layout()
        self.update_language()

    # Set page size
    def setup_page(self):
        # Window configuration
        self.page.window.resizable = False
        self.page.window.maximizable = True
        self.page.auto_scroll = False
        self.page.window.width = 700
        self.page.window.height = 450
        self.page.window.min_width = 700
        self.page.window.min_height = 450
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.spacing = 10
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Fuxee.ico")
        self.page.window.icon = icon_path

    def toggle_theme(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK 
            if self.page.theme_mode == ft.ThemeMode.LIGHT 
            else ft.ThemeMode.LIGHT
        )
        self.theme_button.name = "dark_mode" if self.page.theme_mode == ft.ThemeMode.LIGHT else "light_mode"
        self.page.update()

    def create_widgets(self):
        # Create file picker
        self.file_picker = ft.FilePicker(
            on_result=self.on_folder_picked
        )
        self.page.overlay.append(self.file_picker)
        
        # Theme toggle button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            on_click=self.toggle_theme,
            tooltip="Toggle theme"
        )
        
        # Language selector
        self.language_dropdown = ft.Dropdown(
            width=150,
            label="Language",
            options=[ft.dropdown.Option(lang) for lang in self.lang.available_languages],
            value=self.lang.current_language,
            on_change=self.on_language_change,
            border_width= 2,
            border_color = ft.Colors.INVERSE_SURFACE
        )

        # Folder selection
        self.folder_path = ft.TextField(
            label="Folder Path",  # Default label
            read_only=False,
            width=505,
            border_width=2,
            border_color=ft.Colors.INVERSE_SURFACE
        )
        self.browse_button = ft.ElevatedButton(
            text="Browse",  # Default text
            on_click=lambda _: self.file_picker.get_directory_path(),
            icon=ft.Icons.FOLDER_OPEN
        )

        # Text to add
        self.text_to_add = ft.TextField(
            label="Text to Add",  # Default label
            width=600,
            border_width=2,
            border_color=ft.Colors.INVERSE_SURFACE
        )

        # Prefix/Suffix radio
        self.add_as_text = ft.Text("Add Text As")  # Default text
        self.add_as = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="prefix", label="Prefix"),  # Default labels
                ft.Radio(value="suffix", label="Suffix")
            ]),
            value="prefix"
        )

        # Replace text
        self.replace_text = ft.TextField(
            label="Replace Text",  # Default label
            width=290,
            border_width=2,
            border_color=ft.Colors.INVERSE_SURFACE
        )
        self.with_text = ft.TextField(
            label="With",  # Default label
            width=290,
            border_width=2,
            border_color=ft.Colors.INVERSE_SURFACE
        )

        # Action buttons
        self.rename_button = ft.ElevatedButton(
            text="Rename Files and Folders",  # Default text
            on_click=self.start_renaming,
            width=290,
            icon=ft.Icons.DRIVE_FILE_RENAME_OUTLINE
        )
        self.capitalize_button = ft.ElevatedButton(
            text="Capitalize Names",  # Default text
            on_click=self.start_capitalizing,
            width=290,
            icon=ft.Icons.TEXT_FIELDS
        )

        # Log output
        self.log_label = ft.Text(
            value="Log Output",
            visible = False,
        )  # Default text
        self.log_text = ft.TextField(
            visible=False,
            multiline=True,
            read_only=True,
            min_lines=10,
            max_lines=10,
            width=600,
            border_width=2,
            border_color=ft.Colors.INVERSE_SURFACE
        )

    def setup_layout(self):
        # Set up logging before adding controls
        self.logger = PrintLogger(self.log_text)
        sys.stdout = self.logger

        # Add all controls to the page in a container
        self.page.add(
            ft.Container(
                content=ft.Column([
                    # Top row with language and theme controls
                    ft.Row([self.language_dropdown, self.theme_button]),
                    # File selection row
                    ft.Row([self.folder_path,self.browse_button]),
                    ft.Row([self.text_to_add]),
                    ft.Row([self.add_as_text, self.add_as]),
                    ft.Row([self.replace_text, ft.Container(width=20), self.with_text]),
                    ft.Row([self.rename_button, self.capitalize_button],spacing=20),
                    ft.Row([self.log_label]),
                    ft.Row([self.log_text])
                ], spacing=20),
                padding=10,
            )
        )

    def update_language(self):
        self.page.title = self.lang.get_text('app_name')
        self.language_dropdown.label = self.lang.get_text('language')
        self.folder_path.label = self.lang.get_text('folder_path')
        self.browse_button.text = self.lang.get_text('browse')
        self.text_to_add.label = self.lang.get_text('text_to_add')
        self.add_as_text.value = self.lang.get_text('add_text_as')
        self.add_as.content.controls[0].label = self.lang.get_text('prefix')
        self.add_as.content.controls[1].label = self.lang.get_text('suffix')
        self.replace_text.label = self.lang.get_text('replace_text')
        self.with_text.label = self.lang.get_text('with_text')
        self.rename_button.text = self.lang.get_text('rename_files')
        self.capitalize_button.text = self.lang.get_text('capitalize_names')
        self.log_label.value = self.lang.get_text('log_output')
        self.page.update()

    def on_language_change(self, e):
        self.lang.current_language = self.language_dropdown.value
        self.update_language()

    def on_folder_picked(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.folder_path.value = e.path
            self.page.update()

    def start_renaming(self, e):
        folder_path = self.folder_path.value
        text = self.text_to_add.value
        add_to = self.add_as.value
        replace_text = self.replace_text.value
        with_text = self.with_text.value
        rename_files_and_folders(folder_path, text, add_to, replace_text, with_text)
        self.page.update()

    def start_capitalizing(self, e):
        folder_path = self.folder_path.value
        if not folder_path:
            self.page.dialog = ft.AlertDialog(
                title=ft.Text(self.lang.get_text('error')),
                content=ft.Text(self.lang.get_text('select_folder_error'))
            )
            self.page.dialog.open = True
            self.page.update()
            return
        capitalize_names(folder_path)
        self.page.update()


def main(page: ft.Page):
    app = RenameApp(page)