import search
import random
import time

class VacuumState:
    def __init__( self, m, n, initPos ):    
        self.floor = []
        for i in range(m):
            row = ['_'] * n
            self.floor.append(row.copy())
        self.vacPos = initPos

    def isGoal( self ):
        sum = 0
        for i in range(len(self.floor)):
            sum += self.floor[i].count('_')
        size = len(self.floor) * len(self.floor[0])
        if sum == size:
            return True
        return False

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.        
        """
        moves = []
        if self.floor[self.vacPos[0]][self.vacPos[1]] == '.':
            moves.append('suck')
        if self.vacPos[1] != 0:
            moves.append('left')
        if self.vacPos[1] != len(self.floor[0]) - 1:
            moves.append('right')
        if self.vacPos[0] != 0:
            moves.append('up')
        if self.vacPos[0] != len(self.floor) - 1:
            moves.append('down')
        
        return moves

                    
    def result(self, move):
        """

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """                        
        # Create a copy of the current chess board        
        newFloor = VacuumState(len(self.floor), len(self.floor[0]), self.vacPos.copy())
        for i in range(len(self.floor)):
            newFloor.floor[i] = self.floor[i].copy()
        x, y = newFloor.vacPos
        if move == 'left':
            newFloor.vacPos = [x, y - 1]            
        elif move == 'right':
            newFloor.vacPos = [x, y + 1]
        elif move == 'up':
            newFloor.vacPos = [x - 1, y]
        elif move == 'down':
            newFloor.vacPos = [x + 1, y]
        elif move == 'suck':
            newFloor.floor[x][y] = '_'

        # And update it to reflect the move        
        return newFloor

    # Utilities for comparison and display
    def __eq__(self, other):
        if self.floor == other.floor and \
            self.vacPos == other.vacPos:

            return True
        return False

    def __hash__(self):
        return hash(str(self.floor))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """        
        lines = []
        horizontalLine = ('-' * (4 * len(self.floor[0]) + 1))
        lines.append(horizontalLine)
        for row in range(len(self.floor)):
            rowLine = '|'
            for col in range(len(self.floor[0])):
                if self.vacPos == [row, col] and self.floor[row][col] == '.':
                    val = ':'
                elif self.vacPos == [row, col]:
                    val = 'v'
                else: val = self.floor[row][col]
                rowLine = rowLine + ' ' + val + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)            

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class VacuumProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, floor):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.floor = floor

    def getStartState(self):
        return self.floor

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
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def createFloor(m, n, dirtNum):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    initX = random.randint(0, m - 1)
    initY = random.randint(0, n - 1)
    floor = VacuumState(m, n, [initX, initY])
    
    for i in range(dirtNum):
        dirtX = random.randint(0, m - 1)
        dirtY = random.randint(0, n - 1)
        floor.floor[dirtX][dirtY] = '.'

    return floor

if __name__ == '__main__':
    vac = createFloor(4, 4, 3)
    problem = VacuumProblem(vac)
    startTime = time.time()
    # path = search.breadthFirstSearch(problem)
    path = search.GraphSearch(problem).findSolution(5)
    # path = search.dfs(problem)
    print("Cal: ", time.time() - startTime)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = vac
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        input("Press return for the next state...")   # wait for key stroke
        i += 1
