from PySide6.QtWidgets import QDialog, QLayout, QBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class QuickMessage(QDialog):
    """Window for displaying notifications and errors."""
    def __init__(self, title, text, config, main_widget=None):
        super().__init__(main_widget)

        self.setWindowTitle(title)
        self.setWindowIcon(
            QIcon(str(config.icons_dir / config.theme_config.theme / "headphones.ico"))
        )
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom, self))
        # The widget's size will not be resizable by the user, and will automatically shrink.
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
        label = QLabel(text)
        
        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        
        if config.theme_config.theme == "light":
            self.setStyleSheet("background-color: "+config.theme_config.light)
            button.setStyleSheet("color: "+config.theme_config.dark)
            label.setStyleSheet("color: "+config.theme_config.dark)
        elif config.theme_config.theme == "dark":
            self.setStyleSheet("background-color: "+config.theme_config.dark)
            button.setStyleSheet("color: "+config.theme_config.light)
            label.setStyleSheet("color: "+config.theme_config.light)
        
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