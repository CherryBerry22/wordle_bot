class Wordle:
    def __init__(self):
        self.state = 0

    def solve(self):
        print("solved state: {}".format(self.state))


if __name__ == '__main__':
    wordle = Wordle()

    wordle.solve()