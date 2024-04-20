import random
import time
import threading
import game
import othello
import contextlib
import copy

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
        moves = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]


class RandomAgent(game.Player):
    def choose_move(self, state):
        moves = state.generateMoves()
        return random.choice(moves) if moves != [] else None


class Node(othello.State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ref = hash(str(self.nextPlayerToMove) + "".join([str(e) for row in self.board for e in row]))
        self.depth = 0
        self.is_leaf = False
        self.is_terminated = False
        self.move2child = dict()
        self.expectation = None

    def clone(self):
        new_node = Node(copy.deepcopy(self.board), self.boardSize, self.nextPlayerToMove)
        new_node.ref = self.ref
        return new_node

    def applyMoveCloning(self, move):
        child_node = self.clone()
        child_node.applyMove(move)
        child_node.depth = self.depth + 1
        child_node.ref = hash(str(child_node.nextPlayerToMove) +
                              "".join([str(e) for row in child_node.board for e in row]))
        return child_node, child_node.ref

    def from_state(self, state: othello.State):
        self.board = state.board
        self.boardSize = state.boardSize
        self.nextPlayerToMove = state.nextPlayerToMove
        self.ref = hash(str(self.nextPlayerToMove) + "".join([str(e) for row in self.board for e in row]))
        return self

    def best_move(self):
        if self.expectation is None:
            print(self.move2child)
        # assert not self.is_terminated, "Already game over, no available move"
        # assert self.move2child, "There is no child for the current node, check you code about adding child"
        # assert self.expectation is not None, "You haven't calculate the expectation for current node!"
        return random.choice([move for move, child in self.move2child.items()
                              if child.expectation == self.expectation])

    def all_non_leaf_children(self):
        if self.is_leaf is False:
            all_children = [self]
            for move, child in self.move2child.items():
                all_children.extend(child.all_non_leaf_children())
            return all_children
        else:
            return []


class SearchTree:
    """
    Edit 1:
    I start to create search tree with a simple function. However,
    in this way, every time we need a tree, we have to rebuild it.

    But when comes to the extra credit, I noticed that, when
    searching in different max-depth(deeper and deeper) from the
    same root node(state), instead of rebuild the whole tree, we can
    just expand the leaf nodes in the bottom layer of the older tree.

    Leaf nodes can be expandable or non-expandable. When a node is
    "game over", we don't want to try expanding it every time, we only
    want to try expanding those nodes which might not "game over".
    So I use terminated_nodes and unexplored_nodes to separate the
    leaf nodes into two types.

    While this approach can remember the state of the search tree
    from last probe(search), it can efficiently save the time consumption
    for the extra credit task!

    Edit 2:
    I do have multiple idea to improve the performance, however, some of
    them might be too complex and I don't have much time :)
    So I picked another easy one to do: host a node pool for each search tree.

    The idea is: The same state may exist in our search tree multiple times.
    They may exist in the same depth, or they can even exist in different depth
    because of one's ancestors skip some move. If we have a very deep search tree
    and the nodes represent the same are in very shallow depth, it will take
    us a lot of extra time to build the subtrees and calculate the expectation for
    each one!

    So, why don't we use links? We can link multiple parent node to the
    same child node if their "child" are exactly the same (same player and
    the same board state). Also, this approach will never cause
    loop because one node's ancestors always have more white space(2)
    than the node itself. We don't need to worry about loops, cool!

    Then, if we host a node pool, when we create a new child node and find the new
    node has already existed in the pool(same board and player),
    there could be two situation:

    1. child_existed.depth == child_new.depth: in this way, we only need to point
    new one to the existed one. Because we use backtrack in our minimax: always
    update the deeper nodes before shallower ones. The existed child node has the
    same depth as the new one(current node's depth + 1). So it will be updated
    before both current node and its own father node. (do nothing with the new one,
    just skip it!)

    2. child_existed.depth < child_new.depth: in this way, we need to be careful.
    Like I explained above, this time the existed child node may get update after the
    current node. If it is a non-leaf node, its index in SearchTree.non_leaf_nodes
    may smaller than current node, which will raise an error. We want the child
    nodes always get updated before it father node, so if the existed child node
    is in SearchTree.non_leaf_nodes, the method to solve it is:

        let existed_child.depth = n, current_node = c
        let S = {all the nodes in the subtree with existed_child as root,
            which also in SearchTree.non_leaf_nodes}
        pop all the nodes in S from SearchTree.non_leaf_nodes
        insert S back to non_leaf_nodes, right after c
        point new_child to existed_child, then skip the new_child

    It looks like the second situation is computational expensive, however, it won't
    always happen because players rarely skip their move(only when they have to).
    And also, there is a special case we can't use the method to regulate the tree: When
    both two player skip their move, then the existed_child would be an ancestor of
    the new child node. We should skip this situation!

    By Xiao
    """
    def __init__(self, root_node: othello.State):
        self.root_node = Node().from_state(root_node)
        self.probed_depth = 0  # nodes in probed_depth(unexplored) or "game over" are "leaf nodes"
        self.non_leaf_nodes = []  # explored nodes which are not "game over"
        self.terminated_nodes = []  # explored nodes which are "game over", theoretically, them are also "leaf nodes"
        self.unexplored_nodes = [self.root_node]  # unexplored leaf nodes, some of them may be "game over"
        self.node_pool = {self.root_node.ref: self.root_node}

    def regulate(self, node, move, child, ref):
        """
        For testing:
        assert self.regulate(self.root_node, self.root_node.ref) == self.root_node
        """
        # print("Capture a repeated node!")
        existed_child = self.node_pool[ref]

        # REGULATE the search tree: actually, I test many times, but it rarely needs to regulate
        if existed_child.depth < child.depth and existed_child.is_leaf is False:
            existed_non_leaf_children = existed_child.all_non_leaf_children()

            if child.ref not in [n.ref for n in existed_non_leaf_children]:  # very rarely!!!!! We should skip it
                print("Regulate the search tree...")
                sub_tree = []
                for nlc in existed_non_leaf_children:  # non_leaf_child
                    if nlc in self.non_leaf_nodes:
                        idx = self.non_leaf_nodes.index(nlc)
                        sub_tree.append(self.non_leaf_nodes.pop(idx))

                self.non_leaf_nodes.extend(sub_tree)
                node.move2child[move] = existed_child
                return True  # True means can skip the new_child

            else:
                node.move2child[move] = child
                return False  # False means we shouldn't skip the new_child

        elif existed_child.depth == child.depth:
            node.move2child[move] = existed_child
            return True  # True means can skip the new_child

        # else:
        #     assert existed_child.depth < child.depth and existed_child.is_leaf is True

    def probe(self, max_depth: int):
        # assert max_depth > self.probed_depth, f"SearchTree already has probed_depth of {self.probed_depth}!"
        # fringe contains the nodes which will be exploded with the given max_depth (node.depth < max_depth)
        fringe = self.unexplored_nodes
        self.unexplored_nodes = []  # empty the unexplored_nodes
        # assert fringe[0].depth == self.probed_depth

        for node in fringe:  # node.depth < max_depth
            moves = node.generateMoves()  # explored the node

            if moves:
                node.is_leaf = False
                self.non_leaf_nodes.append(node)  # this node has child, so it is not a "leaf node"
                
                for move in moves:
                    child, ref = node.applyMoveCloning(move)  # child node may be a theoretical "leaf node"

                    # Edit 3 ------------------------------------------------------------------------------ #
                    if ref in self.node_pool and self.node_pool[ref].nextPlayerToMove == child.nextPlayerToMove:
                        if self.regulate(node, move, child, ref):
                            continue  # skip the new child
                    else:
                        self.node_pool[ref] = child
                    # Edit 3 ------------------------------------------------------------------------------ #

                    node.move2child[move] = child
                    
                    if child.depth < max_depth:  # child node may be "game over", but currently we don't know
                        fringe.append(child)  # only when the child node dequeue can we see the result
                    else:  # this child won't be explored with the certain max_depth
                        child.is_leaf = True
                        self.unexplored_nodes.append(child)

            else:  # no available moves, plus, don't use node.game_over() here, it takes one more calculation
                with contextlib.redirect_stdout(None):  # capture the annoying output: "...skip the move!"
                    child, ref = node.applyMoveCloning(None)  # try skip the current move

                child_moves = child.generateMoves()

                if child_moves:  # not game over, has at least one child
                    node.is_leaf = False
                    self.non_leaf_nodes.append(node)  # current node is not "game over", it has one child

                    # Edit 3 ------------------------------------------------------------------------------ #
                    if ref in self.node_pool and self.node_pool[ref].nextPlayerToMove == child.nextPlayerToMove:
                        if self.regulate(node, None, child, ref):
                            continue  # skip the new child
                    else:
                        self.node_pool[ref] = child
                    # Edit 3 ------------------------------------------------------------------------------ #

                    node.move2child[None] = child
                    # save the time for calling generateMoves() of the child node next time
                    child.generateMoves = lambda player=None: [] \
                        if player == node.nextPlayerToMove else child_moves
                    
                    if child.depth < max_depth:  # we already know this child is not "game over"!
                        fringe.append(child)
                    else:  # this child won't be explored with the certain max_depth
                        child.is_leaf = True
                        self.unexplored_nodes.append(child)

                else:  # current node is "game over", early termination
                    node.is_leaf = True
                    node.is_terminated = True
                    self.terminated_nodes.append(node)

        # assert len(self.node_pool) <= len(self.non_leaf_nodes) + len(self.unexplored_nodes) + len(self.terminated_nodes), \
        #     (len(self.node_pool), len(self.non_leaf_nodes) , len(self.unexplored_nodes) , len(self.terminated_nodes))
        self.probed_depth = max_depth
        return self


def minimax(tree: SearchTree) -> othello.OthelloMove or None:

    for node in tree.unexplored_nodes:
        node.expectation = node.score()

    for node in tree.terminated_nodes:
        # the expectation of terminated nodes won't change
        # so if we did calculate it last time, we don't need to calculate it again
        node.expectation = node.score() if node.expectation is None else node.expectation

    # backtrack from the last leaf node to the root node
    for node in tree.non_leaf_nodes[::-1]:
        strategy = max if node.nextPlayerToMove == othello.PLAYER1 else min
        node.expectation = strategy([child.expectation for move, child in node.move2child.items()])

    return tree.root_node.best_move()


def alpha_beta_pruning(tree: SearchTree) -> othello.OthelloMove or None:
    # for each depth, we set an initial value for alpha/beta
    max_depth = tree.probed_depth
    limit = tree.root_node.boardSize ** 2
    base = int(tree.root_node.nextPlayerToMove == othello.PLAYER1)
    alpha_beta = {depth: ((-1) ** (base + depth)) * limit for depth in range(max_depth)}

    # we always need to fully explore the first subtree (with at least one un-pruned child node)
    # in each depth, then can we start to use alpha beta pruning
    explored_first_yet = {depth: False for depth in range(tree.probed_depth)}

    # backtrack from the last leaf node to the root node
    for node in tree.non_leaf_nodes[::-1]:
        # reset the expectation, otherwise the tree might keep the
        # expectation from last searching, it will raise error
        node.expectation = None
        current_depth = node.depth

        # For a certain depth, after the first subtree get fully explored, we can start pruning:
        # PLAYER1 want to maximize the expectation while PLAYER1 want to minimize it.
        # So if in one move should be decided by PLAYER1, in the corresponding depth,
        # prune the subtrees with node greater than alpha. Because we will never get to that subtree.
        # Vice versa.
        if node.nextPlayerToMove == othello.PLAYER1:
            subtree_max_exp = -limit

            for move, child in node.move2child.items():
                child_exp = child.expectation = child.score() if child.is_leaf else child.expectation
                if child_exp is None:  # this child node has been pruned
                    continue

                else:  # child_exp is not None
                    if explored_first_yet[current_depth]:
                        if child.expectation > alpha_beta[current_depth]:
                            # reset subtree_max_exp so that later we can prune the subtree
                            subtree_max_exp = -limit
                            break  # skip other child of current node

                        else:  # update subtree_max_exp
                            if child_exp > subtree_max_exp:
                                subtree_max_exp = child_exp

                    else:  # first subtree, update subtree_max_exp
                        if child_exp > subtree_max_exp:
                            subtree_max_exp = child_exp

            # if subtree_max_exp == -limit, it means this subtree should be pruned
            # there could be two reasons: One is all its child are pruned, so
            # subtree_max_exp didn't get update. Another reason is there exist a
            # child with expectation larger than alpha, so it reset subtree_max_exp.
            # In both case, node.expectation will stay None, which means node also get pruned.
            if subtree_max_exp != -limit:  # this subtree has at least one un-pruned child
                node.expectation = subtree_max_exp
                alpha_beta[current_depth] = subtree_max_exp
                explored_first_yet[current_depth] = True

        else:  # node.nextPlayerToMove == othello.PLAYER2:
            subtree_min_exp = limit

            for move, child in node.move2child.items():
                child_exp = child.expectation = child.score() if child.is_leaf else child.expectation
                if child_exp is None:  # this child node has been pruned
                    continue

                else:  # child_exp is not None
                    if explored_first_yet[current_depth]:
                        if child.expectation < alpha_beta[current_depth]:
                            # reset subtree_max_exp so that later we can prune the subtree
                            subtree_min_exp = limit
                            break  # skip other child of current node

                        else:  # update subtree_max_exp
                            if child_exp < subtree_min_exp:
                                subtree_min_exp = child_exp

                    else:  # first subtree, update subtree_max_exp
                        if child_exp < subtree_min_exp:
                            subtree_min_exp = child_exp

            # if subtree_min_exp == limit, it means this subtree should be pruned
            # there could be two reasons: One is all its child are pruned, so
            # subtree_min_exp didn't get update. Another reason is there exist a
            # child with expectation smaller than beta, so it reset subtree_min_exp.
            # In both case, node.expectation will stay None, which means node also get pruned.
            if subtree_min_exp != limit:  # this subtree has at least one un-pruned child
                node.expectation = subtree_min_exp
                alpha_beta[current_depth] = subtree_min_exp
                explored_first_yet[current_depth] = True

    return tree.root_node.best_move()


class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.max_depth = depth

    def choose_move(self, state: othello.State):
        return minimax(SearchTree(state).probe(self.max_depth))


class AlphaBeta(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.max_depth = depth

    def choose_move(self, state: othello.State):
        return alpha_beta_pruning(SearchTree(state).probe(self.max_depth))


# noinspection PyPep8Naming
class extra(game.Player):
    def __init__(self, time_limit):
        super().__init__()
        self.time_limit = time_limit / 1000  # milliseconds --> seconds

    def choose_move(self, state: othello.State):
        end_time = time.time() + self.time_limit
        best_moves = {0: None}  # {max_depth: best_move in the depth, ...}

        def worker():
            tree = SearchTree(state)
            while time.time() < end_time:
                max_depth = len(best_moves)
                """
                each time we call tree.probe with a larger max_depth,
                it will push the staged unexplored_nodes to fringe,
                and pop nodes from fringe to expand.
                This approach prevent to rebuild the tree every time,
                and can greatly improve the search efficiency.
                """
                tree.probe(max_depth)

                if time.time() > end_time:
                    break

                best_move = alpha_beta_pruning(tree)
                best_moves[max_depth] = best_move

                if time.time() < end_time:
                    print(f"Search with depth of {max_depth}, best move: {best_move}")
                    if not tree.unexplored_nodes:  # that means all the leaf nodes are "game over"
                        print("Already traveled all the available states. Stop searching.")
                        break
            # kill the thread
            exit(0)

        print(f"Start searching with time limit of {self.time_limit} seconds...")
        threading.Thread(target=worker, daemon=True).start()
        time.sleep(self.time_limit)
        print("Time runs out. Current best move:", best_moves[max(best_moves.keys())])
        return best_moves[max(best_moves.keys())]
