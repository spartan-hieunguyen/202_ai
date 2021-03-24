import search
import random

class MissionariesCannibalsState:
    def __init__(self):
        self.state = [3, 3, 1]

    def isGoal(self):
        if self.state == [0, 0, 0]:
            return True
        return False
    
    def legalMoves(self):
        m, c, b = self.state
        moves = []
        
        if b == 1:
            b = 0
            moves.append([m, c - 1, b])
            moves.append([m - 1, c, b])
            moves.append([m, c - 2, b])
            moves.append([m - 2, c, b])
            moves.append([m - 1, c - 1, b])
            
        elif b == 0:
            b = 1
            moves.append([m, c + 1, b])
            moves.append([m + 1, c, b])
            moves.append([m, c + 2, b])
            moves.append([m + 2, c, b])
            moves.append([m + 1, c + 1, b])

        result = moves.copy()
        for i in moves:
            m, c, b = i
            if m < 0 or m > 3 or\
                c < 0 or c > 3 or\
                (c > m and m != 0) or\
                ((3 - c) > (3 - m) and (3 - m) > 0):

                result.remove(i)
        
        return result
        
    def result(self, move):
        newState = MissionariesCannibalsState()
        newState.state = move.copy()
        
        return newState
        
    
    def __eq__(self, other):
        
        if self.state == other.state:
            return True
        return False
    
    def __hash__(self):
        return hash(str(self))

    def __getAsciiString(self): 
        bank1 = []
        bank2 = []
        m, c, b = self.state
        
        bank1.append('m ' * m)
        bank1.append('_ ' * (3 - m))
        bank1.append('c ' * c)
        bank1.append('_ ' * (3 - c))
        
        bank2.append('m ' * (3 - m))
        bank2.append('_ ' * m)
        bank2.append('c ' * (3 - c))
        bank2.append('_ ' * c)

        
        return "".join(bank1) + '-------- ' + "".join(bank2)

    def __str__(self):
        return self.__getAsciiString()

class MissionariesCannibalsSearchProblem:
    def __init__(self, state):
        self.startState = state

    def getStartState(self):
        return self.startState
    
    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
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

if __name__ == '__main__':
    startState = MissionariesCannibalsState()
    prob = MissionariesCannibalsSearchProblem(startState)
    path = search.GraphSearch(prob).findSolution(2)

    curr = startState
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = startState
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        input("Press return for the next state...")   # wait for key stroke
        i += 1

