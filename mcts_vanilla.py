hddddddddddddddd
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    # so i never used board, state, or identity so idk if i fukked up lmao
    # also it's unfinished

    # while loop exits if a leaf node is chosen
    while(true):

        # this node will be the next node to traverse to
        node_to_traverse = None

        # use the equation to pick which branch to go on (FROM LECTURE)
        # c is the exploration/exploitation factor, idk what to set it at rn
        best_value = 0; 
        c = 100

        # first, explore the child nodes
        for child_node in node.child_nodes:
            value = child_node.wins/child_node.visits + c*sqrt(log(child_node.parent.visits)/child_node.visits)
            if value > best_value:
                best_value = value
                node_to_traverse = child_node

        # then, explore the untried actions
        for action in node.untried_actions: 
            #okay i have no idea what to do here
            #the equation doesn't apply??
            #also, if an untried action is picked, I guess I return the parent node
            #because there is no created node for the untried action?

        node = node_to_traverse

        # if node has no children, it is a leaf, so return it
        if not node.child_nodes
            return node

    return False # something messed up probably

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    # arbitrarily pick action from the node
    random_action = choice(node.untried_actions)

    # find all possible actions after that action is made 
    # NOTE - is board a reference or a copy? Should we undo the action? if so how?
    new_state = board.next_state(state, random_action)
    possible_actions = board.legal_actions(new_state)

    # make tha fookin' node
    child_node = MCTSNode(node, random_action, possible_actions)

    # adjust parent node's untried action list and child node dict
    node.child_nodes[random_action] = child_node
    node.untried_actions.remove(randome_action)

    return child_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
