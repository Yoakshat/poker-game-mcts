from random import randint
import functools
import heapq

# should include functionality to select node to expand
# and update a tree

class MCT(): 
    def __init__(self, game, player, numIters): 
        self.root = MCT.Node(parent=None, action=None, game=game, player=player)
        self.numIters = numIters

    # select node and expand
    def selectExpand(self, root):   
        # root might be a leaf node (no more to explore from here OR take an action)
        if(root.isLeaf()):
            return 

        if root.explored(): 
            # explore from best children node
            self.selectExpand(root.children[0])
        else: 
            # take an action
            root.takeAction()

    def solve(self): 
        for _ in range(self.numIters): 
             self.selectExpand(self.root)

        # select the action from parent to best child node
        return self.root.children[0].action


    # every node should include its game object
    # parent, actionFromParent
    @functools.total_ordering
    class Node: 
        def __init__(self, parent, action, game, player):
            self.parent = parent
            self.action = action
            self.qval = 0
            self.n = 0
            self.game = game
            self.player = player

            # sort this in-place
            self.children = [] 
            heapq.heapify(self.children)
            self.exploreActions = player.getLegalActions()

        def isLeaf(self): 
            # no next decision point
            return (self.game is None)

        # updating with a q-val
        def update(self, q): 
            # first update myself
            self.qval += q
            self.n += 1
            # update my parent (recursive case)
            if self.parent is not None: 
                self.parent.update(q)

        # already explored all actions
        def explored(self) -> bool: 
            return len(self.exploreActions) == 0
        
        def takeAction(self): 
            # explore + remove
            action = self.exploreActions[randint(0, len(self.exploreActions)-1)] 
            self.exploreActions.remove(action)

            simulatedGame = self.game.copy()
            virtPlayer = simulatedGame.findPlayer(self.player)

            beforeRollout = virtPlayer.money

            # simulate action
            virtPlayer.runAction(action)
            
            # rollout rest of game
            simulatedGame.makeSimPlayers()
            simulatedGame.playOut(self.player)
            afterRollout = virtPlayer.money

            newGame = virtPlayer.getNextDecision()

            # player stays the same but game state changes
            childNode = MCT.Node(self, action, newGame, self.player)
            childNode.update(afterRollout - beforeRollout)

            # add childNode to children
            heapq.heappush(self.children, childNode)

        def __eq__(self, other): 
            return (self.qval / self.n) == (other.qval / other.n)

        # reversed logic because we're using a min-heap (but want the max score)
        def __lt__(self, other): 
            return (self.qval / self.n) > (other.qval / other.n)







        