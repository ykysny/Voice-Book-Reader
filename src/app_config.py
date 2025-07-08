from pathlib import Path
from PySide6.QtCore import QSettings


class ThemeConfig:
    def __init__(self, theme, dark="#333333", light="#f5f5f5"):
        self.theme = theme
        self.dark = dark
        self.light = light


class CheckFilesConfig:
    def __init__(self, config_dir, icons_dir, books_dir, nltk_data_dir, theme_config):
        self.config_dir = config_dir
        self.icons_dir = icons_dir
        self.books_dir = books_dir
        self.nltk_data_dir = nltk_data_dir
        self.theme_config = theme_config


class MainWindowConfig:
    def __init__(self, settings, icons_dir, theme_config):
        self.settings = settings
        self.icons_dir = icons_dir
        self.theme_config = theme_config


class ReaderConfig:
    def __init__(self, settings, books_dir, config_dir):
        self.settings = settings
        self.books_dir = books_dir
        self.config_dir = config_dir


class SettingsWidgetConfig:
    def __init__(self, settings, config_dir, icons_dir, core_dir, theme_config):
        self.settings = settings
        self.config_dir = config_dir
        self.icons_dir = icons_dir
        self.core_dir = core_dir
        self.theme_config = theme_config


class AppConfig:
    def __init__(self):
        # Root path of the project (points to src/)
        self.BASE_DIR = Path(__file__).resolve().parent

        # Shared resource paths
        self.BOOKS_DIR = self.BASE_DIR / "books"
        self.ICONS_DIR = self.BASE_DIR / "icons"
        self.CONFIG_DIR = self.BASE_DIR / "config"
        self.NLTK_DATA_DIR = self.BASE_DIR / "nltk_data"
        self.CORE_DIR = self.BASE_DIR / "core"

        self.SETTINGS = QSettings(str(self.CONFIG_DIR / "settings.ini"), QSettings.IniFormat)

        self.theme_config = ThemeConfig(theme=self.SETTINGS.value("theme", "dark"))

        # Module-specific configuration objects
        self.check_files = CheckFilesConfig(
            config_dir=self.CONFIG_DIR,
            icons_dir=self.ICONS_DIR,
            books_dir=self.BOOKS_DIR,
            nltk_data_dir=self.NLTK_DATA_DIR,
            theme_config=self.theme_config,
        )

        self.main_window = MainWindowConfig(
            settings=self.SETTINGS,
            icons_dir=self.ICONS_DIR,
            theme_config=self.theme_config,
        )

        self.reader = ReaderConfig(
            settings=self.SETTINGS,
            books_dir=self.BOOKS_DIR,
            config_dir=self.CONFIG_DIR,
        )

        self.settings_widget = SettingsWidgetConfig(
            settings=self.SETTINGS,
            config_dir=self.CONFIG_DIR,
            icons_dir=self.ICONS_DIR,
            core_dir=self.CORE_DIR,
            theme_config=self.theme_config,
        )