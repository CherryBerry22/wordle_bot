import copy
import math
import time
import random
import string
from collections import defaultdict

from screen_reader import ScreenReader


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

        fileObj2 = open("puzzlewords.txt", "r")

        self.puzzle_word_list = fileObj2.read().split("\", \"")

        # solver instance
        #self.solver = Solver(self.word_list, ['*', '*', '*', '*', '*'], "soare")
        self.solver = Solver(self.puzzle_word_list, ['*', '*', '*', '*', '*'], "soare")

    def split(word):
        return [char for char in word]

    def solve(self):

        manual = input('would you like to do (M)anual, (T)esting, or (A)uto?\n')
        if manual.upper() == 'A':
            self.auto()
        elif manual.upper() == 'T':
            self.testing()
        else:
            self.manual()

    def testing(self):
        start_word = input('provide a starting word \n'
                           '(testing can take up to five minutes, python and our algorithm are slow :) )')

        not_solved_list = []
        times_played = 0
        total_turns = 0
        number_solved = 0
        for secret_word in self.puzzle_word_list:
            self.solver = Solver(self.puzzle_word_list, ['*', '*', '*', '*', '*'], start_word)
            guess = Guess(start_word)
            self.solver.guess_history.append(guess)
            turn = 1
            guess.colors = create_pattern(secret_word, guess.word_string)
            while not guess.solved() and turn < 6:
                guess = self.solver.make_guess()
                self.solver.guess_history.append(guess)
                guess.colors = create_pattern(secret_word, guess.word_string)
                turn += 1
            times_played += 1
            total_turns += turn
            if guess.solved():
                number_solved += 1
                #print('Solved!')
            else:
                not_solved_list.append((secret_word, self.solver.guess_history, self.solver.current_word_list))
                #print('Not solved :(')
            # print('{0} in {1} turns\n'
            #        'Games Played: {2}\nAvg Turns: {3}\n'
            #        'Number solved: {4}\nSolve Rate: {5}'.format(secret_word, turn, times_played,
            #                                                     total_turns/times_played,number_solved,
            #                                                     number_solved/times_played))
        print('Games Played: {0}\nAvg Turns: {1}\n'
              'Number solved: {2}\nSolve Rate: {3}'.format(times_played,
                                                           total_turns/times_played,number_solved,
                                                           number_solved/times_played))
        for word in not_solved_list:
            print('unable to solve {0} with these guesses:'.format(word[0]))
            for g in word[1]:
                print(g.word_string, g.colors)
            print('remaining word list: {0}'.format(word[2]))

    def auto(self):
        reader = ScreenReader()
        unlimited = input("keep replaying? y/n (only for wordle unlimited)")
        if unlimited.upper() == 'Y':
            self.replay(reader)
        else:
            g = self.solver.make_guess()
            turn = 1
            reader.input_guess(g, turn)
            while not g.solved() and turn < 6:
                g.colors = reader.get_colors(turn)
                if not g.solved():
                    self.solver.guess_history.append(g)
                    g = self.solver.make_guess()
                    turn = turn + 1
                    reader.input_guess(g, turn)

            if g.solved():
                print('Word was {0}'.format(g.word))
            else:
                print('Unable to solve :(')

    def replay(self, reader):

        times_played = 0
        total_turns = 0
        number_solved = 0
        while(times_played < 3000):
            # start a game
            g = self.solver.make_guess()
            turn = 1
            reader.input_guess(g, turn)
            while not g.solved() and turn < 6:
                g.colors = reader.get_colors(turn)
                if not g.solved():
                    self.solver.guess_history.append(g)
                    g = self.solver.make_guess()
                    turn = turn + 1
                    reader.input_guess(g, turn)
                    g.colors = reader.get_colors(turn)
            #end game
            times_played += 1
            total_turns += turn
            if g.solved():
                print('Word was {0}'.format(g.word))
                number_solved += 1
            else:
                print('Unable to solve :(')
            print('\nGames Played: {0}\nAvg Turns: {1}\n'.format(times_played, total_turns/times_played))
            print('Number solved: {0}\nSolve Rate: {1}'.format(number_solved, number_solved/times_played))
            self.solver = Solver(self.puzzle_word_list, ['*', '*', '*', '*', '*'], "soare")
            time.sleep(3)
            reader.click_replay()
            time.sleep(1.5)

    def manual(self):

        # Get a guess
        print("Try guessing: ")
        g = self.solver.make_guess()

        g.print_word()
        turn = 1
        print("turn:", turn)

        # Loop while the guess is wrong and still within 6 guesses
        while not g.solved() and turn < 6:
            g.colors = list(input("Please input the colors returned"))

            if (g.solved()):
                print("Yay!")
                return

            if turn != 1:
                g.print_word()
            g.print_colors()

            # append guess to list of previous guesses
            self.solver.guess_history.append(g)

            # guess = input("\nput in guess")
            # g = Guess(guess)

            print("Before", len(self.solver.current_word_list))
            g = self.solver.make_guess()
            print("After", len(self.solver.current_word_list))
            turn = turn + 1
            print("turn:", turn)

            print("please make this guess:")
            g.print_word()
        print("end")


class Guess:
    def __init__(self, word):
        self.word = [x for x in word]  # initialize word to guessed word
        self.colors = ['*', '*', '*', '*', '*']  # initialize colors to all "Gray"
        self.word_string = ''
        for letter in word:
            self.word_string += letter

    def print_colors(self):
        print(self.colors)
        print("\n")

    def print_word(self):
        print(self.word)

    def solved(self):
        for i in range(0, len(self.colors)):
            if self.colors[i].upper() != 'G':
                return False
        # print("Correct word chosen!")
        return True


class Solver:
    def __init__(self, word_list, colors, guess_word):
        self.current_word_list = copy.deepcopy(word_list)
        self.colors = colors
        self.guess_word = guess_word
        self.guess_history = []
        self.letter_scores = {
            'a': 43.31, 'b': 10.56, 'c': 23.13, 'd': 17.25, 'e': 56.88, 'f': 9.24,
            'g': 12.59, 'h': 15.31, 'i': 38.45, 'j': 1.00, 'k': 5.61, 'l': 27.98,
            'm': 15.36, 'n': 33.92, 'o': 36.41, 'p': 16.14, 'q': 1.00, 'r': 38.64,
            's': 29.23, 't': 35.43, 'u': 18.51, 'v': 5.13, 'w': 6.57, 'x': 1.48,
            'y': 9.06, 'z': 1.39
        }

        # initialize values to 0 for all letter keys in dictionary
        self.letter_frequency = {}
        # categorize words by
        self.num_unique_letters = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        alphabet_string = string.ascii_lowercase
        alphabet_list = list(alphabet_string)
        for letter in alphabet_list:
            self.letter_frequency.update({letter: 0})

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
       # second_letter = self.most_common_letter_at_index(1)
       # for word in possible_words:
       #     if word[1] != second_letter and len(possible_words) != 1:
       #         possible_words.remove(word)

        guess_word = random.choice(possible_words)
       # current_word_scores = self.calculate_word_scores(possible_words)
       # guess_word = max(zip(current_word_scores.values(), current_word_scores.keys()))[1]
       # print("This word has a score of ", current_word_scores[guess_word])
        return guess_word

    # calculates how frequently each letter appears at a given index in the current word list
    # and returns the most common
    def most_common_letter_at_index(self, index):
        letter_frequency = {}
        alphabet_string = string.ascii_lowercase
        alphabet_list = list(alphabet_string)
        for letter in alphabet_list:
            letter_frequency.update({letter: 0})

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
            new_guess = Guess(self.choose_optimal_word_entropy())
        else:
            new_guess = Guess(self.guess_word)

        return new_guess

    # eliminates words from word list that are impossible given color feedback of a guess
    def eliminate_words(self):
        # get previous guess
        prev_guess = self.guess_history[len(self.guess_history) - 1]

        # remove last guess
        if prev_guess.word_string in self.current_word_list:
            self.current_word_list.remove(prev_guess.word_string)

        # list of letters not in correct word
        wrong_letters = []
        wrong_letters_specific_spot = []

        # list of letters in word, but in wrong position
        misplaced_letters = []

        # list of letters with correct position
        correct_letters = []
        # list of correct letters and misplaced letters to make sure they are accounted for
        letters_in_answer = []


        # needed to not get rid of double letters
        # example, answer is HUMOR and previous guess is RUMOR
        # color pattern would be *gggg meaning first R would be grey and second R is green
        # we don't want to remove words with any R like HUMOR
        # so we keep it out of the wrong letters
        for j in range(len(prev_guess.colors)):
            if prev_guess.colors[j].upper() == 'Y' or prev_guess.colors[j].upper() == 'G':
                letters_in_answer.append(prev_guess.word[j])



        # iterate through colors in previous guess
        for i in range(len(prev_guess.colors)):

            # append tuple of correct letter and index to list
            if prev_guess.colors[i].upper() == 'G':
                correct_letters.append((prev_guess.word[i], i))

            # append tuple of misplaced letter and index to list
            if prev_guess.colors[i].upper() == 'Y':
                misplaced_letters.append((prev_guess.word[i], i))

            # append wrong letter to list
            if prev_guess.colors[i] == "*":
                # append letter to wrong list if its not second occurrence of a misplaced or correct letter in the word
                if prev_guess.word[i] not in letters_in_answer:
                    wrong_letters.append(prev_guess.word[i])
                else:
                    wrong_letters_specific_spot.append((prev_guess.word[i], i))


        # get rid of all words containing wrong letters
        if wrong_letters or wrong_letters_specific_spot:
            for letter in wrong_letters:
                # NOTE: make sure not to modify word list while iterating, so use [:]
                for word in self.current_word_list[:]:
                    if letter in word:
                        self.current_word_list.remove(word)
            # trim words like WITTY, BITTY, etc if the word is FIFTY
            for letter_tuple in wrong_letters_specific_spot:
                for word in self.current_word_list[:]:
                    letter = letter_tuple[0]
                    index = letter_tuple[1]

                    if word[index] == letter:
                        self.current_word_list.remove(word)

        # get rid of all words containing misplaced letter in wrong location
        if misplaced_letters:
           # get rid of all words that dont have the misplaced letter anywhere
            for letter in misplaced_letters:
                for word in self.current_word_list[:]:
                    if letter[0] not in word:
                        self.current_word_list.remove(word)

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

    def choose_optimal_word_entropy(self):
        frequencies = self.calculate_entropy_for_all()
        return frequencies[0][0]

    def calculate_entropy(self, word):
        dict_len = len(self.current_word_list)
        prob_of_patterns = defaultdict(int)

        for if_answer in self.current_word_list:
            pattern = create_pattern(if_answer, word)
            prob_of_patterns[pattern] += 1.0 / dict_len

        information_gain = -1 * sum([probability * math.log(probability) for probability in prob_of_patterns.values()])
        return information_gain

    def calculate_entropy_for_all(self):
        gains = [(word, self.calculate_entropy(word)) for word in self.current_word_list]
        return sorted(gains, key=lambda x: x[1], reverse=True)


def create_pattern(answer, guessed_word):

    green_occurrences = defaultdict(int)
    for s, g in zip(answer, guessed_word):
        if s == g:
            green_occurrences[g] += 1

    occurrences = defaultdict(int)
    pattern = ''
    for s, g in zip(answer, guessed_word):
        if s == g:
            pattern += 'g'
        else:
            square = 'y' if g in answer and occurrences[g] < answer.count(g) - \
                                      green_occurrences[g] else '*'
            pattern += square
            occurrences[g] += 1

    return pattern

if __name__ == '__main__':
    wordle = Wordle()
    wordle.solve()

