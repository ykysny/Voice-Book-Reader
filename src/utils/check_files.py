import os

from src.gui.dialogs import QuickMessage


def check_files(config):
    """Check icons, books, settings files."""
    config.config_dir.mkdir(parents=True, exist_ok=True)
    (config.config_dir / "settings.ini").touch(exist_ok=True)
    (config.config_dir / "books").mkdir(parents=True, exist_ok=True)
    
    if not config.nltk_data_dir.exists():
        dialog = QuickMessage("File Check", "The 'nltk_data' folder was not found.", config)
        dialog.exec()

        return False
    
    # Check icons.
    if not config.icons_dir.exists():
        dialog = QuickMessage("File Check", "The 'icons' folder was not found.", config)
        dialog.exec()
        
        return False
    elif (not (config.icons_dir / "dark/headphones.ico").exists()
          or not (config.icons_dir / "dark/next.ico").exists()
          or not (config.icons_dir / "dark/pause.ico").exists()
          or not (config.icons_dir / "dark/play.ico").exists()
          or not (config.icons_dir / "dark/previous.ico").exists()
          or not (config.icons_dir / "dark/settings.ico").exists()
          or not (config.icons_dir / "light/headphones.ico").exists()
          or not (config.icons_dir / "light/next.ico").exists()
          or not (config.icons_dir / "light/pause.ico").exists()
          or not (config.icons_dir / "light/play.ico").exists()
          or not (config.icons_dir / "light/previous.ico").exists()
          or not (config.icons_dir / "light/settings.ico").exists()
    ):
        dialog = QuickMessage("File Check", "An icon was not found in the 'icons' folder.", config)
        dialog.exec()
        
        return False
    
    # Check books.
    if not config.books_dir.exists():
        dialog = QuickMessage("File Check", "The 'books' folder was not found.", config)
        dialog.exec()
        
        return False
    else:
        book_list = [
            file.with_suffix(".ini").name
            for file in config.books_dir.iterdir()
            if file.suffix == ".txt"
        ]
        config_list = [
            file.name
            for file in (config.config_dir / "books").iterdir()
            if file.suffix == ".ini"
        ]
        
        if book_list == []:
            # Remove all book_name.ini files.
            for c in config_list:
                (config.books_dir / c).unlink()
            
            dialog = QuickMessage(
                "File Check",
                "No '.txt' files were found in the 'books' folder.",
                config
            )
            dialog.exec()
            
            return False
        else:
            for c in config_list:
                if not c in book_list:
                    # Remove book_name.ini if no book_name.txt.
                    (config.config_dir / "books" / c).unlink()
                else:
                    book_list.remove(c)
            
            # Create the .ini file for each new book.
            for book in book_list:
                (config.config_dir / "books" / book).touch(exist_ok=False)
    
    return True