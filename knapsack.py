import random

# define the Knapsack problem
class knapsack():

    # Initiate Knapsack problem object
    def __init__(self, w, v, max_w, pop_size = 100, num_generations = 10):
        self.w = w  # list of weights
        self.v = v  # list of values
        self.max_w = max_w  # maximum weight that bag can carry
        self.N = len(w)
        self.pop_size = pop_size
        self.num_generations = num_generations

    # Solve Knapsack problem with population size pop
    def solve(self, num_generations = 20):
        pop_size = self.pop_size
        num_generations = self.num_generations
        self.pop = self.first_population()  # initiate self.pop = first population

        best_choice = []
        best_fit = 0

        # Number of generations: currently 10
        for gen in range(num_generations):
            new_pop = []
            for i in range(2*pop_size):
                # pick 2 chromosomes to cross over
                choice1 = self.pick_chromosome()
                choice2 = self.pick_chromosome()
                new_choice = self.cross_over(choice1, choice2)
                new_choice = self.mutate(choice = new_choice, prob = 0.1)
                new_pop.append((self.fitness(new_choice), new_choice))

            # Sort by fitness
            new_pop = sorted(new_pop, reverse=True)

            # delete bottom 50% of the new population
            self.pop = new_pop[:pop_size]

            # check if the new population has a chromosome that improves the current choice
            for item in self.pop:
                if (item[0] > best_fit) and (self.total_weight(item[1]) <= self.max_w):
                    best_fit = item[0]  # record the fitness of new best choice
                    best_choice = item[1]  # store new best choice

        # print out results
        print('Congratulations! Your best fit gives a total value of ' + str(self.total_value(best_choice)) + ', and weighs ' + str(self.total_weight(best_choice)))
        print('Items to be packed:')
        for i in range(self.N):
            if best_choice[i] == 1:
                print(' - Item #' + str(i+1) + ' with weight = ' + str(self.w[i]) + ' and value = ' + str(self.v[i]))


    # Calculate total weight of a particular choice
    # choice is a 1-by-N binary vector, where choice[i] = 1 means item i is chosen
    def total_weight(self, choice):
        return sum([choice[i]*self.w[i] for i in range(self.N)])

    # Calculate total value of a particular choice
    # choice is a 1-by-N binary vector, where choice[i] = 1 means item i is chosen
    def total_value(self, choice):
        return sum([choice[i]*self.v[i] for i in range(self.N)])

    # fitness function to calculate fit for a particular choice
    # choice is a 1-by-N binary vector, where choice[i] = 1 means item i is chosen
    def fitness(self, choice):
        # if choice exceeds weight limit, impose a very negative fitness score
        if self.total_weight(choice) > self.max_w:
            return 0.0001

        # if choice satisfies weight limit, fitness score = total values plus space left
        theta = 10000  # how much do we weigh current value versus space still available
        return (self.max_w-self.total_weight(choice))^2 + theta*self.total_value(choice)^2

    def first_population(self):
        init_pop = [] # initialize
        for i in range(self.pop_size):
            choice = [random.choice([0, 1]) for j in range(self.N)]  # generate a random sequence of 0 and 1
            choice = self.fix_choice(choice)  # "fix" it by removing heavy weights until the initial choice is valid (total weight < max weight)
            fit = self.fitness(choice)  # calculate the fitness of this choice
            init_pop.append((fit, choice))  # add to initial population
        return init_pop

    # given a choice, remove (if necessary) weights until it becomes less that the limit
    def fix_choice(self, choice):
        w = self.total_weight(choice)  # the total weight of current choice
        current_items = [i for i in range(self.N) if choice[i] == 1] # items in this choice
        weights = [(self.w[i], i) for i in current_items]  # the weights of these items
        weights = sorted(weights, reverse = True)  # sort by item weights
        while w > self.max_w:  # repeat as long as this choice still exceeds the weight limit
            item = weights.pop(0)  # remove the heaviest item
            choice[item[1]] = 0
            w = w - item[0]  # decrease the total weight after removing
        return choice

    def cross_over(self, choice1, choice2):
        i = random.randint(1, self.N - 1) # randomly choose where the split happens
        return choice1[:i] + choice2[i:]  # get first half from choice1 and second half from choice 2

    def mutate(self, choice, prob): # mutate a choice with some probability
        if random.random() < prob:
            i = random.randint(0, self.N-1)  # choose where it happens randomly
            choice[i] = 1 - choice[i]  # convert 1 to 0 and vice versa
        return choice

    def pick_chromosome(self):
        # get list of items and corresponding fitness
        chromosomes = [item[1] for item in self.pop]
        fit = [item[0] for item in self.pop]
        # make choice using fitness as weight
        sum_fit = sum(fit)
        weight = [item/sum_fit for item in fit]
        return random.choices(population = chromosomes, weights = weight)[0]


# declare the Knapsack problem
w = [20, 30, 60, 90, 50, 70, 30, 30, 70, 20, 20, 60]  # weights
v = [6, 5, 8, 7, 6, 9, 4, 5, 4, 9, 2, 1]  # values
max_weight = 120

prob = knapsack(w = w, v = v, max_w = max_weight, pop_size = 100, num_generations = 100)
prob.solve()
