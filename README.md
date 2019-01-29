mcts
====

Monte-Carlo Tree Search Implementation for general purpose.


https://github.com/muupan/mcts


https://medium.com/swlh/tic-tac-toe-at-the-monte-carlo-a5e0394c7bc2


The cpp project: using MCTS to play Tic-Tac-Toe

The python file: using MCTS to play the game making all sum to 1

井字游戏的规则是：在一个井字格子的棋盘里下棋，横竖斜一旦三子连子，则胜。而事实上，遵循一定的规则，该游戏便能保证不败，即至少是平局。 
若是两人对战，则仅需要判断“胜负平”三种状态即可，比较简单，而人机对战的难点便在于让机器立于不败之地的下棋规则。下面会重点讲解不败的思路。


Tic Tac Toe, like other turn based games where information is not hidden and game mechanics are not reliant on chance, is a perfect information game. This type of game allows every player to predict all possible outcomes from someone’s action. Since the game if fully deterministic, a tree can be constructed with all the possible outcomes from the game with each node of the tree given a value determining its win or loss ratio for each player.

An AI can then traverse this tree and choose a node it deems most likely to lead to a victory.
 If the AI’s strategy in choosing nodes is to pick the node with the smallest possibility of losing, 
 it would be utilizing a minimax strategy. While in theory this sounds like a feasible game plan, 
 in practice the amount of time to render a full game tree and then traverse it can be unrealistic 
 especially for games with large amounts of possible moves (high branching factor) like Go. 
 This is where the Monte Carlo tree search algorithm comes in.
 
 
 Monte Carlo tree search (MCTS) is a heuristic search algorithm that is employed for a large number of game playing AIs. 
 Most notable of them is the Go AI, Alpha Go. MCTS shines in games with high branching factors because 
 unlike minimax which needs a full game tree, MCTS can be configured to stop after a desired amount of time 
 and can select a sufficiently optimal solution based on the partially constructed game tree.  
 While a pure Monte Carlo process would run a multitude of randomly simulated game states, 
 MCTS keeps statistics of each nodes and then applies the Upper Confidence Bound (UCB) algorithm to the node’s stats.
 
 
 There are four basic phases to MCTS: selection, expansion, simulation,and back-propagation
