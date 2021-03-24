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
        path = list()

        while parNode:
            path.insert(0, parNode.getAction())
            parNode = parNode.getParent()
        path.remove(None)
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

class GraphSearch:

    def __init__(self, problem):
        self.problem = problem
        self.count = util.Counter()

    def findSolution(self, kind, limit=0):
        """
        Function use to find solution of graph search problem
        -----------------------------------------
        Param:
            kind: type of search 
                1: bfs
                2: dfs
                3: ucs
        """
        self.startState = self.problem.getStartState()
        print("Start:\n", self.startState)
        self.startNode = Node(self.startState)

        if kind == 1:
            frontier = util.Queue()
            return self.findPath(frontier=frontier)
        elif kind == 2: 
            frontier = util.Stack()
            return self.findPath(frontier=frontier)
        elif kind == 3:
            frontier = util.PriorityQueue()
            return self.uniformCostSearch(frontier=frontier)
        elif kind == 4:
            result = self.depthLimitedSearch(limit)
            if result in [CUT_OFF, FAILURE]: return []
            else: return result
        elif kind == 5:
            depth = 0
            while True:
                result = self.depthLimitedSearch(depth)
                if result not in [CUT_OFF, FAILURE]:
                    return result
                elif result is FAILURE: return []
                depth += 1

    def depthLimitedSearch(self, limit):
        def recurDLS(node, limit):  
            state = node.getState()
            if self.problem.isGoalState(state): 
                return node.getPath()
            elif limit == 0: return CUT_OFF
            else:
                cutOff = False 
                succ = self.problem.getSuccessors(state)
                for state, action, cost in succ:
                    newNode = Node(state, node, action, cost)
                    result = recurDLS(newNode, limit - 1)
                if result == CUT_OFF: cutOff = True
                elif result is not FAILURE:
                    return result
                return CUT_OFF if cutOff else FAILURE

        return recurDLS(self.startNode, limit)                


    def uniformCostSearch(self, frontier):
        """Search the node of least total cost first."""
        "*** YOUR CODE HERE ***"
        def getCostOfActions(actions):
            return self.problem.getCostOfActions(actions)

        def isInFrontier(node, frontier):
            state = node.getState()
            actions = node.getCostActions()
            pathCost = getCostOfActions(actions)

            tmpFrontier = util.PriorityQueue()
            while not frontier.isEmpty():
                currentNode = frontier.pop()
                cActions = currentNode.getCostActions()
                cPathCost = getCostOfActions(cActions)

                if state == currentNode.getState() and\
                    pathCost < cPathCost:

                    tmpFrontier.update(node, pathCost)
                else:
                    tmpFrontier.update(currentNode, cPathCost)
            return tmpFrontier
                

        frontier.push(self.startNode, 0)
        explored = []        

        while not frontier.isEmpty():
            currentNode = frontier.pop()
            currentState = currentNode.getState()

            if self.problem.isGoalState(currentState): 
                return currentNode.getPath()            
            explored.append(currentState)

            succ = self.problem.getSuccessors(currentState)
            for state, action, cost in succ:
                newNode = Node(state, currentNode, action, cost)                
                if state not in explored:
                    actions = newNode.getCostActions()
                    pathCost = getCostOfActions(actions)
                    frontier.update(newNode, pathCost)
                frontier = isInFrontier(newNode, frontier)

        util.raiseNotDefined()
           
    def findPath(self, frontier):
        frontier.push(self.startNode)
        explored = []
        if self.problem.isGoalState(self.startState): 
            return self.startNode.getPath()
        # looping to find solution
        while not frontier.isEmpty():        
            currentNode = frontier.pop()                    
            curState = currentNode.getState()      
            
            explored.append(curState)
            succ = self.problem.getSuccessors(curState)
            
            if isinstance(frontier, util.Stack):
                succ = succ[::-1] 
            for state, action, cost in succ: 
                newNode = Node(state, currentNode, action, cost)
                if state not in explored:
                    if self.problem.isGoalState(state): 
                        return newNode.getPath()
                    frontier.push(newNode)            

        print("Can't find any solutions!")
        return []  
   

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


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
# bfs = breadthFirstSearch
# dfs = depthFirstSearch
# astar = aStarSearch
# ucs = uniformCostSearch