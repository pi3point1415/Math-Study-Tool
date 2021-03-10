# For reading and saving json files
import json
import os
import sys

# For rendering latex
from latex import to_latex
from render import to_svg


def read_cards():
    """Read the json data from the flashcards.json file"""
    try:
        # Try to open the file, if it exists
        with open('flashcards.json', 'r') as file:
            # Load it using the json module
            return json.loads(file.read())

    except FileNotFoundError:
        # If it's not found, we should be in compiled mode, so get the correct path
        try:
            # Get the file from the current directory in compiled mode
            # noinspection PyProtectedMember
            wd = sys._MEIPASS
        except AttributeError:
            # Just in case we're not in compiled mode, this gets the file location
            wd = os.getcwd()
        # Get the file at the location
        path = os.path.join(wd, 'flashcards.json')
        with open(path, 'r') as file:
            # Load it using the json module
            return json.loads(file.read())


def save_cards(data):
    """Save the data to the flashcards.json file"""
    # Open the file and save the data
    with open('flashcards.json', 'w') as file:
        json.dump(data, file, indent=2)


class Flashcard:
    """Class representing a two-sided flashcard"""
    def __init__(self, card_type, problem, answer):
        # Setup variables
        self.type = card_type
        self.problem = problem
        self.answer = answer
        self.side = 0
        # Setting these up later significantly reduces lag
        self.problem_image = None
        self.answer_image = None

    def setup(self):
        """Load images"""
        # Get the images
        self.problem_image = to_svg(to_latex(self.problem))
        self.answer_image = to_svg(to_latex(self.answer))

    def show(self):
        """Show the current flashcard image"""
        # Show the image on the correct side
        if self.side == 0:
            return self.problem_image
        else:
            return self.answer_image

    def flip(self):
        """Flip the card"""
        self.side = 1 if self.side == 0 else 0

    def reset(self):
        """Reset the card to the front"""
        self.side = 0
