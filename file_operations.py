import os
import re
from tkinter import messagebox
from i18n.languages import LanguageManager


def rename_files_and_folders(folder_path, text, add_to, replace_text, with_text):
    lang = LanguageManager()
    try:
        for item_name in os.listdir(folder_path):
            old_path = os.path.join(folder_path, item_name)
            modified_name = item_name.replace(replace_text, with_text)

            if add_to == "prefix":
                new_name = f"{text}{modified_name}"
            else:
                name_root, name_ext = os.path.splitext(modified_name) if os.path.isfile(old_path) else (
                modified_name, "")
                new_name = f"{name_root}{text}{name_ext}"

            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(lang.get_text('renamed_file').format(item_name, new_name))

    except Exception as e:
        messagebox.showerror(
            lang.get_text('error'),
            lang.get_text('operation_error').format(str(e))
        )


def capitalize_names(folder_path):
    lang = LanguageManager()
    try:
        for item_name in os.listdir(folder_path):
            old_path = os.path.join(folder_path, item_name)
            parts = re.split(r"([ _])", item_name)
            new_parts = []
            for part in parts:
                if part not in ('_', ' '):
                    new_part = part[0].upper() + part[1:] if part else part
                    new_parts.append(new_part)
                else:
                    new_parts.append(part)
            new_name = ''.join(new_parts)

            if new_name != item_name:
                new_path = os.path.join(folder_path, new_name)
                os.rename(old_path, new_path)
                print(lang.get_text('renamed_file').format(item_name, new_name))

    except Exception as e:
        messagebox.showerror(
            lang.get_text('error'),
            lang.get_text('operation_error').format(str(e))
        ) 