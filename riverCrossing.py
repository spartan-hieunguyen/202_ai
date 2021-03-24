import search
import random

class RiverCrossingState:
    def __init__(self):
        self.state = [0, 0, 0 ,0]

    def isGoal(self):
        if self.state == [1, 1, 1, 1]:
            return True
        return False
    
    def legalMoves(self):
        f, t, b, g = self.state
        moves = []        

        # left bank
        if f == 0:
            f = 1
            baseAct = [f] + self.state[1:]
            moves.append(baseAct)
            for i in range(1, 4):
                act = baseAct.copy()
                if baseAct[i] == 0:
                    act[i] = 1
                    moves.append(act)
        # right bank
        elif f == 1:
            f = 0
            baseAct = [f] + self.state[1:]
            moves.append(baseAct)
            for i in range(1, 4):
                act = baseAct.copy()
                if baseAct[i] == 1:
                    act[i] = 0
                    moves.append(act)

        result = moves.copy()
        for i in moves:       
            if i in [[0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 1, 1], [1, 1, 0, 0]]:
                result.remove(i)
        
        return result
        
    def result(self, move):
        newState = RiverCrossingState()
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
        f, t, b, g = self.state

        if f == 0:
            bank1.append("F ")
            bank2.append("_ ")
        else: 
            bank1.append("_ ")
            bank2.append("F ")

        if t == 0:
            bank1.append("T ")
            bank2.append("_ ")
        else: 
            bank1.append("_ ")
            bank2.append("T ")
 
        if b == 0:
            bank1.append("B ")
            bank2.append("_ ")
        else: 
            bank1.append("_ ")
            bank2.append("B ")

        if g == 0:
            bank1.append("G ")
            bank2.append("_ ")
        else: 
            bank1.append("_ ")
            bank2.append("G ")

        return "".join(bank1) + '-------- ' + "".join(bank2)

    def __str__(self):
        return self.__getAsciiString()

class RiverCrossingSearchProblem:
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
    startState = RiverCrossingState()
    prob = RiverCrossingSearchProblem(startState)
    path = search.GraphSearch(prob).findSolution(1)

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

