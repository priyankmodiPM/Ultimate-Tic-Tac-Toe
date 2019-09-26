import sys
import random
import signal
from time import time
import copy
from operator import itemgetter


class Team49():

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
     


    def init_zobrist(self , board):
        self.dict = {}
        for i in range(4):
            for j in range(4):
                cur_hash =0
                cnt = 0
                for k in range(4):
                    for l in range(4):
                        x = board.board_status[4*i+k][4*j+l]
                        if (x == self.map_symbol[self.max_player]):
                            cur_hash ^= self.blk_zob[2*cnt]
                        elif (x == self.map_symbol[(self.max_player)^1]):
                            cur_hash ^= self.blk_zob[2*cnt+1]
                        cnt +=1

                self.blk_hash[i][j] = cur_hash
        #print self.blk_hash

    def update(self, board, old_move, new_move, ply):
        
        board.board_status[new_move[0]][new_move[1]] = ply ######
        x = new_move[0]/4
        y = new_move[1]/4
        fl = 0
        bs = board.board_status

        #checking if a block has been won or drawn or not after the current move
        for i in range(4):
            #checking for horizontal pattern(i'th row)
            if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
                board.block_status[x][y] = ply
                return 'SUCCESSFUL', True
            #checking for vertical pattern(i'th column)
            if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
                board.block_status[x][y] = ply
                return 'SUCCESSFUL', True

        #checking for diamond pattern
        #diamond 1
        if (bs[4*x+1][4*y] == bs[4*x][4*y+1] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2]) and (bs[4*x+1][4*y] == ply):
            board.block_status[x][y] = ply
            return 'SUCCESSFUL', True
        #diamond 2
        if (bs[4*x+1][4*y+1] == bs[4*x][4*y+2] == bs[4*x+2][4*y+2] == bs[4*x+1][4*y+3]) and (bs[4*x+1][4*y+1] == ply):
            board.block_status[x][y] = ply
            return 'SUCCESSFUL', True
        #diamond 3
        if (bs[4*x+2][4*y] == bs[4*x+1][4*y+1] == bs[4*x+3][4*y+1] == bs[4*x+2][4*y+2]) and (bs[4*x+2][4*y] == ply):
            board.block_status[x][y] = ply
            return 'SUCCESSFUL', True
        #diamond 4
        if (bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x+3][4*y+2] == bs[4*x+2][4*y+3]) and (bs[4*x+2][4*y+1] == ply):
            board.block_status[x][y] = ply
            return 'SUCCESSFUL', True

        #checking if a block has any more cells left or has it been drawn
        for i in range(4):
            for j in range(4):
                if bs[4*x+i][4*y+j] =='-':
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

        #print self.blk_hash
        #self.update_zobrist_block(old_move, player^1 , 0)

        #curmax = -self.INF
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
                break;
            prevans = ans
            level += 1

        #print level, self.maxlen
        #self.numsteps += 1
        #self.timeup = 0
        #print "Returned answer"
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


    def update_zobrist_block(self,move,player):
    	#print "Update function called"
    	#print self.blk_hash

        row_no = move[0]/4
        col_no = move[1]/4
        x = 4*(move[0]%4) + (move[1]%4)
    

        if (player == self.max_player):        
            self.blk_hash[row_no][col_no] ^= self.blk_zob[2*x]
        else:
      
            self.blk_hash[row_no][col_no] ^= self.blk_zob[2*x+1]


    def move_minimax(self, board, old_move, player, level):
        self.available_moves = board.find_valid_move_cells(old_move)
        #print self.available_moves
        length = len(self.available_moves)
        best_move = self.available_moves[random.randrange(length)]
        maxval = -self.INF
        temp = self.num_blks_won[player]


        for move in self.available_moves:
            self.num_blks_won[player] = temp
            self.update_zobrist_block(move,player)
            
            status, blk_won = self.update(board, old_move, move, self.map_symbol[player])
            if blk_won:
                self.num_blks_won[player] ^= 1
            else:
                self.num_blks_won[player] = 0


        
            if blk_won and self.num_blks_won[player] ==1:
                score = self.minimax(
                level-1, player, move, -self.INF, self.INF, board, player)
                self.num_blks_won[player] = 0
            else:

                score = self.minimax(
                level-1, player ^ 1, move, -self.INF, self.INF, board, player)

              


            # undo move
            self.update_zobrist_block(move,player)
            board.board_status[move[0]][move[1]] = "-"
            board.block_status[move[0]/4][move[1]/4] = "-"
        

            #print "Moves , Score: " ,i,score 
            if score > maxval:
                best_move = move
                maxval = score
        self.num_blks_won[player] = temp
        
        #print level, best_move , score
        return best_move, score








    def minimax(self, level, player, old_move, alpha, beta, board , prev_player):
        #print "Reched minimax"
        # base conditon for recursion
        if self.timeup == 1:
            return self.heuristic(board, prev_player,old_move)
             
        #print (time()-self.starttime)
        #print self.timeup
        if time() - self.starttime >= self.endtime:
            self.timeup = 1
            return self.heuristic(board, prev_player,old_move)
            

        if level == 0 or board.find_terminal_state() != ('CONTINUE', '-'):

            return self.heuristic(board, prev_player,old_move)

        possible_moves = board.find_valid_move_cells(old_move)
        score = self.INF
        
        if (player == self.max_player):

            score = -score

        temp = self.num_blks_won[player]

        for move in possible_moves:
            self.num_blks_won[player] = temp
            self.update_zobrist_block(move,player)

            status, blk_won = self.update(board, old_move, move, self.map_symbol[player])
            if blk_won:
                self.num_blks_won[player] ^= 1
            else:
                self.num_blks_won[player] = 0


            if player == self.max_player:
                if blk_won and self.num_blks_won[player] ==1:
                    score = max(score, self.minimax(
                    level-1, player, move, alpha, beta, board, player))
                    self.num_blks_won[player] = 0
                else:
                    score = max(score, self.minimax(
                    level-1, player ^ 1, move, alpha, beta, board,player))

                alpha = max(alpha, score)

            else:
                if blk_won and self.num_blks_won[player] ==1:
                    score = min(score, self.minimax(
                    level-1, player, move, alpha, beta, board, player))
                    self.num_blks_won[player] = 0
                else:
                    score = min(score, self.minimax(
                    level-1, player ^ 1, move, alpha, beta, board, player))
                
                beta = min(score, beta)

            self.update_zobrist_block(move,player)

            # undo move
            board.board_status[move[0]][move[1]] = "-"
            board.block_status[move[0]/4][move[1]/4] = "-"

            if (alpha >= beta or self.timeup == 1):
                break;
        #print "Player is "+ str(player) 
        #print level , score 
        self.num_blks_won[player]= temp
        return score

    def heuristic(self, board, player,old_move ):
        #print "Reched mheuristic"

        cur_state = board.find_terminal_state()
        if cur_state[1] == "WON":

            #print player , cur_state[0]
            #assert( player == cur_state[0])
            if player == self.max_player:
                #print "YO"
                #print board.block_status

                return self.INF
            else:
                return -self.INF
        cost = []
        for i in range(4):
            cost.append([0]*4)

        row_no = old_move[0]/4
        col_no = old_move[1]/4
        #if (board.block_status[row_no][col_no]=='-' and self.numsteps<=20):
        #    return self.computecost(board,player,row_no,col_no)
        # compute costs for small boards
        cur_player = player^1
        summ = 0
        for i in range(4):
            for j in range(4):
                if (board.block_status[i][j] == self.map_symbol[self.max_player]):
                    cost[i][j] = self.INF/100
                elif(board.block_status[i][j] == self.map_symbol[self.max_player ^ 1]):
                    cost[i][j] = -self.INF/100;
                else:
                    if self.blk_hash[i][j] in self.dict:
                        cost[i][j] = self.dict[self.blk_hash[i][j]]
                        if len(self.dict) > 1000 :
                            self.dict = {}
                        #print cost[i][j] , self.computecost(board, self.max_player, i, j) 
                        #assert(cost[i][j] == self.computecost(board, self.max_player, i, j))
                    else :
                        x = self.computecost(board, self.max_player, i, j)
                        cost[i][j] = x
                        #print "LOL",self.blk_hash[i][j], cost[i][j]

                        self.dict[self.blk_hash[i][j]]= x
                #summ += cost[i][j];

        
        return self.compute_for_bigboard(board,self.max_player, cost)

    def compute_for_bigboard(self, board, player, cost):

        row = []
        col = []
        col_tot = [0]*4
        row_tot = [0]*4
        for i in range(4):
            row.append([])
            col.append([])

        total = 0
        #print row_no
        #print "Reched Computecost"

        for i in range(4):
            for j in range(4):
                row[i].append(board.block_status[i][j])
                row_tot[i] += cost[i][j]
               

        for i in range(4):
            for j in range(4):
                col[j].append(board.block_status[i][j])
                col_tot[j]+= cost[i][j];

        for i in range(4):
            cntmx = row[i].count(self.map_symbol[player])
            cntmn = row[i].count(self.map_symbol[player ^ 1])
            cntemp = row[i].count('-')

            if (cntmx+cntemp ==4   or cntmn+cntemp == 4):
                total += row_tot[i]


        for i in range(4):
            cntmx = col[i].count(self.map_symbol[player])
            cntmn = col[i].count(self.map_symbol[player ^ 1])
            cntemp = col[i].count('-')
            if (cntmx+cntemp ==4   or cntmn+cntemp == 4):
                total += col_tot[i]
           

        for i in range(1,3):
            for j in range(1,3):
                cntmx = 0
                cntmn =0
                cntemp = 0
                summ = 0
                for k in range(4):
                    temp = board.block_status[self.up[k]+i][self.down[k]+j] 
                    if temp == self.map_symbol[player]:
                        cntmx += 1
                    elif temp == self.map_symbol[player^1]:
                        cntmn += 1
                    elif temp == "-":
                        cntemp += 1
                    summ += cost[i+self.up[k]][j+self.down[k]]
                
                if (cntmx+cntemp ==4   or cntmn+cntemp == 4):
                    total += summ

        if (total == 0):
            for i in range(4):
                for j in range(4):
                    total += cost[i][j]
        return total




    def computecost(self, board, player, row_no, col_no):

        row = []
        col = []
        for i in range(4):
            row.append([])
            col.append([])
        total = 0
        #print row_no
        #print "Reched Computecost"

        for i in range(4*row_no, 4*row_no+4):
            for j in range(4*col_no, 4*col_no+4):
                row[i%4].append(board.board_status[i][j])

        for i in range(4*row_no, 4*row_no+4):
            for j in range(4*col_no, 4*col_no+4):
                col[j%4].append(board.board_status[i][j])

        for i in range(4):
            cntmx = row[i].count(self.map_symbol[player])
            cntmn = row[i].count(self.map_symbol[player ^ 1])
            if (cntmx > 0 and cntmn == 0):
                total += self.inc_costs[cntmx]
            elif(cntmx == 0 and cntmn > 0):
                total -= self.inc_costs[cntmn]

        for i in range(4):
            cntmx = col[i].count(self.map_symbol[player])
            cntmn = col[i].count(self.map_symbol[player ^ 1])
            cntemp = col[i].count('-')
            if (cntmx>0 and cntmn==0):
                total += self.inc_costs[cntmx]
        
            elif (cntmx==0 and cntmn>0):
                total-= self.inc_costs[cntmn]
        
        start_row = 4*row_no
        start_col = 4*col_no
        #print "Reched Computecost"

        
        for i in range(1,3):
            for j in range(1,3):
                cntmx = 0
                cntmn =0
                for k in range(4):
                    temp = board.board_status[start_row+self.up[k]+i][start_col+self.down[k]+j] 
                    if temp == self.map_symbol[player]:
                        cntmx += 1
                    elif temp == self.map_symbol[player^1]:
                        cntmn += 1
                
                if (cntmx>0 and cntmn==0):
                    total += self.inc_costs[cntmx]  
                elif (cntmx==0 and cntmn >0):
                    total-= self.inc_costs[cntmn]

        return total

