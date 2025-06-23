import time
import sys
import psutil  # Para monitorar uso de memória
import os

N_QUEENS = 8


# --- Medição de Desempenho ---
def measure_performance(func, *args, **kwargs):
    process = psutil.Process(os.getpid())

    # Medir memória RSS (Resident Set Size) antes da execução
    mem_before = process.memory_info().rss / (1024 * 1024)  # em MB

    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()

    # Medir memória RSS depois da execução
    mem_after = process.memory_info().rss / (1024 * 1024)  # em MB

    elapsed_time = end_time - start_time
    # Usamos a diferença de memória para ter uma estimativa do que foi alocado para a tarefa.
    # É uma aproximação, pois o uso de memória pode variar dinamicamente.

    return result, elapsed_time, (mem_after - mem_before)


print(f"--- Análise de Desempenho para o Problema das {N_QUEENS} Rainhas ---")

# --- 1. Backtracking ---
print("\n### Backtracking ###")
# O Backtracking encontra todas as soluções por natureza.
all_solutions_bt, time_all_bt, mem_all_bt = measure_performance(solve_n_queens_backtracking, N_QUEENS)

print(f"  - Tempo para encontrar TODAS as {len(all_solutions_bt)} soluções: {time_all_bt:.6f} segundos")
print(f"  - Memória RAM (aumento durante a execução): {mem_all_bt:.4f} MB")

if len(all_solutions_bt) > 0:
    print("\n  Exemplo de uma solução (Backtracking):")
    print_board(all_solutions_bt[0], N_QUEENS)

# --- 2. Algoritmo Genético (GA) ---
print("\n### Algoritmo Genético (GA) ###")
# Rodamos o GA múltiplas vezes para ter uma média, já que é estocástico.
NUM_GA_RUNS = 10  # Aumentei o número de runs para uma média mais robusta
ga_successful_times = []
ga_successful_mems = []
ga_last_found_solution = None  # Para mostrar um exemplo

print(f"  Rodando GA {NUM_GA_RUNS} vezes para encontrar UMA solução válida (fitness 1.0)...")
for i in range(NUM_GA_RUNS):
    # Parâmetros otimizados para 8 rainhas; podem ser ajustados
    sol, t, m = measure_performance(solve_n_queens_genetic_algorithm, N_QUEENS, population_size=300, generations=3000,
                                    mutation_rate=0.1)

    if sol and calculate_attacks(sol) == 0:
        ga_successful_times.append(t)
        ga_successful_mems.append(m)
        ga_last_found_solution = sol  # Guarda a última solução válida encontrada
        # print(f"    Tentativa {i+1}: Sucesso em {t:.6f}s")
    # else:
    # print(f"    Tentativa {i+1}: Falha ou solução incompleta em {t:.6f}s (ataques: {calculate_attacks(sol) if sol else 'N/A'})")

if ga_successful_times:
    avg_ga_time = sum(ga_successful_times) / len(ga_successful_times)
    avg_ga_mem = sum(ga_successful_mems) / len(ga_successful_mems)
    print(
        f"  - Tempo médio para encontrar UMA solução (GA): {avg_ga_time:.6f} segundos (sucesso em {len(ga_successful_times)}/{NUM_GA_RUNS} tentativas)")
    print(f"  - Memória RAM média usada (GA): {avg_ga_mem:.4f} MB")
    print("\n  Exemplo de uma solução (GA):")
    print_board(ga_last_found_solution, N_QUEENS)
else:
    print(
        f"  GA não conseguiu encontrar uma solução perfeita em nenhuma das {NUM_GA_RUNS} tentativas com os parâmetros atuais.")

print("  - GA não é projetado para encontrar todas as 92 soluções existentes.")

# --- 3. Otimização por Enxame de Partículas (PSO) ---
print("\n### Otimização por Enxame de Partículas (PSO) ###")
NUM_PSO_RUNS = 10  # Aumentei o número de runs
pso_successful_times = []
pso_successful_mems = []
pso_last_found_solution = None

print(f"  Rodando PSO {NUM_PSO_RUNS} vezes para encontrar UMA solução válida (fitness 1.0)...")
for i in range(NUM_PSO_RUNS):
    # Parâmetros otimizados para 8 rainhas; podem ser ajustados
    sol, t, m = measure_performance(solve_n_queens_pso, N_QUEENS, num_particles=100, max_iterations=1500, c1=2.0,
                                    c2=2.0, w_start=0.9, w_end=0.4)

    if sol and calculate_attacks(sol) == 0:
        pso_successful_times.append(t)
        pso_successful_mems.append(m)
        pso_last_found_solution = sol  # Guarda a última solução válida encontrada
        # print(f"    Tentativa {i+1}: Sucesso em {t:.6f}s")
    # else:
    # print(f"    Tentativa {i+1}: Falha ou solução incompleta em {t:.6f}s (ataques: {calculate_attacks(sol) if sol else 'N/A'})")


def print_board(pso_last_found_solution, N_QUEENS):
    pass


if pso_successful_times:
    avg_pso_time = sum(pso_successful_times) / len(pso_successful_times)
    avg_pso_mem = sum(pso_successful_mems) / len(pso_successful_mems)
    print(
        f"  - Tempo médio para encontrar UMA solução (PSO): {avg_pso_time:.6f} segundos (sucesso em {len(pso_successful_times)}/{NUM_PSO_RUNS} tentativas)")
    print(f"  - Memória RAM média usada (PSO): {avg_pso_mem:.4f} MB")
    print("\n  Exemplo de uma solução (PSO):")
    print_board(pso_last_found_solution, N_QUEENS)
else:
    print(
        f"  PSO não conseguiu encontrar uma solução perfeita em nenhuma das {NUM_PSO_RUNS} tentativas com os parâmetros atuais.")

print("  - PSO não é projetado para encontrar todas as 92 soluções existentes.")