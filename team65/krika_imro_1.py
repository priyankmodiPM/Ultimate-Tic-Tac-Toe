import sys
import random
import signal
import time
import copy

class Team65:
	def __init__(self):
		self.infinity = 99999999
		self.ninfinity = -99999999
		self.next_move = (0, 0, 0)
		self.symbol = 'x'

	def getMarker(self, flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	#def gainEstimate(self, countd, countx, counto):
	#	gain = 0
	#	if(countx == 3 and countd == 0 and counto == 0):
	#		gain = 1000
	#	if(counto == 3 and countd == 0 and countx == 0):
	#		gain = -1000
	#	if(countx == 2 and countd == 1 and counto == 0):
	#		gain = 100
	#	if(counto == 2 and countd == 1 and countx == 0):
	#		gain = -100
	#	if(countx == 1 and countd == 2 and counto == 0):
	#		gain = 10
	#	if(counto == 1 and countd == 2 and countx == 0):
	#		gain = -10
	#	return gain

	def evaluation(self, board, last_move):
		openMove = 30
		lastBlockWin = 30
		contBlock = [0,0,60,150,0]
		cutBlock = [0,0,50,120,0]
		contCell = [0,0,4,10,0]
		cutCell = [0,0,2,5,0]
		blockWin = 25
		blockWinCent = 10
		blockWinCor = 10
		cCell = 0.25
		cellOfC = 0.50
		lastBlockDraw = 15

		ownFlag = self.symbol
		oppFlag = self.getMarker(self.symbol)

		heurVal = 0

		bs = board.small_boards_status[:]
		BS = board.big_boards_status[:]


		##############################################################
		#checking if providing a free move
		##############################################################
		#blockX = last_move[0]%3
		#blockY = last_move[1]%3
		#if bs[brd][blockX][blockY]!='-':
		#	if self.myMove:
		#		heurVal+=openMove
		#	else:
		#		heurVal-=openMove


		##############################################################
		# checking if this move helped us win block
		##############################################################
		blockX = last_move[0]/3
		blockY = last_move[1]/3
		for brd in range(0,2):
			if bs[brd][blockX][blockY] == ownFlag:
				heurVal+=lastBlockWin
			elif bs[brd][blockX][blockY] == oppFlag:
				heurVal-=lastBlockWin
			#elif bs[brd][blockX][blockY] == 'd':
			#	if self.myMove:
			#		heurVal -= lastBlockDraw
			#	else:
			#		heurVal += lastBlockDraw



		##############################################################
		#checking for continuous blocks or cutting other blocks and
		#					and same for other
		##############################################################
		FDdrawCount=0
		BDdrawCount=0
		FDcountSelf=0
		FDcountOther=0
		FDflagSelf=0
		FDflagOther=0
		BDcountSelf=0
		BDcountOther=0
		BDflagSelf=0
		BDflagOther=0

		for brd in range(0,2):
			for i in range(3):
	    	    #forward diagonal block part-1
				if bs[brd][i][i] == ownFlag:
					FDcountSelf+=1
					FDflagSelf = 1
				elif bs[brd][i][i] == oppFlag:
					FDcountOther+=1
					FDflagOther = 1
				elif bs[brd][i][i] == 'd':
					FDdrawCount+=1
	    	    #back diagonal block part-1
				if bs[brd][2-i][i] == ownFlag:
					BDcountSelf += 1
					BDflagSelf = 1
				elif bs[brd][2-i][i] == oppFlag:
					BDcountOther += 1
					BDflagOther = 1
				elif bs[brd][2-i][i] == 'd':
					BDdrawCount+=1
				
				RWdrawCount=0
				CLdrawCount=0
				RWcountSelf=0
				RWflagSelf=0
				RWcountOther=0
				RWflagOther=0
				CLcountSelf=0
				CLflagSelf=0
				CLcountOther=0
				CLflagOther=0
				#loop for rows columns and cells
				for j in range(3):
	    	        #winning/losing centre blocks
					if( (i==0 or i==1) and (j==0 or j==1)):
						if(bs[brd][i][j] == ownFlag):
							heurVal += blockWinCent
						elif(bs[brd][i][j] == oppFlag):
							heurVal -= blockWinCent
	    	        #winning/losing corner blocks
					if((i==0 or i==2) and (j==0 or j==2)):
						if(bs[brd][i][j] == ownFlag):
							heurVal += blockWinCor #3
						elif(bs[brd][i][j] ==oppFlag):
							heurVal -= blockWinCor #3
	    	        #winning/losing blocks
					if bs[brd][i][j] == ownFlag:
						heurVal += blockWin
					elif bs[brd][i][j] == oppFlag:
						heurVal -= blockWin
	    	        #rows block part-1
					if bs[brd][i][j] == ownFlag:
						RWcountSelf += 1
						RWflagSelf = 1
					elif bs[brd][i][j] == oppFlag:
						RWcountOther += 1
						RWflagOther = 1
					elif bs[brd][i][j] == 'd':
						RWdrawCount+=1
	    	        #columns block part-1
					if bs[brd][j][i] == ownFlag:
						CLcountSelf += 1
						CLflagSelf = 1
					elif bs[brd][j][i] == oppFlag:
						CLcountOther += 1
						CLflagOther = 1
					elif bs[brd][j][i] == 'd':
						CLdrawCount+=1
					CCSFD=0
					CFSFD=0
					CCOFD=0
					CFOFD=0
					CCSBD=0
					CFSBD=0
					CCOBD=0
					CFOBD=0
					if bs[brd][i][j] == '-':
						for k in range(3):
			                #forward diagonal cell part-1
							if BS[brd][3*i+k][3*j+k] == ownFlag:
								CCSFD+=1
								CFSFD=1
							elif BS[brd][3*i+k][3*j+k]==oppFlag:
								CCOFD+=1
								CFOFD=1
							#back diagonal cell part-1
							if BS[brd][3*i+2-k][3*j+k] == ownFlag:
								CCSBD+=1
								CFSBD=1
							elif BS[brd][3*i+2-k][3*j+k]==oppFlag:
								CCOBD+=1
								CFOBD=1
							CCSRW=0
							CCORW=0
							CFSRW=0
							CFORW=0
							CCSCL=0
							CCOCL=0
							CFSCL=0
							CFOCL=0
							for l in range(3):
			                    #row cell part-1
								if BS[brd][3*i+k][3*j+l] ==ownFlag:
									CCSRW+=1
									CFSRW=1
								elif BS[brd][3*i+k][3*j+l]==oppFlag:
									CCORW+=1
									CFORW=1
			                    #col cell part-1
								if BS[brd][3*i+l][3*j+k] ==ownFlag:
									CCSCL+=1
									CFSCL=1
								elif BS[brd][3*i+l][3*j+k]==oppFlag:
									CCOCL+=1
									CFOCL=1
							#row cell part-2
							if CFSRW == 1:
								if CFORW == 0:
									heurVal+=contCell[CCSRW]
								else:
									heurVal-=cutCell[CCSRW]
							if CFORW == 1:
								if CFSRW == 0:
									heurVal-=contCell[CCORW]
								else:
									heurVal+=cutCell[CCORW]
							#col cell part-2
							if CFSCL == 1:
								if CFOCL == 0:
									heurVal+=contCell[CCSCL]
								else:
									heurVal-=cutCell[CCSCL]
							if CFOCL == 1:
								if CFSCL == 0:
									heurVal-=contCell[CCOCL]
								else:
									heurVal+=cutCell[CCOCL]
						#forward diagonal cell part-2
						if CFSFD == 1:
							if CFOFD == 0:
								heurVal+=contCell[CCSFD]
							else:
								heurVal-=cutCell[CCSFD]
						if CFOFD == 1:
							if CFSFD == 0:
								heurVal-=contCell[CCOFD]
							else:
								heurVal+=cutCell[CCOFD]
						#back diagonal cell part-2
						if CFSBD == 1:
							if CFOBD == 0:
								heurVal+=contCell[CCSBD]
							else:
								heurVal-=cutCell[CCSBD]
						if CFOBD == 1:
							if CFSBD == 0:
								heurVal-=contCell[CCOBD]
							else:
								heurVal+=cutCell[CCOBD]
				#rows block part-2
				if RWflagSelf == 1:
					if (RWflagOther == 0 and RWdrawCount==0):
						heurVal+=contBlock[RWcountSelf]
					else:
						heurVal-=cutBlock[RWcountSelf]
				if RWflagOther == 1:
					if (RWflagSelf == 0 and RWdrawCount==0):
						heurVal-=contBlock[RWcountOther]
					else:
						heurVal+=cutBlock[RWcountOther]
				#columns block part-2
				if CLflagSelf == 1:
					if (CLflagOther == 0 and CLdrawCount==0):
						heurVal+=contBlock[CLcountSelf]
					else:
						heurVal-=cutBlock[CLcountSelf]
				if CLflagOther == 1:
					if (CLflagSelf == 0 and CLdrawCount==0):
						heurVal-=contBlock[CLcountOther]
					else:
						heurVal+=cutBlock[CLcountOther]
		#forward diagonal block part-2
		if FDflagSelf == 1:
			if FDflagOther==0 and FDdrawCount==0:
				heurVal+=contBlock[FDcountSelf]
			else:
				heurVal-=cutBlock[FDcountSelf]
		if FDflagOther == 1:
			if FDflagSelf == 0 and FDdrawCount==0:
				heurVal-=contBlock[FDcountOther]
			else:
				heurVal+=cutBlock[FDcountOther]

		#back diagonal block part-2
		if BDflagSelf == 1:
			if BDflagOther == 0 and BDdrawCount==0:
				heurVal+=contBlock[BDcountSelf]
			else:
				heurVal-=cutBlock[BDcountSelf]
		if BDflagOther == 1:
			if BDflagSelf == 0 and BDdrawCount==0:
				heurVal-=contBlock[BDcountOther]
			else:
				heurVal+=cutBlock[BDcountOther]


	    ####################################################################################
	    #getting centre/corner squares in blocks AND getting squares in centre/corner blocks
	    ####################################################################################
		for k in range(3):
			for l in range(3):
				if bs[brd][k][l]=='-':
					for i in range(3):
						for j in range(3):

							#getting centre squares in blocks
							if ((i==1 or i==2) and (j==1 or j==2)):
								if BS[brd][3*k+i][3*l+j] == ownFlag:
									# print "centre square mila"
									heurVal += cCell
								elif BS[brd][3*k+i][3*l+j] == oppFlag:
							        # print "centre square kata"
									heurVal -= cCell

							#getting corner squares in blocks
							if ((i==0 or i==2) and (j==0 or j==2)):
								if BS[brd][3*k+i][3*l+j] == ownFlag:
							        # print "corner square mila"
									heurVal += cCell
								elif BS[brd][3*k+i][3*l+j] == oppFlag:
							        # print "corner square kata"
									heurVal -= cCell

							#getting square in centre block
							if ((k==1 or k==2) and (l==1 or l==2)):
								if BS[brd][3*k+i][3*l+j] == ownFlag:
							        # print "centre block me mila"
									heurVal += cellOfC
								elif BS[brd][3*k+i][3*l+j] == oppFlag:
							        # print "centre block me kata"
									heurVal -= cellOfC

							#getting square in corner block
							if ((k==0 or k==2) and (l==0 or l==2)):
								if BS[brd][3*k+i][3*l+j] == ownFlag:
							        # print "corner block me mila"
									heurVal += cellOfC
								elif BS[brd][3*k+i][3*l+j] == oppFlag:
							        # print "corner block me kata"
									heurVal -= cellOfC
		# print "returning heuristics"
		return heurVal

	def move(self, board, old_move, flag):
		self.symbol = flag
		utility = self.minimax_search(board, old_move, 0, self.ninfinity, self.infinity, True, flag)
		return ( self.next_move[0], self.next_move[1], self.next_move[2])

	def minimax_search(self, board, old_move, depth, alpha, beta, max_player, flag):
		status = board.find_terminal_state();

		if depth == 3 or status[0] != 'CONTINUE':
			#return random.randint(0, 1000)
			#return 1
			if self.symbol == 'x':
				return self.evaluation(board, old_move)
			else:
				return (0 - self.evaluation(board, old_move))

		if max_player:
			value = self.ninfinity
			valid_moves = board.find_valid_move_cells(old_move)
			random.shuffle(valid_moves)
			for move in valid_moves:
				board.update(old_move, move, flag)
				#[A, bol] = board.update(old_move, move, flag)

				if flag == 'x':
					next_flag = 'o'
				else:
					next_flag = 'x'
				child_value = self.minimax_search(board, move, depth + 1, alpha, beta, False, next_flag)
				board.big_boards_status[move[0]][move[1]][move[2]] = '-';
				board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'
				if child_value > value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				alpha = max(alpha, value)

				if beta <= alpha:
					break
			return value

		else:
			value = self.infinity
			valid_moves = board.find_valid_move_cells(old_move)
			random.shuffle(valid_moves)
			for move in valid_moves:
				board.update(old_move, move, flag)
				if flag == 'x':
					next_flag = 'o'
				else:
					next_flag = 'x'
				child_value = self.minimax_search(board, move, depth + 1, alpha, beta, True, next_flag)
				board.big_boards_status[move[0]][move[1]][move[2]] = '-';
				board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'
				if child_value < value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				beta = min(beta, value)				
				if beta <= alpha:
						break
			return value