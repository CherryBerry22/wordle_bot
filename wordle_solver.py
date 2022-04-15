import fileinput

class Wordle:
    def __init__(self):
        self.state = 0
        fileObj = open("wordlist.txt", "r")  # opens the file in read mode
        # length is 12971
        self.word_list = fileObj.read().split("\",\"")  # puts the file into an array
        fileObj.close()


    def solve(self):
        print("solved state: {}".format(self.state))
        print(len(self.word_list))
        correct_word = input("put in correct word")
        if(correct_word == ""):
            print("wrong")
            # wrong
        else:
            guess = input("put in guess")
            g = Guess(guess)
            g.print_word()
            turn = 1
            while not g.solved(correct_word) and turn < 6:
                g.get_correct_colors(correct_word)
                #ai does stuff
                g.print_colors()
                guess = input("\nput in guess")
                g = Guess(guess)
                turn = turn + 1
            print("end")



        # get a guess - starter
        # while !solved
        # make a guess
        # get the colors
        # get new guess based on colors

class Guess:
    def __init__(self, word):
        self.word = [x for x in word]
        self.colors = ['n','n','n','n','n']

    def print_colors(self):
        print(self.colors)

    def print_word(self):
        print(self.word)

    def solved(self, correct_word=""):
        if correct_word == "":
            print("get word from screen")
            # call other stuff
        else:
            for i in range(0, len(correct_word)):
                if(correct_word[i] != self.word[i]):
                    return False
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
                        #match = [index for index, f in enumerate(self.word) if f in correct_word]
                        #print(match)
                        if self.word[i] == "g":
                            self.colors[i] = "n"
                        else:
                            self.colors[i] = "y"

class Solver:
    def __init__(self, word_list, colors, word):
        self.word = word
        self.colors = colors
        self.word_list = word_list

    def search_word_list(self,word,colors):
        possible_words = []
        for i in range(0,self.word_list):
            #if word_list[i] matches the color and word criteria
            possible_words.append(self.word_list[i])
        return possible_words

if __name__ == '__main__':
    wordle = Wordle()

    wordle.solve()
