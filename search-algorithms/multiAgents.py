# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect allowed moves and successor states
        allowedMoves = gameState.getAllowedActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in allowedMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return allowedMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessorState(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getAllowedActions(agentIndex):
        Returns a list of allowed actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessorState(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
                # Minimax για πολλούς agents: Pacman = max, Ghosts = min
        numAgents = gameState.getNumAgents()

        def minimaxValue(state, depth, agentIndex):
            """
            Επιστρέφει την minimax τιμή για το state.
            depth: πόσες κινήσεις Pacman έχουμε ήδη "ολοκληρώσει"
            agentIndex: ποιος παίζει τώρα (0 = Pacman, 1.. = ghosts)
            """

            # Τερματικές καταστάσεις ή αν φτάσαμε στο μέγιστο βάθος
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # Pacman (MAX)
            if agentIndex == 0:
                return maxValue(state, depth)
            # Ghost (MIN)
            else:
                return minValue(state, depth, agentIndex)

        def maxValue(state, depth):
            """Pacman: διαλέγει action που μεγιστοποιεί την τιμή."""
            best = float("-inf")

            for action in state.getAllowedActions(0):
                successor = state.generateSuccessorState(0, action)
                best = max(best, minimaxValue(successor, depth, 1))

            return best

        def minValue(state, depth, agentIndex):
            """Ghost: διαλέγει action που ελαχιστοποιεί την τιμή."""
            best = float("inf")

            nextAgent = agentIndex + 1
            nextDepth = depth

            # Αν τελείωσαν όλα τα ghosts, επιστρέφουμε στον Pacman και αυξάνουμε depth
            if nextAgent == numAgents:
                nextAgent = 0
                nextDepth = depth + 1

            for action in state.getAllowedActions(agentIndex):
                successor = state.generateSuccessorState(agentIndex, action)
                best = min(best, minimaxValue(successor, nextDepth, nextAgent))

            return best

        # Επιλέγουμε την καλύτερη κίνηση για τον Pacman (ρίζα του minimax)
        bestAction = Directions.STOP
        bestScore = float("-inf")

        for action in gameState.getAllowedActions(0):
            successor = gameState.generateSuccessorState(0, action)
            score = minimaxValue(successor, 0, 1)  # ξεκινάμε depth=0 και μετά τον Pacman παίζει ghost 1

            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        numAgents = gameState.getNumAgents()

        def alphabetaValue(state, depth, agentIndex, alpha, beta):
            # Terminal ή depth limit
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # Αν δεν υπάρχουν κινήσεις (ασφάλεια)
            actions = state.getAllowedActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            # Pacman (MAX)
            if agentIndex == 0:
                return maxValue(state, depth, alpha, beta)
            # Ghosts (MIN)
            else:
                return minValue(state, depth, agentIndex, alpha, beta)

        def maxValue(state, depth, alpha, beta):
            v = float("-inf")

            for action in state.getAllowedActions(0):
                successor = state.generateSuccessorState(0, action)
                v = max(v, alphabetaValue(successor, depth, 1, alpha, beta))

                # ενημέρωση alpha
                alpha = max(alpha, v)

                # PRUNE (ΠΡΟΣΟΧΗ: strict >, όχι >=)
                if v > beta:
                    return v

            return v

        def minValue(state, depth, agentIndex, alpha, beta):
            v = float("inf")

            nextAgent = agentIndex + 1
            nextDepth = depth

            # αν τελείωσαν τα ghosts -> επιστρέφουμε στον Pacman και αυξάνουμε depth
            if nextAgent == numAgents:
                nextAgent = 0
                nextDepth = depth + 1

            for action in state.getAllowedActions(agentIndex):
                successor = state.generateSuccessorState(agentIndex, action)
                v = min(v, alphabetaValue(successor, nextDepth, nextAgent, alpha, beta))

                # ενημέρωση beta
                beta = min(beta, v)

                # PRUNE (ΠΡΟΣΟΧΗ: strict <, όχι <=)
                if v < alpha:
                    return v

            return v

        # Root: επιλογή κίνησης για Pacman
        bestAction = Directions.STOP
        bestScore = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for action in gameState.getAllowedActions(0):
            successor = gameState.generateSuccessorState(0, action)
            score = alphabetaValue(successor, 0, 1, alpha, beta)

            if score > bestScore:
                bestScore = score
                bestAction = action

            # ενημέρωση alpha στο root
            alpha = max(alpha, bestScore)

        return bestAction



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        allowed moves.
        """
        numAgents = gameState.getNumAgents()

        def expectimaxValue(state, depth, agentIndex):
            # Terminal ή depth limit
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            actions = state.getAllowedActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            # Pacman (MAX)
            if agentIndex == 0:
                v = float("-inf")
                for action in actions:
                    successor = state.generateSuccessorState(0, action)
                    v = max(v, expectimaxValue(successor, depth, 1))
                return v

            # Ghosts (EXPECTED VALUE)
            else:
                nextAgent = agentIndex + 1
                nextDepth = depth

                # αν τελείωσαν τα ghosts -> επιστρέφουμε στον Pacman και αυξάνουμε depth
                if nextAgent == numAgents:
                    nextAgent = 0
                    nextDepth = depth + 1

                total = 0.0
                prob = 1.0 / len(actions)  # ομοιόμορφη πιθανότητα
                for action in actions:
                    successor = state.generateSuccessorState(agentIndex, action)
                    total += prob * expectimaxValue(successor, nextDepth, nextAgent)

                return total

        # Root: διαλέγουμε κίνηση για Pacman
        bestAction = Directions.STOP
        bestScore = float("-inf")

        for action in gameState.getAllowedActions(0):
            successor = gameState.generateSuccessorState(0, action)
            score = expectimaxValue(successor, 0, 1)

            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction



def betterEvaluationFunction(currentGameState: GameState):
    """
    A better evaluation function for the Pacman game state.
    """
    # Βασικό σκορ του παιχνιδιού
    score = currentGameState.getScore()

    pacPos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    foodList = foodGrid.asList()

    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [g.scaredTimer for g in ghostStates]
    ghostPositions = [g.getPosition() for g in ghostStates]

    # Manhattan helper
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # 1) Φαγητό: θέλουμε να είμαστε κοντά στο κοντινότερο food
    if foodList:
        minFoodDist = min(manhattan(pacPos, f) for f in foodList)
        # όσο πιο κοντά, τόσο καλύτερα → αφαιρούμε απόσταση
        score += 10.0 / (minFoodDist + 1)

        # επίσης, λιγότερα foods = καλύτερα
        score -= 2.0 * len(foodList)

    # 2) Φαντάσματα
    for ghostPos, scared in zip(ghostPositions, scaredTimes):
        d = manhattan(pacPos, ghostPos)

        if scared > 0:
            # Αν είναι scared, θέλουμε να το πλησιάσουμε (για να το φάμε)
            score += 20.0 / (d + 1)
        else:
            # Αν δεν είναι scared, θέλουμε να το αποφύγουμε
            # Αν είναι ΠΟΛΥ κοντά, βαριά ποινή
            if d <= 1:
                score -= 200
            else:
                score -= 5.0 / d

    return score


# Abbreviation
better = betterEvaluationFunction
