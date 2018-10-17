
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

    # while loop exits if a leaf node is found
    while(not node.untried_actions and node.child_nodes):

        # this node will be the next node to traverse to
        node_to_traverse = None

        # use the equation to pick which branch to go on (FROM LECTURE)
        # c is the exploration/exploitation factor, idk what to set it at rn
        best_value = 0;
        c = 100

        # select a child nodes to explore
        for child_node in node.child_nodes:
            value = child_node.wins/child_node.visits + c*sqrt(log(child_node.parent.visits)/child_node.visits)
            if value > best_value:
                best_value = value
                node_to_traverse = child_node

        node = node_to_traverse

    # return child node
    return node

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
    # NOTE - board is now changed, bc move was tried and board is a reference
    board.next_state(state, random_action)
    possible_actions = board.legal_actions(new_state)

    # make tha fookin' node
    child_node = MCTSNode(node, random_action, possible_actions)

    # adjust parent node's untried action list and child node dict
    node.child_nodes[random_action] = child_node
    node.untried_actions.remove(random_action)

    return child_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    # play until someone wins
    while not board.is_ended(state):
        actions = board.legal_actions(state)
        random_action = choice(actions)
        board.next_state(state, random_action)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    #go through tree until root node's parent, which is None
    while(node is not None):
        node.wins += node.wins
        node.visits += node.visits
        node = node.parent

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

        # Do MCTS lmaoooo
        child_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        expanded_node = expand_leaf(child_node, board, sampled_game)
        rollout(board, sampled_game)

        # check who won
        if (board.points_values(sampled_game)[identity_of_bot] is 1) 
            backpropogate(expanded_node, True)
        else
            backpropogate(expanded_node, False)

    # select an action after MCTS has built the tree
    win_rate = 0
    action = None
    for child_node in node.child_nodes
        child_node_wr = child_node.wins/child_node.visits
        if child_node_wr > win_rate
            win_rate = child_node_wr
            action = child_node
    return action


    #ASK HOW TREE WORKS- ARE ALL THINGS FROM ROOT EXPLORED BEFORE THE REST??????????????

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.    