from sudoku import Sudoku16x16
from solver import SolverSudoku,Clue
from datetime import datetime
import os, os.path

DIR = os.getcwd()+'/data'
numberFile = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
timeElapsed = {}

for x in range(1,numberFile+1):
	s = "data/test"+str(x)+".txt"
	file = open(s,"r")
	boardOutput = file.read()
	S = Sudoku16x16(boardOutput)
	S.start()
	res = S.print_boardOutput()
	nameOutput = s.split("/")[1].split(".")
	nameFile = "output/"+nameOutput[0]+"_unsolved.txt"
	output = open(nameFile,"w")
	output.write(res)
	

	#solver
	solver = SolverSudoku(S)
	now = datetime.now()
	solver.main_function_solver()
	delta = (datetime.now() - now).total_seconds()
	print('Elapsed real time %fs.' % delta)
	timeElapsed[nameOutput[0]] = str(delta) + "s"
	solved = S.print_boardOutput()
	nameFileSolv = "output/"+nameOutput[0]+"_solved.txt"
	output = open(nameFileSolv,"w")
	output.write(solved)
print(timeElapsed)