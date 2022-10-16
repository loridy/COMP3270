**Sequential Decision Problem**
* Agent’s utility depends on a sequence of decisions
* incorporate utitlities, uncertainty, and sensing
* optimal behavior balances thie risks and rewards of acting in uncertain environment

**Deterministic VS. Stochastic motion**
* unreliable actions (eg. achieve intended effect 80% of the time)

**Transition model**
* T(s,a,s') describes the outcome of each action in each state
* P(s'|s,a) denotes the probability of reaching state s'
* Transitions are [Markovian](https://en.wikipedia.org/wiki/Markovian#:~:text=Markovian%20is%20an%20adjective%20that,property%20of%20a%20stochastic%20process)
  * probability of reaching s' from s depends on s, not history of earlier states
  * named after Andrey Markov

**Markov Decision Process**
* A sequential decision problem for a fully observable, stochastic environment with a Markovian transition model and additive rewards
* Defined by
  * A set of states $s \in S$
  * A set of actions $a \in A$
  * A transition function T(s,a,s')
    * with probability P(s'|s,a)
  * A reward function R(s,a,s')
  * A start state $s_{0}$
  * A terminal state(optional)

**Policy**
* How to solve MDPs
  * A solution must specify what the agent should do for any state that the agent might reach
  * A solution of this kind is called a policy $\pi$
    * $\pi(s)$ is the action recommended by policy $\pi$ for state s
* **Optimal Policy**
  * An optimal policy $\pi^{*}$ is the policy that yields the highest expected utility

**MDP Search Tree**
* Each MDP state projects an expectimax-lik search tree
* Q state
  * The agent has committed to the action but has not done it yet

**Utility of State Sequences**
* Discounting
  * values of rewards decay exponentially by $\gamma$
* Additive rewards
  * $U([s_{0},s_{1},s_{2},...]) = R(s_{0})+R(s_{1})+...$
* Discounted rewards
  * $U([s_{0},s_{1},s_{2},...]) = R(s_{0})+\gamma R(s_{1})+\gamma^{2}R(s_{2})+...$
* Infinity Utilities
  * With discounted rewards, the utility of an infinite sequence is finite
  * $U([s_{0},s_{1},s_{2},...]) = sum_{t = 0}^{\infty} \gamma^{t} R(s_{t}) \le sum_{t = 0}^{\infty} \gamma^{t} R_{max} = R_{max}/(1-\gamma)$

**Optimal Quantities (Computed by Bellman Equation)**
* $V^{\*}(s)$ is value(utility) of a state
  * expected utility starting in s and acting optimally
  * $V^{\*}(s) = maxQ^{\*}(s,a)$
  * $V^{\*}(s) = max\sum_{s'} T(s,a,s')[R(s,a,s')+\gamma V^{\*}(s')] $
* $Q^{\*}(s,a)$ is the value of a q-state(s,a)
  * expected utility for having taken action a from state s
  * $Q^{\*}(s,a) = \sum_{s'} T(s,a,s')[R(s,a,s')+\gamma V^{\*}(s')] $
* $\pi^{\*}(s)$ is the optimal policy for state s
* **Optimal Utility $V^{\*}(s)$ represented by expected value of actions following $\pi^{\*}(s)$**

** ~~Computing Time-Limited Values~~ **

**Value Iteration**
* Start with $V_{0}$
  * No time steps left means an expectd reward sum of zero
* Given vector of $V_{k}(s)$ values, do one round of expectimax
* $V_{k+1}(s) <-- max \sum_{s'} T(s,a,s')[R(s,a,s')+\gamma V_{k}(s')]$
* Repeat until convergence
* Complexity: $O(S^{2}A)$
* Theorem: Converges to unique optimal values


**Policy Methods**
* Policy Evaluation
  * How good a given policy $\pi$ is
  * $V^{\pi}(s)$ = expected total discounted rewards starting in s and following $\pi$
  * $V^{\pi}(s) = \sum_{s'} T(s,\pi(s),s')[R(s,\pi(s),s')+\gamma V^{\pi}(s')]$
  * Idea 1: turn recursive Bellman equations into upadtes(following fixed policy)
    * Efficiency: $O(S^{2})$ per iteration
  * Idea 2: withou max, Bellman equations are just linear system
    * Use a linear system solver
* Policy Extraction
  * If we have optimal values $V^{\*}(s)$, do a one-step mini-expectimax
    * $\pi^{\*}(s) = argmax \sum_{s'} T(s,a,s')[R(s,a,s')+\gamma V^{\*}(s')]$
    * Or $\pi^{\*}(s) = argmax Q^{\*}(s,a)$ (Actions are easier to select from q-values than values)
  * **Idea: get the policy implied by the values**
* Improve runtime of value iteration
  * Slow: $O(S^{2}A) per iteration
  * Max at each state rarely changes (policy often converges long before values)

**Policy Iteration**
* Update policy using one-step look-ahead with resulting converged(but not optimal!) utilities as future values
  * can converge (much) faster under some conditions
* Evaluation
  * Iterate until values converge 
  * $V_{k+1}^{\pi_{i}}(s) <--  \sum_{s'}T(s,\pi_{i}(s),s')[R(s,\pi_{i}(s),s')+\gamma V_{k+1}^{\pi_{i}}(s')]$
* Improvement
  * One step look ahead
  * $\pi_{i+1}(s) = argmax \sum_{s'} T(s,a,s')[R(s,a,s')+\gamma V^{\*}(s')]$

**Comparison**
* Both value iteration and policy iteration compute the same thing(all optimal values)
* In value iteration
  * Every iteration updates both values and the policy
  * Don't track the policy, but taking the max over actions implicitly
* In policy iteration
  * Do several passes that updates utilities with fixed policy **_(each pass is fast because we consider only on action, not all of them)_**
  * After policy evaluated, a new policy is chosen (slow like a value iteration pass)
  * The new policy will be better (or we're done)
* Both are dynamic programs for solving MDPs

**Summary: MDP Algorithms**
* Compute optimal values:
  * value iteration or policy iteration
* Compute values for a particular policy
  * policy evaluation
* Turn values into policy
  * policy extraction (one-step lookahead)
* Similarity:
  * basically the same -- all variations of Bellman updates
  * all use one-step lookahead expectimax fragments
  * Differ only in whether plug in a fixed policy or max over actions
