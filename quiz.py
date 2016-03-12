#!/usr/bin/env python3

import cmd
import colorama
import glob
import os
import random

DATA_DIRECTORY="data/"

def show_image(file_name):
    os.system("display \"" + file_name + "\" &")

def show_random_photo(directory):
    photo = random.choice(glob.glob(directory + "/*.jpg"))
    show_image(photo)

def killall_display():
    os.system("killall display 2> /dev/null")

class Quiz(cmd.Cmd):
    def __init__(self):
        super(Quiz, self).__init__()
        self.init()

    def init(self):
        directories=glob.glob(DATA_DIRECTORY + "/*")

        self.guessing_bird = ""

        self.birds = []
        for directory in directories:
            self.birds.append(directory.split("/")[-1])

        colorama.init(autoreset=True)

        self.correct_answers = 0
        self.incorrect_answers = 0

        self.update_prompt()
        
        killall_display()

    def play(self, intro=None):
        killall_display()
        self.guessing_bird = random.choice(glob.glob(DATA_DIRECTORY + "/*")).split("/")[-1]
        show_random_photo(DATA_DIRECTORY + "/" + self.guessing_bird)

    def do_start(self, arg):
        self.play()

    def do_a(self, guess):
        if guess == self.guessing_bird:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "CORRECT!")
            self.correct_answers += 1
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + "INCORRECT!" + " was:", self.guessing_bird)
            self.incorrect_answers += 1

        self.play()
        self.update_prompt()

    def complete_a(self, text, line, begidx, endidx):
        if not text:
            completions = self.birds[:]
        else:
            completions = [f
                           for f in self.birds
                           if f.startswith(text)
                           ]

        return completions
    
    def do_stats(self, line):
        if self.correct_answers + self.incorrect_answers == 0:
            print("Practise before checking the stats")
        else:
            total=self.correct_answers+self.incorrect_answers
            print("Correct answers: {}".format(self.correct_answers))
            print("Total answers:   {}".format(total))
            print("Success rate:    {:.0f}%".format((self.correct_answers / total)*100))

    def do_reset(self, line):
        self.init()

    def do_birds(self, line):
        print("Possible birds:")
        for bird in self.birds:
            print(" {}".format(bird))

    def update_prompt(self):
        total = self.correct_answers + self.incorrect_answers
        if total == 0:
            self.prompt = "0 0 0%"
        else:
            percentage = (self.correct_answers / total) * 100
            self.prompt = "{}/{} {:.0f}%".format(self.correct_answers, total, percentage)

        self.prompt += " "

    def do_EOF(self, line):
        return True

if __name__ == "__main__":
    Quiz().cmdloop()
