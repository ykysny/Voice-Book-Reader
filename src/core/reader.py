import sounddevice as sd
from PySide6.QtCore import QObject, Signal, Slot, QSettings

from src.core.preprocessing import prepare_book, prepare_sentence, check_readable_symbols
from src.core.voice_engine import text_to_speech


class Reader(QObject):
    """This is the implementation of a voice reader."""
    reading_finished_signal = Signal(str)
    update_text_signal = Signal(str)
    
    def __init__(self, main_widget, config):
        super(Reader, self).__init__()

        self.main_widget = main_widget
        self.config = config
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
        self.current_book = self.config.settings.value("current_book")

        if (self.current_book == None
            or not (self.config.config_dir / "books" / f"{self.current_book}.ini").exists()):
            # Choose the first one element from the generator object.
            self.current_book = next(
                f.stem
                for f in (self.config.config_dir / "books").glob("*.ini")
            )
        
        book_settings = QSettings(
            str(self.config.config_dir / "books" / f"{self.current_book}.ini"),
            QSettings.IniFormat
        )
        
        self.current_sentence = book_settings.value("current_sentence")
        if self.current_sentence == None:
            self.current_sentence = 0
        else:
            self.current_sentence = int(self.current_sentence)
    
    def save_settings(self):
        """Copy "Reader" settings values to the settings store."""
        self.config.settings.setValue("current_book", self.current_book)
        
        book_settings = QSettings(
            str(self.config.config_dir / "books" / f"{self.current_book}.ini"),
            QSettings.IniFormat
        )
        book_settings.setValue("current_sentence", self.current_sentence)
    
    def load_book(self):
        with (self.config.books_dir / f"{self.current_book}.txt").open(encoding="utf-8") as file:
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