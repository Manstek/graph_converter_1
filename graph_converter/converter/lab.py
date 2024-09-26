import numpy as np
from collections import defaultdict, deque

# Пример матрицы инцидентности
incidence_matrix = np.array([
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, -1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 1, 0, 0, 0],
    [-1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 1, 0, 0],
    [0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0],
    [0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, -1]
])

# Создание списка смежности
def build_adjacency_list(incidence_matrix):
    graph = defaultdict(list)
    num_vertices = incidence_matrix.shape[0]
    
    for j in range(incidence_matrix.shape[1]):
        start_vertex = None
        for i in range(num_vertices):
            if incidence_matrix[i][j] == 1:
                start_vertex = i
            elif incidence_matrix[i][j] == -1:
                graph[start_vertex].append(i)
    
    return graph

# Обход графа для выделения уровней
def find_levels(graph):
    levels = defaultdict(list)
    visited = set()
    queue = deque()
    
    # Начинаем с вершины 0
    queue.append((0, 0))  # (номер вершины, уровень)
    visited.add(0)

    while queue:
        current, level = queue.popleft()
        levels[level].append(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))

    return levels

# Построение графа и выделение уровней
graph = build_adjacency_list(incidence_matrix)
levels = find_levels(graph)

# Вывод уровней
print("Иерархические уровни:")
for level in sorted(levels.keys()):
    print(f"{level} уровень: {', '.join(map(str, levels[level]))}")
