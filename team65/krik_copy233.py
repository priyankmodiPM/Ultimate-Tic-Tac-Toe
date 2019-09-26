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

	def gainEstimate(self, countd, countx, counto):
		gain = 0
		if(countx == 3 and countd == 0 and counto == 0):
			gain = 1000
		if(counto == 3 and countd == 0 and countx == 0):
			gain = -1000
		if(countx == 2 and countd == 1 and counto == 0):
			gain = 100
		if(counto == 2 and countd == 1 and countx == 0):
			gain = -100
		if(countx == 1 and countd == 2 and counto == 0):
			gain = 10
		if(counto == 1 and countd == 2 and countx == 0):
			gain = -10
		return gain

	def evaluation(self, board, old_move):
		blockx = old_move[0] / 3
		blocky = old_move[1] / 3
		cellx = old_move[0] % 3
		celly = old_move[1] % 3
		block_no = cellx * 3 + celly
		gain = 0

		for board_number in range(0, 2):
			for i in range(0, 3):
				countx = 0
				counto = 0
				countd = 0
				for j in range(0, 3):
					if board.big_boards_status[board_number][i][j] == '-':
						countd += 1
					elif board.big_boards_status[board_number][i][j] == 'o':
						counto += 1
					elif board.big_boards_status[board_number][i][j] == 'x':
						countx += 1
				if countx == 3:
					gain = 100 * self.gainEstimate(countd, countx, counto)
					return gain
				elif counto == 3:
					gain = 100 * self.gainEstimate(countd, countx, counto)
					return gain
				else:
					gain += 100 * self.gainEstimate(countd, countx, counto)

		for board_number in range(0, 2):
			for j in range(0, 3):
				countx = 0
				counto = 0
				countd = 0
				for i in range(0, 3):
					if board.big_boards_status[board_number][i][j] == '-':
						countd += 1
					elif board.big_boards_status[board_number][i][j] == 'o':
						counto += 1
					elif board.big_boards_status[board_number][i][j] == 'x':
						countx += 1

				if countx == 3 :
					gain = 100 * self.gainEstimate(countd, countx, counto)
					return gain
				elif counto == 3 :
					gain = 100 * self.gainEstimate(countd, countx, counto)
					return gain
				else:
					gain += 100 * self.gainEstimate(countd, countx, counto)

		countx = 0
		counto = 0
		countd = 0
		for board_number in range(0, 2):	
			for i in range(0, 3):
				if board.big_boards_status[board_number][i][i] == '-':
					countd += 1
				elif board.big_boards_status[board_number][i][i] == 'o':
					counto += 1
				elif board.big_boards_status[board_number][i][i] == 'x':
					countx += 1

		if countx == 2 :
			gain = 100 * self.gainEstimate(countd, countx, counto)
			return gain
		elif counto == 2 :
			gain = 100 * self.gainEstimate(countd, countx, counto)
			return gain
		else :
			gain += 100 * self.gainEstimate(countd, countx, counto)

		countx = 0
		counto = 0
		countd = 0
		for board_number in range(0, 2):	
			for i in range(0, 3):
				if board.big_boards_status[board_number][i][3 - i] == '-':
					countd += 1
				elif board.big_boards_status[board_number][i][3 - i] == 'o':
					counto += 1
				elif board.big_boards_status[board_number][i][3 - i] == 'x':
					countx += 1

		if countx == 3:
			gain = 100 * self.gainEstimate(countd, countx, counto)
			return gain
		elif counto == 3:
			gain = 100 * self.gainEstimate(countd, countx, counto)
			return gain
		else :
			gain += 100 * self.gainEstimate(countd, countx, counto)

		for checkx in range(0, 5, 4):
			for checky in range(0, 5, 4):
				local_gain = 0
				local_flag = 0
				for i in range(0, 3):
					countx = 0
					counto = 0
					countd = 0
					for j in range(0, 3):
						if board.big_boards_status[board_number][checkx + i][checky + j] == '-':
							countd += 1
						elif board.big_boards_status[board_number][checkx + i][checky + j] == 'o':
							counto += 1
						elif board.big_boards_status[board_number][checkx + i][checky + j] == 'x':
							countx += 1

					if countx == 3:
						local_gain = self.gainEstimate(countd, countx, counto)
						local_flag = 1
						break
					elif counto == 3:
						local_gain = self.gainEstimate(countd, countx, counto)
						local_flag = 1
						break
					else:
						local_gain += self.gainEstimate(countd, countx, counto)

					if local_flag == 1:
						break
				if local_flag == 1:
					gain += local_gain
					continue

				for j in range(0, 3):
					countx = 0
					counto = 0
					countd = 0
					for i in range(0, 4):
						if board.big_boards_status[board_number][checkx + i][checky + j] == '-':
							countd += 1
						elif board.big_boards_status[board_number][checkx + i][checky + j] == 'o':
							counto += 1
						elif board.big_boards_status[board_number][checkx + i][checky + j] == 'x':
							countx += 1

					if countx == 3 :
						local_gain = self.gainEstimate(countd, countx, counto)
						local_flag = 1
						break
					elif counto == 3 :
						local_gain = self.gainEstimate(countd, countx, counto)
						local_flag = 1
						break
					else:
						local_gain += self.gainEstimate(countd, countx, counto)
					if local_flag == 1:
						break
				if local_flag == 1:
					gain += local_gain	
					continue

				countx = 0
				counto = 0
				countd = 0
				for i in range(0, 3):
					if board.big_boards_status[board_number][checkx + i][checky + i] == '-':
						countd += 1
					elif board.big_boards_status[board_number][checkx + i][checky + i] == 'o':
						counto += 1
					elif board.big_boards_status[board_number][checkx + i][checky + i] == 'x':
						countx += 1

				if countx == 3 :
					local_gain = self.gainEstimate(countd, countx, counto)
					local_flag = 1
				elif counto == 3 :
					local_gain = self.gainEstimate(countd, countx, counto)
					local_flag = 1
				else :
					local_gain += self.gainEstimate(countd, countx, counto)

				if local_flag == 1:
					gain += local_gain
					continue

				countx = 0
				counto = 0
				countd = 0
				for i in range(0, 3):
					if board.big_boards_status[board_number][checkx + i][checky + 3 - i] == '-':
						countd += 1
					elif board.big_boards_status[board_number][checkx + i][checky + 3 - i] == 'o':
						counto += 1
					elif board.big_boards_status[board_number][checkx + i][checky + 3 - i] == 'x':
						countx += 1

				if countx == 3:
					local_gain = self.gainEstimate(countd, countx, counto)
					local_flag = 1
				elif counto == 3:
					local_gain = self.gainEstimate(countd, countx, counto)
					local_flag = 1
				else :
					local_gain += self.gainEstimate(countd, countx, counto)

				gain += local_gain

		return gain

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