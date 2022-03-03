# Reinforcement learning applied to adversarial games
In this project I aim to apply a Monte Carlo Tree Search (MCTS) algorithm to Tic Tac Toe and see how the performance is changed under different configurations of the algorithm. This project was designed by myself, but completed as a project for a machine learning course at my university. 
The reason I chose TicTacToe as my adversarial game of choice is because the relatively limited number of gamestates compared to something like chess. I hopefully will be able to branch out to other games using other algorithms soon.
# General algorithm and methods:
The general algorithm that I followed to implement this MCTS is as follows:
  1.Given a string corresponding to a specific game state, create a node containing a value and a counter for the number of times the node is visited.
  2. Select the node’s best child node by picking the child with the highest UCB. If the node does not have all of their children, then add and select another unique child node.
  3. Take the selected node and simulate a game by playing moves randomly for each player until the game is over. The game is only over when there are 3 of the same pieces connected, or if there are no more available moves to make. If 3 pieces are connected, the result of the simulation will be -1 if the opponent won or +1 if the algorithm won. If the game does not have a winner, the game has been drawn and the result will be 0.
  4. Take the result and add it to the child node we previously selected. Since we visited this child node, increment it’s number of visits.\
  5. Propagate back up the tree of nodes, updating the value by adding the result of the simulation to the value of node. Increment the count of each node we update. Each time we are about to go to the parent node, update the child of the current nodes UCB value.
  6. Repeat starting from step 2.
 The upper confidence bound (UCB) is calculated using the formula x + C(sqrt(ln(N/n))) where x is the mean value of a node, C is an exploration constant used to tune the amount that we want to deviate away from the best current optimal choice, N is the number of times the parent node has been visitied, and n is the number of times the node has been visited.
 The performance of this algorithm is tested with a static exploration constant + dynamic iteration number as well as a static iteration number + dynamic exploration constant.
# Results:
 Constant Iterations:
 
