from channels.generic.websocket import AsyncWebsocketConsumer
from deepgram import Deepgram


class TranscriptConsumer(AsyncWebsocketConsumer):
   dg_client = Deepgram("TEST")

   async def connect(self):
      await self.connect_to_deepgram()
      await self.accept()

   async def receive(self, bytes_data):
      self.socket.send(bytes_data)