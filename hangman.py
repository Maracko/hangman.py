import json
import random
import string
from math import floor
from collections import defaultdict
from typing import Tuple


def select_secret() -> str:
    """Will select a random word from dict"""
    secret = ""
    with open("words_dictionary.json") as f:
        wordsDict: "dict[str, int]" = json.load(f)
    while len(secret) <= 5:
        secret = random.choice(list(wordsDict.keys()))
    return secret


def set_difficulty() -> int:
    """Sets the difficulty"""
    while True:
        difficulty = input("Enter 1 for normal difficulty, 2 for hard: ")
        try:
            difficulty = int(difficulty)
        except:
            print("Invalid input")
            continue
        if difficulty == 1:
            return 1
        elif difficulty == 2:
            return 2
        else:
            print("Invalid input")


def set_lives(difficulty) -> int:
    """Sets the lives variable based on difficulty"""
    return 10 if difficulty == 1 else 5


def show_status(guessed: "defaultdict[str, int]", lives: int, secret: str) -> None:
    """Draws the currently guessed letters"""
    for letter in secret:
        if letter in guessed.keys():
            print(letter, end=" ")
        else:
            print("_", end=" ")
    print("\n")
    print("Lives: {}\n".format(lives))


def guess(guessed: "defaultdict[str, int]", secret: str) -> int:
    """Prompts the user to guess a new letter"""
    guess = input("Enter your guess: ").lower()
    if len(guess) > 1 or guess not in string.ascii_letters:
        print("\nPlease enter only one letter!\n")
        return 0
    elif guess in guessed.keys():
        print("\nPlease enter a letter which you haven't guessed yet.\n")
        return 0
    guessed[guess] += 1
    if guess not in secret:
        return -1
    else:
        return 0


def is_win(secret: str, guessed: "defaultdict[str, int]") -> bool:
    """Checks if the user has won"""
    return set(secret).issubset(set(guessed.keys()))


def game_over(lives: int, secret: str, difficulty: int) -> None:
    """Game over screen"""
    print(hangman(lives, difficulty))
    print("Out of lives, better luck next time!")
    print("Correct answer was: ", end="")
    for letter in secret:
        print(letter, end=" ")
    print("\n")


def play_again() -> bool:
    """Returns wether the user wants to play again"""
    print("Do you want to play again?")
    while True:
        play = input("Please enter Y/N: ")
        if play.lower() in ["y", "n"]:
            if play.lower() == "y":
                return True
            elif play.lower() == "n":
                print("Thank you for playing!")
                return False
        else:
            print("Invalid input")


def reset() -> Tuple[int, str, "defaultdict[str, int]"]:
    """Resets the game"""
    difficulty: int = set_difficulty()
    secret: str = select_secret()
    guessed: "defaultdict[str, int]" = defaultdict(lambda: 0)
    return difficulty, secret, guessed


def hangman(lives: int, difficulty: int) -> str:
    """Returns the art based on the current ammount of lives"""
    hangman = [
        """
        _______
        |/      
        |      
        |      
        |       
        |      
        |
       _|___
        """,
        """
        _______
        |/      |
        |      
        |      
        |       
        |      
        |
       _|___
        """,
        """
        _______
        |/      |
        |      (_)
        |      
        |      
        |     
        |
       _|___
        """,
        """
        _______
        |/      |
        |      (_)
        |      \\|/
        |       
        |      
        |
       _|___
        """,
        """
        _______
        |/      |
        |      (_)
        |      \\|/
        |       |
        |     
        |
       _|___
        """,
        """
        _______
        |/      |
        |      (_)
        |      \\|/
        |       |
        |      / \\
        |
       _|___
        """,
    ]
    return hangman[-floor(lives / 2) - 1] if difficulty == 1 else hangman[-lives - 1]


def main() -> None:
    """Main function"""
    print("Welcome to hangman.py!\n")
    difficulty, secret, guessed = reset()
    lives = set_lives(difficulty)
    print("Word to guess is {} letters long!".format(len(secret)))
    while True:
        print(hangman(lives, difficulty))
        show_status(guessed, lives, secret)
        lives += guess(guessed, secret)
        if is_win(secret, guessed):
            print("\nCongratulations,you won!!!\n")
            print("The secret was: ", end="")
            for letter in secret:
                print(letter, end=" ")
            print("\n")
            if play_again():
                difficulty, secret, guessed = reset()
                lives = set_lives(difficulty)
                print("Word to guess is {} letters long!\n".format(len(secret)))
            break
        elif lives == 0:
            game_over(lives, secret, difficulty)
            if play_again():
                difficulty, secret, guessed = reset()
                lives = set_lives(difficulty)
                print("Word to guess is {} letters long!\n".format(len(secret)))
            break


if __name__ == "__main__":
    main()