from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.


# traverse nodes how does it work???
def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.
    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.
    """
    #if the node is a leaf node
    if (node.untried_actions):
        return node, state
    #if node is end of branch
    elif not node.untried_actions and not node.child_nodes:
        return node, state

    node_to_traverse = None
    best_value = -1
    c = 100

    # select a child node to explore
    for action, child_node in node.child_nodes.items():
        value = child_node.wins / child_node.visits + c * sqrt(log(child_node.parent.visits) / child_node.visits)
        if value > best_value:
            best_value = value
            node_to_traverse = child_node

    state = board.next_state(state, node_to_traverse.parent_action)
    return traverse_nodes(node_to_traverse, board, state, identity)

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.
    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.
    """
    #if the node is a deadend, don't expand!
    if (not node.untried_actions):
        return node, state

    # arbitrarily pick action from the node
    random_action = choice(node.untried_actions)

    # find all possible actions after that action is made
    # NOTE - board is now changed, bc move was tried and board is a reference
    state = board.next_state(state, random_action)
    possible_actions = board.legal_actions(state)

    # make tha fookin' node
    child_node = MCTSNode(node, random_action, possible_actions)

    # adjust parent node's untried action list and child node dict
    node.child_nodes[random_action] = child_node
    node.untried_actions.remove(random_action)

    return child_node, state


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
        state = board.next_state(state, random_action)
    return state


def backpropagate(node, condition):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.
    """

    # go through tree until root node's parent, which is None
    if condition == 1:
        while node is not None:
            node.wins = node.wins + 1
            node.visits = node.visits + 1
            node = node.parent
    #do same for conditions 0 & 2
    else:
        while node is not None:
            node.visits = node.visits + 1
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
        child_node, sampled_game = traverse_nodes(node, board, sampled_game, identity_of_bot)
        expanded_node, sampled_game = expand_leaf(child_node, board, sampled_game)
        sampled_game = rollout(board, sampled_game)

        # check who won
        # if node couldn't be expanded, mark down that it was visited but no win/loss.
        # I'M NOT SURE IF THE ABOVE IS RIGHT BUT SOMETHING NEEDS TO HAPPEN ! 
        # 0: node is an end point 1: player has won 2: player has lost
        if (not expanded_node.untried_actions):
            backpropagate(expanded_node, 0)
        if board.points_values(sampled_game)[identity_of_bot] is 1:
            backpropagate(expanded_node, 1)
        else:
            backpropagate(expanded_node, 2)

    # select an action after MCTS has built the tree
    win_rate = 0
    best_action = None
    for action, child_node in node.child_nodes.items():
        child_node_wr = child_node.wins/child_node.visits
        if child_node_wr > win_rate:
            win_rate = child_node_wr
            best_action = action
    return action