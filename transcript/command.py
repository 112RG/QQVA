import keyboard
import time
from threading import Thread
import time

class CommandThread(Thread):
    def __init__(self):
        super().__init__()
        self.command = None
        self._command = None
        self.command_queue = []
        self.is_running = False
        self.stop_command = False
        self.commands = {
            'forward': self.press_forward,
            'backward': self.press_backward,
            'left': self.press_left,
            'right': self.press_right,
            'stop': self.press_stop,
            'go': self.press_go,
            'spin': self.press_spin,
        }

    def run(self):
        self.is_running = True
        while self.is_running:
            with self.queue_lock:
                if self.command_queue:
                    command = self.command_queue.pop(0)
                    self.play_command(command)
    def stop(self):
        self.is_running = False

    def enqueue_command(self, command):
        if command.get('command') == 'stop':
            self.stop_command = True;
            return;
        with self.queue_lock:
            self.command_queue.append(command)

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
        keyboard.press('up')
        start_time = time.time()
        while time.time() - start_time < sub_command:
            if self.stop_command:
                print("relesing")
                self.stop_command = False
                break
                ("pressing")
            time.sleep(0.1)
        keyboard.release('up')

    def press_backward(self, sub_command):
        print(f'Pressing backward for {sub_command} seconds')
        keyboard.press('down')
        start_time = time.time()
        while time.time() - start_time < sub_command:
            if self.stop_command:
                print("relesing")
                self.stop_command = False
                break
                ("pressing")
            time.sleep(0.1)
        keyboard.release('down')
    def press_spin(self, sub_command):
        print(f'Pressing spin for {sub_command} seconds')
        keyboard.press('left')
        start_time = time.time()
        while time.time() - start_time < sub_command:
            if self.stop_command:
                print("relesing")
                self.stop_command = False
                break
                ("pressing")
            time.sleep(0.1)
        keyboard.release('left')
    def press_left(self, _):
        print('Pressing left')
        keyboard.press('left')
        start_time = time.time()
        while time.time() - start_time < 2:
            if self.stop_command:
                print("relesing")
                self.stop_command = False
                break
                ("pressing")
            time.sleep(0.1)
        keyboard.release('left')

    def press_right(self, _):
        print('Pressing right')
        keyboard.press('right')
        start_time = time.time()
        while time.time() - start_time < 2:
            if self.stop_command:
                print("relesing")
                self.stop_command = False
                break
                ("pressing")
            time.sleep(0.1)
        keyboard.release('right')

    def press_stop(self, _):
        print('Pressing stop')
        self.stop_requested = True
        # Implement the appropriate stop action, such as releasing all keys

    def press_go(self, _):
        print('Pressing go')
        # Implement the appropriate go action, such as pressing a specific key

""" # Example usage
command_server = CommandPlayer()

# Simulating receiving a command
command = {'command': 'forward', 'sub_command': 20}
command_server.play_command(command) """
