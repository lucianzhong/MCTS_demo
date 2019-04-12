#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from collections import defaultdict

#Tic-Tac-Toe game move
class TicTacToeMove(object):
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value
    def __repr__(self):
        return "x:" + str(self.x_coordinate) + " y:" + str(self.y_coordinate) + " v:" + str(self.value)

#Tic-Tac-Toe game state
class TicTacToeGameState(object):
    x = 1
    o = -1 
    def __init__(self, state, next_to_move=1):  
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        self.board = state
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        # check if game is over
        rowsum = np.sum(self.board, 0)
        colsum = np.sum(self.board, 1)
        diag_sum_tl = self.board.trace()
        diag_sum_tr = self.board[::-1].trace()

        if any(rowsum == self.board_size) or any(  colsum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
            return 1.
        elif any(rowsum == -self.board_size) or any( colsum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:
            return -1.
        elif np.all(self.board != 0):
            return 0.
        else:
            # if not over - no result
            return None

    def is_game_over(self):
        return self.game_result != None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.value != self.next_to_move:
            return False

        # check if inside the board
        x_in_range = move.x_coordinate < self.board_size and move.x_coordinate >= 0
        if not x_in_range:
            return False

        # check if inside the board
        y_in_range = move.y_coordinate < self.board_size and move.y_coordinate >= 0
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return self.board[move.x_coordinate, move.y_coordinate] == 0
    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.board + " is not legal")
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        next_to_move = TicTacToeGameState.o if self.next_to_move == TicTacToeGameState.x else TicTacToeGameState.x
        return TicTacToeGameState(new_board, next_to_move)
    def get_legal_actions(self):
        indices = np.where(self.board == 0)
        return [TicTacToeMove(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]




#Node
class MonteCarloTreeSearchNode(object):
    def __init__(self, state: TicTacToeGameState, parent=None):
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    # function DEFAULTPOLICY(s)   
    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result
    # function backup(v)
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [ (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))  for c in self.children  ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
# Node end


# search
class MonteCarloTreeSearch:
    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # exploitation only
        return self.root.best_child(c_param=0.)

    #function TREEPOLICY(v)
    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
# search end



# run
def init():
    state = np.zeros((3, 3))  
    #print("state",state)
    initial_board_state = TicTacToeGameState(state=state, next_to_move=1)
    print("initial_board_state.board",initial_board_state.board)  #  all zeros

    root = MonteCarloTreeSearchNode(state=initial_board_state, parent=None)
    print("root.state ",root.state)

    mcts = MonteCarloTreeSearch(root)

    best_node = mcts.best_action(1000)

    c_state = best_node.state
    c_board = c_state.board
    #print("c_board",c_board) #c_board [[0. 0. 0.] [0. 1. 0.] [0. 0. 0.]]
    return c_state,c_board

# print graph
def graphics(board):
    for i in range(3):
        print("")
        print("{0:3}".format(i).center(8)+"|", end='')
        for j in range(3):
            if c_board[i][j] == 0:
                print('_'.center(8), end='')
            if c_board[i][j] == 1:
                print('X'.center(8), end='')
            if c_board[i][j] == -1:
                print('O'.center(8), end='')
    print("")
    print("______________________________")


def get_action(state):
    try:
        location = input("Your move: ")
        if isinstance(location, str):
            location = [int(n, 10) for n in location.split(",")]
        if len(location) != 2:
            return -1
        x = location[0]
        y = location[1]
        move = TicTacToeMove(x, y, -1)
    except Exception as e:
        move = -1
    if move == -1 or not state.is_move_legal(move):
        print("invalid move")
        move = get_action(state)
    return move


def judge(state):
    if state.is_game_over():
        if state.game_result == 1.0:
            print("You lose!")
        if state.game_result == 0.0:
            print("Tie!")
        if state.game_result == -1.0:
            print("You Win!")
        return 1
    else:
        return -1



if __name__ == "__main__":
 

    c_state,c_board = init()
    #print("c_board",c_board)
    graphics(c_board)


    # function UCTSEARCH(s0)
    while True:
        move1 = get_action(c_state)
        c_state = c_state.move(move1)
        c_board = c_state.board
        graphics(c_board)

        board_state = TicTacToeGameState(state=c_board, next_to_move=1)
        root = MonteCarloTreeSearchNode(state=board_state, parent=None)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.best_action(1000)
        c_state = best_node.state
        c_board = c_state.board
        graphics(c_board)
        if judge(c_state)==1:
            break
        elif judge(c_state)==-1:
            continue
    # run end
    