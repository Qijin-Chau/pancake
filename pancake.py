#!/usr/bin/python
# Author: Qijin Chau

# Running: After running the python script, the UI print statements
#          should be pretty self-explanatory. A couple notes for
#          choosing user input are listed below.
# 
# NOTES: 
#		1) Make sure an integer is entered when choosing the options
#          provided/printed. My UI code casts the user input to an int
#          to be used for comparison to decide which route to take.
#          Thus it will complain and abort if a string is entered.
#       2) UCS is a lot slower than A* for any stack size above 8
#          so keep this in mind when manually entering a size.
#          Also, this means random could be very slow if a number 
#          above 8 is randomly generated. 


import heapq
import random


class Pancakes:
	def __init__(self, pancake_stack = []):
		self.stack = pancake_stack
		self.size_of_stack = len(self.stack)

	# Necessary for heappop to compare different Pancakes objects
	def __lt__(self, other):
		if self.heuristic() < other.heuristic():
			return self.stack
		else:
			return other.stack


	# Reverses the stack parameter passed in, which is a list, and returns it
	def reverseStack(self, stack): 
		size = len(stack) - 1
		new_stack = []
		
		while (size >= 0):
			new_stack = new_stack + [stack[size]]
			size = size - 1
		
		return new_stack


	# Uses the reverseStack function to flip the stack of pancakes
	# at a specified position and return the stack with the
	# pancakes at their new positions
	def flipStack(self, position):
		# Same as just reversing the entire stack as is
		if (position == 1):
			return self.reverseStack(self.stack)
		
		else:
			bottom_half = self.stack[:position-1]
			top_half = self.reverseStack(self.stack[position-1:])
			return bottom_half + top_half
        

	# Gap heuristic function 
	def heuristic(self):
		heuristic_cost = 0
		stack_length = len(self.stack)

		# If the biggest pancake is not on the bottom
		if (self.stack[0] != stack_length): 
			heuristic_cost = heuristic_cost + 1
		
		counter = 0
		
		# Iterate through each pancake in the stack
		while (counter < stack_length-1):
			curr_pancake = self.stack[counter]
			correct_next_pancake = curr_pancake + 1
			correct_prev_pancake = curr_pancake - 1

			# If the current pancake doesn't have at least one appropriate 
			# adjacent neighbor in the stack, then cost increases
			if ((self.stack[counter+1] != correct_next_pancake) & (self.stack[counter+1] != correct_prev_pancake)):

				heuristic_cost = heuristic_cost + 1
			
			counter = counter + 1
		
		return heuristic_cost


	# Checks to see if the stack is correct by comparing it to 
	# what the final stack should look like
	def checkStack(self, final): 
		if (self.stack == final): 
			return True
		else: 
			return False


class Solve:
	# A* algorithm
	def AStar(self, stack):
		stack_size = stack.size_of_stack

		# Desired final stack of pancakes
		target = stack.reverseStack(list(range(1, stack_size+1)))
		
		# If the current stack is already in the correct order, then we are done
		if (stack.checkStack(target)): 
			return []
        
        # Priority queue to store then potentially use the various stacks
        # we will create after each possible flip
		priority_q = [] 
    	
    	# We are going to flip at each possible position to fill up
    	# the queue for initialization and some stuff into the frontier 
		for pos in range(1, stack_size):
			
			# After each flip, if the new stack is in the correct final order,
			# then we return the position of that flip. Otherwise we push
			# the new stack into the priority queue to possibly use later
			# depending on the forwards+backwards cost of these stacks in the queue
			newstack = Pancakes(stack.flipStack(pos))
			if (newstack.checkStack(target)): 
				return [pos]
			else:
				# Cost is the backward cost of the flip plus the forward cost
				# Backward cost is 1 because only one flip has been performed
				backward_cost = 1 
				forward_cost = newstack.heuristic()
				heapq.heappush(priority_q, (backward_cost+forward_cost, newstack, [pos]))
    	

    	# In each loop, we are going to get the least cost expensive pancake 
    	# stack in the priority queue based on total forwards plus backwards
    	# cost for each pancake stack that is in the queue. Then this stack  
    	# is flipped at each position besides the position of the very last 
    	# flip. For each flip, check if the flip solves the stack, if so, then 
    	# return this current flip along with all the previous flips that were 
    	# used. Otherwise we push this stack (after being flipped) back into 
    	# the priority queue and repeat the process until we find the proper
    	# flips used to produce a correct stack. 

    	# While priority queue is not empty
		while len(priority_q) > 0:

			# Get stack with lowest total forwards and backwards cost
			popped_stack = heapq.heappop(priority_q)
			current_stack = popped_stack[1] 
			
			# The flips that were already already performed to
			# produce the popped stack we got
			flips_used = popped_stack[2]

			# The very last flip that was performed on the popped stack we got
			last_flip = flips_used[len(flips_used)-1]

			for pos in range(1, stack_size):
				# Make sure we don't repeat the flip that was last performed
				if (pos != last_flip): 
					new_stack = Pancakes(current_stack.flipStack(pos))
					
					# If the flip we perform solves the stack, then add that flip
					# to the flips that were already performed and return all the flips
					if (new_stack.checkStack(target)): 
						return flips_used + [pos]
					else:
						# Cost is the backward cost plus the forward cost
						# Backward cost is 1 for the current flip just made plus
						# the flips the were already used
						backward_cost = 1 + len(flips_used)
						forward_cost = new_stack.heuristic()
						heapq.heappush(priority_q, (backward_cost+forward_cost, new_stack, flips_used + [pos]))
                        

	# Uniform-Cost-Search algorithm
	# Essentially same as A* above except without the heuristic function
	# Since there is no heuristic function, this search is uninformed and slower
	def Uniform_Cost_Search(self, stack):
		stack_size = stack.size_of_stack
		target = stack.reverseStack(list(range(1, stack_size+1)))
		
		if (stack.checkStack(target)): 
			return []
        
		priority_q = [] 
		for pos in range(1, stack_size):
			newstack = Pancakes(stack.flipStack(pos))
			if (newstack.checkStack(target)): 
				return [pos]
			else:
				backward_cost = 1 
				heapq.heappush(priority_q, (backward_cost, newstack, [pos]))

		while len(priority_q) > 0:
			popped_stack = heapq.heappop(priority_q)
			current_stack = popped_stack[1] 
			flips_used = popped_stack[2]
			last_flip = flips_used[len(flips_used)-1]
			for pos in range(1, stack_size):
				if (pos != last_flip): 
					new_stack = Pancakes(current_stack.flipStack(pos))
					if (new_stack.checkStack(target)): 
						return flips_used + [pos]
					else:
						backward_cost = 1 + len(flips_used)
						heapq.heappush(priority_q, (backward_cost, new_stack, flips_used + [pos]))
                        

    # A separate flip function used for printing purposes in the following function 
	def flipForPrinting(self, pancake_class, pancake_stack, position):
		if (position == 1):
			return pancake_class.reverseStack(pancake_stack)
		else:
			return pancake_stack[:position-1] + pancake_class.reverseStack(pancake_stack[position-1:])


	# Prints the results of the desired algorithm out for a visual
	def printVisual(self, stack, algorithm):
		stack_for_print = stack.stack

		if algorithm == "A*":
			all_correct_flips = self.AStar(stack)
		elif algorithm == "UCS":
			all_correct_flips = self.Uniform_Cost_Search(stack)
		
		counter = 0
		end = len(all_correct_flips)
		if (end == 0):
			print ("The stack of pancakes is already in the correct order") 
		else:
			print ("\nStarting %s" % algorithm + " algorithm") 
			print("Starting stack of pancakes:\n" + str(stack_for_print))
			print()
			print("The optimum order of flips to get the pancakes in correct order is listed below!")
			print()
			while (counter < end):
				stack_for_print = self.flipForPrinting(stack, stack_for_print, all_correct_flips[counter])
				print ("Flipped at position " + str(all_correct_flips[counter]) + ":") 
				print (str(stack_for_print))
				print()
				counter = counter + 1
			print ("\nTotal of " + str(end) + " flips performed") 
			print ("Flips were performed in the order of\n" + str(all_correct_flips))
			print ("\nAlgorithm completed!")
            


# Creates a random stack pancakes of the size passed in
def randomStack(size):
    stack = list(range(1, size+1))
    random.shuffle(stack)
    return stack


# User interface
def pancakeMainUI():
	print ("For the size of the stack would you prefer: ")
	method = int(input("(1) Random (2) Manual\n"))
	while (method != 1 and method != 2):
		method = int(input("Please enter either 1 for random size or 2 for manual size: "))

	# Which algorithm desired
	algorithm = int(input("Which algorithm do you want?\n(1) A* (2) UCS\n"))
	while (algorithm != 1 and algorithm != 2):
		algorithm = int(input("Please enter either 1 for A* or 2 for Uniform-Cost-Search: "))
        
        
	stack_solver = Solve()
	if (method == 1):

		# Random size from 3-25
		rand_size = random.randint(3, 25)

		print ("Random stack size: " + str(rand_size))
		stack = Pancakes(randomStack(rand_size))

		if (algorithm == 1):
			stack_solver.printVisual(stack, "A*")
		else:
			stack_solver.printVisual(stack, "UCS")
	else:
		# Limit user input to 3-15 so the program doesn't take a long time to run
		requested_size = int(input("Enter a stack size between 3 and 25: "))
		while (requested_size < 3 or requested_size > 25):
			requested_size = int(input("Please only input a number between 3 and 25: "))
		
		print ("Stack size requested: " + str(requested_size))
		stack = Pancakes(randomStack(requested_size))
		
		if (algorithm == 1):
			stack_solver.printVisual(stack, "A*")
		else:
			stack_solver.printVisual(stack, "UCS")


if __name__ == "__main__":
	pancakeMainUI()