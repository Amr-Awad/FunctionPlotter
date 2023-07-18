import pytest
import pytestqt.qtbot
from unittest.mock import patch




from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from GraphPlotter import MainApp  # replace with actual module name


@pytest.fixture
def app(qtbot):
    test_app = MainApp()
    qtbot.addWidget(test_app)

    return test_app


class TestValidation:
    def test_correct_equation(self, app):
        assert app.validateExpression('x^2') == 'Correct Equation'
        assert app.validateExpression('(x+2)^2') == 'Correct Equation'

    def test_case_sensitivity(self, app):
        assert app.validateExpression('X^2') == 'Correct Equation'

    def test_beginning_of_equation(self, app):
        assert app.validateExpression('/x^2') == "The Equation cannot begin with one of these characters '^' or '*' or '/'"

    def test_end_of_equation(self, app):
        assert app.validateExpression('x^2 + 1+') == "The Equation cannot end with one of these characters '^' or '+' or '-' or '*' or '/'"

    def test_minimum_x_occurrence(self, app):
        assert app.validateExpression('x^2') == 'Correct Equation'
        assert app.validateExpression('2') == 'The Equation must have at least one x'

    def test_spaces_between_numbers(self, app):
        assert app.validateExpression('x + 10') == 'Correct Equation'
        assert app.validateExpression('x + 1 0') == 'The Equation cannot have spaces between numbers'

    def test_invalid_characters(self, app):
        assert app.validateExpression('gh+x') == 'There are invalid characters in the equation'

    def test_consecutive_xs(self, app):
        assert app.validateExpression('xx') == 'The Equation cannot have 2 or more consecutive Xs'

    def test_consecutive_operators(self, app):
        assert app.validateExpression('x+-2') == 'Correct Equation'
        assert app.validateExpression('x^^2') == 'The Equation cannot have 2 or more consecutive operators'
        assert app.validateExpression('x*-+*2') == 'The Equation cannot have 2 or more consecutive operators'

    def test_concatenated_x(self, app):
        assert app.validateExpression('x * 2') == 'Correct Equation'
        assert app.validateExpression('x2') == 'x cannot be concatenated with something'
        assert app.validateExpression('x(2)') == 'x cannot be concatenated with something'
        assert app.validateExpression('x.2') == 'x cannot be concatenated with something'

    def test_division_by_zero(self, app):
        assert app.validateExpression('x + 1 / 4') == 'Correct Equation'
        assert app.validateExpression('x + 1 / 0') == 'the denominator of the division cannot be zero'

    def test_parentheses_placement(self, app):
        assert app.validateExpression('2*(x+2)^3') == 'Correct Equation'
        assert app.validateExpression('2(x+1)') == 'Opening Parentheses cannot have number before it'
        assert app.validateExpression('(/+x+1)') == 'Opening Parentheses cannot be followed by one of these characters "^" or "*" or "/"'
        assert app.validateExpression('x+1)') == 'Parentheses are not balanced'
        assert app.validateExpression('(x+12') == 'Parentheses are not balanced'
        assert app.validateExpression('(x+1)2') == 'Closing Parentheses cannot have number after it'
        assert app.validateExpression('(x+1/)^2') == 'Closing Parentheses cannot be preceded by one of these characters "^" or "+" or "-" or "*" or "/"'

    def test_float_number_validations(self, app):
        assert app.validateExpression('x + 2.5') == 'Correct Equation'
        assert app.validateExpression('x + 1.0.1') == 'float number cannot contain more than one dot'
        assert app.validateExpression('x + 2.^+5') == "'.' is only used in float numbers"

    def test_negative_number_validations(self, app):
        assert app.validateExpression('x + -2') == 'Correct Equation'
        assert app.validateExpression('x + -2.5') == 'Correct Equation'
        assert app.validateExpression('x + --2') == 'Correct Equation'
        assert app.validateExpression('x + -+2') == 'Correct Equation'
        assert app.validateExpression('x + +-2') == 'Correct Equation'



class TestFullExecution:
    def clear_all(self, app):
        app.equationInput.clear()
        app.minimumXInput.clear()
        app.maximumXInput.clear()
        return app

    def test_valid_input(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x^2')
        qtbot.keyClicks(app.minimumXInput, '-10')
        qtbot.keyClicks(app.maximumXInput, '10')
        qtbot.mouseClick(app.plotButton, Qt.LeftButton)

        assert app.equationInput.text() == 'x^2'
        assert app.minimumXInput.text() == '-10'
        assert app.maximumXInput.text() == '10'

        app = self.clear_all(app)

    def test_empty_equation_input(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, '')
        qtbot.keyClicks(app.minimumXInput, '-10')
        qtbot.keyClicks(app.maximumXInput, '10')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'Please enter the equation.')

        assert app.equationInput.text() == ''
        assert app.minimumXInput.text() == '-10'
        assert app.maximumXInput.text() == '10'

        app = self.clear_all(app)

    def test_invalid_equation_input(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x^^2')
        qtbot.keyClicks(app.minimumXInput, '-10')
        qtbot.keyClicks(app.maximumXInput, '10')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'The Equation cannot have 2 or more consecutive operators')

        assert app.equationInput.text() == 'x^^2'
        assert app.minimumXInput.text() == '-10'
        assert app.maximumXInput.text() == '10'

        app = self.clear_all(app)

    def test_invalid_min_max_x(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x^2')
        qtbot.keyClicks(app.minimumXInput, '10')
        qtbot.keyClicks(app.maximumXInput, '-10')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'Max value of x should be greater than min value.')

        assert app.equationInput.text() == 'x^2'
        assert app.minimumXInput.text() == '10'
        assert app.maximumXInput.text() == '-10'

        app = self.clear_all(app)

    def test_invalid_min_max_x_2(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x^2')
        qtbot.keyClicks(app.minimumXInput, 'a')
        qtbot.keyClicks(app.maximumXInput, 'b')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'Please enter valid min and max values for x.')

        assert app.equationInput.text() == 'x^2'
        assert app.minimumXInput.text() == 'a'
        assert app.maximumXInput.text() == 'b'

        app = self.clear_all(app)

    def test_missing_min_max_x(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x^2')
        qtbot.keyClicks(app.minimumXInput, '')
        qtbot.keyClicks(app.maximumXInput, '')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'Please enter valid min and max values for x.')

        assert app.equationInput.text() == 'x^2'
        assert app.minimumXInput.text() == ''
        assert app.maximumXInput.text() == ''

        app = self.clear_all(app)

    def test_missing_min_x(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x^2')
        qtbot.keyClicks(app.minimumXInput, '')
        qtbot.keyClicks(app.maximumXInput, '10')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'Please enter valid min and max values for x.')

        assert app.equationInput.text() == 'x^2'
        assert app.minimumXInput.text() == ''
        assert app.maximumXInput.text() == '10'

        app = self.clear_all(app)

    def test_missing_max_x(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x^2')
        qtbot.keyClicks(app.minimumXInput, '-10')
        qtbot.keyClicks(app.maximumXInput, '')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'Please enter valid min and max values for x.')

        assert app.equationInput.text() == 'x^2'
        assert app.minimumXInput.text() == '-10'
        assert app.maximumXInput.text() == ''

        app = self.clear_all(app)

    def test_uncatched_invalid_equation(self, qtbot, app):
        qtbot.keyClicks(app.equationInput, 'x/(x-x)')
        qtbot.keyClicks(app.minimumXInput, '-10')
        qtbot.keyClicks(app.maximumXInput, '10')

        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(app.plotButton, Qt.LeftButton)
            mock_warning.assert_called_once_with(app, 'Input Error', 'The entered function is not valid.')

        assert app.equationInput.text() == 'x/(x-x)'
        assert app.minimumXInput.text() == '-10'
        assert app.maximumXInput.text() == '10'


