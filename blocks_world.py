MAX_EPISODES = 1000

class BinaryTree:
  class Node:
    def __init__(self, value = None, left = None, right = None):
      self.value = value
      self.left = left
      self.right = right

  def __init__(self, root = None):
    self.root = root

def induce_tree(examples, root_value = None):
  root = BinaryTree.Node(root_value)
  tree = BinaryTree(root)

  split(root, examples, tree)

  return tree

# TODO: Fix this
def split(node, examples, tree):
  best = None
  # for all possible tests q in node
    if (quality(q) > quality(best)):
      best = q
  # if best yields improvements
    # test(node) = best
    examples_good = [e for e in examples if is_covered(best, e)]
    examples_bad = list(set(examples) - set(examples_good))
    node.left = BinaryTree.Node()
    node.right = BinaryTree.Node()

    split(node.left, examples_good, tree)
    split(node.right, examples_bad, tree)
  # else
    # make node a leaf node
  
# TODO: Fix this
def quality(predicate):
  if (predicate == None): return 0

# TODO: Fix this
def is_covered(predicate, example):
  return True if predicate.covers(example) else False

def select_action(state):
  # exploration_strategy or best from Q

def q_rrl():
  Q = BinaryTree(BinaryTree.Node(0))
  examples = []
  episode = 0

  while (episode < MAX_EPISODES):
    episode += 1
    i = 0
    # generate random state
    while (not is_goal(state)):
      action = select_action(state)
      # new_state = perform action
      # receive immediate reward
      state = new_state
      i += 1
    for j in range(i - 1, -1, -1): # if i was 10 this will start with 9 and end at 0 (-1 is non-inclusive)
      # x = generate_example(s_j, a_j, q_j) where q_j := r_j + γ max_a Q_e(s_(j+1), a)
      if x in examples:
        # replace exiting one with x
      else:
        examples.append(x) # do not empty examples, it should contain every state we've seen in every iteration, not just this one
        # In non-deterministic domains, it would probably be a good idea to average the qˆ values instead of keeping only the most recent value.
    Q = induce_tree(examples)
