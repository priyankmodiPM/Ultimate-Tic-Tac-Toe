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

class Player_me():
    def __init__(self):
        self.available_moves = []
        self.backup_move = (0, 0)
        self.up = [-1, 0, 1, 0]
        self.down = [0, 1, 0, -1]
        self.inc_costs = [0,1, 100, 10000, 100000]
        self.INF = 1000000000
        self.initial_level = 2
        self.endtime = 14
        self.starttime = 0
        self.max_player = 1
        self.map_symbol = ['o', 'x']
        self.blk_zob = []
        self.blk_hash = []
        self.num_blks_won = [0 , 0]
        self.maxlen = 0
        self.mindepth = 9
        self.last_blk_won = 0
        for i in range(4):
            self.blk_hash.append([0]*4)
        self.numsteps = 0
        for i in range(32):
            self.blk_zob.append(2**i)
        #print self.blk_zob
        self.dict = {}
        self.just_start = 1

    def update(self, board, old_move, new_move, ply):
        
        board.board_status[new_move[0]][new_move[1]] = ply ######
        x = new_move[0]/3
        y = new_move[1]/3
        fl = 0
        bs = board.board_status

        #checking if a block has been won or drawn or not after the current move
        for i in range(3):
            #checking for horizontal pattern(i'th row)
            if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2] == bs[3*x+i][3*y+3]) and (bs[3*x+i][3*y] == ply):
                board.block_status[x][y] = ply
                return 'SUCCESSFUL', True
            #checking for vertical pattern(i'th column)
            if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i] == bs[3*x+3][3*y+i]) and (bs[3*x][3*y+i] == ply):
                board.block_status[x][y] = ply
                return 'SUCCESSFUL', True

        #checking if a block has any more cells left or has it been drawn
        for i in range(3):
            for j in range(3):
                if bs[3*x+i][3*y+j] =='-':
                    return 'SUCCESSFUL', False
        board.block_status[x][y] = 'd'
        return 'SUCCESSFUL', False

    def move(self, board, old_move, flag):

        self.starttime = time()
        #print self.starttime
        if flag == "x":
            self.max_player = 1
        else:
            self.max_player = 0
        #print self.max_player

        player = self.max_player
        level = self.initial_level
        self.timeup = 0
        self.init_zobrist(board)
        self.num_blks_won = [0 ,0 ]
        if self.last_blk_won :
            self.num_blks_won[self.max_player] = 1

        self.available_moves = board.find_valid_move_cells(old_move)


        #print self.available_moves
        length = len(self.available_moves)
        prevans = self.available_moves[random.randrange(length)]
        if self.just_start ==1 :
            self.just_start = 0
            return prevans
        while(not self.timeup):
            self.init_zobrist(board)
            ans, val = self.move_minimax(board, old_move, player, level)
           
            self.maxlen = max(self.maxlen, len(self.dict))
            if (self.timeup):
                break
            prevans = ans
            level += 1

        status, blk_won = self.update(board, old_move, prevans, self.map_symbol[player])

        if blk_won == True :
            self.last_blk_won ^= 1
        else:
            self.last_blk_won = 0
            # do something 
        board.board_status[prevans[0]][prevans[1]] = "-"
        board.block_status[prevans[0]/4][prevans[1]/4] = "-"
        self.mindepth = min(self.mindepth, level)
        #print self.mindepth, level , time()-self.starttime
        return prevans
        # except Exception as e:
         #   print e