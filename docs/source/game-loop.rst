Game Loop
=========

Each game loop / tick is broke down into three main stages:

- Getting user input
- Updating physics model
- Update Graphics & Audio

Get User Input
--------------
This stage essentially gets the state of the input buttons either. This can either be from a computer keyboard, of via
physical buttons connected to a microcontroller (e.g. the Arduino). There are only three buttons: left, right and center.
During the main loop of the game, the left and right buttons are used to activate the respective flippers, and the center
button is used to launch new balls when needed.

Update Physics Model
--------------------
During the main loop of the game, the left and right buttons are used to activate the respective flippers, and the center
button is used to launch new balls when needed. The first step of the physics update the actuators accordingly. This is
followed by an update/tick of the actual physics model. Finally the state of the physics is read and stored. State
information includes any/all balls as well as the flippers.

Flow Diagram
------------

.. mermaid:: mermaid/game_loop.md