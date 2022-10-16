**Reinforcement Learning**
* Solving MDPs is offline planning
  * determine all quantities through computation
  * need to know the details of MDP
  * don not actually play the game
* Reinforcement learning
  * Exploration: you have to try unknwon actions to get information
  * Exploitation: eventually, you have to use what you know
  * Regret: even if you learn intelligently, you make mistakes
  * Sampling: because of chance, you have to try things repeatedly
  * Difficulty: learning can be much harder than solving a known MDPs

**Basic idea**
* Receive feedback in the form of rewards
* Agent's utility is defined by the reward function
* Must (learn to) act so as to maximize expected rewards
* All learning is based on observed samples of outcomes
* eg. A MDP with Transition model and Reward unknown
  * A set of states $s \in S$
  * A set of actions $a \in A$
  * A model T(s,a,a')
  * A reward R(s,a,s')
  * Goal: looking for policy $\pi(s)$

**Model-Based Learning**
* Idea
  * Learn an approximate model based on experiences
  * Solve for values as if the learned model were correct
  * Step 1: Learn emperical MDP model
    * Count outcomes s' for each action(s,a)
    * Normalize to give an estimate of $T(s,a,s')$
    * Discover each $R(s,a,s')$ when experience (s,a,s')
  * Step 2: Solve the learned MDP
    * $V_{k+1}^{\pi_{i}}(s) <--  \sum_{s'}T(s,\pi_{i}(s),s')[R(s,\pi_{i}(s),s')+\gamma V_{k+1}^{\pi_{i}}(s')]$

**Model-Free Learning**
* Passive Reinforcement Learning
  * Simplified task: policy evaluation
    * Input: a fixed policy $\pi(s)$
    * Don't know transitions T(s,a,s') and rewards R(s,a,s')
    * Goal: learn the state values
  * No choice about what actions to take
    * Just execute policy and learn from experience
    * **Not Offline Planning!** You can actually take actions in the world
* Direct Evaluation
  * Goal: compute values for each state under $\pi$
  * Idea: Average together observed sample values
    * Act according to $\pi$
    * Once visit a state, write down the sum of discounted rewards
    * Average samples
  * States are evaluated seperately
  * Pros
    * Easy to understand
    * Knowledge of T and R not required
    * Eventually computes the correct values
  * Cons
    * State connections are not considered
    * Each state must be learned seperately
    * Takes a long time to learn

**Sample-Based Policy Evaluation**
* imporve estimate of V by computing averages
  * $V_{k+1}^{\pi_{i}}(s) <--  \sum_{s'}T(s,\pi_{i}(s),s')[R(s,\pi_{i}(s),s')+\gamma V_{k+1}^{\pi_{i}}(s')]$
* Idea: take samples of outcomes s' and average
  * $sample_{1} = R(s,\pi(s), s_{1}') + \gamma V_{k}^{\pi}(s_{1}')$
  * $sample_{2} = R(s,\pi(s), s_{2}') + \gamma V_{k}^{\pi}(s_{2}')$
  * ...
  * $sample_{n} = R(s,\pi(s), s_{n}') + \gamma V_{k}^{\pi}(s_{n}')$
  * $V_{k+1}^{\pi}(s) <-- {1 \over n} \sum_{i} sample_{i}$

**Improvements: Temporal Difference Learning**
* Learn from every experience
  * Update V(s) each time experience a transition (s,a,s',r)
  * outcomes s' will contribute upadtes more often
* Temporal difference learning of values
  * Policy still fixed, still doing evaluation
  * Move values towards value of whatever successor occurs
    * Sample of V(s): $sample = R(s,\pi(s), s') + \gamma V^{\pi}(s')$
    * Update to V(s): $V^{\pi} <-- (1-\alpha) V^{\pi}(s) + (\alpha) sample$
    * $V^{\pi} <-- V^{\pi}(s) + \alpha (sample - V^{\pi}(s))$
  * Exponential Moving Average
    * recent samples more important
    * Forgets about the past(distant past values were wrong anyway)
  * Decreasing learning rate(alpha) can give converging averages


**Active Reinforcement Learning**
* Q-Value Iteration
  * Value iteration: find successive (depth-limiterd) values
    * Start with $V_{0}(s) = 0$
    * Given $V_{k}$, calculate the depth k+1 values for all states:
    * $V_{k+1}(s) <-- max \sum_{s'} T(s,a,s')[R(s,a,s') + \gamma V_{k}(s')]$
  * rather than compute values, compute Q-values
    * Start with $Q_{0}(s,a) = 0 $
    * Given $Q_{k}$
    * $Q_{k+1}(s) <-- \sum_{s'} T(s,a,s')[R(s,a,s') + \gamma max V_{k}(s')]$

**Q-Learning**
* sample-based Q-value Iteration
  * $Q_{k+1}(s) <-- \sum_{s'} T(s,a,s')[R(s,a,s') + \gamma max V_{k}(s')]$ 
* Steps:
  * Receive a sample (s,a,s',r)
  * Consider old estimate: Q(s,a)
  * Consider new estimate
    * $sample = R(s,a,s') + \gamma max Q(s',a')$
  * Incorporate new esitemate into running average:
    * $Q(s,a) <-- (1-\alpha)Q(s,a) + (\alpha)(sample)$
* Properties
  * off-policy learning
    * converges to optimal policy even if you're acting suboptimally
  * Limitations:
    * need to explore enough
    * have to eventually make the learning rate small enought

**Exporation VS. Exploitation**
* Simplest scheme for forcing exploration: random actions($\beta$-greedy)
  * Every time step, flip a coin
    * With small probability $\beta$, act randomly
    * With large probablitiy $1-\beta$, act on current policy
  * Problems:
    * Keep thrashing around once learning is done
  * Solution:
    * Lower $\beta$ over time
    * Using exploration functions
* Exploration Functions
  * Random actions: explore a fixed amount
  * Better idea: explore areas whose badness is not yet established, eventually stop exploring
  * Takes a value estimate u and a vist count n, and returns an optimistic utility
    * f(u,n) = u + k/n
    * Q(s,a) <-- R(s,a,s') + \gamma max f(Q(s',a'), N(s',a'))
    * Note: This propagates the "bonus" k back to states that lead to unknown states as well
* Regret
  * Even if you learn the optimal policy, you still make mistakes
  * Regret is a measure of your toal mistake cost: the difference between your (expected) rewards, including youthful suboptimality, and optimal (expected) rewards
  * Minimizing regret goes beyond learning to be optimal – it requires optimally learning to be optimal
  * eg. random exploration and exploration functions both end up optimal, but random exploration has higher regret









