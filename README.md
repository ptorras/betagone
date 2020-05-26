# betagone
An autonomous vision-based chess robot

This currently uses Stockfish 11 for move generation: https://github.com/official-stockfish/Stockfish
It's tailored to work with Anaconda / Python 3.7

It requires:
	- python-chess
	- pytorch
	- PIL
	- cv2

## Directories

### src
Full source code of the actual engine

#### betacontrol
Code dedicated to route planning and engine moving. Since we have no physical implementation
of the robot as of yet, this code is merely intended to show the potential routing
the robot will make.

#### betaengine
An attempt at a chess engine developed in C++ from scratch. It is currently discontinued
although we plan on completing it in the future

#### betapyengine
An attempt at a chess engine developed in python. We also made a fancy debugging
interface, but its move generation was (painfully) slow, so we had to scrap it for 
something else (namely, betaengine)

#### betatest
Our testing system. We designed a Blender model to load FEN positions and render them
to test our vision algorithms. We also planned to have a FEN Extractor from .PGN databases
but we deemed it unnecessary due to the amount of time that would take

#### betavision
The vision module. It uses a two-layer convolutional network to detect the pieces.
It requires the training file found in:
https://drive.google.com/file/d/1PoyffO24l5NU2To7iiBJyxoi_xcCpGo3/view
It has to be saved inside src/betavision/checkpoints

![Hough Lines detection](betagone/src/betavision/lines_board.gif)

#### stockfish-hook
The current implementation uses Stockfish 11 through python-chess, but with a couple
tweaks it can use any UCI. We plan to finish betaengine and wrap it through this module
It requires a binary distribution inside src/stockfish-hook/stockfish-11

### blueprints
The chess robot model and some conventions

### datasets
All datasets we have used to train the robot (the vision aspect and some FEN tests,
as well as other miscellaneous stuff)

## The contents

Right now we simulate a whole iteration of the program. 
