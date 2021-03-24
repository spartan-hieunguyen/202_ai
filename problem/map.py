import search
import random
import time
# Module Classes

class City:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

COST_TABLE = [
    ['Oradea', 'Sibiu', 151],
    ['Oradea', 'Zerind', 71],
    ['Zerind', 'Arad', 75],
    ['Arad', 'Sibiu', 140],
    ['Arad', 'Timisoara', 118]
    ['Timisoara', 'Lugoj', 111],
    ['Pitesti', 'Lugoj', 120], #
    ['Sibiu', 'Fagaras', 99],
    ['Sibiu', 'Rimnicu Vilcea', 80],
    ['Rimnicu Vilcea', 'Pitesti', 97],
    ['Bucharest', 'Pitesti', 101],
    ['Bucharest', 'Fagaras', 211],
 ]   

CITIES = [
    {'name': 'Oradea', 'neighbor': ['Zerind', 'Sibiu']},
    {'name': 'Zerind', 'neighbor': ['Oradea', 'Arad']},
    {'name': 'Arad', 'neighbor': ['Zerind', 'Sibiu', 'Timisoara']},
    {'name': 'Sibiu', 'neighbor': ['Oradea', 'Arad', 'Fagaras', 'Rimnicu Vilcea']},
    {'name': 'Timisoara', 'neighbor': ['Arad', 'Lugoj']},
    {'name': 'Lugoj', 'neighbor': ['Timisoara', 'Pitesti']},
    {'name': 'Fagaras', 'neighbor': ['Sibiu', 'Bucharest']},
    {'name': 'Rimnicu Vilcea', 'neighbor': ['Sibiu', 'Pitesti']},
    {'name': 'Pitesti', 'neighbor': ['Rimnicu Vilcea', 'Lugoj', 'Bucharest']},
    {'name': 'Bucharest', 'neighbor': ['Pitesti', 'Fagaras']}
]

def getCost(cName1, cName2):
    for i in COST_TABLE:
        if cName1 in i and cName2 in i:
            return i[2]

def getCity(name):
    for c in CITIES:
        if name == c.name:
            return c.copy()

class MapState:
    def __init__( self, cities, cur, des ):    
        self.cities = cities    
        self.cur = getCity(cur)
        self.destination = des       

    def isGoal( self ):    
        if self.cur.name == self.des:
            return True
        return False

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.        
        """
        return self.cur.neighbor

    def result(self, move):
        """

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """                        
        # Create a copy of the current chess board        
        newMap = MapState(CITIES, move, self.des)        
        # And update it to reflect the move        
        return newMap

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 8, 5, 8, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 8, 5, 8, 7, 8]).result('left')
          True
        """
        if self.cur.name != other.cur.name:
            return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        return self.cur.name
        # lines = []
        # horizontalLine = ('-' * (17))
        # lines.append(horizontalLine)
        # for row in self.board:
        #     rowLine = ''
        #     for col in row:                
        #         rowLine = rowLine + ' ' + col.__str__()
        #     lines.append(rowLine)
        #     lines.append(horizontalLine)
        # return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class MapSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, map):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.map = map

    def getStartState(self):
        return map

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            cost = getCost(state.cur.name, a)
            succ.append((state.result(a), a, cost))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum(actions)

if __name__ == '__main__':
    rMap = MapState(CITIES, 'Oradea', 'Sibiu')
    problem = MapSearchProblem(rMap)
    startTime = time.time()    
    path = search.GraphSearch.findSolution(3)
    print("Cal: ", time.time() - startTime)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = rMap
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        input("Press return for the next state...")   # wait for key stroke
        i += 1
