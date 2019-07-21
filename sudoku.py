class Sudoku16x16(object):
	"""
	The main class for the sudoku 16x16

	boardInput  The initial string that we want to parse
	startBoard  The initial board of sudoku unsolved
	boardOutput The board after we solved it
	done        A boolean that shows if the sudoku is solved or not

	"""
	def __init__(self, boardInput):
		super(Sudoku16x16, self).__init__()
		self.boardInput = boardInput
		self.startBoard = SudokuBoard(boardInput).board
		self.done = False
		self.boardOutput = []

	def start(self):
		for i in self.startBoard:
			self.boardOutput.append(i)	


	def check_row(self,row):
		return sorted(self.boardOutput[row]) == [i for i in range(1,17)]

	def check_column(self,column):
		tempColumn = [self.boardOutput[row][column] for row in range(16)]
		return sorted(tempColumn) == [i for i in range(1,17)]

	def check_box(self,row, column):
		tempBox = [
			self.boardOutput[r][c]
	        for r in range(row * 4, (row + 1) * 4)
	        for c in range(column * 4, (column + 1) * 4)
        ]
		return sorted(tempBox) == [i for i in range(1,17)]
	def check_output(self):
		for row in range(16):
			if not self.check_row(row):
				return False
		for column in range(16):
			if not self.check_column(column):
				return False
		for row in range(4):
			for column in range(4):
				if not self.check_box(row, column):
					return False
		self.done = True

	def print_boardOutput(self):
		res = ''
		countLine = 0
		countColumn = 0
		res += '--------------------------------------------------------\n'
		for row in self.boardOutput:
			res += '|'
			for i in row:
				if len(str(i)) == 1:
					res += ' '
				countLine+=1
				if countLine == 4:
					res += str(i)+' | '
					countLine = 0
				else:
					res += str(i)+' '
				
			countColumn+=1
			if countColumn == 4:
				res += '\n--------------------------------------------------------\n'
				countColumn = 0
			else:
				res += '\n'

		return res
		

class SudokuBoard(object):
	"""
	The creation of the board for the sudoku from a string to a 2D array
	"""
	def __init__(self, board):
		super(SudokuBoard, self).__init__()
		self.board = self.create_board(board)
		
	def create_board(self,boardInput):
		board = []
		tempBoard = boardInput.split("\n")
		#inspect for each line if we have 16 numbers
		for line in tempBoard:
			line = line.split(" ")
			#if the length is not 16 throw error
			if len(line) != 16:
				raise Exception("Column is not equal to 16")

			#create a new line in the board to append the number
			board.append([])

			for c in line:
				if not c.isdigit():
					raise Exception("Char not an integer")
				#append c into the last line of our board
				board[-1].append(int(c))

		if len(board) != 16:
			raise Exception("Line is not equal to 16")

		return board
