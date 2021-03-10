# For saving the svg image
from io import BytesIO

# For rendering and graphing
import matplotlib.pyplot as plt
import numpy as np
# PyQt5
from PyQt5.QtCore import Qt
# For symbolic operations
from sympy import *

# Converting to sympy
from calculate import to_sympy

# Set the font
plt.rc('mathtext', fontset='cm')
# Define figure globally. Creating it each time causes lag
fig = plt.figure()


def load_svg(obj, image):
    """Displays a QSvgWidget correctly"""
    # Load the image
    obj.load(image)
    # Set a fixed aspect ratio
    obj.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
    # Update
    obj.updateGeometry()


def to_svg(formula, padding=0.2):
    """Converts a latex expression to an SVG image"""
    try:
        if formula[0] == '$':
            # Plain text
            fig.text(0, 0, formula[1:])
        else:
            # Math
            fig.text(0, 0, f'${formula}$')

        # Place to save the rendered image
        output = BytesIO()

        # Save the figure with given settings
        fig.savefig(output, transparent=True, format='svg', bbox_inches='tight', pad_inches=padding)
    finally:
        # Clear the figure regardless of if anything goes wrong
        fig.clf()

    # Return the image
    output.seek(0)
    return output.read()


def to_graph(formula, args, window_size):
    """Graphs a function and returns an SVG image"""
    # Setup the area to graph
    _, ax = plt.subplots()
    # Show a grid
    ax.grid(True, which='both')
    # Add axes
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    # Convert the formula to a format understood by sympy
    formula = to_sympy(formula)
    # Make x a variable
    x = symbols('x')
    # Turn the function into a lambda
    lambda_f = lambdify(x, formula, modules=['numpy', 'sympy'])
    lambda_f = np.vectorize(lambda_f)
    # Get the x values and y values for the graph
    xx = np.linspace(window_size[0], window_size[1], 1000)
    yy = lambda_f(xx)
    # Plot the graph
    ax.plot(xx, yy, 'b')

    # Check which extra features to show
    for i in args:
        if i == 'Zeroes':
            # Graph zeroes
            # Solve the function for f(x)=0
            # noinspection PyTypeChecker
            xx = list(solveset(Eq(0, formula), x, domain=Interval(window_size[0], window_size[1])))
            # Convert to regular numbers that pyplot can graph
            xx = [float(i) for i in xx]
            try:
                # Get the y values that correspond with the zeroes (they should all be 0)
                yy = lambda_f(xx)
            except ValueError:
                # In case there weren't any zeroes
                yy = []
            # Plot the zeroes in green
            plt.scatter(xx, yy, c='g')
            # Label points
            for x_, y_ in zip(xx, yy):
                x_ = round(x_, 2)
                y_ = round(y_, 2)
                # Add an offset so it's not directly on the point
                x_pos = x_ + (window_size[1] - window_size[0]) / 40
                y_pos = y_ + (window_size[3] - window_size[2]) / 40
                plt.text(x_pos, y_pos, f'({x_}, {y_})', c='g')
        elif i == 'Extrema':
            # Graph extrema
            # Get the derivative
            d = diff(formula, x)
            # Get the second derivative and convert it to a lambda
            dd = diff(d, x)
            dd = lambdify(x, dd, modules=['numpy', 'sympy'])
            dd = np.vectorize(dd)
            # Solve the derivative for f'(x)=0
            # noinspection PyTypeChecker
            xx = list(solveset(Eq(0, d), x, domain=Interval(window_size[0], window_size[1])))
            # Convert to regular numbers that pyplot can graph
            xx = [float(i) for i in xx]
            # Only keep the values where the second derivative is not 0
            xx = list(filter(lambda n: dd(n) != 0, xx))
            try:
                # Get the y values of the extrema
                yy = lambda_f(xx)
            except ValueError:
                # In case there aren't any
                yy = []
            # Plot the extrema in magenta
            plt.scatter(xx, yy, c='m')
            # Label points
            for x_, y_ in zip(xx, yy):
                x_ = round(x_, 2)
                y_ = round(y_, 2)
                # Add an offset so it's not directly on the point
                x_pos = x_ + (window_size[1] - window_size[0]) / 40
                y_pos = y_ + (window_size[3] - window_size[2]) / 40
                plt.text(x_pos, y_pos, f'({x_}, {y_})', c='m')
        elif i == 'Inflection':
            # Graph inflection points
            # Get the second derivative
            dd = diff(formula, x, 2)
            # noinspection PyTypeChecker
            # Solve f''(x)=0 and convert points to float
            xx = list(solveset(Eq(0, dd), x, domain=Interval(window_size[0], window_size[1])))
            xx = [float(i) for i in xx]
            try:
                # Get the y values
                yy = lambda_f(xx)
            except ValueError:
                # In case there aren't any
                yy = []
            # Plot the inflection points in yellow
            plt.scatter(xx, yy, c='y')
            # Label points
            for x_, y_ in zip(xx, yy):
                x_ = round(x_, 2)
                y_ = round(y_, 2)
                # Add an offset so it's not directly on the point
                x_pos = x_ + (window_size[1] - window_size[0]) / 40
                y_pos = y_ + (window_size[3] - window_size[2]) / 40
                plt.text(x_pos, y_pos, f'({x_}, {y_})', c='y')
        elif i == 'Derivative':
            # Get the derivative
            d = diff(formula, x)
            # Get a lambda for the derivative
            lambda_f = lambdify(x, d, modules=['numpy', 'sympy'])
            lambda_f = np.vectorize(lambda_f)
            # Get the x and y values
            xx = np.linspace(window_size[0], window_size[1], 1000)
            yy = lambda_f(xx)
            # Graph in red
            plt.plot(xx, yy, 'r')
        elif i == 'Integral':
            # Get the integral
            d = integrate(formula, x)
            # Get a lambda for the integral
            lambda_f = lambdify(x, d, modules=['numpy', 'sympy'])
            lambda_f = np.vectorize(lambda_f)
            # Get the x and y values
            xx = np.linspace(window_size[0], window_size[1], 1000)
            yy = lambda_f(xx)
            # Graph in cyan
            plt.plot(xx, yy, 'c')
    # Create an object to save the output
    output = BytesIO()
    # Set the y bounds
    plt.ylim([window_size[2], window_size[3]])
    # Save and close the image
    plt.savefig(output, format='svg', bbox_inches='tight', pad_inches=0)
    plt.close()
    # Return the svg
    output.seek(0)
    return output.read()
