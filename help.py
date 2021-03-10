# Import modules for loading files
import json
import os
import sys

# PyQt5 for displaying box
import PyQt5.QtWidgets as Qtw


def load_help():
    """Load the help.json file"""
    # Get the file in the correct directory
    try:
        # noinspection PyProtectedMember
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()
    # Get the file at the location
    path = os.path.join(wd, 'help.json')
    with open(path, 'r') as file:
        # Load it using the json module
        return json.loads(file.read())


def display_help(screen):
    """Show the help text for a given screen"""
    # Load the help file and get the correct screen text
    text = load_help()[screen]

    # Create a message box
    box = Qtw.QMessageBox()
    box.setWindowTitle('Help')

    # Set the help text
    box.setText(text)
    # Add a button
    box.addButton('Okay', Qtw.QMessageBox.AcceptRole)

    # Show the box
    box.exec_()
