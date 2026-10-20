"""
Input Collection and Verification Module

This module handles command-line prompts to the user and the validation of their input as valid.
It ensures that main.py only receives valid integers and characters before proceeding to calculate
render geometry.
"""
#--------------------------
def query_number_sides():
    """
    Prompts user for an integer value to use for the number of sides of the bases
    of the prism and checks that the input is valid before returning it.

    Returns integer between 3 and 7.
    """
    while True:
        try:
            user_in = int(input("\nPlease enter an integer value for n (where 2 < n < 8): "))

            #check that the value is inside the allowed interval
            if user_in < 3 or user_in > 7:
                raise ValueError("\nInput not in valid range.")
            
            #Only when user_in is an integer and is in the valid range does the break
            #end the loop
            break

        except ValueError:
            print("\nError:  Please enter integer using characters [3-7] only.")
        except KeyboardInterrupt:
            print("\nError: Please enter only numbers from (3, 4, 5, 6, or 7).")
    
    #upon receiving valid input, print confirmation message
    print(f"\nValid input received: {user_in}")
    return user_in

#--------------------------------
def query_rotation_axis():
    """
    Prompts user for the axis that the prism should be rotated about in the animation
    and checks that the input is valid before returning it.

    Returns character from {'x', 'y', 'z'}
    """
    valid = {'x', 'y', 'z'}
    while True:
        try:
            # query for choice of axis to rotate the model around, while removing
            # whitespaces and converting to lower case
            user_in = input("\nEnter choice of axis to rotate about (x, y, or z): ").strip().lower()

            # verify that a single character was entered and that it is a valid choice
            if len(user_in) != 1 or user_in not in valid:
                raise ValueError("\nInput is not a valid choice.")
        
            #Only when user_in is a single character and is an element in the array of valid choices 
            #(valid), end the loop
            break

        except ValueError:
            print("\nError: Please enter a single letter (x, y, or z).")
        except KeyboardInterrupt:
            print("\nError: Please enter only letters from (x, y, or z).")
    
    #upon receiving valid input, print confirmation message
    print(f"\nValid input received: {user_in}")
    return user_in