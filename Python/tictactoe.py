import random

class Board:
    def __init__(self):
        self.data = [' '] * 9

    def checkwin(self):
        if self.data[0] == self.data[1] == self.data[2] and self.data[0] != " ":
            return self.data[0]
        elif self.data[3] == self.data[4] == self.data[5] and self.data[3] != " ":
            return self.data[3]
        elif self.data[6] == self.data[7] == self.data[8] and self.data[6] != " ":
            return self.data[6]
        elif self.data[0] == self.data[3] == self.data[6] and self.data[0] != " ":
            return self.data[0]
        elif self.data[1] == self.data[4] == self.data[7] and self.data[1] != " ":
            return self.data[1]
        elif self.data[2] == self.data[5] == self.data[8] and self.data[2] != " ":
            return self.data[2]
        elif self.data[0] == self.data[4] == self.data[8] and self.data[0] != " ":
            return self.data[0]
        elif self.data[2] == self.data[4] == self.data[6] and self.data[2] != " ":
            return self.data[2]
        elif all(slot != " " for slot in self.data) == True:
            return "Nobody"
        else:
            return False

    def display(self):
        print("     |     |")
        print(f"  {self.data[0]}  |  {self.data[1]}  |  {self.data[2]}")
        print('_____|_____|_____')
        print("     |     |")
        print(f"  {self.data[3]}  |  {self.data[4]}  |  {self.data[5]}")
        print('_____|_____|_____')
        print("     |     |")
        print(f"  {self.data[6]}  |  {self.data[7]}  |  {self.data[8]}")
        print("     |     |")

    def set_cell(self, x, y, marker):
        """ Updates the board with the marker specified, i.e. 'x' or 'o'.
        Returns True if successful. """
        if self.data[x + y*3] == " ":
            self.data[x + y*3] = marker
            return True
        else:
            return False
    
    def boardclear(self):
        for x in range(9):
            self.data[x] = " "

def boardtest():
    board = Board()
    board.display()
    board.set_cell(1, 2, 'x')
    board.display()
    board.boardclear()
    board.display()

def compMove(board):
    for x in range(3):
        if board.data[x] == board.data[x+1] == "O" and board.data[x+2] == " ":
            return board.set_cell(x+2, 0, "O")
        if board.data[x+2] == board.data[x+1] == "O" and board.data[x] == " ":
            return board.set_cell(x, 0, "O")
        if board.data[x] == board.data[x+2] == "O" and board.data[x+1] == " ":
            return board.set_cell(x+1, 0, "O")
        if board.data[x] == board.data[x+3] == "O" and board.data[x+6] == " ":
            return board.set_cell(x+6, 0, "O")
        if board.data[x+6] == board.data[x+3] == "O" and board.data[x] == " ":
            return board.set_cell(x, 0, "O")
        if board.data[x] == board.data[x+6] == "O" and board.data[x+3] == " ":
            return board.set_cell(x+3, 0, "O")
    # if board.data[0] == board.data[1] == "O" and board.data[2] == " ":
    #     return board.set_cell(2, 0, "O")
    # elif board.data[1] == board.data[2] == "O" and board.data[0] == " ":
    #     return board.set_cell(0, 0, "O")
    # elif board.data[0] == board.data[2] == "O" and board.data[1] == " ":
    #     return board.set_cell(1, 0, "O")
    # elif board.data[3] == board.data[4] == "O" and board.data[5] == " ":
    #     return board.set_cell(5, 0, "O")
    # elif board.data[5] == board.data[4] == "O" and board.data[3] == " ":
    #     return board.set_cell(3, 0, "O")
    # elif board.data[3] == board.data[5] == "O" and board.data[4] == " ":
    #     return board.set_cell(4, 0, "O")
    # elif board.data[6] == board.data[7] == "O" and board.data[8] == " ":
    #     return board.set_cell(8, 0, "O")
    # elif board.data[6] == board.data[8] == "O" and board.data[7] == " ":
    #     return board.set_cell(7, 0, "O")
    # elif board.data[7] == board.data[8] == "O" and board.data[6] == " ":
    #     return board.set_cell(6, 0, "O")
    
    # elif board.data[0] == board.data[3] == "O" and board.data[6] == " ":
    #     return board.set_cell(6, 0, "O")
    # elif board.data[0] == board.data[6] == "O" and board.data[3] == " ":
    #     return board.set_cell(3, 0, "O")
    # elif board.data[6] == board.data[3] == "O" and board.data[0] == " ":
    #     return board.set_cell(0, 0, "O")
    # elif board.data[1] == board.data[4] == "O" and board.data[7] == " ":
    #     return board.set_cell(7, 0, "O")
    # elif board.data[4] == board.data[7] == "O" and board.data[1] == " ":
    #     return board.set_cell(1, 0, "O")
    # elif board.data[1] == board.data[7] == "O" and board.data[4] == " ":
    #     return board.set_cell(4, 0, "O")
    # elif board.data[2] == board.data[5] == "O" and board.data[8] == " ":
    #     return board.set_cell(8, 0, "O")
    # elif board.data[2] == board.data[8] == "O" and board.data[5] == " ":
    #     return board.set_cell(5, 0, "O")
    # elif board.data[5] == board.data[8] == "O" and board.data[2] == " ":
    #     return board.set_cell(2, 0, "O")
    
    if board.data[0] == board.data[4] == "O" and board.data[8] == " ":
        return board.set_cell(8, 0, "O")
    elif board.data[0] == board.data[8] == "O" and board.data[4] == " ":
        return board.set_cell(4, 0, "O")
    elif board.data[4] == board.data[8] == "O" and board.data[0] == " ":
        return board.set_cell(0, 0, "O")
    elif board.data[2] == board.data[4] == "O" and board.data[6] == " ":
        return board.set_cell(6, 0, "O")
    elif board.data[2] == board.data[6] == "O" and board.data[4] == " ":
        return board.set_cell(4, 0, "O")
    elif board.data[4] == board.data[6] == "O" and board.data[2] == " ":
        return board.set_cell(2, 0, "O")
    else:
        for x in range(3):
            if board.data[x] == board.data[x+1] == "X" and board.data[x+2] == " ":
                return board.set_cell(x+2, 0, "O")
            if board.data[x+2] == board.data[x+1] == "X" and board.data[x] == " ":
                return board.set_cell(x, 0, "O")
            if board.data[x] == board.data[x+2] == "X" and board.data[x+1] == " ":
                return board.set_cell(x+1, 0, "O")
            if board.data[x] == board.data[x+3] == "X" and board.data[x+6] == " ":
                return board.set_cell(x+6, 0, "O")
            if board.data[x+6] == board.data[x+3] == "X" and board.data[x] == " ":
                return board.set_cell(x, 0, "O")
            if board.data[x] == board.data[x+6] == "X" and board.data[x+3] == " ":
                return board.set_cell(x+3, 0, "O")
        # if board.data[0] == board.data[1] == "X" and board.data[2] == " ":
        #     return board.set_cell(2, 0, "O")
        # elif board.data[1] == board.data[2] == "X" and board.data[0] == " ":
        #     return board.set_cell(0, 0, "O")
        # elif board.data[0] == board.data[2] == "X" and board.data[1] == " ":
        #     return board.set_cell(1, 0, "O")
        # elif board.data[3] == board.data[4] == "X" and board.data[5] == " ":
        #     return board.set_cell(5, 0, "O")
        # elif board.data[5] == board.data[4] == "X" and board.data[3] == " ":
        #     return board.set_cell(3, 0, "O")
        # elif board.data[3] == board.data[5] == "X" and board.data[4] == " ":
        #     return board.set_cell(4, 0, "O")
        # elif board.data[6] == board.data[7] == "X" and board.data[8] == " ":
        #     return board.set_cell(8, 0, "O")
        # elif board.data[6] == board.data[8] == "X" and board.data[7] == " ":
        #     return board.set_cell(7, 0, "O")
        # elif board.data[7] == board.data[8] == "X" and board.data[6] == " ":
        #     return board.set_cell(6, 0, "O")
        
        # elif board.data[0] == board.data[3] == "X" and board.data[6] == " ":
        #     return board.set_cell(6, 0, "O")
        # elif board.data[0] == board.data[6] == "X" and board.data[3] == " ":
        #     return board.set_cell(3, 0, "O")
        # elif board.data[6] == board.data[3] == "X" and board.data[0] == " ":
        #     return board.set_cell(0, 0, "O")
        # elif board.data[1] == board.data[4] == "X" and board.data[7] == " ":
        #     return board.set_cell(7, 0, "O")
        # elif board.data[4] == board.data[7] == "X" and board.data[1] == " ":
        #     return board.set_cell(1, 0, "O")
        # elif board.data[1] == board.data[7] == "X" and board.data[4] == " ":
        #     return board.set_cell(4, 0, "O")
        # elif board.data[2] == board.data[5] == "X" and board.data[8] == " ":
        #     return board.set_cell(8, 0, "O")
        # elif board.data[2] == board.data[8] == "X" and board.data[5] == " ":
        #     return board.set_cell(5, 0, "O")
        # elif board.data[5] == board.data[8] == "X" and board.data[2] == " ":
        #     return board.set_cell(2, 0, "O")
        
        if board.data[0] == board.data[4] == "X" and board.data[8] == " ":
            return board.set_cell(8, 0, "O")
        elif board.data[0] == board.data[8] == "X" and board.data[4] == " ":
            return board.set_cell(4, 0, "O")
        elif board.data[4] == board.data[8] == "X" and board.data[0] == " ":
            return board.set_cell(0, 0, "O")
        elif board.data[2] == board.data[4] == "X" and board.data[6] == " ":
            return board.set_cell(6, 0, "O")
        elif board.data[2] == board.data[6] == "X" and board.data[4] == " ":
            return board.set_cell(4, 0, "O")
        elif board.data[4] == board.data[6] == "X" and board.data[2] == " ":
            return board.set_cell(2, 0, "O")
        else:
            if board.data[4] == " ":
                return board.set_cell(1, 1, "O")
            else:
                return board.set_cell(random.randint(0,2), random.randint(0,2), "O")

def Game():
    gameEnd = False
    board = Board()
    entry = False
    compEntry = False
    print(" Welcome to Noughts and Crosses!\n\n You are X\n")
    while gameEnd == False:
        board.display()
        while entry == False:
            x = int(input("x Coordinate: "))
            y = int(input("y Coordinate: "))
            if x <= 2 and x >= 0:
                if y <= 2 and y >= 0:
                    entry = board.set_cell(x, y, "X")
                else:
                    print("y coordinate must be between 0 and 2 inclusive")
            else:
                print("x coordinate must be between 0 and 2 inclusive")
            if entry == False:
                print("Invalid location")
        entry = False
        if not board.checkwin() == False:
            board.display()
            print(f"{board.checkwin()} has won!")
            gameEnd == True
            break
        while compEntry == False:
            compEntry = compMove(board)
        compEntry = False
        if not board.checkwin() == False:
            board.display()
            print(f"{board.checkwin()} has won!")
            gameEnd == True
            break

try:
    Game()
except KeyboardInterrupt:
    print("\n\nAww, you don't like my game?\n")