import copy
import fileinput

# Represents an instance of the game
import random
import string


class Wordle:
    # Initializes state, opens file and puts words into an array
    def __init__(self):

        self.state = 0

        # opens the file in read mode
        fileObj = open("wordlist.txt", "r")

        # length is 12971
        # puts the file into an array
        self.word_list = fileObj.read().split("\",\"")
        fileObj.close()

        # solver instance
        self.solver = Solver(self.word_list, ['*', '*', '*', '*', '*'], "soare")

    def solve(self):
        print("solved state: {}".format(self.state))
        print(len(self.word_list))
        correct_word = input("put in correct word")

        # correct word is not valid
        if correct_word == "":
            print("wrong")
            # wrong
        # correct word is not valid
        else:
            # guess = input("put in guess")
            # g = Guess(guess)

            # Get a guess
            print("Put in a guess: ")
            g = self.solver.make_guess()

            g.print_word()
            turn = 1
            print("turn:", turn)

            # Loop while the guess is wrong and still within 6 guesses
            while not g.solved(correct_word) and turn < 6:
                g.get_correct_colors(correct_word)
                # ai does stuff
                if turn != 1:
                    g.print_word()
                g.print_colors()

                # append guess to list of previous guesses
                self.solver.guess_history.append(g)

                # guess = input("\nput in guess")
                # g = Guess(guess)

                # Get a guess
                print("Put in a guess: ")
                print("Before", len(self.solver.current_word_list))
                g = self.solver.make_guess()
                print("After", len(self.solver.current_word_list))
                turn = turn + 1
                print("turn:", turn)
            print("end")

        # get a guess - starter
        # while !solved
        # make a guess
        # get the colors
        # get new guess based on colors

class Guess:
    def __init__(self, word):
        self.word = [x for x in word] # initialize word to guessed word
        self.colors = ['*', '*', '*', '*', '*'] # initialize colors to all "Gray"

    def print_colors(self):
        print(self.colors)
        print("\n")

    def print_word(self):
        print(self.word)

    def solved(self, correct_word=""):
        if correct_word == "":
            print("get word from screen")
            # call other stuff
        else:
            for i in range(0, len(correct_word)):
                if (correct_word[i] != self.word[i]):
                    return False
            print("Correct word chosen!", correct_word)
            return True

    def get_correct_colors(self, correct_word=""):
        if correct_word == "":
            print("get word from screen")
            # call other stuff
        else:
            for i in range(0, len(correct_word)):
                if correct_word.__contains__(self.word[i]):
                    if self.word[i] == correct_word[i]:
                        self.colors[i] = "g"
                    else:
                        # match = [index for index, f in enumerate(self.word) if f in correct_word]
                        # print(match)
                        if self.colors[i] == "g":
                            self.colors[i] = "*"
                        else:
                            self.colors[i] = "y"


class Solver:
    def __init__(self, word_list, colors, guess_word):
        self.current_word_list = copy.deepcopy(word_list)
        self.colors = colors
        self.guess_word = guess_word
        self.guess_history = []

        # initialize values to 0 for all letter keys in dictionary
        self.letter_frequency = {}
        # categorize words by
        self.num_unique_letters = {1:0, 2:0, 3:0, 4:0, 5:0}
        alphabet_string = string.ascii_lowercase
        alphabet_list = list(alphabet_string)
        for letter in alphabet_list:
            self.letter_frequency.update({letter : 0})

    def search_word_list(self, word, colors):
        possible_words = []
        for i in range(0, self.current_word_list):
            # if word_list[i] matches the color and word criteria
            possible_words.append(self.current_word_list[i])
        return possible_words

    # calculates how many times each letter of the alphabet appears overall in the current word list
    def get_letter_frequency(self):
        for word in self.current_word_list:
            for letter in word:
                self.letter_frequency[letter] = self.letter_frequency.get(letter) + 1

    # finds how many unique letters are in a string and categorizes words accordingly
    def get_num_unique_letters(self):
        for word in self.current_word_list:
            s = set(word)
            num = len(s)
            self.num_unique_letters[num] = self.num_unique_letters.get(len(s)) + 1


    def guess_builder(self):
        first_letter = self.most_common_letter_at_index(0)

        possible_words = []
        for word in self.current_word_list:
            if word[0] == first_letter:
                possible_words.append(word)

        # not sure if this is really a smart way to do this
        second_letter = self.most_common_letter_at_index(1)
        for word in possible_words:
            if word[1] != second_letter and len(possible_words) != 1:
                possible_words.remove(word)

        guess_word = random.choice(possible_words)
        return guess_word


    # calculates how frequently each letter appears at a given index in the current word list
    # and returns the most common
    def most_common_letter_at_index(self, index):
        letter_frequency = {}
        alphabet_string = string.ascii_lowercase
        alphabet_list = list(alphabet_string)
        for letter in alphabet_list:
            letter_frequency.update({letter : 0})

        for word in self.current_word_list:
            letter = word[index]
            letter_frequency[letter] = letter_frequency.get(letter) + 1
        return max(zip(letter_frequency.values(), letter_frequency.keys()))[1]

    # gets the most common overall letter in the current word list
    def most_common_overall_letter(self):
        return max(zip(self.letter_frequency.values(), self.letter_frequency.keys()))[1]

    def make_guess(self):
        self.get_letter_frequency()
        self.get_num_unique_letters()

        # check if guess history is empty
        if self.guess_history:
            self.eliminate_words()
            self.guess_word = self.guess_builder()

        new_guess = Guess(self.guess_word)
        return new_guess

    # eliminates words from word list that are impossible given color feedback of a guess
    def eliminate_words(self):
        # get previous guess
        prev_guess = self.guess_history[-1]

        # list of letters not in correct word
        wrong_letters = []

        # list of letters in word, but in wrong position
        misplaced_letters = []

        #list of letters with correct position
        correct_letters = []

        # iterate through colors in previous guess
        for i in range(len(prev_guess.colors)):

            # append wrong letter to list
            if prev_guess.colors[i] == "*":
                wrong_letters.append(prev_guess.word[i])

            # append tuple of misplaced letter and index to list
            if prev_guess.colors[i] == 'y':
                misplaced_letters.append((prev_guess.word[i], i))

            # append tuple of correct letter and index to list
            if prev_guess.colors[i] == 'g':
                correct_letters.append((prev_guess.word[i], i))


        # get rid of all words containing wrong letters
        if wrong_letters:
            for letter in wrong_letters:
                # NOTE: make sure not to modify word list while iterating, so use [:]
                for word in self.current_word_list[:]:
                    if letter in word:
                        self.current_word_list.remove(word)

        # get rid of all words containing misplaced letter in wrong location
        if misplaced_letters:
            for letter_tuple in misplaced_letters:
                for word in self.current_word_list[:]:
                    letter = letter_tuple[0]
                    index = letter_tuple[1]

                    if word[index] == letter:
                        self.current_word_list.remove(word)

        # get rid of all words that don't have letter in correct place
        if correct_letters:
            for letter_tuple in correct_letters:
                for word in self.current_word_list[:]:
                    letter = letter_tuple[0]
                    index = letter_tuple[1]

                    if word[index] != letter:
                        self.current_word_list.remove(word)

if __name__ == '__main__':
    wordle = Wordle()
    wordle.solve()
