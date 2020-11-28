Author: Qijin Chau

1) The problem as a searching problem is described below.
   
   The five compenents of a search problem:
   
   - Initial state: The starting position. The list of numbers passed in as input data to represent the starting stack of pancakes.
   
   - Possible actions: The possible flips at all n-1 locations for a stack of pancakes with size n.
   
   - Successor function (transition model): The flip or each possible action will reverse the order of all the pancakes from the position being flipped and above. If the flip is at position 3, then all pancakes between and including the third pancake from the bottom and very top pancake will be reversed. 
   
   - Goal test: Checking if the state of the current stack of pancakes has reached the goal state where the largest pancake is on the bottom and decreasing in size up to the smallest pancake on the top.
   
   - Path cost function: The backwards and forwards costs described below.


2) A possible cost function (backwards cost) can be defined as the number of flips that were already made. For example if the stack [4, 3, 2, 5, 1] was flipped at the 2nd position, then at position 3. This would result in the stack [4, 1, 3, 2, 5]. The cost of this one flip would be 2. The number of pancakes flipped should not affect the backwards cost function.


3) A possible heuristic function (forward cost) can be defined using a heuristic function similar to the gap heuristic. For this problem, we can define the "gaps" as places in the stack where a pancake doesn't have correct neighbors. For example, if 4 isn't next to either 3 or 2, then this would be considered a "gap" and we would add 1 to the heuristic cost. The heuristic function would use these gaps to calculate a total heuristic cost which would serve as the estimated number of flips required to correctly order the pancakes from the current position. Now a slight modification we will add is a +1 to the total heuristic cost if the largest pancake is not at the bottom of the stack.


4) A Uniform-Cost-Search algorithm can also be used. We just have to get rid of the heuristic function within the A* algorithm. My implented Uniform-Cost-Search algorithm is below my A* algorithm in the pancake.py file.
