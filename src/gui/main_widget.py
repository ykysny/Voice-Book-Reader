from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QBoxLayout
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtCore import QSize, Qt, Slot, QThread

from src.gui.settings_widget import SettingsWidget
from src.core.reader import Reader
from src.gui.dialogs import QuickMessage


class MainWidget(QWidget):
    """Main window, the class responsible for GUI and common behavior."""
    def __init__(self, config, config_reader, config_settings_widget):
        super().__init__()
        self.setWindowTitle("Voice Book Reader")
        self.config = config
        self.load_settings()
        
        # It is a voice reader class.
        self.reader = Reader(self, config_reader)
        self.reader.reading_finished_signal.connect(self.reading_finished)
        self.reader.update_text_signal.connect(self.update_plain_text)
        
        self.thread = QThread()
        # Move to thread the certain func not the class.
        self.reader.moveToThread(self.thread)
        self.thread.started.connect(self.reader.read)
        
        self.settings_widget = SettingsWidget(self, config_settings_widget)
        
        self.start_stop_button = QPushButton()
        self.start_stop_button.setMaximumSize(40, 40)
        self.start_stop_button.setIconSize(QSize(40, 40))
        self.start_stop_button.setStyleSheet("border: none;")
        self.start_stop_button.clicked.connect(self.start_stop_button_clicked)
        
        self.previous_button = QPushButton()
        self.previous_button.setMaximumSize(40, 40)
        self.previous_button.setIconSize(QSize(40, 40))
        self.previous_button.setStyleSheet("border: none;")
        self.previous_button.clicked.connect(self.previous_button_clicked)
        
        self.next_button = QPushButton()
        self.next_button.setMaximumSize(40, 40)
        self.next_button.setIconSize(QSize(40, 40))
        self.next_button.setStyleSheet("border: none;")
        self.next_button.clicked.connect(self.next_button_clicked)
        
        self.settings_button = QPushButton()
        self.settings_button.setMaximumSize(40, 40)
        self.settings_button.setIconSize(QSize(40, 40))
        self.settings_button.setStyleSheet("border: none;")
        self.settings_button.clicked.connect(self.settings_button_clicked)
        
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.reader.update_plain_text()
        
        # To prevent capture space and arrow keys by widgets.
        # Thus these keys can be captured by "keyPressEvent".
        self.start_stop_button.setFocusPolicy(Qt.NoFocus)
        self.previous_button.setFocusPolicy(Qt.NoFocus)
        self.next_button.setFocusPolicy(Qt.NoFocus)
        self.settings_button.setFocusPolicy(Qt.NoFocus)
        self.text.setFocusPolicy(Qt.NoFocus)
        
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom, self))
        
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.start_stop_button)
        horizontal_layout.addWidget(self.previous_button)
        horizontal_layout.addWidget(self.next_button)
        horizontal_layout.addWidget(self.settings_button)
        
        self.set_theme()
        
        # Sets the width of the outer border on each side of the widget.
        self.layout().setContentsMargins(0, 5, 0, 0)
        self.layout().addLayout(horizontal_layout)
        self.layout().addWidget(self.text)
    
    @Slot()
    def update_plain_text(self, content):
        """Take the content from the "Reader" and update the plain text."""
        self.text.setPlainText(content)
        self.text.moveCursor(QTextCursor.End)
    
    @Slot()
    def start_stop_button_clicked(self):
        if self.thread.isRunning():
            # Stop the reading process.
            self.stop_reading()
        else:
            # Run the reading process.
            self.thread.start()
            self.start_stop_button.setIcon(
                QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "pause.ico"))
            )
    
    @Slot()
    def previous_button_clicked(self):
        if self.reader.process_state == 1:
            # Change the state of the launched reading process.
            self.reader.process_state = 2
        else:
            self.reader.current_reading_position = False
            # Previous sentence (direction == False).
            self.reader.change_current_sentence(False)
    
    @Slot()
    def next_button_clicked(self):
        if self.reader.process_state == 1:
            # Change the state of the launched reading process.
            self.reader.process_state = 3
        else:
            self.reader.current_reading_position = False
            # Next sentence (direction == True).
            self.reader.change_current_sentence(True)
    
    @Slot()
    def settings_button_clicked(self):
        """Open the settings window."""
        if self.thread.isRunning():
            self.stop_reading()
        
        self.settings_widget.setWindowModality(Qt.ApplicationModal)
        self.settings_widget.show()
    
    @Slot()
    def reading_finished(self, error):
        """The book was completely read or the reading process was interrupted."""
        # Exit the event loop of thread (it is not force to quit the reading process).
        self.thread.quit()
        self.thread.wait()
        
        self.start_stop_button.setIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "play.ico"))
        )
        
        if error:
            dialog = QuickMessage("Error", error, self.config, self)
            dialog.exec()
    
    def stop_reading(self):
        """Stop the reading process and close the reading thread."""
        self.reader.process_state = 0
        
        # Exit the event loop of thread (it is not force to quit the reading process).
        self.thread.quit()
        self.thread.wait()
        
        self.start_stop_button.setIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "play.ico"))
        )
    
    def set_theme(self):
        if self.config.theme_config.theme == "light":
            self.setStyleSheet("background-color: "+self.config.theme_config.light)
            self.text.setStyleSheet(
                "color: " + self.config.theme_config.dark +
                "; background-color: " + self.config.theme_config.light
            )
        elif self.config.theme_config.theme == "dark":
            self.setStyleSheet("background-color: "+self.config.theme_config.dark)
            self.text.setStyleSheet(
                "color: " + self.config.theme_config.light +
                "; background-color: " + self.config.theme_config.dark
            )
        
        self.setWindowIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "headphones.ico"))
        )
        self.start_stop_button.setIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "play.ico"))
        )
        self.previous_button.setIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "previous.ico"))
        )
        self.next_button.setIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "next.ico"))
        )
        self.settings_button.setIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "settings.ico"))
        )
    
    def keyPressEvent(self, event):
        """Capture keystrokes."""
        match event.key():
            case Qt.Key_Space:
                self.start_stop_button_clicked()
            case Qt.Key_Escape:
                self.close()
            case Qt.Key_Left:
                self.previous_button_clicked()
            case Qt.Key_Right:
                self.next_button_clicked()
    
    def load_settings(self):
        """Load the GUI settings from the settings store."""
        if self.config.settings.value("main_window_position"):
            self.move(self.config.settings.value("main_window_position"))
        if self.config.settings.value("main_window_size"):
            self.resize(self.config.settings.value("main_window_size"))
    
    def save_settings(self):
        """Copy GUI settings values to the settings store."""
        self.config.settings.setValue("main_window_position",  self.pos())
        self.config.settings.setValue("main_window_size",  self.size())
    
    def closeEvent(self, event=None):
        if self.thread.isRunning():
            self.stop_reading()
        self.reader.save_settings()
        
        if self.settings_widget.isVisible():
            self.settings_widget.close()
        self.settings_widget.save_book_settings()
        
        self.save_settings()
        
        # Close the "OutputStream" of the sounddevice.
        self.reader.stream.close()
        
        # Let the window close.
        event.accept()