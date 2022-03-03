# CS 445 Final Programming Project:
# Monte Carlo Tree Search in Tic Tac Toe
# Written by Jack Sherman


import random
from algorithm import *
import matplotlib.pyplot as plt


class Game:
    def __init__(self):
        self.gamestate = []
        self.playerturn = False
        self.botturn = True
        self.init_board()

    def turns(self):
        while self.check_end() == 0:
            y = input("Enter your position to place a piece: ")
            self.move(int(y))
            self.print_game()
            print("valid moves: ", self.valid_moves())
        if self.check_end() == 2:
            ending = "Win"
        else:
            ending = "Draw"
        print("Game ended: ", ending)

# initialize the game by creating an array with 9 indices. Each index will correspond to a cell in the game
# each cell can contain a x or an o, depending on the move made by the algorithm
    def init_board(self):
        for y in range(9):
            self.gamestate.append("-")

    def move(self, place):
        # decided to make the algorithm always play as x, because it doesnt really matter
        if self.botturn:
            if self.gamestate[place] == "-":
                self.gamestate[place] = "x"
            else:
                print("Invalid move, already a symbol there. \n")
                return
        if self.playerturn:
            if self.gamestate[place] == "-":
                self.gamestate[place] = "o"
            else:
                print("Invalid move, already a symbol there. \n")
                return
        self.playerturn = not self.playerturn
        self.botturn = not self.botturn

# function used to print out a board. Only really useful for debugging or if a user wants to play the algorithm
    def print_game(self):
        index = 0
        for row in range(3):
            print(self.gamestate[(row*3)], self.gamestate[(row*3)+1], self.gamestate[(row*3)+2])

    def check_end(self):
        if self.check_win():
            return 2
        if self.check_draw():
            return 1
        return 0

# function will be used to check if the game has either resulted in a draw or a win for either player
    def check_win(self):
        a = self.gamestate
        # check horizontal
        if a[0] == a[1] and a[1] == a[2] and (not a[0] == "-"):
            return True
        if a[3] == a[4] and a[4] == a[5] and (not a[3] == "-"):
            return True
        if a[6] == a[7] and a[7] == a[8] and (not a[6] == "-"):
            return True
        # check vertical
        if a[0] == a[3] and a[3] == a[6] and (not a[0] == "-"):
            return True
        if a[1] == a[4] and a[4] == a[7] and (not a[1] == "-"):
            return True
        if a[2] == a[5] and a[5] == a[8] and (not a[2] == "-"):
            return True
        # check diagonals
        if a[0] == a[4] and a[4] == a[8] and (not a[0] == "-"):
            return True
        if a[2] == a[4] and a[4] == a[6] and (not a[2] == "-"):
            return True
        return False

    def check_draw(self):
        a = self.gamestate
        for i in range(9):
            if a[i] == "-":
                return False
        return True

    def valid_moves(self):
        moves = []
        for i in range(9):
            if self.gamestate[i] == "-":
                moves.append(i)
        return moves


if __name__ == '__main__':
    botwin = 0
    turns = []
    turnarr = []
    resultswin = []
    resultsdraw = []
    numgames = 500
    iterations = 15
    constant = 1
    botdraw = 0
    for games in range(numgames):
        game = Game()
        turn = 0
        monteCarlo1 = MonteCarlo(iterations, constant)
        while game.check_end() is 0:
            x = monteCarlo1.find_best(game)
            game.move(x)
            if game.check_end() == 0:
                y = random.choice(game.valid_moves())
                game.move(int(y))
            elif game.check_end() == 1:
                botdraw += 1
            else:
                botwin += 1
            turn += 1
        resultswin.append(botwin/(games+1))
        resultsdraw.append(botdraw/(games+1))
        turns.append(turn)
        turnarr.append(games+1)
    print("Results win: ", resultswin, len(resultsdraw), len(turns))
    plt.figure()
    plt.plot(turnarr, resultswin, label="Win rate")
    plt.xlabel('Game')
    plt.plot(turnarr, resultsdraw, label="Draw rate")
    plt.ylabel('Rate')
    ttl = "Graph of win rate and draw rate. \n Iterations: " + str(iterations) + " Constant: " + str(constant) + \
          " \n Total loss rate = " + str((1-((botwin+botdraw)/numgames))*100) + "%" + "\n Average number of turns: " + str(sum(turns)/len(turns))
    plt.title(ttl)
    plt.legend()
    plt.show()
    print("Number of games the bot won: ", botwin, " out of ", numgames)
    print("Number of games the bot drew: ", botdraw)
    print("Games: ", turnarr)
    print("Average number of turns: ", sum(turns) / len(turns))



