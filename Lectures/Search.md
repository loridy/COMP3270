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
