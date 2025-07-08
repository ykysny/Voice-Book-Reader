import sys
from PySide6.QtWidgets import QApplication

from src.app_config import AppConfig
from src.utils.check_files import check_files
from src.gui.main_widget import MainWidget


def main():
    config = AppConfig()

    app = QApplication([])

    if check_files(config.check_files):
        from nltk.data import path
        path.append(config.NLTK_DATA_DIR)

        main_widget = MainWidget(config.main_window, config.reader, config.settings_widget)
        main_widget.show()
        
        sys.exit(app.exec())
    else:
        app.quit()


if __name__ == "__main__":
    main()