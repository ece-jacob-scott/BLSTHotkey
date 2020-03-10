# TODO: Add a ctrl+z handler

from BLSTController import Controller, Observer, Action
from BLSTController.utils import serial_ports
from keyboard import press_and_release, add_hotkey, wait
from Movement import Movement
from Meta import AXIS, DIRECTION
from typing import List, Union
from os import system, name


MOTIONS: List[Movement] = []
COM: Union[str, None] = None


def __is_within_threshold(a: Action, m: Movement) -> bool:
    value = a.value
    if m.is_left():
        value = value['left']
    else:
        value = value['right']
    if m.axis is AXIS.PITCH:
        value = value['pitch']
    elif m.axis is AXIS.ROLL:
        value = value['roll']
    else:
        value = value['yaw']
    if m.trigger(value):
        return True
    return False


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def set_com() -> None:
    print('List of open serial ports')
    ports = serial_ports()
    if len(ports) == 0:
        print("No open ports")
        return
    for i, port in enumerate(serial_ports()):
        print(f'{i}: {port}')
    choice = int(input('::').strip())
    print(f'COM = {ports[choice]}')
    global COM
    COM = ports[choice]
    return


def btn_factory(movement: Movement) -> Observer:
    if movement.hotkey is None:
        raise Exception('No hotkey specified for that movement')

    # Create the observer update function
    def x(self, arg: Action):
        if arg.value is None:
            return
        # print(f'Arg: {arg}') # Testing print statement
        if not self.latch and __is_within_threshold(arg, movement):
            press_and_release(movement.hotkey)
            self.latch = True
        if self.latch and not __is_within_threshold(arg, movement):
            self.latch = False

    return type('o', (), {
        '__init__': Observer.__init__,
        'latch': False,
        'update': x
    })()


def get_observers() -> List[Observer]:
    o = []
    for motion in MOTIONS:
        o.append(btn_factory(motion))
    return o


def start() -> None:
    print(f'COM is {COM}')
    if COM is None:
        print('You have not set an open connection port yet!', end='\n\n')
        return
    if len(MOTIONS) == 0:
        print('There are no registered motions yet!', end='\n\n')
        return
    c = Controller({
        'port': COM,
        'baudrate': 115200,
        'timeout': 2
    })
    for o in get_observers():
        c.attach(o)
    print('Listening!')
    print('To stop lisenting please press ctrl+c', end='\n\n')
    c.start()


def show_current_motions() -> None:
    if len(MOTIONS) is 0:
        print('You have not registered any motions yet')
        return
    print(f'You have mapped {len(MOTIONS)} motions:')
    for motion in MOTIONS:
        print(motion)
    return


def map_motion() -> None:
    print('Please pick a motion to map: ')
    print('Foot')
    print('1. Left')
    print('2. Right')
    print('Axis')
    for axis in AXIS:
        print(axis)
    print('Direction')
    for direction in DIRECTION:
        print(direction)

    foot = int(input('Foot: ').strip())
    if foot == 1:
        foot = 'left'
    elif foot == 2:
        foot = 'right'
    else:
        raise Exception(f'{foot} does not exist')
    axis = AXIS(int(input('Axis: ').strip()))
    direction = DIRECTION(int(input('Direction: ').strip()))

    m = Movement(foot, axis, direction)

    print('Now enter the hotkey to map to the movement')
    print('Please type out special keys such as:')
    print('Alt+F11')
    print('Ctrl+C')
    print('Ctrl+Shift+V, Space')
    m.hotkey = input('Hotkey: ').strip().lower()

    print('Now enter a the threshold value for the movement')
    print('Note: Must be a positive number', end='\n\n')
    m.threshold = int(input('Threshold: ').strip())

    MOTIONS.append(m)


OPTIONS = [
    {
        'id': 0,
        'name': 'Exit',
        'function': lambda: exit()
    },
    {
        'id': 1,
        'name': 'Show current motions',
        'function': show_current_motions
    },
    {
        'id': 2,
        'name': 'Map a new motion',
        'function': map_motion
    },
    {
        'id': 3,
        'name': 'Set connection port',
        'function': set_com
    },
    {
        'id': 4,
        'name': 'Start Listening',
        'function': start
    },
    {
        'id': 5,
        'name': 'Clear',
        'function': clear
    }
]


if __name__ == '__main__':
    print('Welcome to the BLST Foot pedal hotkey program!', end='\n\n')

    while True:
        print('What would you like to do?', end='\n\n')
        for option in OPTIONS:
            print(f'{option["id"]}: {option["name"]}')
        selection = int(input('::').strip())
        print('\n')
        for option in OPTIONS:
            if option['id'] == selection:
                option['function']()
