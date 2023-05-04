from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Dict
import json
class TranscriptConsumer(AsyncWebsocketConsumer):
   #dg_client = Deepgram("9cdc560703b1bf16b0667a256a7626e927005e4a")

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        #r = sr.Recognizer()
        #audio_data = sr.AudioData(text_data, sample_rate=16000, channels=1)
        #try:
        #    text = r.recognize_google(audio_data)
        #except sr.UnknownValueError:
        #    text = "Could not recognize speech"
        #except sr.RequestError:
        #    text = "Could not connect to speech recognition service"
        await self.send(text_data=json.dumps({
            'text': "test"
        }))