import speech_recognition as sr
from pydub import AudioSegment
import os


class Speech2Text:
    def __init__(self):
        self.r = sr.Recognizer()
        self.lang = "ru-RU"

    def recognize(self, audio_file):
        file_path, file_ext = os.path.splitext(audio_file)
        file_ext = file_ext[1:]

        sound = AudioSegment.from_file(audio_file, file_ext)
        wav_path = file_path + ".wav"
        sound.export(wav_path, format="wav")

        with sr.AudioFile(wav_path) as source:
            audio = self.r.record(source)

        try:
            text = self.r.recognize_google(audio, language=self.lang)
        except Exception as e:
            raise e
        finally:
            os.remove(wav_path)

        return text
