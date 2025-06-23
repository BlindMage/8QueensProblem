import time
import sys
import random

# Aumenta o limite de recursão padrão do Python (útil para N grande)
sys.setrecursionlimit(2000)

def solve_n_queens_backtracking(n):
    """
    Resolve o Problema das N Rainhas usando a abordagem de backtracking.
    Retorna uma lista de todas as soluções válidas.
    Cada solução é uma lista de tuplas (linha, coluna) das rainhas.
    """
    solutions = []
    # board[col] = linha da rainha naquela coluna
    board = [-1] * n

    def is_safe(row, col):
        """
        Verifica se é seguro colocar uma rainha na posição (row, col).
        É seguro se não houver rainhas na mesma linha,
        na mesma coluna (já garantido pela representação) ou nas mesmas diagonais.
        """
        for prev_col in range(col):
            # Verifica a mesma linha
            if board[prev_col] == row:
                return False
            # Verifica diagonais (diferença absoluta das linhas == diferença absoluta das colunas)
            if abs(board[prev_col] - row) == abs(prev_col - col):
                return False
        return True

    def backtrack(col):
        """
        Função recursiva para tentar colocar rainhas coluna por coluna.
        """
        if col == n:
            # Todas as rainhas foram colocadas com sucesso
            current_solution = []
            for c in range(n):
                current_solution.append((board[c], c))
            solutions.append(current_solution)
            return

        for row in range(n):
            if is_safe(row, col):
                board[col] = row  # Coloca a rainha
                backtrack(col + 1)  # Tenta colocar a próxima rainha
                # O backtracking ocorre implicitamente quando a função retorna e o loop `for`
                # tenta a próxima `row`, sobrescrevendo `board[col]`.
                # Nao é necessário resetar `board[col] = -1` aqui, mas pode ser feito para clareza.

    backtrack(0)  # Começa da primeira coluna (coluna 0)
    return solutions

def print_board(solution, n):
    """
    Imprime uma representação visual do tabuleiro para uma dada solução.
    'Q' representa uma rainha, '.' representa um espaço vazio.
    """
    if not solution:
        print("Nenhuma solução para exibir.")
        return

    board_display = []
    for _ in range(n):
        row_str = ["."] * n
        board_display.append(row_str)

    # A solução pode vir como lista de tuplas (linha, coluna) ou array de linhas
    if isinstance(solution[0], tuple):
        for r, c in solution:
            board_display[r][c] = "Q"
    else: # Assume que é um array onde o índice é a coluna e o valor é a linha
        for col, row in enumerate(solution):
            board_display[row][col] = "Q"


    print("\n--- Solução ---")
    for row_str in board_display:
        print(" ".join(row_str))
    print("-----------------\n")