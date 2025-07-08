"""The audio generation from a text.

Russian version.
"""
import os
import torch


__all__ = ["text_to_speech", "get_settings", "set_settings"]


device = torch.device("cpu")
torch.set_num_threads(os.cpu_count())

# 8000, 24000, 48000
SAMPLE_RATE = 48000
speaker, voice_model, model = None, None, None


def text_to_speech(sentence):
    """Generate the audio string from a text string."""
    return model.apply_tts(text=sentence, speaker=speaker, sample_rate=SAMPLE_RATE)


def get_settings():
    """Send the settings to display on the settings window."""
    speaker_list = ["Speaker: aidar", "Speaker: baya", "Speaker: kseniya",
                    "Speaker: xenia", "Speaker: eugene"]
    voice_model_list = ["Voice model: v3_1_ru", "Voice model: v4_ru"]
    
    return {"speaker": speaker_list, "voice_model": voice_model_list}


def set_settings(parameter, value, core_dir):
    """Receive the settings from the settings window."""
    match parameter:
        case "speaker":
            global speaker
            
            # Cut the "Speaker: ".
            speaker = value[9:]
        case "voice_model":
            global voice_model, model
            
            # Cut the "Voice model: ".
            voice_model = str(core_dir) + "/" + value[13:] + ".pt"
            model = torch.package.PackageImporter(voice_model).load_pickle("tts_models", "model")
            model.to(device)