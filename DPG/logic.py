from os import system, name
from time import sleep
from sys import stdout





#flushing
def clear_screen():
    system('cls' if name == 'nt' else 'clear')
    stdout.flush()

#pausing
def pause(msg: str = "\n[Press Enter to continue]"):
    input(msg)

#wait
def wait(sec):
    sleep(sec)

#when start func
def start(*functions):
    for func in functions:
        try:
            func()
        except Exception:
            print("Error, this code will pass.")
            pass

#Display message
def display(character: str, message: str, delay: float = 0.02, clear_after: bool = True):
    print(f"{character}: ")
    for ch in (message):
        print(ch, end="", flush=True)
        sleep(delay)

    print() 
    pause()

    if clear_after:
        clear_screen()

#input 2 options
def two_options_with_resultance(character : str,
                option1: str,
                option2: str,
                solution1: str,
                solution2: str,
                breaknum: int = 2,
                ) -> int:
    while True:
        print(f"{character}")
        print(f"[1] {option1}")
        print(f"[2] {option2}")
        user_answer = input("> ").strip()

        if user_answer == "1":
            display(character, solution1)
            return 1

        elif user_answer == "2":
            display(character, solution2)
            if breaknum == 2:
                return 2
        else:
            print("Invalid input. Please enter 1 or 2.\n")
            pause()
            clear_screen()



def options(character : str, *choices: str) -> int:
    while True:
        print(f"{character}")
        for i, choice in enumerate(choices, 1):
            print(f"[{i}] {choice}")
        user_answer = input("> ").strip()

        if user_answer.isdigit():
            idx = int(user_answer)
            if 1 <= idx <= len(choices):
                return idx

        print(f"Invalid input. Please enter a number between 1 and {len(choices)}.\n")
        pause()
        clear_screen()

def get_input(prompt: str) -> str:
    return input(f"{prompt}\n> ").strip()

def get_number_input(prompt: str) -> int:
    while True:
        user_input = input(f"{prompt}\n> ").strip()
        if user_input.isdigit():
            return int(user_input)
        print("Invalid input. Please enter a valid number.\n")

def yes_no_prompt(prompt: str) -> bool:
    while True:
        user_input = input(f"{prompt} (y/n)\n> ").strip().lower()
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        print("Invalid input. Please enter 'y' or 'n'.\n")


        
