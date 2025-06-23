import random
import math


class Particle:
    def __init__(self, n):
        # Posição: lista de linhas para cada coluna (inteiros)
        self.position = [random.randint(0, n - 1) for _ in range(n)]
        # Velocidade: valores flutuantes que influenciam a mudança de posição
        self.velocity = [random.uniform(-1, 1) for _ in range(n)]

        # Melhor posição que a partícula encontrou
        self.best_personal_position = list(self.position)
        self.best_personal_fitness = get_fitness(self.position)


def calculate_attacks(individual):
    """ (Mesma função do GA para calcular ataques) """
    n = len(individual)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if individual[i] == individual[j]:
                attacks += 1
            if abs(individual[i] - individual[j]) == abs(i - j):
                attacks += 1
    return attacks


def get_fitness(individual):
    """ (Mesma função do GA para calcular fitness) """
    attacks = calculate_attacks(individual)
    return 1.0 / (1 + attacks)


def solve_n_queens_pso(n, num_particles=50, max_iterations=500, c1=2.0, c2=2.0, w_start=0.9, w_end=0.4):
    """
    Resolve o Problema das N Rainhas usando Otimização por Enxame de Partículas (PSO).
    Adaptação para problema discreto: as posições são arredondadas para inteiros
    e limitadas aos limites do tabuleiro.
    """
    particles = [Particle(n) for _ in range(num_particles)]

    global_best_position = None
    global_best_fitness = 0.0

    # Inicializa a melhor posição global com a melhor partícula inicial
    for p in particles:
        if p.best_personal_fitness > global_best_fitness:
            global_best_fitness = p.best_personal_fitness
            global_best_position = list(p.position)  # Copia

    for iteration in range(max_iterations):
        # Coeficiente de inércia (w) decresce linearmente
        w = w_start - ((w_start - w_end) * iteration / max_iterations)

        for p in particles:
            # Atualiza a velocidade da partícula
            for i in range(n):
                r1 = random.random()  # Fator aleatório cognitivo
                r2 = random.random()  # Fator aleatório social

                # Componente de inércia: mantém a direção atual
                inertia_component = w * p.velocity[i]
                # Componente cognitivo: atrai a partícula para sua melhor posição pessoal
                cognitive_component = c1 * r1 * (p.best_personal_position[i] - p.position[i])
                # Componente social: atrai a partícula para a melhor posição global do enxame
                social_component = c2 * r2 * (global_best_position[i] - p.position[i])

                p.velocity[i] = inertia_component + cognitive_component + social_component

                # Limita a velocidade para evitar saltos muito grandes
                p.velocity[i] = max(-n, min(n, p.velocity[i]))

            # Atualiza a posição da partícula
            for i in range(n):
                # Arredonda para o inteiro mais próximo para se ajustar ao tabuleiro discreto
                p.position[i] = round(p.position[i] + p.velocity[i])
                # Garante que a posição esteja dentro dos limites do tabuleiro [0, n-1]
                p.position[i] = max(0, min(n - 1, p.position[i]))

            # Atualiza a melhor posição pessoal da partícula
            current_fitness = get_fitness(p.position)
            if current_fitness > p.best_personal_fitness:
                p.best_personal_fitness = current_fitness
                p.best_personal_position = list(p.position)  # Copia

        # Atualiza a melhor posição global do enxame
        for p in particles:
            if p.best_personal_fitness > global_best_fitness:
                global_best_fitness = p.best_personal_fitness
                global_best_position = list(p.best_personal_position)  # Copia

        # Se encontrou uma solução perfeita (fitness 1.0), para
        if global_best_fitness == 1.0:
            break

    # Se uma solução perfeita não foi encontrada, retorna a melhor encontrada
    if global_best_fitness < 1.0:
        print(f"PSO: Melhor solução encontrada após {max_iterations} iterações (fitness: {global_best_fitness:.4f}).")

    return global_best_position  # Retorna a melhor solução encontrada