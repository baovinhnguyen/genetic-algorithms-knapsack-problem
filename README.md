# genetic-algorithms-knapsack-problem
Use genetic algorithms to solve the knapsack problem, which is to fill the backpack to make it as valuable as possible without exceeding the maximum weight. 


Define the problem as genetic algorithm:

-chromosome: a sequence of 0 and 1 - 1 means the item should be picked, and 0 means the item should not be picked.

-mutation: randomly convert 1 to 0 and vice versa with some probability.

-cross over: randomly choose where the split happens, and get first half from choice 1 and second half from choice 2. 

-fitness function: if current total weight is bigger than the maximum weight that the bag can carry, the score is approximately zero. If the choice satisfies the weight limit, fitness score is equal to total values plus space left. I set a parameter theta, which means how much do we weight current values versus space still available. I multiply theta with the total value, which means I prioritize total value over total weight. 

-solution test: "fix" overweight by removing heavy weights until the initial choice is valid, which means total weight is smaller than max weight.

-population size: 100

-generation limit: 100
