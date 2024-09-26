from django.shortcuts import render
from django.http import JsonResponse
from collections import deque

def convert_incidence_matrix(matrix):
    vertices_count = len(matrix)
    edges_count = len(matrix[0])
    adjacency_matrix = [[0] * vertices_count for _ in range(vertices_count)]
    
    for j in range(edges_count):
        start_vertex = end_vertex = None
        for i in range(vertices_count):
            if matrix[i][j] == 1:
                start_vertex = i
            elif matrix[i][j] == -1:
                end_vertex = i
        if start_vertex is not None and end_vertex is not None:
            adjacency_matrix[start_vertex][end_vertex] = 1
    
    return adjacency_matrix


def calculate_left_incidents(matrix):
    vertices_count = len(matrix)
    left_incidents = {f'G-({i+1})': [] for i in range(vertices_count)}

    for j in range(len(matrix[0])):
        start_vertex = end_vertex = None
        for i in range(vertices_count):
            if matrix[i][j] == 1:
                start_vertex = i + 1
            elif matrix[i][j] == -1:
                end_vertex = i + 1
        if start_vertex is not None and end_vertex is not None:
            left_incidents[f'G-({end_vertex})'].append(start_vertex)

    return left_incidents


def hierarchical_levels(matrix):
    levels = {}
    visited = [False] * len(matrix)

    # Определяем корневые вершины
    roots = [i for i in range(len(matrix)) if all(matrix[j][i] == 0 for j in range(len(matrix)))]

    # Присваиваем уровень 0 корневым вершинам
    for root in roots:
        levels[root] = 0

    # BFS для определения уровней
    def bfs():
        queue = deque(roots)
        while queue:
            vertex = queue.popleft()
            current_level = levels[vertex]
            for neighbor in range(len(matrix)):
                if matrix[vertex][neighbor] == 1:
                    if neighbor not in levels:  # Если еще не посещен
                        levels[neighbor] = current_level + 1
                        queue.append(neighbor)

    bfs()

    # Преобразуем уровни в ожидаемый формат
    level_mapping = {}
    for vertex, level in levels.items():
        if level not in level_mapping:
            level_mapping[level] = []
        level_mapping[level].append(vertex + 1)  # Нумерация с 1

    return {k: level_mapping[k] for k in sorted(level_mapping)}


def matrix_converter_view(request):
    if request.method == 'POST':
        incidence_matrix = request.POST.get('matrix')
        matrix = [[int(num) for num in row.split()] for row in incidence_matrix.splitlines()]

        adjacency_matrix = convert_incidence_matrix(matrix)
        left_incidents = calculate_left_incidents(matrix)
        levels = hierarchical_levels(adjacency_matrix)

        return JsonResponse({
            'adjacency_matrix': adjacency_matrix,
            'left_incidents': left_incidents,
            'levels': levels,
        })

    return render(request, 'converter/converter.html')
