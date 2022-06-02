Introduction
============
This program simulates the motion of astronomical bodies in 2-d space.
It is based on the [N-body problem](https://en.wikipedia.org/wiki/N-body_problem).
<p>
The simulation utilizes Newtonian mechanics to calculate the gravitational force between bodies. 
<p>
The simulation simulates 500 random bodies in a square region of 1e10 by 1e10 meters.

How to Use
==========
While on the main menu
----------------------
To load a simulation, first press the <b>Load</b> button, then select the simulation file.

To start a new simulation, press the <b>New</b> button.

To exit the program, press the <b>Exit</b> button.

While on the simulation screen
------------------------------
To start or pause the simulation, press the <b>Start/Pause</b> button.

To access any other options, the simulation must be paused.

To create a new simulation, press the <b>Randomize</b> button.

To adjust the time between frames, press the button under the <b>Randomize</b> button.
<li>1x: 100 ms</li>
<li>2x: 50 ms</li>
<li>5x: 20 ms</li>
<li>10x: 10 ms</li>
<li>100x: 1 ms</li>

To save the simulation, press the <b>Save</b> button.

To record the simulation, press the <b>Record</b> button.
Recording can only be done once a simulation has been saved.

To quit the simulation, press the <b>Quit</b> button.

Video Specifications
===================
This program captures a screenshot of the simulation every 100 frames, and combines them into a video.

The video is saved at 15 fps, and is in mp4 format.

Requirements
============
* Python 3.10 or later
* Windows 10 or later **This program only supports the Windows operating system.**

Required Modules
================
1. [`numpy`](https://numpy.org)
2. [`matplotlib`](https://matplotlib.org)
3. [`opencv-python`](https://pypi.org/project/opencv-python/)
4. [`tkcap`](https://github.com/ghanteyyy/tkcap) **Windows Only**
5. [`tkinter`](https://docs.python.org/3/library/tkinter.html) **Included in Python Installation**