**Uninformed Search -- Evaluate search algorithm: Complete? Optimal? Complexity (Time, Space)?**

* Search Algorithms
   * Tree search algorithm (TSA)
     * Could be stuck in infinite loops
     * Explores redundant paths
     * Requires less memory
     * Easier to implement
   * Graph search algorithm (GSA)
     * Avoid infinite loops
     * Eliminates exponentially many redunant paths
     * requires more memory proportional to its runtime
* Breadth-first Search (BFS)
  * if solutions are close to root of the search tree
* Depth-first Search (DFS)
  * if solutions are deep inside the search tree
* Uniform-cost Search (UCS) - explores the cheapest node first
  * Use priority queue

**Informed Search: more efficient**

* heuristic function - estimate how close you are to the goal
  * h(n) - estimated cost of the cheapest path from the state at node n to a goal state
* Greedy best-first search
  * exoand the node that has the lowest h(n) - (similar to UCS, with key to be h(n))
* A* Search
  * UCS orders by backward cost g(n)
  * Greedy orders by forward cost h(n)
  * A* orders by backward + forward cost f(n) = g(n) + h(n)
  * A* optimal when Heuristic admissible - 0 <= h(n) <= h*(n)
    * Consistency of Heuristic - h(a)-h(c) <= cost(a to c)
    * 
**Local Search: find solution faster for specific types of identification problems**

* Evaluate and modify one current state rather than systematicaly explore paths from intinal state
* suitable for problems were all that matters is the solution state
  * Require little memory
* 8-Queens

**Constrain Satisfaction Problems (CSPs)**

* CSPs use a factored representation for states - a set of variables, each of which has a value
  * A set of variables, X = {X1, ..., Xn}
  * A set of domains, D = {D1, ..., Dn}, where Di = {v1, ..., vk} for each variable Xi
  * A set of constraints C specify allowable combinations of values
* Problem solved when each variable has a value that satisfies constraints
  * **consistent** - no constraints violated
  * **complete** - every variable assigned
  * solution is an assignment that is both consistent and complete
* CSPs can often be solved more efficiently - they elimintate large portions of the search space by identifying combinations that violate constraints
* Backtracking Search - DFS with the idea that
  1. consider a variable at each node and
  2. consider values which do not conflict previous assignments
* Improving Backtracking
  * Forward checking (FC)
    * Filtering: keep track of domains for unassigned variables and cross off bad options
    * Cross off values that violate a constraint when added to the existing assignment
  * Constraint propagation (AC-3) - Check: [Arc consistency](https://www.youtube.com/watch?v=mo0gmLMC72E&ab_channel=AlanMackworth)
    * Constraint propagation repeatedly enforces constraints 
    * Arcs can become inconsistent - If X loses a value, it's neighbors need to be rechecked
    * **Arc consistency detects failure earlier than forward checking**
    * ~~Can be run as a preprocessor or after each assignment~~
  * Improving Further
    * Minimum remaining values (MRV) - Choose the variable with the fewest legal left values in its domain and 
    * Degree Heuristic (Deg) - Choose the variable with the most constraints on remaining variable (own most arcs)
    * Least constraining value (LCV) - Choose the value that rules out the fewest values in remaining variables

**Adversarial Search**

* A multi-agent competitive environment 
* Game Definition 
  * s: States
  * s0: Initial state
  * Players: define which player makes the move
  * Actions: 
  * Result(s,a): define result of a move
  * Terminal test: True when game is over
  * Utility(s,p): defines final numeric value for a game that ends in terminal state s for player p 
* A game tree can be constructed
  * eg. tic-tac-toe(u=-1 if O wins, u=1 if X wins, and u=0 if no one wins)
* Minimax Search
  * A state-apce search tree
  * Players alternate turns
  * Compute each node's minimax value
    * the best achievable utility against a rational(optimal) adversary
    * Minimax(s) = 
    *        Utility(s)                if Terminal-Test(s)
    *        max(Minimax(Result(s,a))) if Player(s) = Max
    *        min(Minimax(Result(s,a))) if Player(s) = Min
  * Complete? **Yes**
  * will **not** lead to optimal play
    * optimal against perfect play
    * Time complexity: O(
$b^m$); Space complexity: O(bm)
* DLS (Depth-limit Search)
  * DFS-TSA with a depth limit and an evaluation function
    * not complete if d > 1; complete if d <= 1
    * not optimal
    * time: O(
  $b^l$); space: O(bl)
  * Replace terminal utilities with an evaluation function for non-terminal positions
  * Problem:
    * No guarantee for optimal action
    * Need to design evaluation function
  * Evaluation Function: Eval(s)
    * an estimate of the expected utility of the game from given position
    * Ideal funcion: The actual minimax value of the position
  * Depth Matters: the deeper the tree, the less quality of the evaluation function matters
  * Horizon Effect: with low depth limit, we don't know some damage is ultimately unavoidable
* Game Tree Pruning ($\alpha-\beta$ pruning algorithm)
  * can determine minimax values without looking at all nodes
  * eg. Min version:
    * consider Min's value at node n
    * if n < m, then Max will avoid n, thus no need to consider n's other children
    * Key: for Max, get max(v) and compare it to $\beta$; if smaller, upadate $\alpha$
  * Problem: can't determine root if node(a)=10, node(b)<=10; effectiveness depends on ordering
  * O(
$b^{m/2}$) rather than O(
$b^m$)
* Expectimax Search -- chance matter ( when the result of an action unknown)
  * Values reflect average case outcomes, not worst case outcomes
    * caculate expected utilities ( weighted average of children)
* Expectiminimax Search
* Multi-Agent Utilities
  * Generalization of minimax
    * terminals and nodes have utility vectors
    * each player maximizes its own component
    * Gives rise to cooperation and competition dynamically
