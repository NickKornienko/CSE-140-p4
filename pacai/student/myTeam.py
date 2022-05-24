from pacai.agents.capture.defense import DefensiveReflexAgent
from pacai.agents.capture.offense import OffensiveReflexAgent
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
        return OffensiveReflexAgent.getFeatures(self, gameState, action)

    def getWeights(self, gameState, action):
        if self.numInvaders > 1:
            return DefensiveReflexAgent.getWeights(self, gameState, action)
        return OffensiveReflexAgent.getWeights(self, gameState, action)


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
        return OffensiveReflexAgent.getFeatures(self, gameState, action)

    def getWeights(self, gameState, action):
        if self.numInvaders > 0:
            return DefensiveReflexAgent.getWeights(self, gameState, action)
        return OffensiveReflexAgent.getWeights(self, gameState, action)


# class OffensiveReflexAgent(ReflexCaptureAgent):
#     """
#     A reflex agent that seeks food.
#     This agent will give you an idea of what an offensive agent might look like,
#     but it is by no means the best or only way to build an offensive agent.
#     """

#     def __init__(self, index, **kwargs):
#         super().__init__(index)

#     def getFeatures(self, gameState, action):
#         features = {}
#         successor = self.getSuccessor(gameState, action)
#         features['successorScore'] = self.getScore(successor)

#         Compute distance to the nearest food.
#         foodList = self.getFood(successor).asList()

#         This should always be True, but better safe than sorry.
#         if (len(foodList) > 0):
#             myPos = successor.getAgentState(self.index).getPosition()
#             minDistance = min([self.getMazeDistance(myPos, food)
#                               for food in foodList])
#             features['distanceToFood'] = minDistance

#         return features

#     def getWeights(self, gameState, action):
#         return {
#             'successorScore': 100,
#             'distanceToFood': -1
#         }


# class DefensiveReflexAgent(ReflexCaptureAgent):
#     """
#     A reflex agent that tries to keep its side Pacman-free.
#     This is to give you an idea of what a defensive agent could be like.
#     It is not the best or only way to make such an agent.
#     """

#     def __init__(self, index, **kwargs):
#         super().__init__(index)

#     def getFeatures(self, gameState, action):
#         features = {}

#         successor = self.getSuccessor(gameState, action)
#         myState = successor.getAgentState(self.index)
#         myPos = myState.getPosition()

#         Computes whether we're on defense (1) or offense (0).
#         features['onDefense'] = 1
#         if (myState.isPacman()):
#             features['onDefense'] = 0

#         Computes distance to invaders we can see.
#         enemies = [successor.getAgentState(i)
#                    for i in self.getOpponents(successor)]
#         invaders = [a for a in enemies if a.isPacman(
#         ) and a.getPosition() is not None]
#         features['numInvaders'] = len(invaders)

#         if (len(invaders) > 0):
#             dists = [self.getMazeDistance(
#                 myPos, a.getPosition()) for a in invaders]
#             features['invaderDistance'] = min(dists)

#         if (action == Directions.STOP):
#             features['stop'] = 1

#         rev = Directions.REVERSE[gameState.getAgentState(
#             self.index).getDirection()]
#         if (action == rev):
#             features['reverse'] = 1

#         return features

#     def getWeights(self, gameState, action):
#         return {
#             'numInvaders': -1000,
#             'onDefense': 100,
#             'invaderDistance': -10,
#             'stop': -100,
#             'reverse': -2
#         }
