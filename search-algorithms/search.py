# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartingState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessorStates(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):

    """ Search the deepest nodes in the search tree first.   """

    # Frontier για DFS: Stack (LIFO)
    frontier = util.Stack()
    start_state = problem.getStartingState()

    # Αν το start είναι ήδη goal, δεν χρειάζεται κίνηση
    if problem.isGoalState(start_state):
        return []

    # Κάθε στοιχείο στο frontier: (state, actions_so_far)
    frontier.push((start_state, []))

    # visited κρατάει states που έχουμε ήδη "δει"
    visited = set()

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        # Αν το είδαμε ήδη, το αγνοούμε (graph search)
        if state in visited:
            continue

        visited.add(state)

        # Goal test
        if problem.isGoalState(state):
            return actions

        # Expand successors
        for successor, action, stepCost in problem.getSuccessorStates(state):
            if successor not in visited:
                frontier.push((successor, actions + [action]))

    # Αν δεν βρεθεί λύση
    return []

    

def breadthFirstSearch(problem: SearchProblem):

    """ Search the shallowest nodes in the search tree first.   """

    # Frontier για BFS: Queue (FIFO)
    frontier = util.Queue()
    start_state = problem.getStartingState()

    # Αν το start είναι ήδη goal, δεν χρειάζεται κίνηση
    if problem.isGoalState(start_state):
        return []

    # Κάθε στοιχείο στο frontier: (state, actions_so_far)
    frontier.push((start_state, []))

    # visited κρατάει states που έχουμε ήδη "δει"
    visited = set()

    # Στο BFS το βάζουμε από την αρχή, όταν το κάνουμε enqueue, για να μην μπει πολλές φορές στην ουρά το ίδιο state
    visited.add(start_state)

    while not frontier.isEmpty():
        # Παίρνουμε το πιο παλιό στοιχείο που μπήκε (FIFO)
        state, actions = frontier.pop()

        # Goal test
        if problem.isGoalState(state):
            return actions

        # Expand successors
        for successor, action, stepCost in problem.getSuccessorStates(state):
            # Αν δεν το έχουμε ξαναδεί, το προσθέτουμε
            if successor not in visited:
                visited.add(successor)
                # Νέα διαδρομή: παλιά actions + η καινούρια action
                frontier.push((successor, actions + [action]))

    # Αν δεν βρεθεί λύση
    return []



def uniformCostSearch(problem: SearchProblem):

    """ Search the node of least total cost first.  """

    # Frontier για UCS: PriorityQueue
    frontier = util.PriorityQueue()
    start_state = problem.getStartingState()

    # Αν το start είναι ήδη goal, δεν χρειάζεται κίνηση
    if problem.isGoalState(start_state):
        return []

    # Κάθε στοιχείο στο frontier: (state, actions_so_far, cost_so_far)
    # Στο start το κόστος είναι 0
    frontier.push((start_state, [], 0), 0)

    # best_cost κρατάει το μικρότερο κόστος που έχουμε βρει για κάθε state
    best_cost = {}
    best_cost[start_state] = 0

    while not frontier.isEmpty():
        state, actions, cost_so_far = frontier.pop()

        # Αν αυτό το node δεν είναι πλέον το καλύτερο για το state (βρήκαμε φθηνότερο),το αγνοούμε
        if cost_so_far > best_cost.get(state, float("inf")):
            continue

        # Goal test
        if problem.isGoalState(state):
            return actions

        # Expand successors
        for successor, action, stepCost in problem.getSuccessorStates(state):
            new_cost = cost_so_far + stepCost

            # Αν είναι η πρώτη φορά ή βρήκαμε φθηνότερο δρόμο προς το successor
            if new_cost < best_cost.get(successor, float("inf")):
                best_cost[successor] = new_cost
                frontier.push((successor, actions + [action], new_cost), new_cost)

    # Αν δεν βρεθεί λύση
    return []



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):

    """ Search the node that has the lowest combined cost and heuristic first.  """

    # Frontier για A*: PriorityQueue
    frontier = util.PriorityQueue()
    start_state = problem.getStartingState()

    # Αν το start είναι ήδη goal, δεν χρειάζεται κίνηση
    if problem.isGoalState(start_state):
        return []

    # Κάθε στοιχείο στο frontier: (state, actions_so_far, cost_so_far=g)
    start_cost = 0
    start_priority = start_cost + heuristic(start_state, problem)
    frontier.push((start_state, [], start_cost), start_priority)

    # best_cost κρατάει το μικρότερο g που έχουμε βρει για κάθε state
    best_cost = {}
    best_cost[start_state] = 0

    while not frontier.isEmpty():
        state, actions, cost_so_far = frontier.pop()

        # Αν αυτό δεν είναι πλέον το καλύτερο g για το state (βρήκαμε φθηνότερο), αρα το αγνοούμε
        if cost_so_far > best_cost.get(state, float("inf")):
            continue

        # Goal test
        if problem.isGoalState(state):
            return actions

        # Expand successors
        for successor, action, stepCost in problem.getSuccessorStates(state):
            new_cost = cost_so_far + stepCost  # νέο g

            # Αν είναι καλύτερος δρόμος προς το successor
            if new_cost < best_cost.get(successor, float("inf")):
                best_cost[successor] = new_cost

                # f = g + h
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, actions + [action], new_cost), priority)

    # Αν δεν βρεθεί λύση
    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
