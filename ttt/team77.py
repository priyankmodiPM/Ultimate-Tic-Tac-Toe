#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import signal
import time
import traceback
from math import exp
import datetime
import copy
import hashlib
import json

class Player77:
	def __init__(self):
		self.INFINITY = 100000
		self.maxSearchDepth = 257
		self.marker = 'x'
		self.myMove = False
		self.timeLimit = datetime.timedelta(seconds = 14.5)
		self.begin = 0
		self.index = 0
		self.zobrist = []
		self.transpositionTable = dict()
		self.moveOrder = dict()
		self.initZobrist()
		return

	def getMarker(self, flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	def allChildren(self, blockIdentifier):
		cells = boardCopy.find_valid_move_cells(blockIdentifier)
		return cells

	def revertBoard(self, root, blockVal):
		boardCopy.board_status[root[0]][root[1]] = '-'
		boardCopy.block_status[root[0]/3][root[1]/3] = blockVal

	def initZobrist(self):
		self.zobrist = []
		for i in xrange(0, 9):
			self.zobrist.append([])
			for j in xrange(0, 9):
				self.zobrist[i].append([])
				for k in xrange(0, 10):
					self.zobrist[i][j].append([])
					for l in xrange(0, 10):
						self.zobrist[i][j][k].append([])
						for m in xrange(0, 2):
							self.zobrist[i][j][k][l].append(random.randint(0, 2**27))

	def move(self, board, old_move, flag):
		self.marker = flag
		# Make a copy of board and old_move for future use
		global boardCopy
		boardCopy = copy.deepcopy(board)
		move = copy.deepcopy(old_move)
		self.moveOrder = dict()
		answer_index = self.IDS(move)
		del move
		del boardCopy
		return answer_index

	def IDS(self, root):
		firstGuess = 0
		# Initialize beginning time
		self.begin = datetime.datetime.utcnow()
		# Search for best possible move for as long as time permits
		for depth in range(1, self.maxSearchDepth):
			self.transpositionTable = dict()
			firstGuess, move = self.MTDF(root, firstGuess, depth)
			if datetime.datetime.utcnow() - self.begin > self.timeLimit:
				break
			finalMove = move
			# print depth
		return finalMove

	def MTDF(self, root, firstGuess, depth):
		g = firstGuess

		upperBound = self.INFINITY
		lowerBound = -self.INFINITY

		while lowerBound < upperBound:
			if g == lowerBound:
				beta = g + 1
			else:
				beta = g

			self.myMove = True
			self.index = 0
			g, move = self.alphaBeta(root, beta-1, beta, depth)

			# Return value if time up
			if datetime.datetime.utcnow() - self.begin > self.timeLimit:
				return g, move

			if g < beta:
				upperBound = g
			else:
				lowerBound = g

		return g, move

	def cantorPairing(self, a, b):
		return (a + b)*(a + b + 1)/2 + b

	def zobristHash(self, root):
		h = 0
		BS = boardCopy.board_status
		for i in xrange(0, 9):
			for j in xrange(0, 9):
				if BS[i][j] == 'x':
					h = h^self.zobrist[i][j][root[0]+1][root[1]+1][0]
				elif BS[i][j] == 'o':
					h = h^self.zobrist[i][j][root[0]+1][root[1]+1][1]
		return h

	def alphaBeta(self, root, alpha, beta, depth):

		# Get Zobrist Hash of current Board State
		board_md5 = self.zobristHash(root)
		nLower = self.cantorPairing(board_md5, 1)
		nUpper = self.cantorPairing(board_md5, 2)

		lower = -2*self.INFINITY, root
		upper = 2*self.INFINITY, root

		# Transposition table lookup
		if (nLower in self.transpositionTable):
			lower = self.transpositionTable[nLower]
			if (lower[0] >= beta):
				return lower

		if (nUpper in self.transpositionTable):
			upper = self.transpositionTable[nUpper]
			if (upper[0] <= alpha):
				return upper

		status = boardCopy.find_terminal_state()
		if status[1] == "WON":
			if self.myMove:
				return -self.INFINITY, root
			else:
				return self.INFINITY, root

		# Update values of alpha and beta based on values in Transposition Table
		alpha = max(alpha, lower[0])
		beta = min(beta, upper[0])

		# Get Unique Hash for moveOrder Table lookup
		moveHash = self.cantorPairing(board_md5, self.index)
		moveInfo = []

		# Reordered moves already present!
		if moveHash in self.moveOrder:
			children = []
			children.extend(self.moveOrder[moveHash])
			nSiblings = len(children)

		else:
			children = self.allChildren(root)
			nSiblings = len(children)

		if depth == 0 or nSiblings == 0:
			answer = root
			g = self.evaluate(root)

		# Node is a max node
		elif self.myMove:
			g = -self.INFINITY
			answer = children[0]
			# Return value if time up
			if datetime.datetime.utcnow() - self.begin > self.timeLimit:
					return g, answer

			# Save original alpha value
			a = alpha
			i = 0
			while ((g < beta) and (i < nSiblings)):
				self.myMove = False
				c = children[i]

				#Retain current block state for later restoration
				blockVal = boardCopy.block_status[c[0]/3][c[1]/3]

				# Mark current node as taken by us for future reference
				boardCopy.update(root, c, self.marker)
				self.index += 1

				val, temp = self.alphaBeta(c, a, beta, depth-1)

				# Revert Board state
				self.revertBoard(c, blockVal)
				self.index -= 1

				# Append returned values to moveInfo
				temp = (val, c)
				moveInfo.append(temp)

				if val > g:
					g = val
					answer = c

				a = max(a, g)
				i = i + 1
			self.myMove = True

		# Node is a min node
		else:
			g = self.INFINITY
			answer = children[0]
			# Return value if time up
			if datetime.datetime.utcnow() - self.begin > self.timeLimit:
					return g, answer

			# Save original beta value
			b = beta
			i = 0
			while ((g > alpha) and (i < nSiblings)):
				self.myMove = True
				c = children[i]
				# Retain current block state for later restoration
				blockVal = boardCopy.block_status[c[0]/3][c[1]/3]

				# Mark current node as taken by us for future reference
				boardCopy.update(root, c, self.getMarker(self.marker))
				self.index += 1

				val, temp = self.alphaBeta(c, alpha, b, depth-1)

				# Revert Board state
				self.revertBoard(c, blockVal)
				self.index -= 1

				# Append returned values to moveInfo
				temp = (val, c)
				moveInfo.append(temp)

				if val < g:
					g = val
					answer = c

				b = min(b, g)
				i = i + 1
			self.myMove = False

		temp = []

		if self.myMove:
			moveInfo = sorted(moveInfo, reverse = True)
		else:
			moveInfo = sorted(moveInfo)

		for i in moveInfo:
			temp.append(i[1])
			children.remove(i[1])

		random.shuffle(children)

		self.moveOrder[moveHash] = []
		self.moveOrder[moveHash].extend(temp)
		self.moveOrder[moveHash].extend(children)

		# if(len(self.moveOrder[moveHash]) != nSiblings):
			# print "I've Given UUUUUUUUUUPPPPPP"

		# Traditional transposition table storing of bounds
		# ----------------------------------------------------#
		# Fail low result implies an upper bound
		if g <= alpha:
			self.transpositionTable[nUpper] = g, answer

		# Fail high result implies a lower bound
		if g >= beta:
			self.transpositionTable[nLower] = g, answer

		return g, answer

	def evaluate(self, old_move):
		return self.heuristics(old_move)


	def heuristics(self,last_move):
		# print 'enter'
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

		ownFlag = self.marker
		oppFlag = self.getMarker(self.marker)

		heurVal = 0

		bs = boardCopy.block_status
		BS = boardCopy.board_status



		##############################################################
		#checking if providing a free move
		##############################################################
		blockX = last_move[0]%3
		blockY = last_move[1]%3
		if bs[blockX][blockY]!='-':
			if self.myMove:
				heurVal+=openMove
			else:
				heurVal-=openMove



		##############################################################
		# checking if this move helped us win block
		##############################################################
		blockX = last_move[0]/3
		blockY = last_move[1]/3
		if bs[blockX][blockY] == ownFlag:
			heurVal+=lastBlockWin
		elif bs[blockX][blockY] == oppFlag:
			heurVal-=lastBlockWin
		elif bs[blockX][blockY] == 'd':
			if self.myMove:
				heurVal -= lastBlockDraw
			else:
				heurVal += lastBlockDraw



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

		for i in range(3):

	        #forward diagonal block part-1
			if bs[i][i] == ownFlag:
				FDcountSelf+=1
				FDflagSelf = 1
			elif bs[i][i] == oppFlag:
				FDcountOther+=1
				FDflagOther = 1
			elif bs[i][i] == 'd':
				FDdrawCount+=1

	        #back diagonal block part-1
			if bs[2-i][i] == ownFlag:
				BDcountSelf += 1
				BDflagSelf = 1
			elif bs[2-i][i] == oppFlag:
				BDcountOther += 1
				BDflagOther = 1
			elif bs[2-i][i] == 'd':
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
				if( (i==1) and (j==1)):
					if(bs[i][j] == ownFlag):
						heurVal += blockWinCent
					elif(bs[i][j] == oppFlag):
						heurVal -= blockWinCent

	            #winning/losing corner blocks
				if((i==0 or i==2) and (j==0 or j==2)):
					if(bs[i][j] == ownFlag):
						heurVal += blockWinCor #3
					elif(bs[i][j] ==oppFlag):
						heurVal -= blockWinCor #3

	            #winning/losing blocks
				if bs[i][j] == ownFlag:
					heurVal += blockWin
				elif bs[i][j] == oppFlag:
					heurVal -= blockWin


	            #rows block part-1
				if bs[i][j] == ownFlag:
					RWcountSelf += 1
					RWflagSelf = 1
				elif bs[i][j] == oppFlag:
					RWcountOther += 1
					RWflagOther = 1
				elif bs[i][j] == 'd':
					RWdrawCount+=1

	            #columns block part-1
				if bs[j][i] == ownFlag:
					CLcountSelf += 1
					CLflagSelf = 1
				elif bs[j][i] == oppFlag:
					CLcountOther += 1
					CLflagOther = 1
				elif bs[j][i] == 'd':
					CLdrawCount+=1

				CCSFD=0
				CFSFD=0
				CCOFD=0
				CFOFD=0
				CCSBD=0
				CFSBD=0
				CCOBD=0
				CFOBD=0
				if bs[i][j] == '-':
					for k in range(3):

		                #forward diagonal cell part-1
						if BS[3*i+k][3*j+k] == ownFlag:
							CCSFD+=1
							CFSFD=1
						elif BS[3*i+k][3*j+k]==oppFlag:
							CCOFD+=1
							CFOFD=1

						#back diagonal cell part-1
						if BS[3*i+2-k][3*j+k] == ownFlag:
							CCSBD+=1
							CFSBD=1
						elif BS[3*i+2-k][3*j+k]==oppFlag:
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
							if BS[3*i+k][3*j+l] ==ownFlag:
								CCSRW+=1
								CFSRW=1
							elif BS[3*i+k][3*j+l]==oppFlag:
								CCORW+=1
								CFORW=1

		                    #col cell part-1
							if BS[3*i+l][3*j+k] ==ownFlag:
								CCSCL+=1
								CFSCL=1
							elif BS[3*i+l][3*j+k]==oppFlag:
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
				if bs[k][l]=='-':
					for i in range(3):
						for j in range(3):

							#getting centre squares in blocks
							if ((i==1) and (j==1)):
								if BS[3*k+i][3*l+j] == ownFlag:
									# print "centre square mila"
									heurVal += cCell
								elif BS[3*k+i][3*l+j] == oppFlag:
							        # print "centre square kata"
									heurVal -= cCell

							#getting corner squares in blocks
							if ((i==0 or i==2) and (j==0 or j==2)):
								if BS[3*k+i][3*l+j] == ownFlag:
							        # print "corner square mila"
									heurVal += cCell
								elif BS[3*k+i][3*l+j] == oppFlag:
							        # print "corner square kata"
									heurVal -= cCell

							#getting square in centre block
							if ((k==1) and (l==1)):
								if BS[3*k+i][3*l+j] == ownFlag:
							        # print "centre block me mila"
									heurVal += cellOfC
								elif BS[3*k+i][3*l+j] == oppFlag:
							        # print "centre block me kata"
									heurVal -= cellOfC

							#getting square in corner block
							if ((k==0 or k==2) and (l==0 or l==2)):
								if BS[3*k+i][3*l+j] == ownFlag:
# print "corner block me mila"
									heurVal += cellOfC
								elif BS[3*k+i][3*l+j] == oppFlag:
							        # print "corner block me kata"
									heurVal -= cellOfC
		# print 'exit'
		return heurVal
