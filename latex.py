# Blank latex character
BLANK = r'\ '
# Special functions
FUNCTIONS = ('sqrt', 'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'int', 'lim', 'sum', 'ln')


def par_count(infix):
    """Return the start and end of a parenthesized expression"""
    # Variables for parentheses count and for first parenthesis location
    count = 0
    first = 0
    for i, exp in enumerate(infix):
        # If it's an open parenthesis, add one
        if exp == '(':
            count += 1
            # If the count after adding 1 is 1, it must be the first parenthesis
            if count == 1:
                first = i
        # If it's a close parenthesis, remove 1
        elif exp == ')':
            count -= 1
            # If we get back to 0, we're at the end
            if count == 0:
                return first, i
    # In case there are no parentheses
    return None


# Checks if an entire expression is parenthesized
def remove_pars(infix):
    """Checks if an entire expression is parenthesized and removes unnecessary parentheses

    Example: (x+1) becomes x+1
    Example: (x+1)*(x+2) stays the same
    """
    # Only continue if the expression has parentheses on both sides
    if infix == '' or not (infix[0] == '(' and infix[-1] == ')'):
        return infix
    # Get the location of the parenthesized expression
    start, stop = par_count(infix)
    # If the first parenthesis is at the beginning and the last parenthesis is at the end
    # Prevents removing parentheses from case like (1+2)*(3+4)
    if start == 0 and stop == len(infix) - 1:
        # Return the infix without the parentheses
        return infix[1:-1]
    return infix


def fraction(infix):
    """Convert fractions to LaTeX form"""
    # If there are no fractions, we don't need to do anything
    if '/' not in infix:
        return infix
    # Iterate through the expression
    for i in range(len(infix)):
        # If we find a division symbol
        if infix[i] == '/':
            # Find the end of the left expression
            # We cant just use par_count since we need to check for extra cases
            count = 0
            left = max(i - 1, 0)
            for j in range(1, i + 1):
                # Adjust the count if it's a parenthesis
                if infix[i - j] == '(':
                    count -= 1
                    # Break if we get below a count of 0 on a left parenthesis
                    # This is a case like (a/b)
                    if count < 0:
                        break
                elif infix[i - j] == ')':
                    count += 1
                # If we're not in a parenthesized expression and we get an operator that requires a new term
                elif infix[i - j] in ('+', '-', '=', ' ', ',', '|') and count == 0:
                    break
                left = i - j
            # Find the end of the right expression
            count = 0
            right = i
            for j in range(1, len(infix[i + 1:]) + 1):
                # Adjust the count if it's a parenthesis
                if infix[i + j] == '(':
                    count += 1
                elif infix[i + j] == ')':
                    count -= 1
                    # Break if we get below a count of 0
                    if count < 0:
                        break
                # If we're not in a parenthesized expression and we get an operator that requires a new term
                elif infix[i + j] in ('+', '-', '*', '/', '=', ' ', ',', '|') and count == 0:
                    break
                right = i + j

            # Remove parentheses around the top and bottom if they can be removed
            top = remove_pars(infix[left:i])
            # Check the bottom expression to see if there's a fraction
            # This check doesn't need to be done for the top since it would have been evaluated already
            bottom = remove_pars(fraction(infix[i + 1: right + 1]))
            # Set a blank character if it's empty
            top = BLANK if top == '' else top
            bottom = BLANK if bottom == '' else bottom
            # Get the part of the expression to the left and right
            left = infix[:left]
            right = infix[right + 1:]

            infix = fr'{left}\frac{{{top}}}{{{bottom}}}{right}'

            # Check if there are any other fractions and return
            return fraction(infix)

    # Return what's left just in case we didn't
    return infix


def to_latex(infix):
    """Converts an expression to LaTeX form"""
    if infix == '':
        return BLANK
    if infix is None:
        return BLANK
    # $ means it's just text, not math
    if infix[0] == '$':
        return infix

    # Fix unmatched parentheses
    while infix.count('(') > infix.count(')'):
        infix += ')'
    while infix.count(')') > infix.count('('):
        infix = '(' + infix

    # Convert the fractions to latex form
    infix = fraction(infix)

    # Fix derivatives
    # Removes the extra space needed to keep the function from being grouped with d/dx
    if infix.startswith(r'\frac{d}{d'):
        if infix[12] == ' ':
            infix = list(infix)
            infix.pop(12)
            infix = ''.join(infix)

    # Fix whitespace
    infix = infix.replace(' ', r'\ ')

    # Convert functions to LaTeX form
    for i in FUNCTIONS:
        infix = infix.replace(i, fr'\{i} ')

    # Check for superscripts and subscripts
    for i in range(len(infix)):
        # If we find a superscript or subscript symbol
        if infix[i] in ('^', '_'):
            # If it's at the very end, add a blank character
            if i == len(infix) - 1:
                infix += '{' + BLANK + '}'
            else:
                # If We have a parenthesized expression
                if infix[i + 1] == '(':
                    try:
                        # Get the ends of the expression
                        left, right = par_count(infix[i + 1:])
                        # Set the end parentheses to curly brackets to make it look better
                        # i.e. e^(x+1) -> e^{x+1}
                        # Strings don't support item assignment, so we convert to a list and back
                        infix = list(infix)
                        infix[i + 1 + left] = '{'
                        infix[i + 1 + right] = '}'
                        infix = ''.join(infix)
                    except TypeError:
                        # In case we run into an error with there not being parentheses
                        continue

    # Special case for roots
    for i in range(len(infix) - 3):
        # If sqrt is in the string
        if infix[i:i + 4] == 'sqrt':
            try:
                # Get the ends of the expression
                left, right = par_count(infix[i + 4:])
                infix = list(infix)
                # Set the ends to curly brackets
                infix[i + 4 + left] = '{'
                infix[i + 4 + right] = '}'
                # Insert a blank character if the right parenthesis is one after the left one
                # i.e. sqrt( -> sqrt() -> sqrt{} -> sqrt{\ }
                if right == left + 1:
                    infix.insert(i + 4 + right, BLANK)
                infix = ''.join(infix)
            except TypeError:
                # Add a blank character if we're at the end
                infix += '{' + BLANK + '}'

    # Pi
    infix = infix.replace('pi', r'\pi ')
    # Replace times symbol with better looking multiplication dot
    # Could alternative do \times or leave it as implied multiply
    infix = infix.replace('*', r'\cdot ')
    # Infinity
    infix = infix.replace('infty', r'\infty ')
    infix = infix.replace('infinity', r'\infty ')
    # Plus or minus
    infix = infix.replace('+-', r'\pm ')
    # Right arrow
    infix = infix.replace('to', r'\to')
    # Inequalities
    infix = infix.replace('not=', r'\neq')
    infix = infix.replace('>=', r'\geq')
    infix = infix.replace('<=', r'\leq')
    # Parentheses
    infix = infix.replace('(', r'\left(')
    infix = infix.replace(')', r'\right)')

    return infix
