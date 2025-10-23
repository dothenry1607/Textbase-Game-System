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
def display(character: str, message: str, delay: float = 0.05, clear_after: bool = True):
    print(f"{character}: ")
    for ch in (message):
        print(ch, end="", flush=True)
        sleep(delay)

    print() 
    pause()

    if clear_after:
        clear_screen()

#input 2 options
def two_options(character : str,
                option1: str,
                option2: str,
                solution1: str,
                solution2: str,
                breaknum: int = 2,
                ) -> int:
    while True:
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




