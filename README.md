# Pizza Invaders

## Overview

Pizza Invaders is a game inspired by Space Invaders. The objective is to avoid the pineapples that fall down the screen, as you do not want them on your pizza. You play as the President of Iceland, Guðni Th. Jóhannesson.

![Screen Shot of Pizza Invaders](game.png)

## Controls

To start the game, press any key.

Move: `Arrow keys` (left and right)

Shoot: `Space`

Quit: `Escape`

## Setup (prebuilt)

Packaged, executable versions of the game for Windows, macOS and Linux (all 64-bit) can be downloaded from the [Releases](https://github.com/reyniraron/pizza-invaders/releases) tab.

## Setup (from source)

### Requirements

Pizza Invaders requires Python 3 and Pygame. Pipenv is recommended.

### Installation

#### Clone the repository to your computer and `cd` into it

```bash
git clone https://github.com/reyniraron/pizza-invaders.git
cd pizza-invaders
```

#### Set up a Pipenv environment for the game and activate it

```bash
pipenv install
pipenv shell
```

#### Run the game

```bash
python lokaverkefni.py
```

## Building packaged versions

### Windows/Linux

#### Install the development dependencies

```bash
pipenv install --dev
```

#### Build an executable using PyInstaller

```bash
pyinstaller "Pizza Invaders.spec"
```

The packaged executable can be found in the `dist/` directory.

### macOS

#### Install the development dependencies

```bash
pipenv install --dev
```

#### Build an executable using py2app

```bash
python setup.py py2app --packages=pygame
```

The packaged app bundle can be found in the `dist/` directory.

### Mac users

Old versions of Pygame don't play nicely with Homebrew's Python on macOS Mojave. Pygame 1.9.5 or later is recommended to avoid any issues. If you are using an older version, please read the notice below.

#### Old versions of Pygame

If you are using Mojave and installed Python via Homebrew, chances are Pygame won't work properly. A workaround is to install [Miniconda](https://conda.io/en/latest/miniconda.html) and use its distribution of Python, or download Python from [Python.org](https://www.python.org/downloads/) and use it instead of Homebrew's Python. You can specify the path to the interpreter when setting up Pipenv as such:

```bash
pipenv shell --python $path_to_interpreter
pipenv install
```

Once you've created a Pipenv environment, you can uninstall Miniconda or the Python binary, as Pipenv creates a copy for its environment.
