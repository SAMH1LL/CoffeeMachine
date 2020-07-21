import random


scores = {}
rating_file = open("rating.txt")
for line in rating_file:
    score = line.replace("\n", "").split(" ")
    scores[score[0]] = int(score[1])
rating_file.close()

your_name = input("Enter your name: ")
print("Hello, {}".format(your_name))

score = scores.get(your_name)
if score is None:
    score = 0

options_input = input()
if options_input == "":
    plays = ['rock', 'paper', 'scissors']
else:
    plays = options_input.split(",")

print("Okay, let's start")

user_pick = input()
while user_pick != "!exit":
    if user_pick not in plays and user_pick not in ["!exit", "!rating"]:
        print("Invalid input")
    else:
        computer_selection = random.choice(plays)

        if user_pick == "!rating":
            print("Your rating: {}".format(score))
        elif user_pick == computer_selection:
            score += 50
            print("There is a draw ({})".format(user_pick))
        else:
            half = (len(plays) - 1) // 2
            player_option_index = plays.index(user_pick)

            if player_option_index == len(plays) - 1:
                losers = plays[player_option_index + 1:]
            else:
                losers = plays[player_option_index + 1:player_option_index + 1 + half]
            if len(losers) != half:
                losers.extend(plays[0:half - len(losers)])

            if computer_selection in losers:
                print("Sorry, but computer chose {}".format(computer_selection))
            else:
                score += 100
                print("Well done. Computer chose {} and failed".format(computer_selection))

    user_pick = input()

print("Bye!")
