from pacai.agents.capture.defense import DefensiveReflexAgent
from pacai.agents.capture.reflex import ReflexCaptureAgent


def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = CTFAgent
    secondAgent = CTFAgent2

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
            return DefensiveReflexAgent.getFeatures(self, gameState, action)
        return OffensiveCTFAgent.getFeatures(self, gameState, action)

    def getWeights(self, gameState, action):
        if self.numInvaders > 1:
            return DefensiveReflexAgent.getWeights(self, gameState, action)
        return OffensiveCTFAgent.getWeights(self, gameState, action)


class CTFAgent2(ReflexCaptureAgent):
    """
    Hybrid agent that will attack unless there are invaders
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

        if self.numInvaders > 0:
            return DefensiveReflexAgent.getFeatures(self, gameState, action)
        return OffensiveCTFAgent.getFeatures(self, gameState, action)

    def getWeights(self, gameState, action):
        if self.numInvaders > 0:
            return DefensiveReflexAgent.getWeights(self, gameState, action)
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
        # enemies = [successor.getAgentState(i)
        #            for i in self.getOpponents(successor)]
        # ghosts = [a for a in enemies if not a.isPacman() and a.getPosition()
        #           is not None]
        # ghostDistances = [self.getMazeDistance(
        #     myPos, ghost._position) for ghost in ghosts]

        features['ghostProximity'] = 0
        features['scaredGhostProximity'] = 0
        # for ghostDistance in ghostDistances:
        #     if ghostDistance > 1:
        #         if ghosts[0]._scaredTimer > 0:
        #             features['scaredGhostProximity'] = 1
        #         else:
        #             features['ghostProximity'] = 1

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
