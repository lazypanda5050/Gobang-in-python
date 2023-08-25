from random import choice
from math import inf
from copy import deepcopy

def advantage(board):
    x = 0
    o = 0
    directions = [[0,1],[1,1],[1,0],[1,-1]]
    for i in range(18):
        for j in range(18):
            if board[i][j] == "X":
                for direction in directions:
                    count = 1
                    if i+(-direction[0]) >= 0 and j+(-direction[1]) >= 0 and i+(-direction[0]) <= 17 and j+(-direction[1]) <= 17:
                        if board[i+(-direction[0])][j+(-direction[1])] != "X":
                            a = i
                            b = j
                            while a+direction[0] <= 17 and b+direction[1] <= 17:
                                try:
                                    if board[a+direction[0]][b+direction[1]] == "X":
                                        count += 1
                                        a += direction[0]
                                        b += direction[1]
                                    elif board[a+direction[0]][b+direction[1]] == "O":
                                        break
                                    else:
                                        count += 1
                                        break
                                except:
                                    pass
                    else:
                        a = i
                        b = j
                        while a+direction[0] <= 17 and b+direction[1] <= 17:
                            if board[a+direction[0]][b+direction[1]] == "X":
                                count += 1
                                a += direction[0]
                                b += direction[1]
                            elif board[a+direction[0]][b+direction[1]] == "O":
                                break
                            else:
                                count += 1
                                break
                    x += count
    for i in range(18):
        for j in range(18):
            if board[i][j] == "O":
                for direction in directions:
                    count = 1
                    if i+(-direction[0]) >= 0 and j+(-direction[1]) >= 0 and i+(-direction[0]) <= 17 and j+(-direction[1]) <= 17:
                        if board[i+(-direction[0])][j+(-direction[1])] != "O":
                            a = i
                            b = j
                            while a+direction[0] <= 17 and b+direction[1] <= 17:
                                if board[a+direction[0]][b+direction[1]] == "O":
                                    count += 1
                                    a += direction[0]
                                    b += direction[1]
                                elif board[a+direction[0]][b+direction[1]] == "X":
                                    break
                                else:
                                    count += 1
                                    break
                    else:
                        a = i
                        b = j
                        while a+direction[0] <= 17 and b+direction[1] <= 17:
                            if board[a+direction[0]][b+direction[1]] == "X":
                                count += 1
                                a += direction[0]
                                b += direction[1]
                            elif board[a+direction[0]][b+direction[1]] == "O":
                                break
                            else:
                                count += 1
                                break
                    o += count
    return x - o

def showBoard(board):
    print("   A B C D E F G H I J K L M N O P Q R")
    for i in range(9):
        print(i+1,end="  ")
        print(*board[i])
    for i in range(9,18):
        print(i+1,end=" ")
        print(*board[i])

def checkWin(board):
    if checkCell(board,"X"):
        return 1
    elif checkCell(board,"O"):
        return 2

def checkCell(board,state):
    directions = [[0,1],[1,1],[1,0],[1,-1]]
    for i in range(18):
        for j in range(18):
            if board[i][j] == state:
                count = 1
                a = i
                b = j
                for direction in directions:
                    while a+direction[0] <= 17 and b+direction[1] <= 17 and a+direction[0] >= 0 and b+direction[1] >= 0:
                        if board[a+direction[0]][b+direction[1]] == state:
                            count += 1
                            a += direction[0]
                            b += direction[1]
                            if count >= 5:
                                return True
                        else:
                            break

def getMove(forbidden,state):
    global board
    try:
        if forbidden:
            move = input(f"Illegal move. Player {i+1}, please enter the coordinates of where you want to place your piece (Number, Letter) seperated by space (ie. \"11 H\"): ").split()
        else:
            move = input(f"Player {i+1}, please enter the coordinates of where you want to place your piece (Number, Letter) seperated by space (ie. \"11 H\"): ").split()
        if int(move[0])-1 >= 0 and int(move[0])-1 <= 17 and ord(move[1].upper())-65 >= 0 and ord(move[1].upper())-65 <= 17:
            if board[int(move[0])-1][ord(move[1].upper())-65] == ".":
                board[int(move[0])-1][ord(move[1].upper())-65] = state
            else:
                getMove(True,state)
        else:
            getMove(True, state)
    except:
        getMove(True,state)

def alphaBeta(board,depth,alpha,beta,maximizingPlayer):
    if depth == 0 or not (checkWin(board) == None):
        return advantage(board)
    
    if maximizingPlayer:
        maxEval = -inf
        for position in findMoves(board,"X"):
            nextNode = alphaBeta(position,depth-1,alpha,beta,False)
            maxEval = max(maxEval, nextNode)
            alpha = max(alpha, nextNode)
            if alpha >= beta:
                break
        return maxEval
    
    else:
        minEval = inf
        for position in findMoves(board,"O"):
            nextNode = alphaBeta(position,depth-1,alpha,beta,True)
            minEval = min(minEval, nextNode)
            beta = min(beta, nextNode)
            if beta <= alpha:
                break
        return minEval

def getAIMove(board,evaluation,xMove):
    goodMoves = []
    if xMove:
        difPos = findMoves(board,"X")
        for pos in difPos:
            if advantage(pos) == evaluation:
                goodMoves.append(getDifference(pos,board))

    else:
        difPos = findMoves(board,"O")
        for pos in difPos:
            if advantage(pos) == evaluation:
                goodMoves.append(getDifference(pos,board))
    return choice(goodMoves)

def findMoves(board,turn):
    difPos = []
    for i in range(18):
        for j in range(18):
            left = False
            right = False
            top = False
            down = False
            nb = deepcopy(board)
            if nb[i][j] == ".":
                for k in range(2):
                    try:
                        if board[i][j+k+1] != ".":
                            left = True
                            break
                    except:
                        pass
                    try:
                        if board[i][j-k-1] != ".":
                            right = False
                            break
                    except:
                        pass
                    try:
                        if board[i+k+1][j] != ".":
                            top = False
                            break
                    except:
                        pass
                    try:
                        if board[i-k-1][j] != ".":
                            down = False
                            break
                    except:
                        pass
                nb[i][j] = turn
                if not left and not right and not top and not down:
                    difPos.append(nb)
    return difPos

def getDifference(m1,m2):
    for i in range(18):
        for j in range(18):
            if m1[i][j] != m2[i][j]:
                return i, j

board = [["." for i in range(18)] for j in range(18)]
p1 = input("Please select a mode to be player 1 (h for human, c for computer): ")
p2 = input("Please select a mode to be player 2 (h for human, c for computer): ")
mode = p1.strip() + p2.strip()
win1 = False
win2 = False

if mode == "hh":
    showBoard(board)
    while not win1 and not win2:
        for i in range(2):
            if i == 0:
                getMove(False,"X")
                showBoard(board) 
            else:
                getMove(False,"O")
                showBoard(board)
            if checkWin(board) == 1:
                win1 = True
                break
            elif checkWin(board) == 2:
                win2 = True
                break

    if win1:
        print("Player 1 wins! 👏")

    elif win2:
        print("Player 2 wins! 👏")

elif mode == "hc":
    showBoard(board)
    while not win1 and not win2:
        for i in range(2):
            if i == 0:
                xMove = True
                getMove(False,"X")
                showBoard(board)

            else:
                xMove = False
                print("Computer is thinking...")
                aiMove = getAIMove(board,alphaBeta(board,1,-inf,inf,False),False)
                print(f"Computer moves to {aiMove[0]+1} {chr(aiMove[1]+65)}")
                board[aiMove[0]][aiMove[1]] = "O"
                showBoard(board)

            if checkWin(board) == 1:
                win1 = True
                break

            elif checkWin(board) == 2:
                win2 = True
                break

    if win1:
        print("Player 1 wins! 👏")
    elif win2:
        print("Computer wins! 🤖")

elif mode == "ch":
    showBoard(board)

elif mode == "cc":
    showBoard(board)
else:
    print("Unknown mode")