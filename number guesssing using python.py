import random
number_to_guess=random.randint(1,100)
while True:
    
    try:
        guess=int(input("Enter a number from 1-100: "))
        if guess<number_to_guess:
                  print("too low")
        elif guess>number_to_guess:
                  print("too high")
        else:
                      print("congratulations")
                      break
    except ValueError:
        print("invalid number")
                  
