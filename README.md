# ThereminAi
A personal project to train an Ai to play the Theremin Digital Music Instrument

## Slack Channel

https://thereminai.slack.com

# Installation Guide

This is a step-by-step installation guide to get everything ready to work on the project.
- Install main dependencies **Python 3.6**, **PIP Python Package Manager** and **Python Virtual Environments**
- Setting up a **Python Virtual Environment** to isolate the project
- Install specific project dependencies from the requirements.txt file

## Operating System
- Tested on `Ubuntu 18.04.4 LTS`

## Libraries

This will be a longer story between Linux and Windows to get this working...

### Python Sounddevice

Simple and great library to get audio signals from devices into NumPy Arrays
https://python-sounddevice.readthedocs.io/en/0.3.15/

### PortAudio http://www.portaudio.com/download.html

sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

## Install Python

TODO

### Check Python Version

Run `python3 --version` to check your Python version it should be 3.6 or later.

## Install Python Package Manager

TODO

## Install Virtual Environments

- Run `pip3 install virtualenv`
- Check version with `virtualenv --version`


## Clone the Project

- Run `git clone ...`

## Setup Virtual Environment for the project

For ease of use the virtual environment (foler `venv`) will be created in the project folder itself **but excluded** from version conrol using the `.gitignore`file.

- Navigate into the cloned project folder `cd ThereminiAi`
- Run `virtualenv venv` to create the virtual environment

In the next step the virtual environment is activated

- Run `source venv/bin/activate`
- (Windows Users need to run `venv\Scripts\activate` inside the project folder where the venv folder has been created)

Your Terminal should now change and include the (venv) prefix e.g.:

```
(venv) user@computer:~/04_projects/ThereminAi$
```

## Install required dependencies

The requirements.txt file contains all necessary requirements. Go ahead and install them:
sounddevice

- Run `pip3 install -r requirements.txt`


# Notes on GitIgnore

- Further Reading: https://github.com/github/gitignore


# Hardware

## Theremini

- Further Reading: https://www.moogmusic.com/products/etherwave-theremins/theremini



## Contributor

- Julian H.
- Jathavan S.

## Basic Requirements

 1. Milestone:
    Design and build mechanical aparatus with the ability to play the chamber tone A using both axis (amplitude & frequency)
    this includes:
      - Mechanical structure to create variable frequencies
      - Program to control the mechanical apparature
      - Create interface to read generated sound of theremin
      - Program to fit generated sound to predefined tone
 2. Milestone:
    Update the aparatus with the ability to play the intro of the Star Trek Fanfare using both axis (amplitude & frequency)
