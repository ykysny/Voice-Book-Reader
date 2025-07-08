import contextlib
from nltk.data import path
import sounddevice as sd
import pytest

from src.app_config import AppConfig
from src.utils.check_files import check_files
from src.gui.main_widget import MainWidget


class _NullStream(contextlib.AbstractContextManager):
    """Stand-in for sounddevice.OutputStream that does absolutely nothing."""
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        return self

    def stop(self):
        return self

    def close(self):
        return self

    # enable “with _NullStream(): …”
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


@pytest.mark.usefixtures("qtbot")
def test_app_starts(qtbot, monkeypatch):
    config = AppConfig()

    assert check_files(config.check_files), "Required files missing for app startup"

    path.append(config.NLTK_DATA_DIR)

    # Patch sounddevice so no real audio hardware is required
    monkeypatch.setattr(sd, "OutputStream", _NullStream, raising=True)

    main_widget = MainWidget(config.main_window, config.reader, config.settings_widget)
    qtbot.addWidget(main_widget)

    assert main_widget is not None
