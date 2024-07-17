"""The audio generation from a text.

English version.
"""
import os
import torch


__all__ = ["text_to_speech", "get_settings", "set_settings"]


device = torch.device("cpu")
torch.set_num_threads(os.cpu_count())
model = torch.package.PackageImporter("v3_en.pt").load_pickle("tts_models", "model")
model.to(device)

# 8000, 24000, 48000
SAMPLE_RATE = 48000
speaker = None


def text_to_speech(sentence):
    """Generate the audio string from a text string."""
    return model.apply_tts(text=sentence, speaker=speaker, sample_rate=SAMPLE_RATE)


def get_settings():
    """Send the settings to display on the settings window."""
    speaker_list = []
    for i in range(0, 118):
        speaker_list.append("Speaker: en_"+str(i))
    
    return {"speaker": speaker_list}


def set_settings(parameter, value):
    """Receive the settings from the settings window."""
    match parameter:
        case "speaker":
            global speaker
            
            # Cut the "Speaker: ".
            speaker = value[9:]