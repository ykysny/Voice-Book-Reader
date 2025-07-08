from PySide6.QtWidgets import QWidget, QLayout, QBoxLayout, QComboBox, QSpinBox
from PySide6.QtCore import Slot, QSettings
from PySide6.QtGui import QIcon

from src.core.voice_engine import get_settings, set_settings


class SettingsWidget(QWidget):
    """Window for displaying settings."""
    def __init__(self, main_widget, config):
        super().__init__()
        
        self.main_widget = main_widget
        self.config = config
        
        self.setWindowTitle("Settings")
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom, self))
        # The widget's size will not be resizable by the user, and will automatically shrink.
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
        # "Book" field.
        self.current_book = QComboBox()
        config_list = [f.stem for f in (self.config.config_dir / "books").glob("*.ini")]
        for c in config_list:
            self.current_book.addItem("Book: "+c)
        index = self.current_book.findText("Book: "+self.main_widget.reader.current_book)
        self.current_book.setCurrentIndex(index)
        
        self.current_book.currentTextChanged.connect(self.current_book_changed)
        self.layout().addWidget(self.current_book)
        
        # Fields from voice engine.
        # This "get_settings" function is from the "voice_engine" module.
        self.combobox_dict = get_settings()
        for c in self.combobox_dict:
            temp = self.combobox_dict[c]
            self.combobox_dict[c] = QComboBox()
            self.combobox_dict[c].addItems(temp)
            
            # Load the value from book settings.
            temp = self.load_book_settings(c)
            index = self.combobox_dict[c].findText(temp)
            self.combobox_dict[c].setCurrentIndex(index)
            # This "set_settings" function is from the "voice_engine" module.
            set_settings(c, temp, self.config.core_dir)
            
            self.layout().addWidget(self.combobox_dict[c])
            self.combobox_dict[c].currentTextChanged.connect(self.combobox_dict_changed)
        
        # "Current sentence" field.
        # The "showEvent" method is responsible for the value "current_sentence".
        self.current_sentence = QSpinBox()
        self.current_sentence.setPrefix("Current sentence (0:"
                                        +str(len(self.main_widget.reader.book)-1)
                                        +"): ")
        self.current_sentence.setRange(0, len(self.main_widget.reader.book)-1)
        
        self.current_sentence.valueChanged.connect(self.current_sentence_changed)
        self.layout().addWidget(self.current_sentence)
        
        # "Theme" field.
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Theme: light", "Theme: dark"])
        index = self.theme_combobox.findText("Theme: "+self.config.theme_config.theme)
        self.theme_combobox.setCurrentIndex(index)
        
        self.set_theme()
        
        self.theme_combobox.currentTextChanged.connect(self.theme_combobox_changed)
        self.layout().addWidget(self.theme_combobox)
        
        self.layout().setContentsMargins(3, 3, 3, 3)
    
    @Slot()
    def current_book_changed(self, text):
        # Save settings of a previous book.
        self.save_book_settings()
        self.main_widget.reader.save_settings()
        
        # Cut the "Book: ", set the new book.
        self.config.settings.setValue("current_book",  text[6:])
        
        # Load settings for a new book.
        self.main_widget.reader.current_reading_position = False
        self.main_widget.reader.load_settings()
        self.main_widget.reader.load_book()
        self.main_widget.reader.update_plain_text()
        
        for c in self.combobox_dict:
            temp = self.load_book_settings(c)
            index = self.combobox_dict[c].findText(temp)
            self.combobox_dict[c].setCurrentIndex(index)
        
        temp = self.main_widget.reader.current_sentence
        self.current_sentence.setPrefix("Current sentence (0:"
                                        +str(len(self.main_widget.reader.book)-1)
                                        +"): ")
        self.current_sentence.setRange(0, len(self.main_widget.reader.book)-1)
        self.current_sentence.setValue(temp)
    
    @Slot()
    def current_sentence_changed(self, value):
        self.main_widget.reader.current_sentence = value
        self.main_widget.reader.current_reading_position = False
        self.main_widget.reader.update_plain_text()
    
    @Slot()
    def combobox_dict_changed(self, text):
        """Set a new parameter for the voice engine."""
        for c in self.combobox_dict:
            if text == self.combobox_dict[c].currentText():
                # This "set_settings" function is from the "voice_engine" module.
                set_settings(c, text, self.config.core_dir)
                break
    
    @Slot()
    def theme_combobox_changed(self, text):
        self.config.settings.setValue("theme", text[7:])
        self.config.theme_config.theme = text[7:]
        self.main_widget.set_theme()
        self.set_theme()
    
    def set_theme(self):
        if self.config.theme_config.theme == "light":
            self.setStyleSheet("background-color: "+self.config.theme_config.light)
            self.current_book.setStyleSheet("color: "+self.config.theme_config.dark)
            self.current_sentence.setStyleSheet("color: "+self.config.theme_config.dark)
            self.theme_combobox.setStyleSheet("color: "+self.config.theme_config.dark)
            for c in self.combobox_dict:
                self.combobox_dict[c].setStyleSheet("color: "+self.config.theme_config.dark)
        elif self.config.theme_config.theme == "dark":
            self.setStyleSheet("background-color: "+self.config.theme_config.dark)
            self.current_book.setStyleSheet("color: "+self.config.theme_config.light)
            self.current_sentence.setStyleSheet("color: "+self.config.theme_config.light)
            self.theme_combobox.setStyleSheet("color: "+self.config.theme_config.light)
            for c in self.combobox_dict:
                self.combobox_dict[c].setStyleSheet("color: "+self.config.theme_config.light)
        
        self.setWindowIcon(
            QIcon(str(self.config.icons_dir / self.config.theme_config.theme / "headphones.ico"))
        )
    
    def keyPressEvent(self, event):
        """Capture keystrokes."""
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def load_book_settings(self, value):
        """Load settings from the settings store."""
        book_settings = QSettings(
            str(self.config.config_dir / "books" / f"{self.main_widget.reader.current_book}.ini"),
            QSettings.IniFormat
        )
        
        temp = book_settings.value(value)
        if temp == None:
            # This "get_settings" function is from the "voice_engine" module.
            temp = get_settings()[value][0]
        
        return temp
    
    def save_book_settings(self):
        """Copy voice engine settings values to the book settings store."""
        book_settings = QSettings(
            str(self.config.config_dir / "books" / f"{self.main_widget.reader.current_book}.ini"),
            QSettings.IniFormat
        )
        
        for c in self.combobox_dict:
            book_settings.setValue(c, self.combobox_dict[c].currentText())
    
    def showEvent(self, event):
        # Center the "SettingsWidget" window on the main window.
        self.current_sentence.setValue(self.main_widget.reader.current_sentence)
        
        self.move(self.main_widget.geometry().x()
                  +(self.main_widget.geometry().width()-self.geometry().width())//2,
                  self.main_widget.geometry().y()
                  +(self.main_widget.geometry().height()-self.geometry().height())//2)
