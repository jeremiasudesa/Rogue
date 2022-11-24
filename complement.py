matriz = [
    [0,0,0,1],
    [0,0,1,1],
    [1,1,0,0],
    [1,1,1,0]
]

movimientos = {
    'w' : (-1, 0),
    'a' : (0, -1),
    's' : (1, 0),
    'd' : (0, 1)
}

def is_available(matrix: list, pos: tuple, air) -> bool:
    '''given a matrix, a set of coordinates and the air parameter the function gives true if the coordinate is not a air and false if it is.'''

    if matrix[pos[0]][pos[1]] == air:
        return True
    
    return False

def is_inmatrix(matrix, pos):
    '''given a set of coordinates and a matrix the function gives true if the coordinates are in the matrix'''

    is_fila_contained = -1 < pos[0] < len(matrix)
    is_columna_contained = -1 < pos[1] < len(matrix[0])

    return is_fila_contained and is_columna_contained

def adjacent_coordinates(matrix, pos, moves: dict, air):
    '''recieves a matrix, a set of coordinates to evaluate its adjacents, the possible moves and the air and gives the adjacent movable coordinates'''
    list_adjacent_coordinates = []
    for movements in moves:
        new_coordinate = (pos[0]+moves[movements][0], pos[1]+moves[movements][1])
        if is_inmatrix(matrix, new_coordinate):
            if is_available(matrix, new_coordinate, air):
                list_adjacent_coordinates.append(new_coordinate)
    return list_adjacent_coordinates

def get_path(pos1, pos2, matrix, moves, air):
    '''recieves an origin tuple, a goal tuple a matrix and a air and earchs the best path avoiding the airs to get from tuple 1 to tuple 2'''
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    queue = [pos1]
    visited[pos1[0]][pos1[1]] = True
    dirs = [['y' for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    while queue:       
        actual = queue.pop(0)
        if actual == pos2:
            break
        adjacent_coords = adjacent_coordinates(matrix, actual, moves, air)
        visited[actual[0]][actual[1]] = True
        for coords in adjacent_coords:
            if not(visited[coords[0][0]][coords[0][1]]):
                dirs[coords[0][0]][coords[0][1]] = coords[1]
                queue.append(coords[0])
    curr = pos2
    anti_path = []
    while dirs[curr[0]][curr[1]] != 'y':
        anti_path.append(curr)
        movimiento = moves[dirs[curr[0]][curr[1]]]
        movimiento_inverso = (-movimiento[0],-movimiento[1])
        curr = (curr[0] + movimiento_inverso[0], curr[1] + movimiento_inverso[1])
    return anti_path[::-1]

def pintador_complemento(matrix, moves):
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    i = -1
    for filas in range(len(visited)):
        for columnas in range(len(visited[filas])):
            if visited[filas][columnas] == False:
                i+=1
                queue = []
                queue.append((filas, columnas))
                while queue:
                    actual = queue.pop(0)
                    adjacent_coords = adjacent_coordinates(matrix, actual, moves, matrix[actual[0]][actual[1]])
                    visited[actual[0]][actual[1]] = True
                    for coords in adjacent_coords:
                        if not(visited[coords[0]][coords[1]]):
                            queue.append(coords)
                    matriz[actual[0]][actual[1]] = i

        
            


pintador_complemento(matriz, movimientos)
                




