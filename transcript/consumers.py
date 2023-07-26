from channels.generic.websocket import AsyncWebsocketConsumer
import os
from pydub import AudioSegment
import speech_recognition as sr
import datetime
from transcript import command
from channels.db import database_sync_to_async
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
from django.apps import apps
from asgiref.sync import async_to_sync
import Levenshtein
import socket
import json
# Class to get audio from web page and convert it to text then return it to the page. Also will log commands
class TranscriptConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_thread = None
    async def connect(self):
        self.command_thread = command.CommandThread()
        self.command_thread.start()
        await self.accept()

    def stop_restart_thread():
        self.command_thread.stop()
        self.command_thread.join()
        self.command_thread = command.CommandThread()
        self.command_thread.start()

    async def disconnect(self, close_code):
        if self.command_thread:
            self.command_thread.stop()
            self.command_thread.join()
        pass

    async def receive(self, text_data=None, bytes_data=None):
      # Define current dir location for relative path 
      __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

      # This is a hack to get the audio correctly loaded into the model so we need to delete the files before we process voice again or will it will still have the audio bytes from last time
      try:
          os.remove(os.path.join(__location__, 'audio.webm'))
          os.remove(os.path.join(__location__, 'recording2.wav'))
          print("Files removed successfully.")
      except OSError as e:
          print(f"Error: {e.filename} - {e.strerror}.")
      except Exception as e:
          print(f"An error occurred: {str(e)}")
      if bytes_data:
        with open(os.path.join(__location__, 'audio.webm'), 'ab') as f:
          f.write(bytes_data)
        # Save byts as webm file in ogg codec
        webm_audio = AudioSegment.from_file(os.path.join(__location__, 'audio.webm'), format="ogg")
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
        # Log the matched command
        print(f"Matched Command: {result[0]}")
        print(f"Sub-Command: {result[1]}")
        Command = apps.get_model('main', 'Command')
        _command = Command(command=f"[{result[0]} sub_command: {result[1]}]")
        await _command.asave()
        # Send to matlab
        text_sender = TcpTextSender("localhost", 8080)
        message = {"command": result[0], "sub_command": result[1]}
        text_sender.send_text(json.dumps(message))
        self.command_thread.command = message
        # Return to client  
        await self.send(text_data=f"Command: {result[0]} sub_command {result[1]}")

class CommandMatcher:
    def __init__(self):
        self.commands = ['forward', 'spin', 'backward', 'stop', 'left', 'right', 'follow']
        self.colors = ['red', 'green', 'black']
        
    def convert_to_number(self, string):
        """
        Helper method that attempts to convert a string into a number.
        It removes non-digit characters from the string and tries to convert the cleaned string to a float.
        If the conversion succeeds, the resulting number is returned; otherwise, it returns None.
        """
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
        """
        Matches the second word of the input string as a distance value.
        Calls the `convert_to_number()` method to convert the second word to a number.
        If the conversion is successful, the distance value is returned; otherwise, None is returned.
        """
        print(f"Second word: {string}")
        distance = self.convert_to_number(string) 
        if distance is not None:
            print(f"distance: {distance}")
            return distance
        else:
            return None
    def color_match(self,word):
        """
        Matches a given word against the color keywords in the `colors` list using Levenshtein distance.
        Calculates the distance between the word and each color keyword and returns the color with the smallest distance.
        """
        distances = {}

        for color in self.colors:
            distance = Levenshtein.distance(word, color)
            distances[color] = distance
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])

        for distance in sorted_distances:
            print(f"Color: {distance[0]}, Levenshtein Distance: {distance[1]}")
        return sorted_distances[0][0]
    def match(self, string):
        """
        Performs the command matching and additional operations based on the matched command.
        Splits the input string into words and extracts the first word as the command keyword.
        Calculates the Levenshtein distance between the first word and each command keyword in the `commands` list.
        The command with the smallest distance is considered the matched command.
        If the matched command requires additional matching or operations, the respective methods are called.
        The matched command and any sub-command (distance value or color) are returned.
        """
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
        elif matched_command == 'spin':
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
        return matched_command, sub_command
class TcpTextSender:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_text(self, message):
        """
        Sends a text message over a TCP connection to the specified host and port.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                sock.sendall(message.encode())
                print("Text message sent successfully.")
        except (socket.error, socket.timeout) as e:
            print(f"An error occurred while sending the text message: {e}")
