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
FAILURE = "FAILURE"
CUT_OFF = "CUTOFF"

import util

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost        
        self.depth = self.parent.getDepth() + 1\
            if self.parent is not None else 0        

    def getState(self):
        return self.state
    
    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getCost(self):
        return self.cost

    def getPath(self):
        parNode = self.parent
        if parNode is None: return []

        action = parNode.getAction()
        path = list()

        while action is not None:
            path.insert(0, action)
            parNode = parNode.getParent()
            action = parNode.getAction()            
        path.append(self.action)

        return path

    def getCostActions(self):
        parrentNode = self.parent
        actions = list()

        while parrentNode:
            actions.insert(0, parrentNode.getCost())
            parrentNode = parrentNode.getParent()        
        actions.append(self.cost)
        
        return actions

    def getDepth(self):
        return self.depth    

    def __eq__(self, other):
        if self.state == other.state:
            return True
        return False    

class GraphSearch:

    def __init__(self, problem):
        self.problem = problem
        self.explored = util.Counter()        
        print("Start:\n", self.problem.getStartState())

    def expandNode(self, node, frontier, func):
        succ = self.problem.getSuccessors(node.getState())

        if isinstance(frontier, util.Stack):
            succ = succ[::-1]

        for state, action, cost in succ: 
            newNode = Node(state, node, action, cost)
            if hash(state) not in self.explored:
                func(newNode, frontier)

    def getCostOfActions(self, actions):
        return 0 if not actions else\
            self.problem.getCostOfActions(actions)

    def addPriorQueue(self, node, frontier):
        actions = node.getCostActions()
        pathCost = self.getCostOfActions(actions)            
        frontier.update(node, pathCost)

    def addSQ(self, node, frontier):
        frontier.push(node)

    def search(self, frontier, limit=None):

        startNode = Node(self.problem.getStartState())

        if isinstance(frontier, util.Stack) or\
            isinstance(frontier, util.Queue): 
            f = self.addSQ
        elif isinstance(frontier, util.PriorityQueue):
            f = self.addPriorQueue
        
        f(startNode, frontier)     
        while not frontier.isEmpty():
            currentNode = frontier.pop()                    
            currentState = currentNode.getState()      

            if limit is not None and\
                currentNode.getDepth() > limit and\
                frontier.isEmpty():
                
                return CUT_OFF

            if self.problem.isGoalState(currentState):
                return currentNode.getPath()            
            self.explored[hash(currentState)] = currentState
            self.expandNode(currentNode, frontier, f)
        
        return FAILURE        

class InformedGraphSearch(GraphSearch): 
    def __init__(self, problem, heuristic, typ):
        super().__init__(problem)
        self.heuristic = heuristic
        self.type = typ

    def addPriorQueue(self, node, frontier):
        actions = node.getCostActions()                
        g = self.getCostOfActions(actions)
        h = self.heuristic(node.getState())
        if self.type == 'BFS':
            f = h
        else:
            f = g + h        
        frontier.update(node, f)        

    # def expandNode(self, node, frontier, func):
    #     succ = self.problem.getSuccessors(node.getState())
        
    #     for state, action, cost in succ:
    #         newNode = Node(state, node, action, cost)
    #         if hash(state) not in self.explored:


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
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

    def getSuccessors(self, state):
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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    path = GraphSearch(problem).search(frontier)
    return path
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    path = GraphSearch(problem).search(frontier)
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    path = GraphSearch(problem).search(frontier)
    return path

def depthLimitedSearch(problem, limit):
    frontier = util.Stack()
    path = GraphSearch(problem).search(frontier, limit)
    return path

def iterativeDeepeningSearch(problem):
    frontier = util.Queue()
    depth = 1
    while True:
        path = GraphSearch(problem).search(frontier, depth)
        if path is not CUT_OFF: return path
        depth += 1

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    path = InformedGraphSearch(problem, heuristic, 'ASS').search(frontier)
    return path
    # util.raiseNotDefined()

def greedyBestFirstSearch(problem, heuristic=nullHeuristic):
    frontier = util.PriorityQueue()
    path = InformedGraphSearch(problem, heuristic, 'BFS').search(frontier)
    return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
dls = depthLimitedSearch
ids = iterativeDeepeningSearch
astar = aStarSearch
gbfs = greedyBestFirstSearch
ucs = uniformCostSearch