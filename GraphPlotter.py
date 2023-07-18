import re as re
import sys
import warnings

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QWidget, \
    QHBoxLayout, QGroupBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from sympy import symbols, lambdify


class MainApp(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.message_box_shown = Signal(str)

        self.layout = QVBoxLayout(self)

        # create a label and input for the equation
        self.yLabel = QLabel('y =')
        self.equationInput = QLineEdit()

        # horizontal layout for the Label and input of the equation
        equationLayout = QHBoxLayout()
        # add the label and input of the equation to the horizontal layout
        equationLayout.addWidget(self.yLabel)
        equationLayout.addWidget(self.equationInput)

        # create a group box for the equation
        wholeEquationGroupBox = QGroupBox()
        wholeEquationGroupBox.setFixedHeight(70)
        wholeEquationGroupBox.setTitle('Enter the Equation')
        # add the horizontal layout to the group box
        wholeEquationGroupBox.setLayout(equationLayout)



        # create the group box for the whole range of x

        # create a label and input for the minimum value of x
        self.minimumXLabel = QLabel('min x =')
        self.minimumXInput = QLineEdit()

        # horizontal layout for the Label and input of the minimum value of x
        minimumXLayout = QHBoxLayout()
        # add the label and input of the minimum value of x to the horizontal layout
        minimumXLayout.addWidget(self.minimumXLabel)
        minimumXLayout.addWidget(self.minimumXInput)

        # create a label and input for the maximum value of x
        self.maximumXLabel = QLabel('max x =')
        self.maximumXInput = QLineEdit()

        # horizontal layout for the Label and input of the maximum value of x
        maximumXLayout = QHBoxLayout()
        # add the label and input of the maximum value of x to the horizontal layout
        maximumXLayout.addWidget(self.maximumXLabel)
        maximumXLayout.addWidget(self.maximumXInput)

        # vertical layout for the whole range of x
        WholeRangeXLayout = QVBoxLayout()
        # add the horizontal layouts of the minimum and maximum values of x to the vertical layout
        WholeRangeXLayout.addLayout(minimumXLayout)
        WholeRangeXLayout.addLayout(maximumXLayout)

        # create a group box for the whole range of x
        wholeRangeXGroupBox = QGroupBox()
        wholeRangeXGroupBox.setFixedHeight(100)
        wholeRangeXGroupBox.setTitle('Enter Minimum and Maximum values of x')
        # add the vertical layout to the group box
        wholeRangeXGroupBox.setLayout(WholeRangeXLayout)

        # create a button to plot the function
        self.plotButton = QPushButton('Plot Function')

        # create a figure and a canvas for the plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # add the group boxes, button and canvas to the main layout
        self.layout.addWidget(wholeEquationGroupBox)
        self.layout.addWidget(wholeRangeXGroupBox)
        self.layout.addWidget(self.plotButton)
        self.layout.addWidget(self.canvas)
        # connect the button to the function plotFunction
        self.plotButton.clicked.connect(self.plotFunction)

    def plotFunction(self):
        # create a symbol for x
        x = symbols('x')

        # get the equation from the input
        equationFunction = self.equationInput.text()
        # check if the equation is empty
        if equationFunction == '':
            message = 'Please enter the equation.'
            QMessageBox.warning(self, 'Input Error', message)
            return

        # check if the equation is valid
        validateMessage = self.validateExpression(equationFunction)
        if validateMessage != 'Correct Equation':
            QMessageBox.warning(self, 'Input Error', validateMessage)
            return

        try:
            # get the minimum and maximum values of x
            minX = float(self.minimumXInput.text())
            maxX = float(self.maximumXInput.text())
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid min and max values for x.')
            return

        # check if the minimum value of x is greater than the maximum value of x
        if minX >= maxX:
            QMessageBox.warning(self, 'Input Error', 'Max value of x should be greater than min value.')
            return

        try:
            # lambdify the equation
            with warnings.catch_warnings():
                warnings.filterwarnings("error")
                lambdifyEquation = lambdify(x, equationFunction.replace('^', '**').lower(), 'numpy')

                # create an array of x values
                xs = np.linspace(minX, maxX, 400)
                # create an array of y values
                ys = lambdifyEquation(xs)

                # for i in range (len(xs)):
                #     print(i, xs[i], ys[i])

                # plot the function
                self.figure.clear()
                ax = self.figure.subplots()
                ax.plot(xs, ys)
                self.canvas.draw()

        except:
            QMessageBox.warning(self, 'Input Error', 'The entered function is not valid.')
            return

    def validateExpression(self , expression):
        # Get the expression from the input


        # convert the expression to lower case
        expression = expression.lower()

        # Initialize valid characters and operators
        validCharacters = set('0123456789.x^+-/*() ')
        operators = set('^+-/*')
        nonBeginningOperators = set('^*/')
        repeatableOperators = set('+-')

        # Initialize counters for parentheses and dots
        openParentheses = 0
        dotCount = 0

        # check if the expression is starting with an invalid operator
        if expression[0] in nonBeginningOperators:
            return "The Equation cannot begin with one of these characters '^' or '*' or '/'"

        # check if the expression is ending with an invalid operator
        if expression[len(expression) - 1] in operators:
            return "The Equation cannot end with one of these characters '^' or '+' or '-' or '*' or '/'"

        # check if the expression is having at least one x
        if expression.count('x') == 0:
            return 'The Equation must have at least one x'

        # check if there is 2 numbers with spaces between them in the expression
        spacesBetweenNumberPattern = r"\d+\s+\d+"
        if re.search(spacesBetweenNumberPattern, expression):
            return 'The Equation cannot have spaces between numbers'
        invalidFollowingOperators = r"([*/^])([+-^])+([*/^])"
        if re.search(invalidFollowingOperators, expression):
            return 'The Equation cannot have 2 or more consecutive operators'

        # remove all spaces from the expression
        expression = expression.replace(' ', '')

        # Loop through each character in the expression
        for i, char in enumerate(expression):

            # Check for invalid characters
            if char not in validCharacters:
                return 'There are invalid characters in the equation'

            # Check for consecutive operators
            if 0 < i and char in nonBeginningOperators and expression[i - 1] in nonBeginningOperators:
                return 'The Equation cannot have 2 or more consecutive operators'

            # Check for consecutive Xs
            if 0 < i and char == 'x' and expression[i - 1] == 'x':
                return 'The Equation cannot have 2 or more consecutive Xs'

            # Check for x being part of a number or x with dot or opening parentheses
            if i > 0 and ((char == 'x' and (expression[i - 1].isdigit() or expression[i - 1] == '.' or expression[i-1] == ')')) or
                          (char.isdigit() and expression[i - 1] == 'x') or
                          ((char == '.' or char == '(') and expression[i - 1] == 'x')):
                return 'x cannot be concatenated with something'

            #check if there is division by zero
            if (char == '0' and expression[i - 1] == '/'):
                return 'the denominator of the division cannot be zero'

            # Validating parentheses
            if char == '(':
                openParentheses += 1
                if i > 0 and expression[i - 1].isdigit():
                    return 'Opening Parentheses cannot have number before it'
                if i < len(expression) - 1:
                    if expression[i + 1] in nonBeginningOperators:
                        return 'Opening Parentheses cannot be followed by one of these characters "^" or "*" or "/"'
            elif char == ')':
                if openParentheses == 0:
                    return 'Parentheses are not balanced'
                openParentheses -= 1
                if i + 1 < len(expression) and (expression[i + 1].isdigit()):
                    return 'Closing Parentheses cannot have number after it'
                if i > 0:
                    if expression[i - 1] in operators:
                        return 'Closing Parentheses cannot be preceded by one of these characters "^" or "+" or "-" or "*" or "/"'

            # Validating dots
            if char == '.':
                if i + 1 < len(expression):
                    if not expression[i - 1].isdigit() or not expression[i + 1].isdigit():
                        return "'.' is only used in float numbers"
                else:
                    return "'.' is only used in float numbers"
                dotCount += 1
            elif char.isdigit():
                continue
            else:
                if dotCount > 1:
                    return 'float number cannot contain more than one dot'
                dotCount = 0

        # Check for unbalanced parentheses
        if openParentheses != 0:
            return 'Parentheses are not balanced'

        # Check for consecutive dots
        if dotCount > 1:
            return 'float number cannot contain more than one dot'

        return 'Correct Equation'


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainApp()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

