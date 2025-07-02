from random import randint
import functools
import heapq

# should include functionality to select node to expand
# and update a tree

class MCT(): 
    def __init__(self, game, playerName, numIters): 
        self.root = MCT.Node(parent=None, action=None, game=game, playerName=playerName)
        self.numIters = numIters

    # select node and expand
    def selectExpand(self, root): 
        exploreFrom = root
        if root.explored(): 
            # explore from best children node
            exploreFrom = self.selectNode(root.children[0])

        # take an action
        exploreFrom.takeAction()

    def solve(self): 
        for _ in range(self.numIters): 
            self.selectExpand(self.root)

        # select the action from parent to best child node
        return self.root.children[0].action


    # every node should include its game object
    # parent, actionFromParent
    @functools.total_ordering
    class Node: 
        def __init__(self, parent, action, game, playerName):
            self.parent = parent
            self.action = action
            self.qval = 0
            self.n = 1
            self.game = game
            self.playerName = playerName

            # sort this in-place
            self.children = [] 
            heapq.heapify(self.children)
            self.exploreActions = game.getLegalActions(playerName)

        def update(self, q): 
            # first update myself
            self.qval += q
            # update my parent (recursive case)
            if self.parent is not None: 
                self.parent.update(self.qval)
                self.parent.n += 1

        # already explored all actions
        def explored(self) -> bool: 
            return len(self.exploreActions) == 0
        
        def takeAction(self): 
            # action is whatever is left in exploreActions (pick at random)

            # explore + remove
            action = self.exploreActions[randint(0, len(self.exploreActions)-1)] 
            self.exploreActions.remove(action)

            # returns (return of action + game immediately after taking first action)
            # run a virtual round where this player takes this action
            returnForAction, newGame = self.game.copy().virtualRound(self.playerName, action)

            childNode = MCT.Node(self, action, newGame, self.playerName)
            childNode.update(returnForAction)

            # add childNode to children
            heapq.heappush(self.children, childNode)

        def __eq__(self, other): 
            return (self.qval / self.n) == (other.qval / other.n)

        # reversed logic because we're using a min-heap (but want the max score)
        def __lt__(self, other): 
            return (self.qval / self.n) > (other.qval / other.n)







        