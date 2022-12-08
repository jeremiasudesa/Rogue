import random
from typing import Optional
import items
import opensimplex
import bisect
import vars

Location = tuple[int, int]
colors = [[66,172,175],[78, 188, 185], [119, 192, 180], [177, 201, 167], [231, 213, 147], [210, 227, 111], [200, 220, 147]]
heights = [-1, 0.45, 0.5, 0.55, 0.62, 0.68]

class Tile:
    """Tile(char: str, walkable: bool=True)

    A Tile is the object used to represent the type of the dungeon floor.

    Arguments

    char (str) -- string of length 1 that is rendered when rendering a map.
    walkable (bool) -- states if the tile is walkable or not.
    """
    def __pickColor(self, num):
        return colors[bisect.bisect_left(heights, num)-1]

    def __init__(self, noise):
        self.color = self.__pickColor(noise)

#create directions
directions = []
for x in range(-1, 2):
    for y in range(-1, 2):
        if(x == 0 and y == 0):
            continue
        directions.append((x, y))

AIR, WALL, STAIR_UP, STAIR_DOWN, PLAYER, PICKAXE, ENEMY, ORB, TROPHY = range(9)

class NoiseMap:
    """NoiseMap(rows:int, columns:int, zoom:int, seed:int)
    Arguments

    rows (int) -- is the number of rows for the map
    columns (int) -- is the number of columns for the map
    zoom (float) -- the amount of zoom for the map construction
    seed (int) -- map seed
    pos (list) -- offset position
    
    Returns OpenSimplex Noise map 
    """
    def __init__(self, rows:int, columns:int, zoom:float, seed:int, pos:Location):
        self.rows, self.columns, self.zoom, self.seed, self.pos = rows, columns, zoom, seed, pos
        opensimplex.seed(self.seed)
        self.__map = [[0.0 for _ in range(self.columns)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                self.__map[i][j] += (opensimplex.noise2(x = self.zoom*(i - self.pos[0]), y = self.zoom*(j - self.pos[1]))+1)/2
        
    def getMap(self):
        return self.__map

#TODO: corregir error de memoria... complejidad O(4*n)
class Chunk:
    """Chunk(top_left_position: tuple):
    Arguments

    top_left_position (tuple) -- is the position of the top left tile.

    Returns an instance of a chunk.
    Every grid computation should be done in the chunk itself, it is like a level
    """
    def __init__(self, rows:int, columns:int, top_left:Location, id, seed, start = False):
        self.id = id
        #init values
        self.rows, self.columns, self.origin, self.adj_chunks, self.killed = rows, columns, top_left, [None, None, None, None, None, None], False
        #create noise
        self.noise = NoiseMap(self.rows, self.columns, 0.065, seed, top_left)
        self.noisemap = self.noise.getMap()
        #create tilemap
        self.state = [[(WALL if self.noisemap[i][j] > 0.62 else AIR) for j in range(columns)] for i in range(rows)]
        self.tilemap = [[Tile(self.noisemap[i][j]) for j in range(columns)] for i in range(rows)]
        if(start):
            for i in range(self.rows//4, self.rows-self.rows//4):
                for j in range(self.columns//4, self.columns-self.columns//4):
                    self.state[i][j] = AIR
                    self.tilemap[i][j] = Tile(-1)


class Level:
    """Level(rows: int, columns: int) -> Level

    Arguments

    rows (int) -- is the number of rows for the level.
    columns (int) -- is the number of columns for the level.

    Returns an instance of a level.
    """
    def __init__(self, rows: int, columns: int, seed):
        """Initializes a dungeon level class. See class documentation."""
        self.rows, self.columns, self.seed, self.adj_level = rows, columns, seed, {}
        self.enemy_probability = 0.0005
        self.adj_level['u'], self.adj_level['d'] = None, None
        self.locToEnemy = {}
        self.unlocked = False
        #define elements locations
        self.update_map_chunk(Chunk(rows, columns, Location([0, 0]), 0, seed, True))
        self.initLoc()

    def initLoc(self):
        center = [self.rows//2, self.columns//2]
        self.spawn = center
        self.upStair = [center[0]+10, center[1]-10]
        self.downStair = [center[0]-10, center[1]+10]
        self.orb, self.pickaxe, self.trophy = None, None, None
        if(vars.ORIGIN_SEED == self.seed):self.pickaxe = [center[0]+10, center[1]]
        if(vars.ORIGIN_SEED == self.seed):self.orb = [center[0]-10, center[1]]
        if(vars.ORIGIN_SEED + 3 == self.seed):self.trophy = [self.rows//2+5, self.columns//2]

    def update_map_chunk(self, chunk):
        self.curr_chunk, self.state, self.tilemap, self.divided = chunk, chunk.state, chunk.tilemap, False
        self.divideComponents()
    
    def newChunk(self, dir, side):
        if(self.curr_chunk.adj_chunks[side] != None):return
        opposite = (side - 1 if (side % 2 == 0) else side + 1)
        new_tl = Location([self.curr_chunk.origin[0] + dir[0], self.curr_chunk.origin[1] + dir[1]])
        vars.chunks+=1
        new_c = Chunk(self.rows, self.columns, new_tl, vars.chunks, self.seed)
        new_c.adj_chunks[opposite] = self.curr_chunk
        self.curr_chunk.adj_chunks[side] = new_c

    def whereIsPos(self, pos:Location):
        ret = [0]
        if(pos[0] >= self.rows):
            ret = [1, [-self.rows+1, 0]]
        if(pos[0] <= -1):
            ret = [2, [self.rows-2, 0]]
        if(pos[1] >= self.columns):
            ret = [3, [0, -self.columns+1]]
        if(pos[1] <= -1):
            ret = [4, [0, self.columns-2]]
        return ret

    def findBorder(self, posarr):
        ret = [0]
        for pos in posarr:
            where = self.whereIsPos(pos)
            if(not where[0] == 0):ret = where
        return ret

    def get_random_location(self) -> Location:
        """Compute and return a random location in the map."""
        return random.randint(0, self.columns - 1), random.randint(0, self.rows - 1)

    def is_walkable(self, location: Location, only_allowed = -1):
        """Check if a player can walk through a given location."""
        if(self.whereIsPos(location)[0] != 0):return False
        i, j = location
        if(only_allowed != -1):return(self.state[int(i)][int(j)] == only_allowed)
        return (self.state[int(i)][int(j)] != WALL)

    def loc(self, xy: Location) -> Tile:
        """Get the tile type at a given location."""
        if(self.whereIsPos(xy)[0] != 0):return None
        i, j = xy
        return self.state[int(i)][int(j)]

    def is_inmatrix(self, pos):
        '''given a set of coordinates and a matrix the function gives true if the coordinates are in the matrix'''

        is_fila_contained = -1 < pos[0] < len(self.state)
        is_columna_contained = -1 < pos[1] < len(self.state[0])

        return is_fila_contained and is_columna_contained

    def adjacent_coordinates(self, pos, allowed):
        '''recieves a matrix, a set of coordinates to evaluate its adjacents, the possible moves and the air and gives the adjacent movable coordinates'''
        list_adjacent_coordinates = []
        for i in range(len(vars.DIRS)):
            new_coordinate = (pos[0]+vars.DIRS[i][0], pos[1]+vars.DIRS[i][1])
            if self.is_inmatrix(new_coordinate):
                if self.is_walkable(new_coordinate, allowed):
                    list_adjacent_coordinates.append((new_coordinate, i))
        return list_adjacent_coordinates

    def get_path(self, pos1, pos2, component, allowed):
        '''recieves an origin tuple, a goal tuple a matrix and a air and earchs the best path avoiding the airs to get from tuple 1 to tuple 2'''
        visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        dirs = [[-1 for _ in range(self.columns)] for _ in range(self.rows)]
        queue = [pos1]
        while queue:       
            actual = queue.pop(0)
            if actual == pos2:
                break
            if(visited[actual[0]][actual[1]]):continue
            visited[actual[0]][actual[1]] = True
            adjacent_coords = self.adjacent_coordinates(actual, allowed)
            component.append(actual)
            for coords in adjacent_coords:
                dirs[coords[0][0]][coords[0][1]] = coords[1]
                queue.append(coords[0])
        curr = pos2

    def divideComponents(self):
        self.components, self.where = [], [[-1 for _ in range(self.columns)] for _ in range(self.rows)]
        visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        comp = -1
        for i in range(self.rows):
            for j in range(self.columns):
                if visited[i][j] == False:
                    visited[i][j] = True
                    comp+=1
                    self.components.append([])
                    self.get_path((i, j), (-1,-1), self.components[comp], self.state[i][j])
                    for x in self.components[comp]:
                        self.where[x[0]][x[1]] = comp
                        visited[x[0]][x[1]] = True
        self.divided = True
