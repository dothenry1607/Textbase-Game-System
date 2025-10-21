import time, os, sys
from msvcrt import kbhit, getch




#flushing
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.flush()

#pausing
def pause(msg: str = "\n[Press Enter to continue]"):
    input(msg)

#wait
def wait(sec):
    time.sleep(sec)

def start(func):
    if __name__ == "__main__":
        print("work")
        func()


def display(character: str, message: str, delay: float = 0.05, clear_after: bool = True):
    print(f"{character}: ")
    for i, ch in enumerate(message):
        if kbhit():
            key = getch()
            if key == b'\r':  
                print(message[i:], end="", flush=True)
                break
        print(ch, end="", flush=True)
        time.sleep(delay)

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



