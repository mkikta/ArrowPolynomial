import gauss_code as gc
from sympy import init_printing, pprint

# Parse a string and convert it into a gauss code. Return None if the provided
# text is not a valid Gauss code.
def parse_input(text):
    codes = []
    
    # Parse each symbol in the text.
    for i in range(len(text)):
        
        # The first of every three symbols in the input should be an 'O' for
        # over or a 'U' for under.
        if i % 3 == 0:
            if text[i] == 'O':
                codes.append(gc.code(True, None, None))
            elif text[i] == 'U':
                codes.append(gc.code(False, None, None))
            else:
                return None
            
        # The second should be the label of the crossing.
        elif i % 3 == 1:
            codes[i // 3].number = text[i]
            
        # The third should be the sign of the crossing, '+' or '-'.
        else:
            if text[i] == '+':
                codes[i // 3].sign = True
            elif text[i] == '-':
                codes[i // 3].sign = False
            else:
                return None
            
    # Verify that the result is a valid Gauss code .
    res = gc.gauss_code(codes)
    if res.is_valid():
        return res
    return None

# Prompt the user for a gauss code or to quit. If they enter something invalid,
# prompt them again.
def prompt_user():
    
    # Prompt the user.
    print("Please enter a valid Gauss code (or \"quit\"):")
    text = input("> ")
    
    # Terminate the program if they quit.
    if text == "quit":
        print("Exiting...")
        return False
    
    # Otherwise determine if they entered a valid Gauss code, and act
    # accordingly.
    else:
        gc = parse_input(text)
        if gc is not None:
            pprint(gc.arrow_poly())
    return True

# Repeatedly prompt the user until they wish to exit.
def main():
    while (prompt_user()):
        pass

# Set up sympy printing and start the program.
init_printing()
main()
