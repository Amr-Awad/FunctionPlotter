# Function Plotter

This repository contains the documentation for Function Plotter.

## Contents

- [Overview](#overview)
- [Functions](#functions)
  - [ValidateExpression](#validateexpression)
  - [PlotFunction](#plotfunction)
- [Technologies](#technologies)
- [Testing](#testing)

## Overview 

Function Plotter is a GUI Desktop Application that takes an equation and minimum value and maximum value from the user. It checks if the equation is valid, parses it, and plots a graph based on the equation. The application draws a line on the graph using the coordinates (x, y) generated from the provided minimum and maximum values.

## Functions

### ValidateExpression

The `ValidateExpression` function ensures that the expression follows the specified rules. If any violations are found, it returns an error message. If the expression is valid, it returns 'Correct Equation'.

### PlotFunction

The `PlotFunction` function plots a graph based on the user-provided equation. It validates the equation, checks the input values, converts the equation into a mathematical function, generates x values, evaluates the function to obtain y values, and plots the resulting graph. It handles any errors that occur during the process and displays appropriate error messages.

## Technologies

### Libraries Used for the GUI:
> **_NOTE:_**  I used PySide6 instead of PySide2 as there was error in using PySide2.

- PySide6
- matplotlib
- numpy
- sympy

### Libraries Used for Testing:

- pytest
- pytest-qt
- unittest

## Testing
There are 2 classes for testing.
- TestValidation<br/>
    Used in testing the validateExpression function.
- TestFullExecution<br/>
    Used in testing the full GUI window.
  
