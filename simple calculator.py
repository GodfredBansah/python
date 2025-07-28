import tkinter as tk
import math

# --- Backend Arithmetic Functions (from your previous solution) ---
# These functions are designed to accept a variable number of arguments (*numbers)
# For the GUI, they will typically be called with two arguments (first_operand, second_operand)
# to fit the standard calculator interaction flow.

def add(*numbers):
    """Adds a variable number of numbers. Returns 0 if no numbers."""
    if not numbers:
        return 0
    return sum(numbers)

def subtract(*numbers):
    """Subtracts a variable number of numbers.
    The first number is the initial value, and subsequent numbers are subtracted from it.
    Returns 0 if no numbers. If one number, returns that number."""
    if not numbers:
        return 0
    if len(numbers) == 1:
        return numbers[0]
    
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

def multiply(*numbers):
    """Multiplies a variable number of numbers. Returns 1 if no numbers."""
    if not numbers:
        return 1
    
    result = 1
    for num in numbers:
        result *= num
    return result

def divide(*numbers):
    """Divides the first number by subsequent numbers.
    Handles division by zero errors by raising a ValueError.
    Returns 1 if no numbers. If one number, returns that number."""
    if not numbers:
        return 1
    if len(numbers) == 1:
        return numbers[0]
    
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            raise ValueError("Division by zero is not allowed.")
        result /= num
    return result

# --- Advanced Math Functions (Bonus) ---

def power(base, exponent):
    """Calculates the base raised to the power of the exponent."""
    return base ** exponent

def square_root(number):
    """Calculates the square root of a number.
    Handles negative numbers by raising a ValueError."""
    if number < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(number)

# --- GUI Implementation using Tkinter ---

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("GODFRED BANSAH AI CALCULATOR ")
        master.geometry("300x400") # Set a fixed size for better appearance
        master.resizable(False, False) # Prevent resizing

        # --- Calculator State Variables ---
        # Stores the text currently displayed on the calculator screen
        self.current_input = tk.StringVar(value="0") 
        # Stores the first operand of a binary operation (e.g., '5' in '5 + 3')
        self.first_operand = None
        # Stores the operator selected (+, -, *, /, ^)
        self.operator = None
        # Flag to indicate if the next digit pressed should clear the display
        # (e.g., after an operator or '=' is pressed)
        self.new_input_needed = True 

        # --- Display Entry Widget ---
        # An Entry widget to show input and results. Set to 'readonly' to prevent direct typing.
        self.display = tk.Entry(master, textvariable=self.current_input,
                                font=('Arial', 24), bd=10, insertwidth=2,
                                width=14, borderwidth=4, justify='right',
                                state='readonly') 
        self.display.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        # --- Button Layout Definition ---
        # Each tuple: (button_text, row, column)
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('√', 5, 1), ('^', 5, 2)
        ]

        # --- Create and Place Buttons ---
        for (text, row, col) in buttons:
            # Common button styling
            button = tk.Button(master, text=text, font=('Arial', 18), padx=20, pady=20)
            
            # Assign command based on button type
            if text == '=':
                button.config(command=self.calculate)
            elif text in ('/', '*', '-', '+', '^'): # Operators and Power
                button.config(command=lambda op=text: self.set_operator(op))
            elif text == 'C': # Clear button
                button.config(command=self.clear_display)
            elif text == '√': # Square Root button
                 button.config(command=self.do_square_root)
            else: # Number and decimal point buttons
                button.config(command=lambda num=text: self.button_press(num))
            
            # Place button in grid
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # --- Configure Grid Weights ---
        # This makes the buttons expand to fill the window space dynamically
        for i in range(6): # Rows 0 (display) to 5 (last row of buttons)
            master.grid_rowconfigure(i, weight=1)
        for i in range(4): # Columns 0 to 3
            master.grid_columnconfigure(i, weight=1)

    def button_press(self, num):
        """
        Handles number and decimal point button presses.
        Updates the display string.
        """
        current = self.current_input.get()
        
        # If starting a new number (after operator/equals, or initial "0", or error state)
        if self.new_input_needed or current == "0" or current == "Error":
            if num == '.': # If starting with '.', prepend "0"
                self.current_input.set("0.")
            else:
                self.current_input.set(num)
            self.new_input_needed = False
        elif num == '.' and '.' in current:
            pass # Do nothing if decimal already exists in the current number
        else:
            self.current_input.set(current + num)

    def clear_display(self):
        """
        Clears the display and resets all calculator state variables.
        """
        self.current_input.set("0")
        self.first_operand = None
        self.operator = None
        self.new_input_needed = True

    def set_operator(self, op):
        """
        Stores the current display value as the first operand and sets the chosen operator.
        If a previous operation is pending (e.g., 5 + 3, then user presses another +),
        it calculates the pending operation first.
        """
        try:
            current_value = float(self.current_input.get())
        except ValueError:
            # Handle cases where current display is "Error" or invalid
            self.current_input.set("Error")
            self.first_operand = None
            self.operator = None
            self.new_input_needed = True
            return

        if self.first_operand is not None and self.operator is not None:
            # If there's a pending operation (e.g., 5 + 3, then user presses *),
            # calculate the previous operation first (5+3=8), then use 8 as first_operand for *
            self.calculate()
            # The result of calculate() will be in current_input, so use that as the new first_operand
            try:
                self.first_operand = float(self.current_input.get())
            except ValueError: # In case calculate resulted in an error
                self.first_operand = None
                self.operator = None
                self.new_input_needed = True
                return
            self.operator = op # Set the new operator
        else:
            # If no pending operation, just store the current display as the first operand
            self.first_operand = current_value
            self.operator = op
            
        self.new_input_needed = True # Next digit pressed will start a new number

    def calculate(self):
        """
        Performs the calculation based on the stored first_operand, operator,
        and the current number on the display (second_operand).
        """
        # Do nothing if there's no pending operation
        if self.first_operand is None or self.operator is None:
            return 

        try:
            second_operand = float(self.current_input.get())
        except ValueError:
            # Handle cases where the second operand is invalid
            self.current_input.set("Error")
            self.first_operand = None
            self.operator = None
            self.new_input_needed = True
            return

        result = None
        try:
            # Call the appropriate backend function with the two operands
            if self.operator == '+':
                result = add(self.first_operand, second_operand)
            elif self.operator == '-':
                result = subtract(self.first_operand, second_operand)
            elif self.operator == '*':
                result = multiply(self.first_operand, second_operand)
            elif self.operator == '/':
                result = divide(self.first_operand, second_operand)
            elif self.operator == '^':
                result = power(self.first_operand, second_operand)
            
            # Display the result
            self.current_input.set(str(result))
            # Set the result as the new first_operand for potential chained operations
            self.first_operand = result 
            self.operator = None # Clear the operator after calculation
            self.new_input_needed = True # Next digit will start a new number

        except ValueError as e: # Catch specific errors from backend functions (e.g., division by zero, sqrt negative)
            self.current_input.set(f"Error: {e}")
            self.first_operand = None
            self.operator = None
            self.new_input_needed = True
        except Exception as e: # Catch any other unexpected errors
            self.current_input.set("Error")
            self.first_operand = None
            self.operator = None
            self.new_input_needed = True
            print(f"An unexpected error occurred during calculation: {e}") # For debugging

    def do_square_root(self):
        """
        Calculates the square root of the number currently on the display.
        """
        try:
            num = float(self.current_input.get())
            result = square_root(num)
            self.current_input.set(str(result))
            self.new_input_needed = True
            self.first_operand = result # Make result available for further operations
            self.operator = None # Clear any pending operator
        except ValueError as e:
            self.current_input.set(f"Error: {e}")
            self.first_operand = None
            self.operator = None
            self.new_input_needed = True
        except Exception as e:
            self.current_input.set("Error")
            self.first_operand = None
            self.operator = None
            self.new_input_needed = True
            print(f"An unexpected error occurred during square root: {e}") # For debugging


# --- Main Application Execution ---
if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    # Create an instance of our CalculatorGUI class
    calculator = CalculatorGUI(root)
    # Start the Tkinter event loop (makes the window appear and respond to interactions)
    root.mainloop()

    

