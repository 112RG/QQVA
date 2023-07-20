import keyboard
import time

class CommandPlayer:
    def __init__(self):
        self.commands = {
            'forward': self.press_forward,
            'backward': self.press_backward,
            'left': self.press_left,
            'right': self.press_right,
            'stop': self.press_stop,
            'go': self.press_go
        }

    def play_command(self, command):
        if 'command' not in command:
            print('Invalid command: Missing "command" key')
            return

        if command['command'] not in self.commands:
            print('Invalid command: Unknown command')
            return

        sub_command = command.get('sub_command', None)

        if command['command'] in ['forward', 'backward'] and sub_command is None:
            print('Invalid command: Missing "sub_command" for forward or backward')
            return

        self.commands[command['command']](sub_command)

    def press_forward(self, sub_command):
        print(f'Pressing forward for {sub_command} seconds')
        keyboard.press('w')
        time.sleep(sub_command)
        keyboard.release('w')

    def press_backward(self, sub_command):
        print(f'Pressing backward for {sub_command} seconds')
        keyboard.press('s')
        time.sleep(sub_command)
        keyboard.release('s')

    def press_left(self, _):
        print('Pressing left')
        keyboard.press('a')
        keyboard.release('a')

    def press_right(self, _):
        print('Pressing right')
        keyboard.press('d')
        keyboard.release('d')

    def press_stop(self, _):
        print('Pressing stop')
        # Implement the appropriate stop action, such as releasing all keys

    def press_go(self, _):
        print('Pressing go')
        # Implement the appropriate go action, such as pressing a specific key

# Example usage
command_server = CommandPlayer()

# Simulating receiving a command
command = {'command': 'forward', 'sub_command': 20}
command_server.play_command(command)