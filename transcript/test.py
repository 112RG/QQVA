import keyboard
import time
from threading import Thread, Event

class CommandThread(Thread):
    def __init__(self):
        super().__init__()
        self.command = None
        self.stop_event = Event()

    def run(self):
        while not self.stop_event.is_set():
            if self.command is not None:
                command = self.command
                self.command = None
                self.execute_command(command)
            else:
                time.sleep(0.1)

    def stop(self):
        self.stop_event.set()

    def set_command(self, command):
        self.command = command

    def execute_command(self, command):
        if 'command' not in command:
            print('Invalid command: Missing "command" key')
            return

        if command['command'] not in CommandPlayer.commands:
            print('Invalid command: Unknown command')
            return

        sub_command = command.get('sub_command', None)

        if command['command'] in ['forward', 'backward'] and sub_command is None:
            print('Invalid command: Missing "sub_command" for forward or backward')
            return

        CommandPlayer.commands[command['command']](sub_command)


class CommandPlayer:
    commands = {
        'forward': lambda sub_command: CommandPlayer.press_forward(sub_command),
        'backward': lambda sub_command: CommandPlayer.press_backward(sub_command),
        'left': lambda _: CommandPlayer.press_key('left'),
        'right': lambda _: CommandPlayer.press_key('right'),
        'stop': lambda _: CommandPlayer.release_keys(),
        'go': lambda _: None
    }

    @staticmethod
    def press_key(key):
        keyboard.press(key)
        keyboard.release(key)

    @staticmethod
    def release_keys():
        print('Releasing all keys')
        keyboard.release('up')
        keyboard.release('down')
        keyboard.release('left')
        keyboard.release('right')

    @staticmethod
    def press_forward(sub_command):
        print(f'Pressing forward for {sub_command} seconds')
        keyboard.press('up')
        time.sleep(sub_command)
        keyboard.release('up')

    @staticmethod
    def press_backward(sub_command):
        print(f'Pressing backward for {sub_command} seconds')
        keyboard.press('down')
        time.sleep(sub_command)
        keyboard.release('down')


# Example usage
command_thread = CommandThread()
command_thread.start()

# Simulating receiving commands
command1 = {'command': 'forward', 'sub_command': 5}
command_thread.set_command(command1)

time.sleep(2)  # Wait for a moment (simulate other commands being received)

command2 = {'command': 'backward', 'sub_command': 3}
command_thread.set_command(command2)

time.sleep(2)  # Wait for a moment (simulate other commands being received)

# Stop the command thread
command_stop = {'command': 'stop'}
command_thread.set_command(command_stop)

command_thread.join()  # Wait for the command thread to finish
