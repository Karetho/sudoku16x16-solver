class Clue(object):
    """
    This class allow to gives all the possibility for one case of our sudoku

    Attributes:
        row              The position compared to the row in the sudoku.
        column           The position compared to the column in the sudoku.
        possibilities    The list of possible values.
        possibilities_eliminated The list of values that has been tested
        peers The cases that are related to the case
    """
    def __init__(self):
        super(Clue, self).__init__()
        self.row = 0
        self.column = 0
        self.possibilities = []
        self.possibilities_eliminated = []
        self.peers = []
        
    def __str__(self):
        return '(row=%d column=%d possibilities=%s possibilities_eliminated=%s peers =%s)' % (self.row, self.column, self.possibilities, self.possibilities_eliminated, self.peers)
        
class SolverSudoku(object):
    """
    The main class for the solver

    Attributes:
        sudokuGame The sudoku game we created from the string we passed earlier
        board      A shortcut to directly access to board of our sudoku game
    """
    def __init__(self, sudokuGame):
        super(SolverSudoku, self).__init__()
        self.sudokuGame = sudokuGame
        self.board = self.sudokuGame.boardOutput

    #Append the peers of the cell in the same column
    def peers_column(self,column):
        return [row[column] for row in self.board]

    #Append the peers of the cell in the same row
    def peers_row(self,row):
        return self.board[row]

    #Append the peers of the cells in the same box
    def peers_box(self,row,column):
        tempBox = []
        numRow = divmod(row,4)[0]
        numCol = divmod(column,4)[0]
        for i in range(numRow*4,(numRow*4)+4):
            for j in range(numCol*4,(numCol*4)+4):
                tempBox.append(self.board[i][j])
        return tempBox

    def peers(self,row,column):
        peers = self.peers_row(row) + self.peers_column(column) + self.peers_box(row,column)
        return peers

    def possible_value(self,peers,value):
        if value in peers:
            return False
        return True

    def define_possibilities(self,row,column):
        possibilities = []
        peers = self.peers(row,column)
        for i in range(1,17):
            if self.possible_value(peers,i):
                possibilities.append(i)
        return possibilities

    def define_clue(self,row,column):
        clue = Clue()
        clue.row = row
        clue.column = column
        clue.possibilities = self.define_possibilities(row,column)
        clue.peers = self.peers(row,column)
        return clue

    def calculate_clues(self):
        clues = []
        for i in range(16):
            for j in range(16):
                if self.board[i][j] == 0:
                    clues.append(self.define_clue(i,j))
        clues.sort(key=lambda x: (-len(x.possibilities), x.possibilities), reverse=True)
        return clues
        
    def checkClueOnlyOneValue(self,clues):
        res = []
        for clue in clues:
            if len(clue.possibilities) == 1:
                res.append(clue)
        return res

    def fillFirstValue(self,clue):
        self.board[clue.row][clue.column] = clue.possibilities[0]
        clue.possibilities_eliminated.append(clue.possibilities[0])
        clue.possibilities.remove(clue.possibilities[0])

    def fillValue(self,clues,oldClues):
        if not clues or not clues[0].possibilities:
            self.board[clues[0].row][clues[0].column] = 0
            clues[0].possibilities += clues[0].possibilities_eliminated
            if not oldClues:
                clues = self.calculate_clues()
                self.fillValue(clues, oldClues)
            i = len(oldClues) - 1
            oldClue = oldClues[i]
            oldClue.possibilities += oldClue.possibilities_eliminated
            self.board[oldClue.row][oldClue.column] = 0
            clues.insert(0,oldClue)
            oldClues.remove(oldClue)
            for clue in reversed(oldClues):
                self.board[clue.row][clue.column] = 0
                clues.insert(0,clue)
                oldClues.remove(clue)
                if len(clue.possibilities):
                    if clues[0].possibilities:
                        self.fillFirstValue(clues[0])
                        return
                    else:
                        clues = self.calculate_clues()
                        self.fillValue(clues,oldClues)
        self.fillFirstValue(clues[0])
        oldClues.append(clues[0])
        clues.remove(clues[0])
        
    def main_function_solver(self):
        print("-------------------------- START ------------------------------")
        print(self.sudokuGame.print_boardOutput())
        firstClear = False
        oldClues = []
        while not firstClear:
            #Calculate all the clue for all the empty case
            clues = self.calculate_clues()
            #Start with the clue that only has one possibility
            first_clues = self.checkClueOnlyOneValue(clues)
            for clue in first_clues:
                self.fillFirstValue(clue)
            clues = self.calculate_clues()
            #Start with the clue that only has one possibility
            first_clues = self.checkClueOnlyOneValue(clues)
            #If there's no clue with one possibility we did the first clear
            if not first_clues:
                firstClear = True
        print("-------------------------- First clear ------------------------------")
        print(self.sudokuGame.print_boardOutput())
        #Propagate the value by checking again the clues
        self.sudokuGame.check_output()
        while not self.sudokuGame.done:
            #Calculate all the clue for all the empty case
            clues = self.calculate_clues()
            #Fill the value for the case with the less possibilities
            self.fillValue(clues,oldClues)
            self.sudokuGame.check_output()
        print("-------------------------- Cleared ------------------------------")
        print(self.sudokuGame.print_boardOutput())