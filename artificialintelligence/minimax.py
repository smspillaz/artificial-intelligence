# /artificialintelligence/minimax.py
#
# Play a game using the minimax algorithm.
#
# See LICENCE.md for Copyright information
"""Play a game using the minimax algorithm."""

"""
Mancala game v1.0
Lyndon While, 3 April 2014

The program prompts the user for the game size X, then it plays a
game of Mancala between two random players and creates an SVG file

    MancalaGameX.svg

that shows the history of the board during the game. Each board is
annotated with the next move made, and the final board is annotated
with the average branching factor during the game. 

Software to run the program is available from python.org. Get Python 3. 

The size of the displayed boards and the fonts used can be controlled
by changing the variable size below. 

The colours used in the display can be controlled by changing the
variable colours. 

Please report any bugs on help3001. Unless they're embarrassing ones. :-) 
"""

import random 
import copy 

from collections import namedtuple

import pprint

import colorama

import tabulate

#a board position is a 2x7 list with the stores at the ends 
#a player is 0 or 1, and is used to index the board 
#a move is a list of indices into a board

#------------------------------------------------------------- This is the display code 

size = 5 #controls the board-size and fonts - don't change anything else 

side      = size * 5
housefont = size * 2
storefont = size * 3

colours = [(0, 0, 0), (255,150,150), (215,215,0)]
#          black      pink           green-yellow 

def mkhouse(k, p, x, r):
    h = side * (3.4 + k + r // 10 * 9)
    v = side * (1.5 - p + r % 10 * 3)
    return (colours[p + 1], [(h, v), (h + side, v), (h + side, v + side), (h, v + side), (h, v)],
            #text placement and font
            (h + side / 2 - len(str(x)) * side / 8, v + 2 * side / 3, str(x), housefont))

def mkstore(p, x, r):
    h = side * (9.4 - 7 * p + r // 10 * 9)
    v = side * (0.5 + r % 10 * 3)
    return (colours[p + 1], [(h, v), (h + side, v), (h + side, v + 2 * side), (h, v + 2 * side), (h, v)],
            #text placement and font
            (h + side / 2 - len(str(x)) * side / 5, v + 6 * side / 5, str(x), storefont))

def writeColor(c):
    (r, g, b) = c
    return "".join(["rgb(", str(r), ",", str(g), ",", str(b), ")"])

def writeText(t):
    (h, v, z, s) = t
    return "".join(["<text x=\"", str(h), "\" y=\"", str(v), "\" font-family=\"Verdana\" font-size=\"",
                     str(s), "\" fill=\"black\">", z, "</text>\n"])

def writePolygons(f, ps):
    for (c, p, t) in ps:
        f.write("<polygon points=\"")
        for (x, y) in p:
            f.write("".join([str(x), ",", str(y), " "]))
        f.write("\" style=\"fill:")
        f.write(writeColor(c))
        f.write(";stroke:")
        f.write(writeColor(colours[0]))
        f.write(";stroke-width:3\"/>\n")
        f.write(writeText(t))

def mancalaDisplay(b, m, r, f):
    if r % 2 == 1: t = "green"
    else:          t = "pink"
    if r < 10:
        f.write(writeText((size, side * (1.0 + r % 10 * 3), t + "'s", housefont)))
        f.write(writeText((size, side * (1.5 + r % 10 * 3), "move", housefont)))
    #display the move 
    f.write(writeText((size + side * (2 + (r - 1) // 10 * 9), side * (3 + (r - 1) % 10 * 3), "".join([str(k + 1) for k in m]), housefont)))
    writePolygons(f, [mkhouse(k, p, b[p][5 * p + k * (1 - 2 * p)], r) for p in range(2) for k in range(6)] + 
                     [mkstore(   p, b[p][6],                       r) for p in range(2)])

#------------------------------------------------------------- This is the game mechanics code 

def moves(b, p):
#returns a list of legal moves for player p on board b
    zs = []
    #for each non-empty house on p's side
    for m in [h for h in range(6) if b[p][h] > 0]:
        #if the final seed will be sown in p's store 
        if (b[p][m] + m) % 13 == 6:
            #copy b, make move m, and check for recursive possibilities 
            c = copy.deepcopy(b)
            move(c, p, [m])
            ms = moves(c, p)
            if ms == []:
                zs += [[m]]
            else:
                zs += [[m] + n for n in ms]
        else:
            zs += [[m]]
    return zs

def move(b, p, ms):
#make the move ms for player p on board b
    for m in ms:
        x = b[p][m]
        b[p][m] = 0
        (capturePossible, z) = sow(b, p, m + 1, 6, x)
    #if the last seed was sown in an empty house on p's side, with seeds opposite
    if capturePossible and b[p][z] == 1 and b[1 - p][5 - z] > 0:
        b[p][6] += b[p][z] + b[1 - p][5 - z] 
        b[p][z] = 0
        b[1 - p][5 - z] = 0

def sow(b, p, m, y, x):
#sow x seeds for player p on board b, starting from house m, with limit y
#the limit is used to exclude the opponent's store
#it returns (possibleCapture, lastHouseSown)
    while x > 0:
        for z in range(m, min(y + 1, m + x)):
            b[p][z] += 1
        x -= y + 1 - m
        p = 1 - p
        m = 0
        y = 11 - y
    return (y == 5, z)

def render(board):
    """Render the board and print it."""
    print tabulate.tabulate(board)


def evaluate(board):
    """Evaluate board for score.

    This function is really dumb.
    """
    boardScore = sum(board[0]) - sum(board[1])

    # Now evalute how many empty houses we have which are next to
    # a non-empty house of the opponent
    for house_index in range(0, 6):
        if board[0][house_index] == 0 and board[1][house_index] != 0:
            # Look at all of our available houses and see if we can start
            # from any of them to finish in this square.
            for i in range(0, 6):
                if i + board[0][i] % 13 == house_index:
                    boardScore += 20
        elif board[0][house_index] != 0 and board[1][house_index] == 0:
            # Look at all of our available houses and see if we can start
            # from any of them to finish in this square.
            for i in range(0, 6):
                if i + board[1][i] % 13 == house_index:
                    boardScore -= 20

    return boardScore

ScoredMove = namedtuple("AvailableMove", "score move")

PLAYER_MOVE_INDEX = [0, -1]
PLAYER_COLORS = [colorama.Fore.RED, colorama.Fore.GREEN]


def moveScore(nextMove, board, player):
    nextBoard = copy.deepcopy(board)
    move(nextBoard, player, nextMove)
    return evaluate(nextBoard)


def pickMoveForPlayer(player, board, available_moves, scoreFunction):
    score_moves = [ScoredMove(score=scoreFunction(m,
                                                  board,
                                                  player), move=m) for m in available_moves]
    score_moves = sorted(score_moves, key=lambda s: s.score)
    return (score_moves, score_moves[PLAYER_MOVE_INDEX[player]].move)


def minimax(board, player, depth):
    available_moves = moves(board, player)

    if depth != 0 and len(available_moves) != 0:
        best_move = pickMoveForPlayer(player, board, available_moves, moveScore)[1]
        nextBoard = copy.deepcopy(board)
        move(nextBoard, player, best_move)
        return minimax(nextBoard, 1 - player, depth - 1)

    return evaluate(board)


def minimaxScoreFunction(depth):
    def minimaxScore(nextMove, board, player):
        nextBoard = copy.deepcopy(board)
        move(nextBoard, player, nextMove)
        return minimax(nextBoard, 1 - player, depth)

    return minimaxScore


def mancala(n):
    #start with n seeds in each small house
    b = [[n] * 6 + [0] for p in [0, 1]]
    #open the SVG file 
    f = open("".join(["MancalaGame", str(n), ".svg"]), 'w')
    f.write("<svg xmlns=\"http://www.w3.org/2000/svg\">\n")
    mancalaDisplay(b, [], 0, f)
    r = 1
    current_player = 0
    tm = 0 
    #while both players have seeds in their small houses
    while all ([sum(b[p][:6]) > 0 for p in [0, 1]]):
        ms = moves(b, current_player)
        print colorama.Fore.WHITE
        render(b)
        if current_player == 0:
            score_moves, best_move = pickMoveForPlayer(current_player, b, ms, minimaxScoreFunction(5))
            m = best_move
            print PLAYER_COLORS[current_player] + pprint.PrettyPrinter().pformat([(i, mv) for i, mv in enumerate(score_moves)])
            print PLAYER_COLORS[current_player] + repr(best_move)
        else:
            print "Chose between \n", pprint.PrettyPrinter().pformat([(i, mv) for i, mv in enumerate(ms)])
            choice = 999999999
            while choice > len(ms):
                choice = int(input("What move? "))
            m = ms[choice]

        move(b, current_player, m)
        mancalaDisplay(b, m, r, f)
        r += 1
        current_player = 1 - current_player
        tm += len(ms)
    #move the remaining seeds to the stores
    for p in [0, 1]:
        for k in [0, 1, 2, 3, 4, 5]:
            b[p][6] += b[p][k]
            b[p][k] = 0
    mancalaDisplay(b, [round(tm / (r - 1), 2)], r, f)
    f.write("</svg>\n")
    f.close()

def main():
    mancala(int(input("What size game? ")))

main()