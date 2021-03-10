# Module for randomness
import random
# To limit the time of a problem if it's taking too long
import time
from threading import Thread

# Module for symbolic calculations
from sympy import *

# Get special functions
from latex import FUNCTIONS


def text(expression):
    """Convert a sympy expression into plain text"""
    # Converts inverse hyperbolic functions into ln format
    if 'sinh' in str(expression) or 'cosh' in str(expression) or 'tanh' in str(expression):
        expression = expression.rewrite(log)
    # Get the string value
    expression = str(expression)
    # ln is preferred notation over log
    expression = expression.replace('log', 'ln')
    # Use regular exponents instead of python ones
    expression = expression.replace('**', '^')
    # Sympy likes to put spaces around + and -
    expression = expression.replace(' + ', '+')
    expression = expression.replace(' - ', '-')
    # Use LaTeX-supported inverse trig notation
    expression = expression.replace('asin', 'sin^(-1)')
    expression = expression.replace('acos', 'cos^(-1)')
    expression = expression.replace('atan', 'tan^(-1)')
    expression = expression.replace('acot', 'cot^(-1)')
    expression = expression.replace('asec', 'sec^(-1)')
    expression = expression.replace('acsc', 'csc^(-1)')
    # Use e^( instead of exp(
    expression = expression.replace('exp', 'e^')
    # Use lowercase e instead of capital E
    expression = expression.replace('E', 'e')

    # Remove unnecessary multiplication signs and fix exponents
    # We can't use a normal for loop since the length of the expression can change throughout
    i = 0
    while i < len(expression):
        # Remove unnecessary multiplication signs
        if expression[i] == '*':
            try:
                # If the values to the sides of the sign are numbers, don't remove the sign
                # 1*2 is very different from 12
                int(expression[i - 1])
                int(expression[i + 1])
            except ValueError:
                # If there's an error, then they're not both numbers. Remove the sign
                expression = expression[:i] + expression[i + 1:]
                continue
        # Fix expressions like x^12 getting interpreted as (x^1)*2
        # Make them be in the form x^(12)
        elif expression[i] == '^':
            # Find when the exponent is over if it's an integer
            right = i
            for j in range(i + 1, len(expression)):
                try:
                    # If it's an integer, then keep going
                    int(expression[j])
                    right = j + 1
                except ValueError:
                    # If it's not an integer, we don't need to worry about it
                    break
            # If there was a number in the exponents
            if right != i:
                # Add the parentheses around the exponent
                expression = list(expression)
                expression.insert(right, ')')
                expression.insert(i + 1, '(')
                expression = ''.join(expression)
        # Iterate
        i += 1

    return expression


def to_sympy(expression):
    """Convert an expression to something that can be understood by sympy
    This primarily fixes implied multiplication
    """
    # Fix unmatched parentheses
    while expression.count('(') > expression.count(')'):
        expression += ')'
    while expression.count(')') > expression.count('('):
        expression = '(' + expression

    # Set a character around functions so we don't add implied multiplications
    # We don't want things like sin(x) to become s*i*n*(x)
    for i in FUNCTIONS + ('pi',):
        expression = expression.replace(i, f'_{i}_')
    expression = list(expression)
    # Variable for whether we're in a function
    underscore = False
    # We can't use a normal for loop since the expression's length can change
    i = 0
    while i < len(expression) - 1:
        # If we find an underscore, we're in a function, so don't add implied multiplies
        # This would result in something like sin(x) becoming s*i*n*(x)
        if expression[i] == '_':
            # If we were in an underscore, now we're not, If we weren't, now we are.
            underscore = not underscore
            i += 1
            continue
        # Continue if we're in a function
        if underscore:
            i += 1
            continue
        # Get the character on both sides of the potential implied multiplication
        x1 = expression[i]
        x2 = expression[i + 1]
        # Checks the following types of cases for implied multiplies:
        # ab, a2, a(, a_sin_, 2a, 2(, 2_sin, )a, )2, )(, )_sin_
        # Does not add implied multiplies in situations like 12 (12 is 12, not 1*2)
        if (x1.isalpha() or x1.isdigit() or x1 == ')') and (x2.isalpha() or x2.isdigit() or x2 in ['(', '_']) and not \
                (x1.isdigit() and x2.isdigit()):
            # Add the multiplication sign
            expression.insert(i + 1, '*')
        i += 1

    expression = ''.join(expression)
    # Get rid of the underscores we added
    expression = expression.replace('_', '')

    # Sympy doesn't like inverse trig in the format sin^(-1)
    # It prefers asin
    for i in ('sin', 'cos', 'tan', 'cot', 'sec', 'csc'):
        expression = expression.replace(f'{i}^(-1)*', f'a{i}')

    # Convert the expression to a sympy form
    expression = sympify(expression)
    # Replace e with the actual value of E
    return expression.subs(symbols('e'), E)


def generate_term(problem_type, parameter):
    """Generate one term of a problem"""
    # Derivatives
    if problem_type == 'Derivative':
        if parameter == 'Polynomials':
            exponent = random.randint(1, 9)
            # x^a
            return f'x^{exponent}'
        elif parameter == 'Exponential rules':
            base = random.choice(('E', random.randint(2, 9)))
            # a^x
            return f'{base}^x'
        elif parameter == 'Logarithms':
            # We don't have custom bases because sympy just converts them to ln(x)/ln(a) form
            # ln(x)
            return f'log(x)'
        elif parameter == 'Trig':
            # sin(x)
            function = random.choice(('sin', 'cos', 'tan', 'cot', 'sec', 'csc'))
            return f'{function}(x)'
        elif parameter == 'Inverse trig':
            # sin^(-1)(x)
            function = random.choice(('asin', 'acos', 'atan', 'acot', 'asec', 'acsc'))
            return f'{function}(x)'
        elif parameter == 'Logarithmic differentiation':
            # x^x
            return f'x^x'
        # Just in case the parameter doesn't match anything
        else:
            return 'x'
    # Integrals
    elif problem_type == 'Integral':
        if parameter == 'Polynomials':
            exponent = random.randint(1, 4)
            # x^a
            return f'x^{exponent}'
        elif parameter == 'Exponential rules':
            base = random.choice(('E', random.randint(2, 9)))
            # a^x
            return f'{base}^x'
        elif parameter == 'Logarithms':
            # 1/x
            return '1/x'
        elif parameter == 'Trig':
            # sin(x)
            function = random.choice(('sin', 'cos', 'tan', 'cot', 'sec', 'csc'))
            return f'{function}(x)'
        elif parameter == 'Inverse trig':
            # 1/sqrt(1-x^2)
            a = random.randint(1, 9) ** 2
            # Sympy doesn't work well with arcsec, so we don't use it
            function = random.choice((f'1/sqrt({a}-x^2)', f'1/(x^2+{a})'))
            return function
        elif parameter == 'Partial fractions':
            # a/((x-b)(x-c))
            a, b, c = [random.randint(1, 9) for _ in range(3)]
            return f'{c}/((x-{a})*(x-{b}))'
        elif parameter == 'Trigonometric substitution':
            r = random.randint(1, 9) ** 2
            # Random coefficients, can't both be negative
            a, b = random.choice(((1, 1), (-1, 1), (1, -1)))
            f = f'sqrt({a}*x^2+{b}*{r})'
            if random.randint(1, 2) == 1:
                # sqrt(x^2+1)
                return f
            else:
                # 1/sqrt(x^2+1)
                return f'1/{f}'
        # Just in case the parameter doesn't match anything
        else:
            return 'x'


def generate(problem_type, parameters, complexity):
    """Generate a problem with the given arguments"""
    # Derivatives
    if problem_type == 'Derivative':
        args = []
        operators = []
        # Find out which rules for combining things are allowed
        for i in parameters:
            if i == 'Sum rule':
                operators.append('+')
                operators.append('-')
            elif i == 'Product rule':
                operators.append('*')
            elif i == 'Quotient rule':
                operators.append('/')
            elif i == 'Chain rule':
                operators.append('chain')
            else:
                args.append(i)

        # Randomly generate terms for the problem
        parts = []
        for i in range(complexity):
            # Generate the term
            term = generate_term(problem_type, random.choice(args))
            parts.append(term)

        # Combine the parts
        output = ''
        for i in range(len(parts) - 1):
            # Get a random operator
            op = random.choice(operators)
            # If it's a chain rule, replace x with the special operator
            # Only replace one instance. This keeps logarithmic differentiation somewhat reasonable
            if op == 'chain':
                parts[i + 1] = parts[i + 1].replace('x', f'({parts[i]})', 1)
            else:
                # If it's not a chain rule, add to the output with the operator (+, -, *, or /)
                output += parts[i] + op
        # Add the last item to the output. It doesn't need an operator since it's at the end
        output += parts[-1]

        # Convert the problem to sympy and calculate the derivative
        problem = sympify(output)
        solution = diff(problem)

        # Catch problems in the generated problem. This shouldn't happen, but just in case
        while problem in [nan, zoo] or str(problem) == '0':
            problem, solution = generate(problem_type, parameters, complexity)

        # Convert to text
        return text(problem), text(solution)
    # Integrals
    elif problem_type == 'Integral':
        args = []
        operators = []
        # Find out which rules for combining things are allowed
        for i in parameters:
            if i == 'Sum rule':
                operators.append('+')
                operators.append('-')
            elif i == 'Integration by parts':
                operators.append('*')
            elif i == 'U substitution':
                operators.append('u')
            else:
                args.append(i)

        # Generate the individual terms
        parts = [generate_term(problem_type, random.choice(args))]
        ops = []
        for i in range(complexity - 1):
            # Get a random operator
            op = random.choice(operators)
            if op in ('+', '-'):
                parts.append(generate_term(problem_type, random.choice(args)))
                ops.append(op)
            elif op == '*':
                # Polynomials are the only thing that always work with integration by parts
                parts.append(generate_term(problem_type, 'Polynomials'))
                ops.append(op)
            elif op == 'u':
                # Create a u-substitution
                u = generate_term(problem_type, random.choice(args))
                du = diff(u)
                parts[-1] = f"({parts[-1].replace('x', f'({u})')})*{du}"

        # Add the terms together with the appropriate operator
        output = ''
        for i in range(len(ops)):
            output += f'({parts[i]}){ops[i]}'
        output += f'({parts[-1]})'

        # Convert to sympy
        problem = sympify(output)
        solution = [None]

        # Integrate a function
        def integrate_():
            solution[0] = integrate(problem)

        # Start a thread to integrate
        thread = Thread(target=integrate_)
        thread.start()
        # Try integrating for roughly 1.5 seconds
        # Some functions take a really long time, so we use this to limit the time
        for i in range(15):
            time.sleep(0.1)
            # If the solution has been found, we're good
            if solution[0] is not None:
                break
        # If it took too long, try a different problem instead
        if solution[0] is None:
            return generate(problem_type, parameters, complexity)
        else:
            solution = solution[0]

        # If it was a function that can't be integrated, try again
        if 'Integral' in str(solution):
            return generate(problem_type, parameters, complexity)
        else:
            # Convert to text and return
            return text(problem), text(solution)
    # Series
    elif problem_type == 'Series':
        # Choose a random parameter
        i = random.choice(parameters)
        if i == 'Nth term':
            # Random series that diverges by the nth term test
            j = random.randint(1, 6)
            if j == 1:
                problem = ['n', 0]
            elif j == 2:
                problem = [str(random.randint(1, 10)), 0]
            elif j == 3:
                problem = [f'n-(n+{random.randint(1, 5)})', 0]
            elif j == 4:
                problem = [f'(-1)^n', 0]
            elif j == 5:
                problem = ['sin(x)', 0]
            else:
                problem = ['ln(x)', 1]
            answer = 'Divergent'
        elif i == 'Geometric':
            # Random geometric series
            start = random.randint(0, 5)
            a0 = random.randint(1, 5)
            n = random.randint(1, 5)
            d = random.randint(1, 5)
            problem = [f'{a0}*({random.choice(("", "-"))}{n}/{d})^n', start]
            answer = 'Convergent' if n / d < 1 else 'Divergent'
        elif i == 'Telescoping':
            # Random telescoping series
            a = random.randint(1, 5)
            b = random.randint(a + 1, a + 6)
            problem = [f'1/(n+{a})-1/(n+{b})', 0]
            answer = 'Convergent'
        elif i == 'P-series':
            # Random p-series
            if random.randint(0, 1) == 0:
                p = f'1/{random.randint(1, 5)}'
                answer = 'Divergent'
            else:
                p = random.randint(1, 5)
                answer = 'Convergent' if p != 1 else 'Divergent'
            problem = [f'1/(n^({p}))', 1]
        elif i == 'Integral test':
            # Random series that works with the integral test
            # The integral test has a lot of functions it works with, so we only choose a certain type
            exp1 = random.randint(1, 5)
            c1 = random.randint(1, 5)
            exp2 = random.randint(exp1, exp1 + 5)
            c2 = random.randint(1, 5)
            c3 = random.randint(1, 5)
            n = f'{c1}*n^({exp1})'
            d = f'{c2}*n^({exp2})+{c3}'
            problem = [f'{n}/({d})', 0]
            answer = 'Convergent' if exp2 - exp1 >= 2 else 'Divergent'
        elif i == 'Direct comparison test':
            # Random direct comparison test series
            # Only does functions in a specific form since the test is very versatile
            if random.randint(0, 1) == 0:
                answer = 'Convergent'
                exp1 = random.randint(1, 5)
                exp2 = random.randint(exp1 + 2, exp1 + 7)
                c1 = random.randint(1, 5)
                c2 = random.randint(1, 5)
                problem = [f'(n^{exp1}-{c1})/(n^{exp2}+{c2})', 0]
            else:
                answer = 'Divergent'
                exp1 = random.randint(1, 5)
                exp2 = exp1 + 1
                c1 = random.randint(1, 5)
                c2 = random.randint(1, 5)
                problem = [f'(n^{exp1}+{c1})/(n^{exp2}-{c2})', 0]
        elif i == 'Limit comparison test':
            # Random limit comparison test series
            # Only does functions in a specific form since the test is very versatile
            exp1 = random.randint(1, 5)
            exp2 = random.randint(exp1 + 1, exp1 + 6)
            c1 = random.randint(1, 5)
            c2 = random.randint(1, 5)
            problem = [f'(n^{exp1}{random.choice(("+", "-"))}{c1})/(n^{exp2}{random.choice(("+", "-"))}{c2})', 0]
            answer = 'Convergent' if exp2 - exp1 >= 2 else 'Divergent'
        elif i == 'Alternating series':
            # Creates another series that passes the nth term test and makes it alternating
            args = ('P-series', 'Integral test', 'Direct comparison test', 'Limit comparison test')
            problem, answer = generate(problem_type, args, None)
            problem = [f'(-1)^n*({problem[0]})', problem[1]]
            answer = 'Convergent'
        else:
            # In case the parameter didn't match, return the harmonic series
            problem = ['1/n', 1]
            answer = 'Divergent'

        # Convert to sympy, then back to text, and return
        # We convert to sympy since that simplifies the series
        problem[0] = text(to_sympy(problem[0]))
        return problem, answer


def calculate(problem_type, function, variable, start=None, end=None, value=0, do_it=False):
    """Solve a calculus problem"""
    # Derivatives
    if problem_type == 'Derivative':
        try:
            return text(diff(to_sympy(function), symbols(variable)))
        except SympifyError:
            return '$Input error!'
        except TypeError:
            return '$Input error!'
        except ValueError:
            return '$Input error!'
        except AttributeError:
            return '$Input error!'
    # Integrals
    elif problem_type == 'Integral':
        try:
            if start == '' or end == '':
                return text(integrate(to_sympy(function), symbols(variable)))
            else:
                return text(integrate(to_sympy(function), (symbols(variable), to_sympy(start), to_sympy(end))))
        except SympifyError:
            return '$Input error!'
        except TypeError:
            return '$Input error!'
        except ValueError:
            return '$Input error!'
        except AttributeError:
            return '$Input error!'
    # Series
    elif problem_type == 'Series':
        try:
            answer = Sum(to_sympy(function), (symbols(variable), value, oo))
            if do_it:
                answer = text(answer.doit())
                if 'zoo' in answer or 'oo' in answer:
                    return '$Divergent'
                else:
                    return answer
            else:
                if answer.is_convergent():
                    return '$Convergent'
                else:
                    return '$Divergent'
        except SympifyError:
            return '$Input error!'
        except TypeError:
            return '$Input error!'
        except ValueError:
            return '$Input error!'
        except NotImplementedError:
            return '$Input error!'
        except AttributeError:
            return '$Input error!'
