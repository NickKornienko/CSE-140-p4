from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions


def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = CTFAgent
    secondAgent = DefensiveCTFAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class CTFAgent(ReflexCaptureAgent):
    """
    Hybrid agent that will attack unless there are 2 invaders
    """

    def __init__(self, index, **kwargs):
        self.numInvaders = 0
        super().__init__(index)

    def getFeatures(self, gameState, action):
        enemies = [gameState.getAgentState(i)
                   for i in self.getOpponents(gameState)]
        invaders = [a for a in enemies if a.isPacman(
        ) and a.getPosition() is not None]
        self.numInvaders = len(invaders)

        if self.numInvaders > 1:
            return DefensiveCTFAgent.getFeatures(self, gameState, action)
        return OffensiveCTFAgent.getFeatures(self, gameState, action)

    def getWeights(self, gameState, action):
        if self.numInvaders > 1:
            return DefensiveCTFAgent.getWeights(self, gameState, action)
        return OffensiveCTFAgent.getWeights(self, gameState, action)


class OffensiveCTFAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food,
    avoids ghosts at all costs,
    and eats nearby capsules
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food)
                              for food in foodList])
            features['distanceToFood'] = minDistance

        # avoid ghosts at all costs unless scared
        enemies = [successor.getAgentState(i)
                   for i in self.getOpponents(successor)]
        ghosts = [a for a in enemies if not a.isPacman() and a.getPosition()
                  is not None]
        ghostDistances = [self.getMazeDistance(
            myPos, ghost._position) for ghost in ghosts]

        features['ghostProximity'] = 0
        features['scaredGhostProximity'] = 0
        for ghostDistance in ghostDistances:
            if ghostDistance < 2:
                if ghosts[0]._scaredTimer > 0:
                    features['scaredGhostProximity'] = 1
                else:
                    features['ghostProximity'] = 1

        # give a bonus for eating capsules
        features['capsulesRemaining'] = len(successor.getCapsules())

        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            'ghostProximity': -999999,
            'capsulesRemaining': -50,
            'scaredGhostProximity': 999999
        }


class DefensiveCTFAgent(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    If no invaders are present it will move towards the middle
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i)
                   for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman(
        ) and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        # Go after invaders, or approach enemies on the other side
        if (len(invaders) > 0):
            dists = [self.getMazeDistance(
                myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)
        else:
            dists = [self.getMazeDistance(
                myPos, a.getPosition()) for a in enemies]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(
            self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2
        }
