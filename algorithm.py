import random
import numpy as np
import copy

# class defining the nodes used in a monte carlo search algorithm
# each node will have a parent (beside the root node) and each node will correspond to a specific gamestate
# these gamestates could be redundant based on move order.
# for example, there are 2 nodes that correspond to [x, o, x, -, -, -, -, -, -]
# the first is if the x player places the x in the 3rd index on their first move
# the second is if the x player places the x in the 3rd index on their second move.
# these redundant nodes could be pruned out, but since tic tac toe is not that complex, we arent running
# into too many copies where we are taking a long time to compute the best move.


class Node:
    def __init__(self, gamestate, parent):
        # Need to keep track of the children to each node, whether or not the node is terminal, the number of visits
        # to that specific node, the parent of each node, and also the actual gamestate the node is corresponding to
        self.game = gamestate
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.ucb = 0
        self.terminal = self.game.check_end()
        self.expanded = 0
        self.children = []


class MonteCarlo:
    def __init__(self, iterations, constant):
        self.iterations = iterations
        self.explore = constant

    def find_best(self, game):
        # define a root node
        self.start = Node(game, None)
        # for loop is used to change the amount of iterations the algorithm trains on
        for iterations in range(self.iterations):
            # the main steps of the monte carlo algorithm are:
            # 1. Selection
            # 2. Expansion
            # 3. Simulation
            # 4. Backpropagation
            # I skip over expansion here because it's only called in selection when we want to select a node that
            # has yet to be expanded.

            # select a node. If not all children exist yet, expand and test the expansion.
            node = self.select(self.start)

            # simulate the selected node and return the result of the game simulated.
            returned_reward = self.simulate(node.game)
            # backpropagate through the tree updating the visits and total reward of each parent node.
            # nothing is returned from backprop because we are just modifying the tree in place.
            self.backprop(node, returned_reward, self.explore)

        best_move = self.get_best_child(self.start)
        # best move is a child, so find the actual move made in best_move by comparing it's games gamestate with root.
        index = 0

        for move in best_move.game.gamestate:
            if self.start.game.gamestate[index] is not move:
                return index
            index += 1

    #                                      SELECTION STEP                                            #
    # We are starting at a root node. We want to move down the tree by selecting the best child of each node
    # until we reach a node that has no children. It could have no children because it is yet to be expanded,
    # so check if it is entirely expanded.
    def select(self, node):
        # While loop will end on the last parent nodes.

        # check to see if the current node is entirely expanded.
        # if the current node is terminal, pick
        # if the current node is entirely expanded, then pick the best node.
        # if the current node isnt expanded, then expand once and return the expansion node




        while node.terminal == 0:
            # If the last parent node is entirely expanded, the length of the valid moves array in the game object
            # will be equal to the length of the list of children.
            if len(node.game.valid_moves()) == len(node.children):
                # look for its best child
                node = self.get_best_child(node)

            else:
                # The only ELSE is if the node isn't entirely expanded, so expand it and return the expanded version.
                return self.expand(node)
        # node being returned is either a node that was expanded upon and should be evaluated, or the best move
        return node.parent

    #                                     EXPANSION STEP                                             #
    # The expansion function is given a node. Each node either has anywhere between 0 and 8 children ( 9 total )
    # Each node has a game. Each game has a list of valid moves in ascending order. Look at each element of that list
    # and try to check if there is a child related to it. If that child does not exist, then create a new node and
    # append it to the list of children. Take this node containing the single new child and return it to be
    # simulated and evaluated for backpropagation.
    def expand(self, node):
        index = 0
        if node.terminal is not 0:
            print("TRIED EXPANDING A TERMINAL NODE")
            return node
        valid_moves = node.game.valid_moves()
        # Theoretically this if statement below is redundant. We check if the node is a terminal node in the
        # parent function. Just checking to be sure I guess.
        if len(node.game.valid_moves()) == 0:
            return node
        # if there are no children, just create a child and return the node
        if len(node.children) == 0:
            # Copy over the game from the current node and make the valid move. Create a new
            # node using this "new" game and append this node to the list of children of the parent.
            temp = copy.deepcopy(node.game)
            temp.move(valid_moves[0])
            child_node = Node(temp, node)
            if temp.check_end() is not 0:
                child_node.terminal = 1
            node.children.append(child_node)
            # Return the child node to be evaluated.
            return child_node
        # if there are children, go through the list of valid moves and make sure they are accounted for.
        valid = valid_moves[len(node.children)]
        # Copy over the game from the current node and make the valid move. Create a new
        # node using this "new" game and append this node to the list of children of the parent.
        temp = copy.deepcopy(node.game)
        temp.move(valid)
        child_node = Node(temp, node)
        if temp.check_end() is not 0:
            child_node.terminal = 1
        node.children.append(child_node)
        # Return the child node to be evaluated.
        return child_node
        # There should not be any other case. If the list of children is iterated through and all the valid
        # moves are indeed present, then this function should have never been called.

    #                                            SIMULATION STEP                                            #
    # This following function is used to simulate a random game given a current gamestate and then return the value
    # of the simulated result. The algorithm winning results in a positive 1 being returned, a draw results in 0, and
    # if the algorithm's opponent wins, a negative one is returned. This is because we want to positively reward winning
    # and give negative reinforcement to losing.
    def simulate(self, game):
        if game.check_end() is not 0:
            if game.check_end() == 1:
                return 0
            if game.check_end() == 2:
                if game.botturn:
                    return -1
                if game.playerturn:
                    return 1
        temp = copy.deepcopy(game)
        moves = temp.valid_moves()
        # select random moves by shuffling the list of valid moves.
        random.shuffle(moves)
        # Turns are flipped after moves are made, but before wins are checked. To correctly declare a winner,
        # check if 1 or 2 was returned from check_end(). If 1 was returned, there isn't a winner and return 0 for a draw
        # If 2 was returned, the person whose turn it currently is after check_end() is called is the loser.
        for m in moves:
            temp.move(m)
            check = temp.check_end()
            if check == 1:
                return 0
            if check == 2:
                if temp.botturn:
                    return -1
                if temp.playerturn:
                    return 1


    #                                            BACKPROPAGATION STEP                                       #
    # The algorithm for backprop is to take the result returned from the simulation and update all nodes up to the root
    # by adding the result of the simulation to their value and increasing the respective counts.
    # Nothing needs to be returned because we are just modifying the entire tree in place.
    # This function takes an additional argument constant. This constant is used to fine tune the amount of exploration
    # that the algorithm does. I write more about this in the paper, but in short, it is to make sure we are exploring
    # multiple paths down the tree. This ties into the concept of exploration vs exploitation.
    # The UCB is the upper confidence bound for a specific node. It is calculated using the formula provided in the
    # paper. The child with the highest UCB will be selected in the get_best_child function.
    def backprop(self, node, reward, constant):
        # if statement to check if we've modified everything. If the node is none, then we've updated the root.
        if node is None:
            return
        if node.parent is None:
            node.visits += 1
            return
        else:
            node.score += reward
            node.visits += 1
            # recursive call to move up the tree
            self.backprop(node.parent, reward, self.explore)
            node.ucb = node.score/node.visits + (constant * np.sqrt(np.log(node.parent.visits)/node.visits))




    #                                       SELECTING THE BEST CHILD NODE                                   #
    # This step is a part of the selection step. All it does is just look through the list of children of a node
    # and selects the best child. Function is never called before children exists, so it will always return
    # whatever child has the best uct.
    def get_best_child(self, node):
        # arbitrarily large placeholder value for the best uct of the children.
        best = -999999999
        best_options = []
        for child in node.children:
            if child.ucb > best:
                best = child.ucb
                best_options = [child]
            if child.ucb == best:
                best_options.append(child)
        return random.choice(best_options)
