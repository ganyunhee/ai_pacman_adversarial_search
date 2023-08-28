from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)



class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    
    move = gameState.getLegalActions() # default agent is pacman
    utility = [self.MiniMax(0, 0, gameState.generatePacmanSuccessor(action)) for action in move] # call minimax from root node
    max_value = max(utility)
    Index=[index for index in range(len(utility)) if utility[index]==max_value]
    get_index=random.choice(Index)

    return move[get_index]

  def MiniMax(self,agent, depth, gameState):
    # Terminal Test
    if gameState.isLose() or gameState.isWin() or depth==self.depth:
      return self.evaluationFunction(gameState)
    # Pacman
    # select max value
    if agent==0:
      return max(self.MiniMax(1, depth,gameState.generateSuccessor(0,action)) for action in gameState.getLegalActions())
    # Ghost
    # select min value
    else:
      next_agent=agent+1
      if gameState.getNumAgents()==agent+1:
        next_agent=0
        # one cycle end then increase depth
        depth+=1
      return min(self.MiniMax(next_agent, depth, gameState.generateSuccessor(agent,action)) for action in gameState.getLegalActions(agent))

    #raise Exception("Not implemented yet")

    ############################################################################

class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBetaAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  
  def Action(self, gameState):
    ####################### Write Your Code Here ################################

    move = gameState.getLegalActions() # default agent is pacman
    utility = [self.AlphaBeta(0, 0, gameState.generatePacmanSuccessor(action)) for action in move] # call minimax from root node
    max_value = max(utility)
    Index=[index for index in range(len(utility)) if utility[index]==max_value]
    get_index=random.choice(Index)

    return move[get_index]


    #raise Exception("Not implemented yet")

  def AlphaBeta(self, agent, depth, gameState, alpha, beta):
    # Terminal Test
    if gameState.isLose() or gameState.isWin() or depth==self.depth:
      return self.evaluationFunction(gameState)
    # pacman
    if agent==0:
      pacman_actions=gameState.getLegalActions()
      tmp=-math.inf
      for action in pacman_actions:
        tmp=max(tmp, self.AlphaBeta(1,depth,gameState.generatePacmanSuccessor(action), alpha,beta))
        alpha=max(alpha,tmp)
        if tmp>=beta:
          break # pruning the redundant branch
      return tmp
    # ghost
    else:
      ghost_actions=gameState.getLegalActions(agent)
      tmp=math.inf
      next_agent=agent+1
      if gameState.getNumAgents()==agent+1:
        next_agent=0
        # end of one cycle
        depth+=1
      for action in ghost_actions:
        tmp=min(tmp, self.AlphaBeta(next_agent,depth,gameState.generateSuccessor(agent,action), alpha,beta))
        beta=min(beta,tmp)
        if tmp<=alpha:
          break # pruning the redundant branch
      return tmp

    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] ExpectimaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """

  def Action(self, gameState):
    ####################### Write Your Code Here ################################

    move = gameState.getLegalActions() # default agent is pacman
    utility = [self.Expectimax(0, 0, gameState.generatePacmanSuccessor(action)) for action in move] # call minimax from root node
    max_value = max(utility)
    Index=[index for index in range(len(utility)) if utility[index]==max_value]
    get_index=random.choice(Index)

    return move[get_index]



    #raise Exception("Not implemented yet")
    
  def Expectimax(self, agent, depth, gameState):
    #Terminal Test
    if gameState.isLose() or gameState.isWin() or depth==self.depth:
      return self.evaluationFunction(gameState)

    # pacman
    if agent==0:
      pacman_actions=gameState.getLegalActions()
      actions_num=len(pacman_actions)
      return sum(self.Expectimax(1,depth, gameState.generatePacmanSuccessor(action)) for action in pacman_actions)/(actions_num)
    # Ghost
    else:
      next_agent=agent+1
      ghost_actions=gameState.getLegalActions(agent)
      actions_num=len(ghost_actions)
      if gameState.getNumAgents()==agent+1: # end of one cycle
        next_agent=0
        depth+=1
      return sum(self.Expectimax(next_agent, depth, gameState.generateSuccessor(agent, action))for action in ghost_actions)/(actions_num)
    
    ############################################################################
