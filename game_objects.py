from minimax_calc import *


class C4_Game(object):
    users = [None, None]
    user_turn = None
    grid = None
    winner = None
    tokens = ["r", "b"]
    curr_iteration = None
    is_over = None
    
    def __init__(self):
        self.grid = []
        self.winner = None
        self.curr_iteration = 1
        self.is_over = False

        print("Please start by creating users for the game")
        print("Is the first user a person or computer player?")
        while self.users[0] is None:
            user_input = str(input("Type P for person or C for computer: "))
            name = "User1"
            if user_input == "P":
                self.users[0] = Person(name, self.tokens[0])
            elif user_input == "C":
                self.users[0] = Computer(name, self.tokens[0])
            else:
                print("Input was not correct format")

        print("Is the second user a person or computer player?")
        while self.users[1] is None:
            user_input = str(input("Type P for person or C for computer: "))
            name = "User2"
            if user_input == "P":
                self.users[1] = Person(name, self.tokens[1])
            elif user_input == "C":
                self.users[1] = Computer(name, self.tokens[1])
            else:
                print("Input was not correct format")
        
        print("Which player will go first?")
        first_player = int(input("Enter '0' for User1 or '1' for User2: "))
        self.user_turn = self.users[first_player]

        for i in range(6):
            self.grid.append([])
            for j in range(7):
                self.grid[i].append(' ')

    def change_iteration(self):
        iter_dict = {0: 1, 1: 0}
        if self.user_turn == self.users[0]:
            self.user_turn = self.users[iter_dict[0]]
        else:
            self.user_turn = self.users[iter_dict[1]]
        self.curr_iteration += 1

    def place_token(self):
        player = self.user_turn

        col_choice = player.col_choice(self.grid)

        for i in range(6):
            if self.grid[i][col_choice] == ' ':
                self.grid[i][col_choice] = player.color
                self.change_iteration()
                self.checkForFours()
                self.print_grid()
                return

        print("Invalid move (column is full)")
        return

    def checkForFours(self):
        for i in range(6):
            for j in range(7):
                if self.grid[i][j] != ' ':
                    if self.verticalCheck(i, j):
                        self.is_over = True
                        return

                    if self.horizontalCheck(i, j):
                        self.is_over = True
                        return

                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.is_over = True
                        return

    def verticalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0

        for i in range(row, 6):
            if self.grid[i][col].lower() == self.grid[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.users[0].color.lower() == self.grid[row][col].lower():
                self.winner = self.users[0]
            else:
                self.winner = self.users[1]

        return fourInARow

    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0

        for j in range(col, 7):
            if self.grid[row][j].lower() == self.grid[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.users[0].color.lower() == self.grid[row][col].lower():
                self.winner = self.users[0]
            else:
                self.winner = self.users[1]

        return fourInARow

    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.grid[i][j].lower() == self.grid[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.users[0].color.lower() == self.grid[row][col].lower():
                self.winner = self.users[0]
            else:
                self.winner = self.users[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.grid[i][j].lower() == self.grid[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.users[0].color.lower() == self.grid[row][col].lower():
                self.winner = self.users[0]
            else:
                self.winner = self.users[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope

    def check_for_win(self):
        for i in range(6):
            for j in range(7):
                if self.grid[i][j] != ' ':
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')

                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')

                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)

    def highlightFour(self, row, col, direction, slope=None):
        if direction == 'vertical':
            for i in range(4):
                self.grid[row + i][col] = self.grid[row + i][col].upper()

        elif direction == 'horizontal':
            for i in range(4):
                self.grid[row][col + i] = self.grid[row][col + i].upper()

        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.grid[row + i][col + i] = self.grid[row + i][col + i].upper()

            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.grid[row - i][col + i] = self.grid[row - i][col + i].upper()

        else:
            print("Error - Cannot enunciate four-of-a-kind")

    def print_grid(self):
            print("Round: " + str(self.curr_iteration))

            for i in range(5, -1, -1):
                print("\t", end="")
                for j in range(7):
                    print("| " + str(self.grid[i][j]), end=" ")
                print("|")
            print("\t  _   _   _   _   _   _   _ ")
            print("\t  1   2   3   4   5   6   7 ")

            if self.is_over:
                print("Game Over!")
                if self.winner != None:
                    print(str(self.winner.name) + " is the winner")
                else:
                    print("Game was a draw")


class Person(object):
    token_color = None
    type = None
    name = None

    def __init__(self, name, color):
        self.type = "Person"
        self.name = name
        self.token_color = color

    def col_choice(self, state):
        print(str(self.name) + " is currently up. Represented by color " + str(self.token_color))
        column = None
        while column is None:
            try:
                col_input = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                col_input = None
            if 0 <= col_input <= 6:
                column = col_input
            else:
                print("Invalid choice, try again")
        return column


class Computer(Person):
    mm_tree_level = None
    name = None
    token_color = None

    def __init__(self, name, token_color, depth=5):
        self.type = "Computer"
        self.name = name
        self.token_color = token_color
        self.mm_tree_level = depth

    def col_choice(self, state):
        print(str(self.name) + " is currently up. Represented by color " + str(self.token_color))

        computer_decision = Minimax_Decision_Tree(state)
        best_move, value = computer_decision.optimum_placement(self.mm_tree_level, state, self.token_color)
        return best_move



