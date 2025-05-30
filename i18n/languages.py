SUPPORTED_LANGUAGES = {
    'English': {
        'app_name': 'Refilea',
        'language': 'Language',
        'folder_path': 'Folder Path:',
        'browse': 'Browse',
        'text_to_add': 'Text to Add:',
        'add_text_as': 'Add Text As:',
        'prefix': 'Prefix',
        'suffix': 'Suffix',
        'replace_text': 'Replace Text:',
        'with_text': 'With:',
        'rename_files': 'Rename Files',
        'capitalize_names': 'Capitalize Names',
        'log_output': 'Log Output:',
        'error': 'Error',
        'select_folder_error': 'Please select a folder first.',
        'operation_error': 'An error occurred: {}',
        'renamed_file': "Renamed '{}' to '{}'"
    },
    '简体中文': {
        'app_name': '复序',
        'language': '语言',
        'folder_path': '文件夹路径：',
        'browse': '浏览',
        'text_to_add': '添加文本：',
        'add_text_as': '添加方式：',
        'prefix': '前缀',
        'suffix': '后缀',
        'replace_text': '替换文本：',
        'with_text': '替换为：',
        'rename_files': '重命名文件',
        'capitalize_names': '首字母大写',
        'log_output': '日志输出：',
        'error': '错误',
        'select_folder_error': '请先选择文件夹。',
        'operation_error': '发生错误：{}',
        'renamed_file': "已将 '{}' 重命名为 '{}'"
    }
}

class LanguageManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._current_language = 'English'
        return cls._instance
    
    @property
    def current_language(self):
        return self._current_language
    
    @current_language.setter
    def current_language(self, lang_code):
        if lang_code in SUPPORTED_LANGUAGES:
            self._current_language = lang_code
        else:
            raise ValueError(f"Language {lang_code} is not supported")
    
    def get_text(self, key):
        return SUPPORTED_LANGUAGES[self._current_language].get(key, f"Missing text: {key}")
    
    @property
    def available_languages(self):
        return list(SUPPORTED_LANGUAGES.keys()) 