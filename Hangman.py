import random

print("H A N G M A N")
words = ['python', 'java', 'kotlin', 'javascript']

word_to_guess = random.choice(words)
word_to_guess_hidden = []
word_to_check = set(word_to_guess)

for i in range(0, len(word_to_guess)):
    word_to_guess_hidden += "-"

while input("Type \"play\" to play the game, \"exit\" to quit:") == "play":
    misses = 0
    guesses = set()
    while misses != 8:
        print("\n" + "".join(word_to_guess_hidden))

        letter = input("Input a letter:")

        if len(letter) != 1:
            print("You should input a single letter")
        elif not letter.islower():
            print("It is not an ASCII lowercase letter")
        elif letter in guesses:
            print("You already typed this letter")
        else:
            guesses.add(letter)

            if letter in word_to_check:
                for i in range(0, len(word_to_guess)):
                    if word_to_guess[i] == letter:
                        word_to_guess_hidden[i] = letter

                if word_to_guess == "".join(word_to_guess_hidden):
                    print("You guessed the word!\nYou survived!\n")
                    break
            else:
                misses += 1
                print("No such letter in the word")

        if misses == 8:
            print("You are hanged!\n")
