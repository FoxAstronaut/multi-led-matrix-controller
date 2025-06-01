# multi-led-matrix-controller

## Overview
Application for controlling written in Python.

## Hardware Overview
The application is made to be run on a Raspberry PI Zero W.

Options to switch between Bluetooth & WiFi server modes for different controller options.

WiFi - Sets up a WiFi network with password that allows for connection to a locally hosted web page where different animations can be connected.
Bluetooth - Sets up a Bluetooth server which can be connected to and talked to over a serial connection to a supported device (e.g. bluetooth hand controller for suiting)

Pin (TBC) can be pulled LOW (TBC) using a switch to toggle between WiFi & Bluetooth modes.

LOW - WiFi
HIGH - Bluetooth

## Software Overview
The controller application starts a web or bluetooth server depending on the selected mode and sends instructions on selected animation to the animation controller.

Animations are separated into folders with a JSON file of meta-data about the animations and frames stored in a BMP file named with their order.
Meta-data stored includes name & framerate.

The animation controller loads the folder relating to the animation.
It reads the meta-data file to know what name to log & sets the cycle clock to the necessary framerate.

We load in all the frames & format them into the most easily accessible formate (TBC).

On each clock cycle it loads in a new frame and sends it each pixel to the matrix controller with it's position and RGB value. (DO I NEED TO CONSIDER BUFFERS IN CASE OF SLOW READ TIMES?)

The matrix controller application takes in the position and RGB value and using hard coded values figures out which physical matrix relates to the X,Y position in the animation.

It then triggers the necessary pin change to create that affect. This will include different mechanisms for controlling a 

### Shift Register Fun

RGB Led matrix has 32 pins, 24 Column pins & 8 Row pins. Each Column has a pin for Red, Green & Blue.
We can load in the column RGB values into a 

## Plan

# Future Plans
- Continuous Control - Allow for animations to be set in motion with finer control being passed in continuous from the controller. E.g. Animation speeds up, slows down, glitches out, or changes colours