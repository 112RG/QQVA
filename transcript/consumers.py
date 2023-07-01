from channels.generic.websocket import AsyncWebsocketConsumer
import os
from pydub import AudioSegment
import speech_recognition as sr
import datetime     
from channels.db import database_sync_to_async
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
from django.apps import apps
from asgiref.sync import async_to_sync
import Levenshtein
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
        # Perform command matching based on the recognized text
        matcher = CommandMatcher()
        result = matcher.match(text)
        print
        # Log the matched command
        Command = apps.get_model('main', 'Command')
        command = Command(command=f"[{result[0]} sub_command: {result[1]}]")
        await command.asave()

        # Send to matlab


        # Return to client
        await self.send(text_data=f"Command: {result[0]} sub_command {result[1]}")

class CommandMatcher:
    def __init__(self):
        self.commands = ['forward', 'backward', 'stop', 'left', 'right', 'follow']
        self.colors = ['red', 'green', 'black']
    def convert_to_number(self, string):
        try:
            # Remove special characters and whitespace from the string
            cleaned_string = ''.join(char for char in string if char.isdigit() or char in ['.', '-'])
            # Attempt to convert the cleaned string to a number
            number = float(cleaned_string)
            return number
        except ValueError:
            # Return None if the conversion fails
            return None
    def distance_match(self, string):
        print(f"Second word: {string}")
        distance = self.convert_to_number(string) 
        if distance is not None:
            print(f"distance: {distance}")
            return distance
        else:
            return None
    def color_match(self,word):
        distances = {}

        for color in self.colors:
            distance = Levenshtein.distance(word, color)
            distances[color] = distance
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])

        for distance in sorted_distances:
            print(f"Color: {distance[0]}, Levenshtein Distance: {distance[1]}")
        return sorted_distances[0][0]
    def match(self, string):
        words = string.split()
        if words:
            first_word = words[0].lower()
        else:
            first_word = ''

        print(f"Got string: {string}")
        print(f"First word: {first_word}")

        distances = {}

        for command in self.commands:
            distance = Levenshtein.distance(first_word, command)
            distances[command] = distance
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])

        for distance in sorted_distances:
            print(f"Command: {distance[0]}, Levenshtein Distance: {distance[1]}")

        # Switch on the matched command
        matched_command = sorted_distances[0][0] if sorted_distances else 'No matching command'
        sub_command = None
        if matched_command == 'forward':
           sub_command = self.distance_match(words[1])
        elif matched_command == 'backward':
            sub_command = self.distance_match(words[1])
        elif matched_command == 'go':
            sub_command = self.distance_match(words[1])
        elif matched_command == 'stop':
            # Do something for 'stop' command
            pass
        elif matched_command == 'left':
            # Do something for 'left' command
            pass
        elif matched_command == 'right':
            # Do something for 'right' command
            pass
        elif matched_command == 'follow':
            sub_command = self.color_match(words[1])
            # Do something for 'right' command
            pass
        print(f"Command: {matched_command} sub_command: {sub_command}")
        return matched_command, sub_command
