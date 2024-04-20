import random
import numpy as np
import matplotlib.pyplot as plt

class Item:
    def __init__(self, id, length, width, height):
        self.id = id
        self.length = length
        self.width = width
        self.height = height

    @property
    def volume(self):
        return self.length * self.width * self.height

class Container:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.remaining_capacity = length * width * height
        self.items = []
    
    def add_item(self, item, orientation=0):
        if self.remaining_capacity >= item.volume:
            self.items.append((item, orientation))
            self.remaining_capacity -= item.volume
            self.items.sort(key=lambda x: (x[1], -x[0].length * x[0].width * x[0].height))
            return True
        else:
            return False

    @property
    def volume(self):
        return self.length * self.width * self.height

class GeneticAlgorithm:
    def __init__(self, population_size=1000, max_generations=2000, mutation_rate=0.1):
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.colors = {} 

    def optimize(self, num_containers, items, container_length, container_width, container_height):
        population = self.generate_initial_population(num_containers, items, container_length, container_width, container_height)
        best_solution = None
        best_fitness = float('inf')

        for generation in range(self.max_generations):
            population_fitness = [(containers, self.fitness(containers)) for containers in population]
            population_fitness.sort(key=lambda x: x[1])

            if population_fitness[0][1] < best_fitness:
                best_solution = population_fitness[0][0]
                best_fitness = population_fitness[0][1]

            parents = [population_fitness[i][0] for i in range(2)]
            child = self.crossover(parents[0], parents[1])
            self.mutate(child)

            population[-1] = child

            print("Generation:", generation, "Best fitness:", best_fitness)
            if best_solution is not None:
                print("Best solution:")
                for container in best_solution:
                    print("Container Capacity:", container.volume)
                    print("Items:", [(item[0].id, item[0].length, item[0].width, item[0].height, item[1]) for item in container.items])
                    print("Remaining Capacity:", container.remaining_capacity)
                    self.plot_solution(best_solution, container_length, container_width, container_height)

    def generate_initial_population(self, num_containers, items, container_length, container_width, container_height):
        population = []
        for _ in range(self.population_size):
            containers = [Container(container_length, container_width, container_height) for _ in range(num_containers)]
            random.shuffle(items)
            for item in items:
                container_index = random.randint(0, num_containers - 1)
                orientation = random.randint(0, 2)
                while not containers[container_index].add_item(item, orientation):
                    container_index = random.randint(0, num_containers - 1)
            population.append(containers)
        return population

    def fitness(self, containers):
        return sum(container.remaining_capacity for container in containers)

    def crossover(self, parent1, parent2):
        child = [Container(parent1[i].length, parent1[i].width, parent1[i].height) for i in range(len(parent1))]
        for i in range(len(parent1)):
            for item, orientation in parent1[i].items:
                child[i].add_item(item, orientation)
            for item, orientation in parent2[i].items:
                if not child[i].add_item(item, orientation):
                    break
        return child

    def mutate(self, containers):
        for container in containers:
            if random.random() < self.mutation_rate:
                item_index = random.randint(0, len(container.items) - 1)
                new_container_index = random.randint(0, len(containers) - 1)
                new_container = containers[new_container_index]
                new_container.add_item(container.items.pop(item_index)[0])  # 修改此行



    def plot_solution(self, containers, container_length, container_width, container_height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制容器
        ax.plot([0, container_length], [0, 0], [0, 0], color='k')  # 底部边
        ax.plot([0, container_length], [container_width, container_width], [0, 0], color='k')  # 顶部边
        ax.plot([0, 0], [0, container_width], [0, 0], color='k')  # 侧边1
        ax.plot([0, 0], [0, container_width], [container_height, container_height], color='k')  # 侧边2
        ax.plot([container_length, container_length], [0, container_width], [0, 0], color='k')  # 侧边3
        ax.plot([container_length, container_length], [0, container_width], [container_height, container_height], color='k')  # 侧边4

        # 绘制物体
        for i, container in enumerate(containers):
            for item, orientation in container.items:
                x = 0
                y = 0
                z = 0
                if orientation == 0:
                    x = random.uniform(0, container.length - item.length)
                    y = random.uniform(0, container.width - item.width)
                    z = random.uniform(0, container.height - item.height)
                elif orientation == 1:
                    x = random.uniform(0, container.length - item.length)
                    y = random.uniform(0, container.width - item.height)
                    z = random.uniform(0, container.height - item.width)
                else:
                    x = random.uniform(0, container.length - item.width)
                    y = random.uniform(0, container.width - item.height)
                    z = random.uniform(0, container.height - item.length)

                ax.bar3d(x, y, z, item.length, item.width, item.height, color=self.get_item_color(item), edgecolor='k')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Packing Solution')
        plt.show()

    def get_item_color(self, item):
        if item.id not in self.colors:
            self.colors[item.id] = np.random.rand(3,)
        return self.colors[item.id]

if __name__ == "__main__":
    items = [
        Item('1', 1300, 750, 1600),
        Item('2', 800, 800, 1900),
        Item('3', 800, 800, 1900),
        Item('4', 2100, 860, 1100),
        Item('5', 2100, 860, 1100),
        Item('6', 2100, 860, 1100),
        Item('7', 2100, 860, 1100),
        Item('8', 2100, 860, 1100),
        Item('9', 2100, 860, 1100),
        Item('10', 2100, 860, 1100),
        Item('11', 2100, 860, 1100),
        Item('12', 2100, 860, 1100),
        Item('13', 2100, 860, 1100),
        Item('14', 2100, 860, 1100),
        Item('15', 2100, 860, 1100),
        Item('16', 2100, 860, 1100),
        Item('17', 2100, 860, 1100),
        Item('18', 2100, 860, 1100),
        Item('19', 2100, 860, 1100),
        Item('20', 2100, 860, 1100),
        Item('21', 3030, 1150, 1100),
        Item('22', 3030, 1150, 1100),
        Item('23', 3030, 1150, 1100),
        # Add other items here
    ]

    container_length = 12050
    container_width = 2320
    container_height = 2550

    num_containers = 1

    genetic_algorithm = GeneticAlgorithm()
    genetic_algorithm.optimize(num_containers, items, container_length, container_width, container_height)
