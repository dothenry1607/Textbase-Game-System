from os import system, name
from time import sleep
from sys import stdout
from typing import Sequence


# simple day/night cycle; actions should call ``advance_time`` after each choice
_periods = ["morning", "afternoon", "evening", "night"]
_current_index = 0

def current_time() -> str:
    """Return current time-of-day (one of morning/afternoon/evening/night)."""
    return _periods[_current_index]


def advance_time() -> None:
    """Advance to the next period, wrapping to morning at the end."""
    global _current_index
    _current_index = (_current_index + 1) % len(_periods)


def reset_time() -> None:
    """Force the cycle back to morning (useful on sleep or new game)."""
    global _current_index
    _current_index = 0



# utility functions --------------------------------------------------------

def clear_screen() -> None:
    """Clear the terminal screen (cross-platform)."""
    system('cls' if name == 'nt' else 'clear')
    stdout.flush()


def pause(msg: str = "\n[Press Enter to continue]") -> None:
    """Wait for the user to press enter."""
    input(msg)


def wait(sec: float) -> None:
    """Sleep for ``sec`` seconds."""
    sleep(sec)


def run_sequence(*funcs) -> None:
    """Run a sequence of callables, ignoring any exceptions.

    This replaces the previous ``start`` helper and shields the caller from
    errors in the provided functions.
    """
    for func in funcs:
        try:
            func()
        except Exception:
            # silently ignore faulty callbacks
            pass


def display(character: str, message: str, delay: float = 0.02,
            clear_after: bool = True, pause_after: bool = True) -> None:
    """Print a message one character at a time like a typewriter.

    ``character`` is shown as the speaker name.  If ``pause_after`` is
    ``False`` the function will not wait for user input (useful in tests).
    """
    if character == "":
        print()
    else:
        print(f"{character}: ")
    for ch in message:
        print(ch, end="", flush=True)
        sleep(delay)
    print()
    if pause_after:
        pause()
    if clear_after:
        clear_screen()


# menu helpers -------------------------------------------------------------

def options(prompt: str, choices: Sequence[str]) -> int:
    """Display a numbered menu and return the selected 1-based index.

    ``prompt`` appears above the list of ``choices``.  Invalid inputs clear
    the screen and repeat until a valid number is entered.
    """
    while True:
        print(prompt)
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


def yes_no_prompt(prompt: str) -> bool:
    """Ask a yes/no question interactively.

    Returns ``True`` when the user selects yes, ``False`` for no.
    """
    while True:
        user_input = input(f"{prompt} (y/n)\n> ").strip().lower()
        if user_input in ('y', 'yes'):
            return True
        if user_input in ('n', 'no'):
            return False
        print("Invalid input. Please enter 'y' or 'n'.\n")
        pause()


def get_input(prompt: str) -> str:
    """Prompt the user and return the trimmed response."""
    return input(f"{prompt}\n> ").strip()


def get_number_input(prompt: str) -> int:
    """Prompt until a valid integer is entered and return it."""
    while True:
        user_input = input(f"{prompt}\n> ").strip()
        if user_input.isdigit():
            return int(user_input)
        print("Invalid input. Please enter a valid number.\n")
        pause()
