from pybricks.hubs import TechnicHub
from pybricks.pupdevices import ColorDistanceSensor, DCMotor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.tools import wait, StopWatch
import urandom

OPENING = -70
CLOSING = 70
MIN_INTERVAL = 10
MAX_INTERVAL = 20

hub = TechnicHub()
sensor = ColorDistanceSensor(Port.A)
doorMotor = DCMotor(Port.B)

# Function to open or close door.
# Run motor in specified direction until colour reached.
def doorMove(direction, end_color):
    hub.light.on(end_color)
    doorMotor.dc(direction)
    # Wait for end colour to be detected.
    while (sensor.color() != end_color):
        wait(20);
    doorMotor.stop()
    hub.light.off()

# Function to wait random number of seconds.
def pauseBeforeMoving():
    # Turn light orange while waiting.
    hub.light.on(Color.ORANGE)
    # Set up timer to wait a random interval.
    timer = StopWatch()
    seconds = urandom.randint(MIN_INTERVAL, MAX_INTERVAL)
    print("Waiting for ", seconds, " seconds.")
    awaiting = seconds * 1000
    timer.reset()
    while (timer.time() < awaiting):
        wait(20)
        # If center button pressed, end wait period early.
        if (Button.CENTER in hub.buttons.pressed()):
            return

# Disable stop button.
hub.system.set_stop_button(None)
# Enter infinite loop.
while True:
    direction = CLOSING
    end_color = Color.RED

    pauseBeforeMoving()
    
    start_color = sensor.color()
    if (start_color == Color.RED):
        direction = OPENING

    if (direction == CLOSING):
        end_color = Color.RED
        print("Closing door...")
    else:
        end_color = Color.BLUE
        print("Opening door...")

    doorMove(direction, end_color)

