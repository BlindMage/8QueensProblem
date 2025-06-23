import random


def calculate_attacks(individual):
    """
    Calcula o número de ataques (pares de rainhas que se atacam) para um indivíduo.
    Um ataque ocorre se duas rainhas estão na mesma linha ou na mesma diagonal.
    Como a representação garante que não há rainhas na mesma coluna,
    só precisamos verificar linhas e diagonais.
    """
    n = len(individual)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Verifica ataques na mesma linha
            if individual[i] == individual[j]:
                attacks += 1
            # Verifica ataques nas diagonais
            if abs(individual[i] - individual[j]) == abs(i - j):
                attacks += 1
    return attacks


def get_fitness(individual):
    """
    Calcula o fitness de um indivíduo.
    O fitness é o inverso do número de ataques.
    Quanto menos ataques, maior o fitness.
    Para uma solução perfeita (0 ataques), o fitness é 1.0.
    """
    attacks = calculate_attacks(individual)
    return 1.0 / (1 + attacks)


def generate_individual(n):
    """
    Gera um indivíduo aleatório (uma configuração de tabuleiro).
    Cada valor é a linha da rainha para a coluna correspondente.
    """
    return [random.randint(0, n - 1) for _ in range(n)]


def selection(population, fitness_scores, num_parents):
    """
    Realiza a seleção dos pais usando o método da roleta.
    """
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:  # Evita divisão por zero se todos tiverem fitness 0
        # Se todos têm fitness zero, a seleção é aleatória
        return random.sample(population, num_parents)

    probabilities = [f / total_fitness for f in fitness_scores]

    parents = random.choices(population, weights=probabilities, k=num_parents)
    return parents


def crossover(parent1, parent2):
    """
    Realiza o cruzamento de dois pais para produzir dois filhos (crossover de ponto único).
    """
    n = len(parent1)
    if n <= 1: return parent1, parent2  # Crossover não faz sentido para 1 ou 0 rainhas

    crossover_point = random.randint(1, n - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(individual, mutation_rate, n):
    """
    Realiza a mutação em um indivíduo com uma certa taxa.
    Altera aleatoriamente a linha de uma rainha em uma coluna.
    """
    if random.random() < mutation_rate:
        idx = random.randint(0, n - 1)  # Escolhe uma coluna aleatoriamente
        individual[idx] = random.randint(0, n - 1)  # Altera a linha para um novo valor aleatório
    return individual


def solve_n_queens_genetic_algorithm(n, population_size=100, generations=1000, mutation_rate=0.05):
    """
    Resolve o Problema das N Rainhas usando um Algoritmo Genético.
    Retorna a melhor solução encontrada (uma lista de linhas para cada coluna).
    """
    population = [generate_individual(n) for _ in range(population_size)]
    best_solution = None
    best_fitness = 0.0

    for generation in range(generations):
        fitness_scores = [get_fitness(ind) for ind in population]

        # Encontra a melhor solução na geração atual
        current_best_individual = population[0]
        current_best_fitness = fitness_scores[0]
        for i in range(1, population_size):
            if fitness_scores[i] > current_best_fitness:
                current_best_fitness = fitness_scores[i]
                current_best_individual = population[i]

        # Atualiza a melhor solução global
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_solution = current_best_individual[:]  # Cria uma cópia da lista

        # Se encontrou uma solução perfeita (fitness 1.0), para
        if best_fitness == 1.0:
            break

        # Gerar nova população
        new_population = []
        # Elitismo: mantém uma porcentagem dos melhores indivíduos diretamente para a próxima geração
        num_elites = int(population_size * 0.1)
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
        new_population.extend([ind for ind, _ in sorted_population[:num_elites]])

        while len(new_population) < population_size:
            parents = selection(population, fitness_scores, 2)
            child1, child2 = crossover(parents[0], parents[1])

            new_population.append(mutate(child1, mutation_rate, n))
            if len(new_population) < population_size:
                new_population.append(mutate(child2, mutation_rate, n))

        population = new_population

    return best_solution