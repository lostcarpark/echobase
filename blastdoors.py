from pybricks.hubs import TechnicHub
from pybricks.pupdevices import ColorDistanceSensor, DCMotor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.tools import wait, StopWatch
import urandom

DEBUG = False
OPENING = 70 # Motor speed opening door.
CLOSING = -70 # Motor speed closing door.
CLOSE_COLOR = Color(356, 95, 84) # Closed color - Red
OPEN_COLOR = Color(128, 80, 52) # Open color - Green
INTERVAL_COLOR = Color(223, 87, 69) # Color of track - Blue
EXTRA_CLOSE_TIME = 5000 # When closed color detected wait extra time.
EXTRA_OPEN_TIME = 0
MIN_INTERVAL = 90 # Minimum number of seconds between door cycles.
MAX_INTERVAL = 180 # Maximum number of seconds between door cycles.

hub = TechnicHub()
sensor = ColorDistanceSensor(Port.A)
sensor.detectable_colors([CLOSE_COLOR, OPEN_COLOR, INTERVAL_COLOR])
doorMotor = DCMotor(Port.B)

# Function to open or close door.
# Run motor in specified direction until colour reached.
def doorMove(direction, end_color, delay):
    hub.light.on(end_color)
    doorMotor.dc(direction)
    # Wait for end colour to be detected.
    while (sensor.color() != end_color):
        wait(20)
    if (DEBUG):
        print("Color detected: ", sensor.hsv())
    wait(delay)
    doorMotor.stop()
    hub.light.off()

# Function to wait random number of seconds.
def pauseBeforeMoving():
    # Turn light orange while waiting.
    hub.light.on(Color.ORANGE)
    # Set up timer to wait a random interval.
    timer = StopWatch()
    seconds = urandom.randint(MIN_INTERVAL, MAX_INTERVAL)
    if (DEBUG):
        print("Waiting for ", seconds, " seconds.")
    awaiting = seconds * 1000
    timer.reset()
    while (timer.time() < awaiting):
        hue = Color.YELLOW.h + (Color.RED.h - Color.YELLOW.h) / awaiting * timer.time()
        sat = Color.YELLOW.s + (Color.RED.s - Color.YELLOW.s) / awaiting * timer.time()
        val = Color.YELLOW.v + (Color.RED.v - Color.YELLOW.v) / awaiting * timer.time()
        hub.light.on(Color(hue, sat, val))
        wait(20)
        # If center button pressed, end wait period early.
        if (Button.CENTER in hub.buttons.pressed()):
            return

# Disable stop button.
hub.system.set_stop_button(None)

# If open colour (blue) detected, assume just opened. Otherwise, assume just 
# closed, as that's the condition out of the box.
start_color = sensor.color()
if (start_color == OPEN_COLOR):
    direction = OPENING
else:
    direction = CLOSING

# Enter infinite loop.
while True:
    # Wait a while before doing anything.
    pauseBeforeMoving()
    
    if (direction == CLOSING):
        direction = OPENING
        end_color = OPEN_COLOR
        delay = EXTRA_OPEN_TIME
        if (DEBUG):
            print("Opening door...")
    else:
        direction = CLOSING
        end_color = CLOSE_COLOR
        delay = EXTRA_CLOSE_TIME
        if (DEBUG):
            print("Closing door...")

    doorMove(direction, end_color, delay)
