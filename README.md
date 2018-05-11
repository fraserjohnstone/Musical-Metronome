# Musical Metronome

## The Application

A simple command line application for musicians looking for a fast, extremely accurate, and flexible metronome capable of advanced beat groupings.

This application is designed to be run on windows with python 3.x installed.


## Keeping it Simple

Im music, the number and length of each beat is given by a time signature (3/4, 4/4, 3/8, 9/8 etc.). The top number in the time signature is the only number we are concerned with as it tells us how many beats there are in a bar.

Given that we are ignoring the other number in the time signature, all that we need to know is the beats per minute value from the user and we have a simple metronome.


## Getting More Advanced

In many situations we need to be able to group the number of beats in a bar into smaller sub-groups. This application automatically generates all possible groupings using sub-group lengths of 2, 3, and 4 and allows the user to choose from any of these.


## Requirements

You will need to download and install the following modules:

    - PyAudio
    - pprint
    - Numpy


## Usage

Simply run the start.bat file located in the root directory. You will be asked to choose the number of beats in each bar, the bpm value, and how you would like to group the beats.