from math import ceil
from random import gauss, randint, triangular
import sys
from os import system, name
from time import sleep
from colorama import init, Fore, Back

init(autoreset=True)

TIME_DELAY = 1.5
"""
The time delay in seconds between displaying information about
a guess and deleting it off the screen.
"""

keyboard_colours = {}


def reset_keyboard_colours():
    global keyboard_colours
    keyboard_colours = {
        letter: Back.WHITE + Fore.BLACK for letter in "qwertyuiopasdfghjklzxcvbnm"
    }


def delete_last_n_lines(n):
    """
    Deletes the last n lines in the STDOUT.
    """

    for _ in range(n):
        # cursor up one line
        sys.stdout.write("\x1b[1A")

        # delete last line
        sys.stdout.write("\x1b[2K")


def clear_output():
    """
    Clears STDOUT
    """
    # For windows
    if name == "nt":
        _ = system("cls")

    # For mac and linux (here, os.name is 'posix')
    else:
        _ = system("clear")


def choose_random_word():
    """
    Returns a random 5-letter word.
    """
    TOTAL_WORDS = 5757
    with open("5-letter-words.txt", "r") as f:
        # line = randint(1, TOTAL_WORDS)  # [1, TOTAL_WORDS]
        # line = ceil(triangular(0, TOTAL_WORDS, 0))
        line = min(ceil(abs(gauss(0, TOTAL_WORDS / 3))), TOTAL_WORDS)

        for _ in range(line - 1):
            f.readline()

        return f.readline().replace("\n", "")


def is_real_word(guess):
    """
    Checks if the guess is a real word, i.e. if it is in the
    "5-letter-words.txt" file.
    """
    with open("5-letter-words.txt", "r") as f:
        for line in f:
            word = line.replace("\n", "")
            if guess == word:
                return True

        return False


def display_coloured_keyboard():
    """
    Displays the keyboard with the colours for each letter
    """
    row_1_out = ""
    for letter in "qwertyuiop":
        row_1_out += keyboard_colours[letter] + letter
    print(row_1_out)

    row_2_out = ""
    for letter in "asdfghjkl":
        row_2_out += keyboard_colours[letter] + letter
    print(" " + row_2_out)

    row_3_out = ""
    for letter in "zxcvbnm":
        row_3_out += keyboard_colours[letter] + letter
    print("  " + row_3_out)


def get_valid_guess(guess_number):
    """
    Gets a valid, 5-letter guess from the user. Also displays coloured
    keyboard and deletes lines from output to not clutter it.
    """
    print(f"\nGuess a word. This is guess {guess_number} out of 6")
    display_coloured_keyboard()

    while True:
        guess = input()

        if not guess.isalpha():
            print("Letters only")
            sleep(TIME_DELAY)

        elif len(guess) != 5:
            print("Must be a 5 letter word")
            sleep(TIME_DELAY)

        elif not is_real_word(guess):
            print("Not a real word")
            sleep(TIME_DELAY)

        else:
            delete_last_n_lines(6)
            return guess.lower().replace("\n", "")

        delete_last_n_lines(2)


def display_colours_and_update_keyboard(word, guess):
    """
    Displays the colours of the letters for the guess, and updates
    the colours for the keyboard
    """
    possible_letters = list(word)
    out_letters = [""] * 5
    letters_handled = [False] * 5

    for i in range(5):
        if guess[i] == word[i]:
            letters_handled[i] = True

            out_letters[i] = Back.GREEN + Fore.BLACK + guess[i]
            keyboard_colours[guess[i]] = Back.GREEN + Fore.BLACK

            possible_letters.remove(guess[i])

    for i in range(5):
        if guess[i] in possible_letters and not letters_handled[i]:
            letters_handled[i] = True
            out_letters[i] = Back.YELLOW + Fore.BLACK + guess[i]

            keyboard_colours[guess[i]] = Back.YELLOW + Fore.BLACK
            possible_letters.remove(guess[i])

    for i in range(5):
        if not letters_handled[i]:
            letters_handled[i] = True

            out_letters[i] = Back.BLACK + Fore.WHITE + guess[i]
            keyboard_colours[guess[i]] = Back.BLACK + Fore.WHITE

    out = ""
    for letter in out_letters:
        out += letter
    print(out)


def get_play_again():
    while True:
        again = input("Play again (y/n)? ").lower()
        if again == "y":
            return True
        elif again == "n":
            return False
        else:
            print("y or n only")
            sleep(TIME_DELAY)
            delete_last_n_lines(2)


def main():
    clear_output()
    while True:
        print("\nWORDLE\n")

        reset_keyboard_colours()

        word = choose_random_word()

        win = False

        for guess_number in range(1, 6 + 1):
            guess = get_valid_guess(guess_number)

            display_colours_and_update_keyboard(word, guess)

            if guess == word:
                win = True
                break

        print()

        if win:
            print(f"WIN in {guess_number} guesses\n")
        else:
            print(f"TOO BAD Word was {word}\n")

        again = get_play_again()

        if again:
            clear_output()
        else:
            break


if __name__ == "__main__":
    main()
