# For randomness
import random

# PyQt5
import PyQt5.QtWidgets as Qtw
# Sympy math functions
from sympy import SympifyError

# Import screens
from UiScreens.Py.Calculator import Ui_Calculator
from UiScreens.Py.FlashcardEditLine import Ui_FlashcardEditLine
from UiScreens.Py.FlashcardSelection import Ui_FlashcardSelection
from UiScreens.Py.FlashcardSetEdit import Ui_FlashcardSetEdit
from UiScreens.Py.Flashcards import Ui_Flashcards
from UiScreens.Py.Graph import Ui_Graph
from UiScreens.Py.Home import Ui_Home
from UiScreens.Py.Problem import Ui_Problem
from UiScreens.Py.ProblemSelection import Ui_ProblemSelection
from UiScreens.Py.ProblemSeries import Ui_ProblemSeries
# Module for generating and solving problems
from calculate import generate, to_sympy, calculate
# Module to manage loading and saving flashcard sets
from flashcard import read_cards, save_cards, Flashcard
# Module for displaying help boxes
from help import display_help
# Modules for rendering functions
from latex import to_latex, BLANK
from render import load_svg, to_svg, to_graph


class MainWindow(Qtw.QStackedWidget):
    """Main window class which inherits from QStackedWidget, allowing for multiple screens"""

    def __init__(self):
        # Initialize the widget
        super().__init__()

        # Variable for keeping track of screen indices
        self.screens = {}

        # Window title
        self.setWindowTitle('Math!')

        # Add screens
        for i in ('Home', 'Calculator', 'Flashcards', 'FlashcardSelection', 'FlashcardSetEdit', 'Graph', 'Problem',
                  'ProblemSelection', 'ProblemSeries'):
            self.add_screen(i)

        # Show the MainWindow and resize it
        self.show()
        self.resize(1024, 576)

    # Function to add a new screen
    def add_screen(self, name):
        """Adds the screen that matches the given name"""
        # Get the class that matches the screen name and initialize it, passing the main window as an argument
        screen = globals()[name](self)
        # Add the widget to the main window
        self.addWidget(screen)
        # Set the index for the screen in the screens dictionary, so we can change screens later
        self.screens[name] = len(self.screens)

    # Function to change screens
    def change_screen(self, screen, parameters=None):
        """Switch to the screen with the given name"""
        # Gets the correct index from the screens dictionary and switches to it
        self.setCurrentIndex(self.screens[screen])
        # For special screens with parameters
        if parameters is not None:
            # Set the parameters for the screen
            self.currentWidget().set_parameters(parameters)


class Home(Qtw.QWidget):
    """Home screen"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_Home()
        self.ui.setupUi(self)

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Connect the buttons to their functions
        self.ui.button_flashcards.clicked.connect(lambda: self.main_window.change_screen('FlashcardSelection'))
        self.ui.button_problems.clicked.connect(lambda: self.main_window.change_screen('ProblemSelection'))
        self.ui.button_calculator.clicked.connect(lambda: self.main_window.change_screen('Calculator'))
        self.ui.button_graph.clicked.connect(lambda: self.main_window.change_screen('Graph'))


class FlashcardSelection(Qtw.QWidget):
    """Screen for choosing flashcard sets"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_FlashcardSelection()
        self.ui.setupUi(self)

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Connect the buttons to their functions
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_help.clicked.connect(lambda: display_help('FlashcardSelection'))

        # Display the available flashcard sets
        self.setup_flashcards()

        # Buttons for new sets
        self.ui.derivatives_new_button.clicked.connect(lambda: self.new_set('Derivatives'))
        self.ui.integrals_new_button.clicked.connect(lambda: self.new_set('Integrals'))
        self.ui.series_new_button.clicked.connect(lambda: self.new_set('Series'))

    def setup_flashcards(self):
        """Creates buttons for every flashcard"""
        # Reset layout by removing all buttons
        for layout in (
                self.ui.derivatives_area_contents, self.ui.integrals_area_contents, self.ui.series_area_contents):
            # Get the layout
            layout = layout.layout()
            # While there are buttons left
            # We use >3 to account for the title, spacer, and new flashcard set button
            while layout.count() > 3:
                # Remove the widget
                widget = layout.itemAt(1).widget()
                widget.setParent(None)
                layout.removeWidget(widget)

        # Load the current flashcard data
        cards = read_cards()
        # List the derivative, integral, and series sets
        for i in ('Derivatives', 'Integrals', 'Series'):
            # Iterate through all of the sets and add buttons
            for j in cards[i]:
                self.add_button(i, j)
            # Add the button for all sets
            self.add_button(i, 'All')

    def add_button(self, card_type, card_set):
        """Adds the button for a specific set"""
        # Choose the correct area for derivatives, integrals, or series
        layout = {'Derivatives': self.ui.derivatives_area_contents,
                  'Integrals': self.ui.integrals_area_contents,
                  'Series': self.ui.series_area_contents}
        # Get the layout of the right type
        layout = layout[card_type].layout()

        # Create a new button
        widget = Qtw.QPushButton()
        # Set the button text to the current set
        widget.setText(card_set)

        # Add the widget to the layout
        # Add it in the -2 position to be before the spacer and new set button
        layout.insertWidget(layout.count() - 2, widget)

        # Connect the button to the appropriate change screen function
        # Passing the arguments to the lambda is required to avoid all buttons connecting to the same set
        widget.clicked.connect(lambda state, card=(card_type, card_set):
                               self.main_window.change_screen(f'Flashcards', card))

    def new_set(self, set_type):
        """Creates a new set of flashcards"""
        # Get a name for the set
        name = ''
        # While invalid name
        while name == '' or name == 'All' or name in read_cards()[set_type]:
            # Display a dialog box for the user to input a name for the set
            name, okay = Qtw.QInputDialog.getText(
                self, 'New Set', 'Enter a name for the set: ', Qtw.QLineEdit.Normal, '')
            # If they hit cancel, we don't need to make a new set
            if not okay:
                return
        # Get the current cards
        data = read_cards()
        # Add a blank set to the cards
        data[set_type][name] = [{'Problem': '0', 'Answer': '0'}]
        # Save the changes
        save_cards(data)
        # Setup the flashcards
        self.setup_flashcards()
        # Go to the edit set area
        self.main_window.change_screen('FlashcardSetEdit', (set_type, name))


class Flashcards(Qtw.QWidget):
    """Screen for showing flashcards"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_Flashcards()
        self.ui.setupUi(self)

        # Set main window
        self.main_window = main_window
        # Index in set
        self.index = 0
        # Set of cards
        self.set = []
        # Set of cards in order
        self.set_inorder = None

        # Type of set and specific set
        self.card_type = None
        self.card_set = None

        # Connect buttons
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('FlashcardSelection'))
        self.ui.button_help.clicked.connect(lambda: display_help('Flashcards'))
        # Flip - either by button or by clicking the card
        self.ui.button_flip.clicked.connect(self.flip)
        self.ui.flashcard.mouseReleaseEvent = lambda event: self.flip()
        # Previous and next
        self.ui.button_previous.clicked.connect(self.previous)
        self.ui.button_next.clicked.connect(self.next)
        # Edit card
        self.ui.button_edit.clicked.connect(lambda: self.main_window.change_screen(
            'FlashcardSetEdit', (self.card_type, self.card_set)))
        # Randomize order
        self.ui.check_random.clicked.connect(self.randomize)

    def set_parameters(self, card_set):
        """Set the current set for the flashcards"""
        # Get the type and set
        self.card_type, self.card_set = card_set
        # Get the cards from the json data
        cards = read_cards()
        # Get the specific set
        if self.card_set == 'All':
            # If it's all cards, add all of them
            cards_ = []
            for i in cards[self.card_type].values():
                cards_ += i
            cards = cards_
            # Don't allow enabling of the "All" set
            self.ui.button_edit.setDisabled(True)
        else:
            # Get the correct set
            cards = cards[self.card_type][self.card_set]
            self.ui.button_edit.setDisabled(False)

        # Reset the current index
        self.index = 0

        # Setup flashcards
        self.set = []
        for i in cards:
            # Create a Flashcard object for each card
            card = Flashcard(self.card_type, i['Problem'], i['Answer'])
            self.set.append(card)
        if len(cards) == 0:
            # Create a blank Flashcard object if the set is empty
            self.set.append(Flashcard(self.card_type, None, None))

        # Previous button is disabled since you start at the left
        self.ui.button_previous.setEnabled(False)
        # If the set has 0 or 1 cards, you're at the end, so set the next button to disabled
        if len(self.set) in [0, 1]:
            self.ui.button_next.setEnabled(False)
        else:
            self.ui.button_next.setEnabled(True)

        # Randomize if the box is checked
        if self.ui.check_random.isChecked():
            self.randomize()

        # Update the image
        self.update_image()

    def randomize(self):
        """Toggle randomized or inorder set"""
        # Don't bother randomizing 0 or 1 card sets
        if len(self.set) < 2:
            return
        # If it's random
        if self.ui.check_random.isChecked():
            # Create a copy of the set with everything in order
            self.set_inorder = self.set[::]
            # Shuffle the cards
            random.shuffle(self.set)
        # If it's not random
        else:
            # Set it back to the in order set
            self.set = self.set_inorder[::]
        # Reset to the beginning of the set
        self.index = 1
        # Call the previous function because it handles reset functions for us
        self.previous()

    def update_image(self):
        """Updates the screen's flashcard image"""
        # Get the current card
        card = self.set[self.index]
        # Setup the card if it's blank
        if card.show() is None:
            card.setup()
        # Load the image
        load_svg(self.ui.flashcard, card.show())

    def previous(self):
        """Go to the previous card"""
        # Decrease index
        self.index -= 1
        # Reset to the front side
        self.set[self.index].reset()
        # Update the image
        self.update_image()
        # Se the previous button to be disabled if you're at the end
        if self.index == 0:
            self.ui.button_previous.setEnabled(False)
        # If you just moved to the left, you're not at the right end
        self.ui.button_next.setEnabled(True)

    def next(self):
        """Go to the next card"""
        # Increase index
        self.index += 1
        # Reset to the front side
        self.set[self.index].reset()
        # Update the image
        self.update_image()
        # Set the next button to be disabled if you're at the end
        if self.index == len(self.set) - 1:
            self.ui.button_next.setEnabled(False)
        # If you just moved to the right, you're not at the left end
        self.ui.button_previous.setEnabled(True)

    def flip(self):
        """Flip the current card"""
        # Flip the card and update the image
        self.set[self.index].flip()
        self.update_image()


class FlashcardSetEdit(Qtw.QWidget):
    """Screen for editing a flashcard set"""

    class FlashcardEditLine(Qtw.QWidget):
        """Widget for each individual card in the edit screen"""

        def __init__(self, screen, card_type, card_set, index):
            # Initialize widget
            super().__init__()
            self.ui = Ui_FlashcardEditLine()
            self.ui.setupUi(self)

            # Get the main screen (FlashcardSetEdit)
            self.screen = screen

            # Get the set information
            self.type = card_type
            self.set = card_set
            self.index = index

            # Read the cards
            cards = read_cards()
            # Get the problem and answer
            self.problem = cards[self.type][self.set][self.index]['Problem']
            self.answer = cards[self.type][self.set][self.index]['Answer']

            # Load the images
            load_svg(self.ui.question_image, to_svg(to_latex(self.problem), 0))
            load_svg(self.ui.answer_image, to_svg(to_latex(self.answer), 0))

            # Edit buttons
            self.ui.edit_question_button.clicked.connect(lambda: self.edit('problem'))
            self.ui.edit_answer_button.clicked.connect(lambda: self.edit('answer'))
            # Remove button
            self.ui.remove_button.clicked.connect(self.remove)

        def remove(self):
            """Removes the card from the set"""
            # Read the cards
            cards = read_cards()
            # Remove the set
            cards[self.type][self.set].pop(self.index)
            # Save the cards
            save_cards(cards)

            # Reset layout
            self.screen.set_parameters((self.type, self.set))

        def edit(self, which):
            """Edits the problem or answer for a card"""
            # Read the cards
            cards = read_cards()
            # Continue until the user inputs something valid or cancels
            while True:
                try:
                    if which == 'problem':
                        # Show a dialog for the user to input a new expression
                        text, okay = Qtw.QInputDialog.getText(
                            self, 'Edit', 'Enter a new problem: ', Qtw.QLineEdit.Normal, self.problem)
                        # Return if the user clicks cancel
                        if not okay:
                            return
                        # Load the image
                        load_svg(self.ui.question_image, to_svg(to_latex(text), 0))
                        # Set the new problem
                        self.problem = text
                        cards[self.type][self.set][self.index]['Problem'] = text
                    elif which == 'answer':
                        # Show a dialog for the user to input a new expression
                        text, okay = Qtw.QInputDialog.getText(
                            self, 'Edit', 'Enter a new problem: ', Qtw.QLineEdit.Normal, self.answer)
                        # Return if the user clicks cancel
                        if not okay:
                            return
                        # Load the image
                        load_svg(self.ui.answer_image, to_svg(to_latex(text), 0))
                        # Set the new answer
                        self.answer = text
                        cards[self.type][self.set][self.index]['Answer'] = text
                    # Save the changes to the cards
                    save_cards(cards)
                    break
                # If the user inputs an invalid expression
                except ValueError:
                    pass

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_FlashcardSetEdit()
        self.ui.setupUi(self)

        # Variables for the specific set
        self.type = None
        self.set = None

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Connect the buttons to their functions
        # Back button is not connected here because it depends on the parameters
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_help.clicked.connect(lambda: display_help('FlashcardSetEdit'))

        # Connect delete set and new card buttons
        self.ui.delete_button.clicked.connect(self.delete)
        self.ui.new_button.clicked.connect(self.new)

    def set_parameters(self, parameters):
        """Sets the current card set"""
        # Reset layout by removing extra items
        layout = self.ui.scrollAreaWidgetContents.layout()
        # >1 to allow for the spacer
        while layout.count() > 1:
            # Remove the widget
            widget = layout.itemAt(0).widget()
            widget.setParent(None)
            layout.removeWidget(widget)

        # Get the parameters
        self.type, self.set = parameters
        # Connect the back button
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('Flashcards', (self.type, self.set)))

        # Add lines for each card
        cards = read_cards()
        for i in range(len(cards[self.type][self.set])):
            self.add_line(i)

    def add_line(self, index):
        """Adds a card to the edit menu"""
        # Create a widget for the line
        line = self.FlashcardEditLine(self, self.type, self.set, index)
        layout = self.ui.scrollAreaWidgetContents.layout()
        # Insert the widget before the spacer
        layout.insertWidget(layout.count() - 1, line)

    def delete(self):
        """Deletes the current set"""
        # Remove the card from the json data
        cards = read_cards()
        cards[self.type].pop(self.set)
        save_cards(cards)
        # Go back to the flashcard selection screen
        self.main_window.change_screen('FlashcardSelection')
        # Reload the sets; there is one missing now
        self.main_window.currentWidget().setup_flashcards()

    def new(self):
        """Adds a new card to the current set"""
        # Add a blank card to the json data
        cards = read_cards()
        cards[self.type][self.set].append({'Problem': '0', 'Answer': '0'})
        save_cards(cards)
        # Add a line that corresponds to the last item added to the set
        self.add_line(len(cards[self.type][self.set]) - 1)


class ProblemSelection(Qtw.QWidget):
    """Screen for choosing a problem mode"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_ProblemSelection()
        self.ui.setupUi(self)

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Connect the buttons to their functions
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_help.clicked.connect(lambda: display_help('ProblemSelection'))

        # Connect the buttons to go to the problem screen
        self.ui.button_d.clicked.connect(lambda: self.go('d'))
        self.ui.button_i.clicked.connect(lambda: self.go('i'))
        self.ui.button_s.clicked.connect(lambda: self.go('s'))

        # Connect every check box to a function that checks if the button selection is valid
        for layout in (self.ui.d_buttons.layout(), self.ui.i_buttons.layout(), self.ui.s_buttons.layout()):
            # Skip the last item; it's a spacer
            for i in range(layout.count() - 1):
                # Connect the button
                layout.itemAt(i).widget().clicked.connect(self.check_buttons)

    def go(self, button):
        """Go to the correct problem screen"""
        # Variables for buttons and which of those are checked
        checked = []
        buttons = []
        # Derivative buttons
        if button == 'd':
            buttons = [self.ui.check_d_polynomial, self.ui.check_d_exponential, self.ui.check_d_log,
                       self.ui.check_d_trig, self.ui.check_d_inverse_trig, self.ui.check_d_log_diff,
                       self.ui.check_d_sum, self.ui.check_d_product, self.ui.check_d_quotient, self.ui.check_d_chain]
            # Pass type and complexity
            checked.append('Derivative')
            checked.append(self.ui.complexity_d.value())
        # Integral buttons
        if button == 'i':
            buttons = [self.ui.check_i_polynomial, self.ui.check_i_exponential, self.ui.check_i_log,
                       self.ui.check_i_basic_trig, self.ui.check_i_inverse_trig, self.ui.check_i_sum,
                       self.ui.check_i_u, self.ui.check_i_partial_fractions, self.ui.check_i_trig_sub,
                       self.ui.check_i_parts]
            # Pass type and complexity
            checked.append('Integral')
            checked.append(self.ui.complexity_i.value())
        # Series buttons
        if button == 's':
            buttons = [self.ui.check_s_nth, self.ui.check_s_geometric, self.ui.check_s_telescoping, self.ui.check_s_p,
                       self.ui.check_s_integral, self.ui.check_s_direct, self.ui.check_s_limit,
                       self.ui.check_s_alternating]
            # Pass type, series doesn't have complexity
            checked.append('Series')
            checked.append(None)
        # Get the text that corresponds with each checked button
        for i in buttons:
            if i.isChecked():
                checked.append(i.text())
        # Change screens
        if button == 's':
            # Series has its own special screen
            self.main_window.change_screen('ProblemSeries', checked)
        else:
            self.main_window.change_screen('Problem', checked)

    def check_buttons(self):
        """Check if the current check box states are valid"""

        def check_layout(layout, a, b):
            """Check a range in a layout for at least one button press"""
            # Check a range in a layout to see if at least one button is checked
            for i in range(a, b):
                if layout.itemAt(i).widget().isChecked():
                    return True
            return False

        # Derivatives
        if check_layout(self.ui.d_buttons.layout(), 0, 6) and check_layout(self.ui.d_buttons.layout(), 6, 10):
            self.ui.button_d.setDisabled(False)
        else:
            self.ui.button_d.setDisabled(True)

        # Integrals
        if check_layout(self.ui.i_buttons.layout(), 0, 7) and check_layout(self.ui.i_buttons.layout(), 7, 10):
            self.ui.button_i.setDisabled(False)
        else:
            self.ui.button_i.setDisabled(True)

        # Series
        if check_layout(self.ui.s_buttons.layout(), 0, self.ui.s_buttons.layout().count() - 1):
            self.ui.button_s.setDisabled(False)
        else:
            self.ui.button_s.setDisabled(True)


class Problem(Qtw.QWidget):
    """Screen for problems"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_Problem()
        self.ui.setupUi(self)

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Connect the buttons to their functions
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('ProblemSelection'))
        self.ui.button_help.clicked.connect(lambda: display_help('Problem'))

        # Buttons for new problem and checking answer
        self.ui.button_new.clicked.connect(self.new_problem)
        self.ui.button_check.clicked.connect(self.check)
        # Pressing enter in the text box is the same as pressing the check button
        self.ui.text_entry.returnPressed.connect(self.check)

        # Connect the input box to a function that updates the image
        self.ui.text_entry.textChanged.connect(self.update_text)

        # Variables for the problem parameters
        self.parameters = None
        self.complexity = None
        self.problem = None
        self.answer = None
        self.problem_type = None

    def set_parameters(self, parameters):
        """Set the parameters for the problem type"""
        # Get the values from the parameters
        self.problem_type, self.complexity, *self.parameters = parameters
        # Reset score
        self.ui.score.setText('Score: 0/0')
        self.ui.score_percent.setText('0%')
        # Load a new problem
        self.new_problem()

    def new_problem(self):
        """Generates a new problem"""
        # Generate the problem
        self.problem, self.answer = generate(self.problem_type, self.parameters, self.complexity)
        # Add d/dx of int for the appropriate problem types
        if self.problem_type == 'Derivative':
            self.problem = f'd/dx ({self.problem})'
        elif self.problem_type == 'Integral':
            self.problem = f'int {self.problem} dx'

        # Update the image
        try:
            load_svg(self.ui.problem, to_svg(to_latex(self.problem)))
        except ValueError:
            # Since we're dealing with computer-generated problems, it's good to catch unforeseen problems
            self.new_problem()

        # Reset text input
        self.ui.text_entry.clear()

    def update_text(self):
        """Called whenever the text is updated"""
        # Get the text
        text = self.ui.text_entry.text()
        try:
            # Blank input
            if len(text) == 0:
                load_svg(self.ui.answer, to_svg(BLANK))
            # Not blank input
            else:
                load_svg(self.ui.answer, to_svg(to_latex(text)))
        except ValueError:
            # If there's an input error
            pass

    def check(self):
        """Check the user's answer"""
        # Get the user's input
        text = self.ui.text_entry.text()
        # Create a message box
        box = Qtw.QMessageBox()
        box.setWindowTitle('Check')

        # Whether the user got it correct or not
        correct = False
        try:
            # Get the user's input and the answer
            text = to_sympy(text)
            answer = to_sympy(self.answer)
            # We use .equals because it covers more cases than ==
            if text.equals(answer):
                correct = True
                # Set the text
                box.setText('Correct!')
                # Add appropriate buttons
                box.addButton('Cancel', Qtw.QMessageBox.RejectRole)
                box.addButton('New', Qtw.QMessageBox.AcceptRole)
                # Adjust the score
                text = self.ui.score.text()
                # Get just the numbers in a list and add a correct answer
                text = list(map(int, text[6:].split('/')))
                try:
                    # Adjust score percent:
                    percent = round(100 * (text[0] + 1) / (text[1] + 1), 1)
                    self.ui.score_percent.setText(f'{percent}%')
                except ZeroDivisionError:
                    # In case there aren't any answer done (this really shouldn't happen)
                    self.ui.score_percent.setText('0%')
                # Set the score text
                self.ui.score.setText(f'Score: {text[0] + 1}/{text[1] + 1}')

            else:
                # Set the text
                box.setText('Incorrect!')
                # Add the appropriate buttons
                box.addButton('Cancel', Qtw.QMessageBox.RejectRole)
                box.addButton('Answer', Qtw.QMessageBox.AcceptRole)
                # Adjust the score
                text = self.ui.score.text()
                # Get just the numbers in a list and add a correct answer
                text = list(map(int, text[6:].split('/')))
                try:
                    # Adjust score percent:
                    percent = round(100 * (text[0]) / (text[1] + 1), 1)
                    self.ui.score_percent.setText(f'{percent}%')
                except ZeroDivisionError:
                    # In case there aren't any answer done (this really shouldn't happen)
                    self.ui.score_percent.setText('0%')
                # Set the score text
                self.ui.score.setText(f'Score: {text[0]}/{text[1] + 1}')
        # If the user typed something in incorrectly
        except SympifyError:
            # Set the text
            box.setText('Input error!')
            # Add a cancel button
            box.addButton('Cancel', Qtw.QMessageBox.RejectRole)
        # Show the box and save the button clicked into a variable
        result = box.exec_()

        # Accepted means the user clicked either 'Answer' or 'New'
        # We can check which one based on the value of correct
        if result == Qtw.QMessageBox.Accepted:
            if correct:
                # Create a new problem if they clicked 'New'
                self.new_problem()
            else:
                # Give them the answer if they clicked 'Answer'
                self.ui.text_entry.setText(self.answer)


class ProblemSeries(Qtw.QWidget):
    """Screen for problems with series"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_ProblemSeries()
        self.ui.setupUi(self)

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Connect the buttons to their functions
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('ProblemSelection'))
        self.ui.button_help.clicked.connect(lambda: display_help('ProblemSeries'))

        # Set the buttons for a new problem and checking answer
        self.ui.button_new.clicked.connect(self.new_problem)
        self.ui.button_check.clicked.connect(self.check)

        # Variables for problem parameters
        self.parameters = None
        self.problem = None
        self.answer = None

    def set_parameters(self, parameters):
        """Set the parameters for the problem"""
        # Get the parameters
        # We can ignore the problem type since we know it's series
        # We can ignore the complexity since series don't have a specific complexity
        self.parameters = parameters[2:]
        # Reset score
        self.ui.score.setText('Score: 0/0')
        self.ui.score_percent.setText('0%')
        self.new_problem()

    def new_problem(self):
        """Generates a new problem"""
        # Get the problem
        self.problem, self.answer = generate('Series', self.parameters, None)
        # Add the special text for series
        # Problem is in the format (problem, initial value)
        self.problem = f'sum_(n={self.problem[1]})^infty {self.problem[0]}'

        # Update image
        try:
            load_svg(self.ui.problem, to_svg(to_latex(self.problem)))
        except ValueError:
            # Since we're dealing with computer-generated problems, it's good to catch unforeseen problems
            self.new_problem()

    def check(self):
        """Check the user's answer"""
        # Create a message box
        box = Qtw.QMessageBox()
        box.setWindowTitle('Check')

        # Whether the user got it correct or not
        button = 'Convergent' if self.ui.button_converge.isChecked() else 'Divergent'
        correct = button == self.answer

        if correct:
            # Set the text
            box.setText('Correct!')
            # Add appropriate buttons
            box.addButton('Cancel', Qtw.QMessageBox.RejectRole)
            box.addButton('New', Qtw.QMessageBox.AcceptRole)

            # Adjust the score
            text = self.ui.score.text()
            # Get just the numbers in a list and add a correct answer
            text = list(map(int, text[6:].split('/')))
            try:
                # Adjust score percent:
                percent = round(100 * (text[0] + 1) / (text[1] + 1), 1)
                self.ui.score_percent.setText(f'{percent}%')
            except ZeroDivisionError:
                # In case there aren't any answer done (this really shouldn't happen)
                self.ui.score_percent.setText('0%')
            # Set the score text
            self.ui.score.setText(f'Score: {text[0] + 1}/{text[1] + 1}')
        else:
            # Set the text
            box.setText('Incorrect!')
            # Add the appropriate buttons
            box.addButton('Cancel', Qtw.QMessageBox.RejectRole)

            # Adjust the score
            text = self.ui.score.text()
            # Get just the numbers in a list and add a correct answer
            text = list(map(int, text[6:].split('/')))
            try:
                # Adjust score percent:
                percent = round(100 * (text[0]) / (text[1] + 1), 1)
                self.ui.score_percent.setText(f'{percent}%')
            except ZeroDivisionError:
                # In case there aren't any answer done (this really shouldn't happen)
                self.ui.score_percent.setText('0%')
            # Set the score text
            self.ui.score.setText(f'Score: {text[0]}/{text[1] + 1}')

        # Show the box and save the button clicked into a variable
        result = box.exec_()

        # Accepted means the user clicked 'New'
        if result == Qtw.QMessageBox.Accepted:
            self.new_problem()


class Calculator(Qtw.QWidget):
    """Screen for calculating derivatives, integrals, and convergence"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_Calculator()
        self.ui.setupUi(self)

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Set base mode
        self.mode = 'Derivative'
        self.ui.radio_d.setChecked(True)

        # Connect the buttons to their functions
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_help.clicked.connect(lambda: display_help('Calculator'))
        # Radio buttons
        self.ui.radio_d.clicked.connect(self.change_mode)
        self.ui.radio_i.clicked.connect(self.change_mode)
        self.ui.radio_s.clicked.connect(self.change_mode)
        self.ui.button_convergence.clicked.connect(self.change_mode)
        self.ui.button_value.clicked.connect(self.change_mode)
        # Text boxes
        self.ui.text_entry_d.textChanged.connect(self.update_text)
        self.ui.text_entry_i.textChanged.connect(self.update_text)
        self.ui.text_entry_s.textChanged.connect(self.update_text)
        self.ui.lower_bound.textChanged.connect(self.update_text)
        self.ui.upper_bound.textChanged.connect(self.update_text)
        # Variable buttons
        self.ui.variable_d.currentTextChanged.connect(self.update_text)
        self.ui.variable_i.currentTextChanged.connect(self.update_text)
        self.ui.variable_s.currentTextChanged.connect(self.update_text)
        self.ui.value_s.textChanged.connect(self.update_text)

    def change_mode(self):
        """Change the calculator mode"""
        # Get the correct mode based on the button pressed
        if self.ui.radio_d.isChecked():
            self.mode = 'Derivative'
        elif self.ui.radio_i.isChecked():
            self.mode = 'Integral'
        elif self.ui.radio_s.isChecked():
            self.mode = 'Series'
        # Update
        self.update_text()

    def update_text(self):
        """Called whenever the text is updated"""
        # Blank value for answer
        answer = ''
        # Get the text
        # Get the variable (and start value if applicable)
        # Get the answer
        # Give the text the extra d/dx, int, or sum
        if self.mode == 'Derivative':
            text = self.ui.text_entry_d.text()
            if len(text) > 0:
                variable = self.ui.variable_d.currentText()
                answer = calculate(self.mode, text, variable)
                text = f'd/d{variable} ({text})'
        elif self.mode == 'Integral':
            text = self.ui.text_entry_i.text()
            if len(text) > 0:
                variable = self.ui.variable_i.currentText()
                answer = calculate(self.mode, text, variable,
                                   start=self.ui.lower_bound.text(), end=self.ui.upper_bound.text())
                text = f'int {text}d{variable}'
        else:
            text = self.ui.text_entry_s.text()
            if len(text) > 0:
                variable = self.ui.variable_s.currentText()
                value = self.ui.value_s.text()
                answer = calculate(self.mode, text, variable, value=value, do_it=self.ui.button_value.isChecked())
                text = fr'sum_({variable}={value})^infty {text}'
        try:
            # Blank input
            if len(text) == 0:
                load_svg(self.ui.input, to_svg(BLANK))
                load_svg(self.ui.output, to_svg(BLANK))
            # Not blank input
            else:
                load_svg(self.ui.input, to_svg(to_latex(text)))
                load_svg(self.ui.output, to_svg(to_latex(answer)))
        except ValueError:
            # If there's an input error
            pass


class Graph(Qtw.QWidget):
    """Screen for graphing a function"""

    def __init__(self, main_window):
        # Initialize screen
        super().__init__()
        self.ui = Ui_Graph()
        self.ui.setupUi(self)

        # Set a variable for the main window so that we can access it later
        self.main_window = main_window

        # Variable for window size
        self.window_size = [-10, 10, -10, 10]

        # Connect the buttons to their functions
        self.ui.button_home.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_back.clicked.connect(lambda: self.main_window.change_screen('Home'))
        self.ui.button_help.clicked.connect(lambda: display_help('Graph'))

        # Text box
        self.ui.function_entry.textChanged.connect(self.update_graph)
        # Check boxes
        self.ui.check_zeroes.clicked.connect(self.update_graph)
        self.ui.check_extrema.clicked.connect(self.update_graph)
        self.ui.check_inflection.clicked.connect(self.update_graph)
        self.ui.check_derivative.clicked.connect(self.update_graph)
        self.ui.check_integral.clicked.connect(self.update_graph)
        # Window box
        self.ui.button_window.clicked.connect(self.change_window)

    def update_graph(self):
        """Update the graph"""
        # Get the text
        text = self.ui.function_entry.text()
        # Graph
        try:
            if len(text) == 0:
                # Blank graph
                load_svg(self.ui.graph, to_graph('0', None, self.window_size))
            else:
                # Get the checked boxes
                args = []
                if self.ui.check_zeroes.isChecked():
                    args.append('Zeroes')
                if self.ui.check_extrema.isChecked():
                    args.append('Extrema')
                if self.ui.check_inflection.isChecked():
                    args.append('Inflection')
                if self.ui.check_derivative.isChecked():
                    args.append('Derivative')
                if self.ui.check_integral.isChecked():
                    args.append('Integral')
                # Graph the function
                load_svg(self.ui.graph, to_graph(text, args, self.window_size))
        # Lots of things can go wrong with bad inputs; check for all of them
        except SympifyError:
            pass
        except TypeError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass

    def change_window(self):
        new_window = []
        while not new_window:
            new_window, okay = Qtw.QInputDialog.getText(
                self, 'Change Window', 'xmin, xmax, ymin, ymax: ',
                Qtw.QLineEdit.Normal, ','.join([str(i) for i in self.window_size]))
            # If they hit cancel, we don't need to make a new set
            if not okay:
                return
            try:
                # Get the new window
                new_window = [float(i) for i in new_window.split(',')]
                # Must be length 4
                if len(new_window) != 4:
                    continue
                # Minimum can't be greater than maximum
                if new_window[0] >= new_window[1] or new_window[2] >= new_window[3]:
                    continue
                self.window_size = new_window
            except ValueError:
                # If the user inputted a bad window size
                new_window = []
        # Update the graph
        self.update_graph()
