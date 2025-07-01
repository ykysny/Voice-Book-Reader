import os
import sounddevice as sd
import sys
from voice_engine import *
from preprocessing import *
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QLayout, QBoxLayout, \
    QHBoxLayout, QApplication, QLabel, QComboBox, QSpinBox, QDialog
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtCore import Slot, QSettings, QSize, QThread, QObject, Signal, Qt


SETTINGS, THEME, DARK, LIGHT = None, None, None, None


def check_files():
    """Check icons, books, settings files."""
    # Check config.
    if not os.path.exists("config"):
        os.mkdir("config")
    
    if not os.path.exists("config/settings.ini"):
        f = open("config/settings.ini", "x")
        f.close()
    
    if not os.path.exists("config/books"):
        os.mkdir("config/books")
    
    set_global_parameters()
    
    # Check icons.
    if not os.path.exists("icons"):
        dialog = QuickMessage("File check", "The 'icons' folder was not found.")
        dialog.exec()
        
        return False
    elif (not os.path.exists("icons/dark/headphones.ico")
          or not os.path.exists("icons/dark/next.ico")
          or not os.path.exists("icons/dark/pause.ico")
          or not os.path.exists("icons/dark/play.ico")
          or not os.path.exists("icons/dark/previous.ico")
          or not os.path.exists("icons/dark/settings.ico")
          or not os.path.exists("icons/light/headphones.ico")
          or not os.path.exists("icons/light/next.ico")
          or not os.path.exists("icons/light/pause.ico")
          or not os.path.exists("icons/light/play.ico")
          or not os.path.exists("icons/light/previous.ico")
          or not os.path.exists("icons/light/settings.ico")):
        dialog = QuickMessage("File check", "Icon was not found in the 'icons' folder.")
        dialog.exec()
        
        return False
    
    # Check books.
    if not os.path.exists("books"):
        dialog = QuickMessage("File check", "The 'books' folder was not found.")
        dialog.exec()
        
        return False
    else:
        book_list = [file[:-4]+".ini"
                     for file
                     in os.listdir("books") if file.endswith(".txt")]
        config_list = [file for file in os.listdir("config/books") if file.endswith(".ini")]
        
        if book_list == []:
            # Remove all book_name.ini files.
            for c in config_list:
                os.remove("config/books/"+c)
            
            dialog = QuickMessage("File check",
                                  "No '.txt' files were found in the 'books' folder.")
            dialog.exec()
            
            return False
        else:
            for c in config_list:
                if not c in book_list:
                    # Remove book_name.ini if no book_name.txt.
                    os.remove("config/books/"+c)
                else:
                    book_list.remove(c)
            
            # Create the .ini file for each new book.
            for book in book_list:
                f = open("config/books/"+book, "x")
                f.close()
    
    return True


def set_global_parameters():
    global SETTINGS
    SETTINGS = QSettings("config/settings.ini", QSettings.IniFormat)
    
    global THEME
    THEME = SETTINGS.value("theme")
    if THEME != "dark" and THEME != "light":
        THEME = "dark"
    
    global DARK
    DARK = "#333333"
    
    global LIGHT
    LIGHT = "#f5f5f5"


class QuickMessage(QDialog):
    """Window for displaying notifications and errors."""
    def __init__(self, title, text, main_widget=None):
        super().__init__(main_widget)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icons/"+THEME+"/headphones.ico"))
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom, self))
        # The widget's size will not be resizable by the user, and will automatically shrink.
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
        label = QLabel(text)
        
        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        
        if THEME == "light":
            self.setStyleSheet("background-color: "+LIGHT)
            button.setStyleSheet("color: "+DARK)
            label.setStyleSheet("color: "+DARK)
        elif THEME == "dark":
            self.setStyleSheet("background-color: "+DARK)
            button.setStyleSheet("color: "+LIGHT)
            label.setStyleSheet("color: "+LIGHT)
        
        self.layout().addWidget(label)
        self.layout().addWidget(button)
    
    def keyPressEvent(self, event):
        """Capture keystrokes."""
        if (event.key() == Qt.Key_Space or event.key() == Qt.Key_Escape
            or event.key() == Qt.Key_Enter):
            self.close()
    
    def showEvent(self, event):
        # Center the "QuickMessage" window on the main window.
        if self.parent():
            self.move(self.parent().geometry().x()
                      +(self.parent().geometry().width()-self.width())//2,
                      self.parent().geometry().y()
                      +(self.parent().geometry().height()-self.height())//2)


class MainWidget(QWidget):
    """Main window, the class responsible for GUI and common behavior."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Book Reader")
        self.load_settings()
        
        # It is a voice reader class.
        self.reader = Reader(self)
        self.reader.reading_finished_signal.connect(self.reading_finished)
        self.reader.update_text_signal.connect(self.update_plain_text)
        
        self.thread = QThread()
        # Move to thread the certain func not the class.
        self.reader.moveToThread(self.thread)
        self.thread.started.connect(self.reader.read)
        
        self.settings_widget = SettingsWidget(self)
        
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
            self.start_stop_button.setIcon(QIcon("icons/"+THEME+"/pause.ico"))
    
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
        
        self.start_stop_button.setIcon(QIcon("icons/"+THEME+"/play.ico"))
        
        if error:
            dialog = QuickMessage("Error", error, self)
            dialog.exec()
    
    def stop_reading(self):
        """Stop the reading process and close the reading thread."""
        self.reader.process_state = 0
        
        # Exit the event loop of thread (it is not force to quit the reading process).
        self.thread.quit()
        self.thread.wait()
        
        self.start_stop_button.setIcon(QIcon("icons/"+THEME+"/play.ico"))
    
    def set_theme(self):
        if THEME == "light":
            self.setStyleSheet("background-color: "+LIGHT)
            self.text.setStyleSheet("color: "+DARK+"; background-color: "+LIGHT)
        elif THEME == "dark":
            self.setStyleSheet("background-color: "+DARK)
            self.text.setStyleSheet("color: "+LIGHT+"; background-color: "+DARK)
        
        self.setWindowIcon(QIcon("icons/"+THEME+"/headphones.ico"))
        self.start_stop_button.setIcon(QIcon("icons/"+THEME+"/play.ico"))
        self.previous_button.setIcon(QIcon("icons/"+THEME+"/previous.ico"))
        self.next_button.setIcon(QIcon("icons/"+THEME+"/next.ico"))
        self.settings_button.setIcon(QIcon("icons/"+THEME+"/settings.ico"))
    
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
        if SETTINGS.value("main_window_position"):
            self.move(SETTINGS.value("main_window_position"))
        if SETTINGS.value("main_window_size"):
            self.resize(SETTINGS.value("main_window_size"))
    
    def save_settings(self):
        """Copy GUI settings values to the settings store."""
        SETTINGS.setValue("main_window_position",  self.pos())
        SETTINGS.setValue("main_window_size",  self.size())
    
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


class Reader(QObject):
    """This is the implementation of a voice reader."""
    reading_finished_signal = Signal(str)
    update_text_signal = Signal(str)
    
    def __init__(self, main_widget):
        super(Reader, self).__init__()

        self.main_widget = main_widget
        self.load_settings()
        self.load_book()
        
        self.current_reading_position = False
        
        self.CHUNK = 1024
        self.stream = sd.OutputStream(samplerate=48000, channels=1)
        
        # This is the receiver of signals from buttons.
        # 0 - stop the reading process (pause/settings button)
        # 1 - run the reading process (play button)
        # 2 - run the previous audio string (previous button)
        # 3 - run the next audio string (next button)
        self.process_state = 0
    
    @Slot()
    def read(self):
        """The function-process of book reading. Run in separate thread to unblock the GUI."""
        self.process_state = 1
        
        error = None
        while True:
            match self.process_state:
                case 0:
                    break
                case 1:
                    if not self.current_reading_position:
                        # This "prepare_sentence" function is from the "preprocessing" module.
                        sentence = prepare_sentence(self.book[self.current_sentence])
                        # This "check_readable_symbols" function is from the "preprocessing"
                        # module.
                        if check_readable_symbols(sentence):
                            try:
                                # This "text_to_speech" function is from the "voice_engine"
                                # module.
                                audio = text_to_speech(sentence)
                            except:
                                error = "Text to speech function has failed."
                                self.process_state = 0
                            else:
                                self.play(audio)
                        else:
                            # Next sentence (direction == True).
                            self.change_current_sentence(True)
                    else:
                        self.play()
                case 2:
                    self.process_state = 1
                    self.current_reading_position = False
                    # Previous sentence (direction == False).
                    self.change_current_sentence(False)
                case 3:
                    self.process_state = 1
                    self.current_reading_position = False
                    # Next sentence (direction == True).
                    self.change_current_sentence(True)
        
        # Finishing of "Reader" work.
        self.reading_finished_signal.emit(error)
    
    def change_current_sentence(self, direction):
        # Next sentence (direction == True).
        if direction:
            if len(self.book) > self.current_sentence + 1:
                self.current_sentence += 1
                self.update_plain_text()
            else:
                self.process_state = 0
                self.reading_finished_signal.emit("")
        # Previous sentence (direction == False).
        else:
            if -1 < self.current_sentence - 1:
                self.current_sentence -= 1
                self.update_plain_text()
    
    def play(self, audio=False):
        """Play the audio string from voice engine."""
        if self.current_reading_position:
            audio, cursor = self.current_reading_position
        else:
            # It is a position in the audio string to resumption of reading.
            cursor = 0
        
        self.stream.start()
        
        for cursor in range(cursor, len(audio), self.CHUNK):
            match self.process_state:
                case 0:
                    self.current_reading_position = (audio, cursor)
                    break
                case 1:
                    self.stream.write(audio[cursor:cursor+self.CHUNK])
                case _:
                    self.current_reading_position = False
                    break
        else:
            self.current_reading_position = False
            # Next sentence (direction == True).
            self.change_current_sentence(True)
        
        self.stream.stop()
    
    @Slot()
    def load_settings(self):
        """Load the "Reader" settings from the settings store."""
        self.current_book = SETTINGS.value("current_book")

        if (self.current_book == None
            or not os.path.exists("config/books/"+self.current_book+".ini")):
            # Choose the first one element from the generator object.
            self.current_book = next(file[:-4]
                                     for file
                                     in os.listdir("config/books")
                                     if file.endswith(".ini"))
        
        book_settings = QSettings("config/books/"+self.current_book+".ini",
                                  QSettings.IniFormat)
        
        self.current_sentence = book_settings.value("current_sentence")
        if self.current_sentence == None:
            self.current_sentence = 0
        else:
            self.current_sentence = int(self.current_sentence)
    
    def save_settings(self):
        """Copy "Reader" settings values to the settings store."""
        SETTINGS.setValue("current_book", self.current_book)
        
        book_settings = QSettings("config/books/"+self.current_book+".ini",
                                  QSettings.IniFormat)
        book_settings.setValue("current_sentence", self.current_sentence)
    
    def load_book(self):
        with open("books/"+self.current_book+".txt") as file:
            self.book = file.read()
        # This "prepare_book" function is from the "preprocessing" module.
        self.book = prepare_book(self.book)
    
    def update_plain_text(self):
        """Prepare and send the content to show in the plain text widget."""
        content = ""
        for i in range(0,100):
            if self.current_sentence - i < 0:
                break
            
            content = ("\n::"
                       +str(self.current_sentence-i)
                       +"::\n"
                       +self.book[self.current_sentence-i]
                       +"\n"
                       +content)
        
        # Send the content to MainWidget's slot.
        self.update_text_signal.emit(content)


class SettingsWidget(QWidget):
    """Window for displaying settings."""
    def __init__(self, main_widget):
        super().__init__()
        
        self.main_widget = main_widget
        
        self.setWindowTitle("Settings")
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom, self))
        # The widget's size will not be resizable by the user, and will automatically shrink.
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
        # "Book" field.
        self.current_book = QComboBox()
        config_list = [file[:-4]
                       for file
                       in os.listdir("config/books") if file.endswith(".ini")]
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
            set_settings(c, temp)
            
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
        index = self.theme_combobox.findText("Theme: "+THEME)
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
        SETTINGS.setValue("current_book",  text[6:])
        
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
                set_settings(c, text)
                break
    
    @Slot()
    def theme_combobox_changed(self, text):
        SETTINGS.setValue("theme", text[7:])
        global THEME
        THEME = text[7:]
        self.main_widget.set_theme()
        self.set_theme()
    
    def set_theme(self):
        if THEME == "light":
            self.setStyleSheet("background-color: "+LIGHT)
            self.current_book.setStyleSheet("color: "+DARK)
            self.current_sentence.setStyleSheet("color: "+DARK)
            self.theme_combobox.setStyleSheet("color: "+DARK)
            for c in self.combobox_dict:
                self.combobox_dict[c].setStyleSheet("color: "+DARK)
        elif THEME == "dark":
            self.setStyleSheet("background-color: "+DARK)
            self.current_book.setStyleSheet("color: "+LIGHT)
            self.current_sentence.setStyleSheet("color: "+LIGHT)
            self.theme_combobox.setStyleSheet("color: "+LIGHT)
            for c in self.combobox_dict:
                self.combobox_dict[c].setStyleSheet("color: "+LIGHT)
        
        self.setWindowIcon(QIcon("icons/"+THEME+"/headphones.ico"))
    
    def keyPressEvent(self, event):
        """Capture keystrokes."""
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def load_book_settings(self, value):
        """Load settings from the settings store."""
        book_settings = QSettings("config/books/"
                                  +self.main_widget.reader.current_book
                                  +".ini",
                                  QSettings.IniFormat)
        
        temp = book_settings.value(value)
        if temp == None:
            # This "get_settings" function is from the "voice_engine" module.
            temp = get_settings()[value][0]
        
        return temp
    
    def save_book_settings(self):
        """Copy voice engine settings values to the book settings store."""
        book_settings = QSettings("config/books/"
                                  +self.main_widget.reader.current_book
                                  +".ini",
                                  QSettings.IniFormat)
        
        for c in self.combobox_dict:
            book_settings.setValue(c, self.combobox_dict[c].currentText())
    
    def showEvent(self, event):
        # Center the "SettingsWidget" window on the main window.
        self.current_sentence.setValue(self.main_widget.reader.current_sentence)
        
        self.move(self.main_widget.geometry().x()
                  +(self.main_widget.geometry().width()-self.geometry().width())//2,
                  self.main_widget.geometry().y()
                  +(self.main_widget.geometry().height()-self.geometry().height())//2)


if __name__ == "__main__":
    app = QApplication([])
    
    if check_files():
        main_widget = MainWidget()
        main_widget.show()
        
        sys.exit(app.exec())
    else:
        app.quit()