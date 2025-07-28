import math

# --- Basic Arithmetic Functions (Variadic) ---

def add(*numbers):
    """
    Adds a variable number of numbers.
    If no numbers are provided, returns 0.
    """
    if not numbers:
        return 0
    return sum(numbers)

def subtract(*numbers):
    """
    Subtracts a variable number of numbers.
    The first number is the initial value, and subsequent numbers are subtracted from it.
    If no numbers are provided, returns 0. If one number, returns that number.
    """
    if not numbers:
        return 0
    if len(numbers) == 1:
        return numbers[0]
    
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

def multiply(*numbers):
    """
    Multiplies a variable number of numbers.
    If no numbers are provided, returns 1.
    """
    if not numbers:
        return 1
    
    result = 1
    for num in numbers:
        result *= num
    return result

def divide(*numbers):
    """
    Divides the first number by subsequent numbers.
    Handles division by zero errors.
    If no numbers are provided, returns 1. If one number, returns that number.
    """
    if not numbers:
        return 1
    if len(numbers) == 1:
        return numbers[0]
    
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            return "Error: Division by zero is not allowed."
        result /= num
    return result

# --- Advanced Math Functions (Bonus) ---

def power(base, exponent):
    """
    Calculates the base raised to the power of the exponent.
    """
    return base ** exponent

def square_root(number):
    """
    Calculates the square root of a number.
    Handles negative numbers.
    """
    if number < 0:
        return "Error: Cannot calculate the square root of a negative number."
    return math.sqrt(number)

# --- Helper Function for User Input ---

def get_numbers_input(operation_name, min_count=1):
    """
    Prompts the user to enter numbers for an operation.
    Keeps asking until 'done' is entered and minimum count is met.
    Handles non-numeric input.
    """
    numbers = []
    print(f"\nEnter numbers for {operation_name} (type 'done' when finished):")
    while True:
        num_str = input(f"Enter number {len(numbers) + 1}: ").strip()
        if num_str.lower() == 'done':
            if len(numbers) < min_count:
                print(f"Please enter at least {min_count} number(s) for this operation.")
                continue
            break
        try:
            numbers.append(float(num_str))
        except ValueError:
            print("Invalid input. Please enter a valid number or 'done'.")
    return numbers

# --- Main Calculator Program ---

def run_calculator():
    """
    Runs the main interactive calculator program.
    """
    print("Welcome to the Simple Python Calculator!")

    while True:
        print("\n--- Select an operation ---")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Power (^)")
        print("6. Square Root (√)")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            nums = get_numbers_input("addition", min_count=1)
            if nums:
                print(f"Result: {add(*nums)}")
        elif choice == '2':
            nums = get_numbers_input("subtraction", min_count=1)
            if nums:
                print(f"Result: {subtract(*nums)}")
        elif choice == '3':
            nums = get_numbers_input("multiplication", min_count=1)
            if nums:
                print(f"Result: {multiply(*nums)}")
        elif choice == '4':
            nums = get_numbers_input("division", min_count=1)
            if nums:
                print(f"Result: {divide(*nums)}")
        elif choice == '5':
            try:
                base = float(input("Enter the base number: "))
                exponent = float(input("Enter the exponent: "))
                print(f"Result: {power(base, exponent)}")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        elif choice == '6':
            try:
                num = float(input("Enter the number to find the square root of: "))
                print(f"Result: {square_root(num)}")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == '7':
            print("Exiting calculator. Goodbye, Godfred!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# Run the calculator when the script is executed
if __name__ == "__main__":
    run_calculator()
