class TicTacToe:
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.coordinates_map = [["", "", "", ""], ["", [2, 0], [1, 0], [0, 0]], ["", [2, 1], [1, 1], [0, 1]], ["", [2, 2], [1, 2], [0, 2]]]
        self.turn = "X"
        self.move_count = 0

    def print_board(self):
        print("---------")
        print("| {} {} {} |".format(self.board[0][0], self.board[0][1], self.board[0][2]))
        print("| {} {} {} |".format(self.board[1][0], self.board[1][1], self.board[1][2]))
        print("| {} {} {} |".format(self.board[2][0], self.board[2][1], self.board[2][2]))
        print("---------")

    def check_win(self, symbol):
        win = False
        for i in range(3):
            if len([cell for cell in self.board[i] if cell == symbol]) == 3:
                win = True
                break
            elif [self.board[0][i], self.board[1][i], self.board[2][i]] == [symbol, symbol, symbol]:
                win = True
                break

        if [self.board[0][0], self.board[1][1], self.board[2][2]] == [symbol, symbol, symbol]:
            win = True

        if [self.board[0][2], self.board[1][1], self.board[2][0]] == [symbol, symbol, symbol]:
            win = True

        return win

    def make_move(self, symbol, coordinates):
        map_val = self.coordinates_map[coordinates[0]][coordinates[1]]
        board_val = self.board[map_val[0]][map_val[1]]
        if board_val == " " or board_val == "_":
            self.board[map_val[0]][map_val[1]] = symbol

            self.move_count += 1
        else:
            print("This cell is occupied! Choose another one!")

    def run(self):
        self.print_board()

        while True:
            coordinates_string = input("Enter the coordinates: ")
            coordinates = coordinates_string.split(" ")
            if not coordinates[0].isnumeric() or not coordinates[1].isnumeric():
                print("You should enter numbers!")
            else:
                coordinates = [int(x) for x in coordinates]

                if coordinates[0] < 1 or coordinates[0] > 3 or coordinates[1] < 1 or coordinates[1] > 3:
                    print("Coordinates should be from 1 to 3!")
                else:
                    self.make_move(self.turn, coordinates)
                    self.turn = "X" if self.turn == "O" else "O"

            self.print_board()

            x_win = self.check_win("X")
            o_win = self.check_win("O")
            if x_win and not o_win:
                print("X wins")
                break
            elif o_win and not x_win:
                print("O wins")
                break
            else:
                if self.move_count == 9:
                    print("Draw")
                    break


game = TicTacToe()
game.run()


