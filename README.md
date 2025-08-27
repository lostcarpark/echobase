# Echo Base

This project may eventually contain PyBricks code for controlling multiple aspects of Battle of Hoth, but for now it only contains one piece of functionality.

## Blast Doors

This program controls the main hanger blast doors.

### Assumptions

- Runs on Powered Up Technic Hub
- Color and Distance sensor connected to port A
- Motor with Rotation Sensor connected to port B

### Functionality

- Color and Distance sensor detects state of door. Red when closed, blue when open.
- Between door cycles, wait a random number of seconds, normally between 90 and 180 seconds.
- If center button pressed while waiting, skip to next movement.
- If door is closed set motor to open. Otherwise set to close.
- Start movement in specified direction.
- If opening, set light to green, if closing set to red.
- If opening, wait for green brick. If closing wait for red brick.
- If motor stalls, treat as having reached limit.

This application is released as open source under the MIT licence.
