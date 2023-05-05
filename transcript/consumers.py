from channels.generic.websocket import AsyncWebsocketConsumer
import os
from pydub import AudioSegment
import speech_recognition as sr
class TranscriptConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
      os.remove("audio.webm")
      os.remove("recording.wav")

      if bytes_data:
        print(bytes_data)
        with open('audio.webm', 'ab') as f:
          f.write(bytes_data)
        webm_audio = AudioSegment.from_ogg("audio.webm")

        # Convert the WebM file to a WAV file
        webm_audio.export("recording.wav", format="wav")

        # Load the WAV file into a speech recognizer
        r = sr.Recognizer()
        with sr.AudioFile("recording.wav") as source:
            audio_data = r.record(source)
        try:
            print("You said " + r.recognize_sphinx(audio_data))
            text = r.recognize_sphinx(audio_data)
        except sr.UnknownValueError:
            text = "Could not recognize speech"
        except sr.RequestError:
            text = "Could not connect to speech recognition service"
        await self.send(text_data=text)