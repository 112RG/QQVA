from channels.generic.websocket import AsyncWebsocketConsumer
import os
from pydub import AudioSegment
import speech_recognition as sr
import datetime     
from channels.db import database_sync_to_async
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
from django.apps import apps
from asgiref.sync import async_to_sync
# Class to get audio from web page and convert it to text then return it to the page. Also will log commands
class TranscriptConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
      # This is a hack to get the audio correctly loaded into the model so we need to delete the files before we process voice again or will it will still have the audio bytes from last time
      os.remove("audio.webm")
      os.remove("recording.wav")

      if bytes_data:
        with open('audio.webm', 'ab') as f:
          f.write(bytes_data)
        # Save byts as webm file in ogg codec
        webm_audio = AudioSegment.from_ogg("audio.webm")

        # Convert the WebM file to a WAV file
        webm_audio.export("recording.wav", format="wav")

        # Load the WAV file into a speech recognizer
        r = sr.Recognizer()
        with sr.AudioFile("recording.wav") as source:
            audio_data = r.record(source)
        try:
            # User openapi_whisper to recongnize text in audio data
            text = r.recognize_whisper(audio_data, 'base')
        except sr.UnknownValueError:
            text = "Could not recognize speech"
        except sr.RequestError as e:
            print(e)
            text = "Could not connect to speech recognition service"
        # return text data
        Command = apps.get_model('main', 'Command')
        command = Command(command=text)
        await command.asave()
        await self.send(text_data=text)