import random
from typing import Optional
import items
import opensimplex
import bisect

Location = tuple[int, int]

class Tile:
    """Tile(char: str, walkable: bool=True)

    A Tile is the object used to represent the type of the dungeon floor.

    Arguments

    char (str) -- string of length 1 that is rendered when rendering a map.
    walkable (bool) -- states if the tile is walkable or not.
    """
    __colors = [[0, 50, 80],[0, 71, 171],[0, 94, 184], [90,90,90], [110,110,110], [169,169,169], [192,192,192], [211,211,211], [220,220,220]]
    __heights = [-1, 0.4, 0.44, 0.5, 0.63, 0.7, 0.8, 0.83, 0.85]
    def __pickColor(self, num):
        return self.__colors[bisect.bisect_left(self.__heights, num)-1]

    def __init__(self, noise):
        self.color = self.__pickColor(noise)

#create directions
directions = []
for x in range(-1, 2):
    for y in range(-1, 2):
        if(x == 0 and y == 0):
            continue
        directions.append((x, y))

AIR, WALL, STAIR_UP, STAIR_DOWN, PLAYER, PICKAXE = range(6)

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
        self.rows, self.columns, self.origin, self.adj_chunks = rows, columns, top_left, [None, None, None, None, None, None]
        #create noise
        self.noise = NoiseMap(self.rows, self.columns, 0.065, seed, top_left)
        self.noisemap = self.noise.getMap()
        #create tilemap
        self.state = [[(WALL if self.noisemap[i][j] > 0.5 else AIR) for j in range(columns)] for i in range(rows)]
        self.tilemap = [[Tile(self.noisemap[i][j]) for j in range(columns)] for i in range(rows)]
        if(start):
            for i in range(self.rows//5, self.rows-self.rows//5):
                for j in range(self.columns//5, self.columns-self.columns//5):
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
        self.update_map_chunk(Chunk(rows, columns, Location([0, 0]), 0, seed, True))
        self.rows, self.columns, self.seed, self.adj_level = rows, columns, seed, {}
        self.adj_level['u'], self.adj_level['d'] = None, None
        #define elements locations
        self.initLoc()

    def initLoc(self):
        center = [self.rows//2, self.columns//2]
        self.spawn = center
        self.upStair = [center[0]+10, center[1]-10]
        self.downStair = [center[0]-10, center[1]+10]
        self.pickaxe = [center[0]+5, center[1]]

    def update_map_chunk(self, chunk):
        self.curr_chunk, self.state, self.tilemap = chunk, chunk.state, chunk.tilemap
    
    def newChunk(self, dir, side):
        if(self.curr_chunk.adj_chunks[side] != None):return
        opposite = (side - 1 if (side % 2 == 0) else side + 1)
        new_tl = Location([self.curr_chunk.origin[0] + dir[0], self.curr_chunk.origin[1] + dir[1]])
        new_c = Chunk(self.rows, self.columns, new_tl, -1, self.seed)
        new_c.adj_chunks[opposite] = self.curr_chunk
        self.curr_chunk.adj_chunks[side] = new_c

    def whereIsPos(self, pos):
        ret = [0]
        if(pos[0] == self.rows):
            ret = [1, [-self.rows+1, 0]]
        if(pos[0] == -1):
            ret = [2, [self.rows-2, 0]]
        if(pos[1] == self.columns):
            ret = [3, [0, -self.columns+1]]
        if(pos[1] == -1):
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

    def is_walkable(self, location: Location):
        """Check if a player can walk through a given location."""
        i, j = location
        return (self.state[i][j] != WALL)

    def loc(self, xy: Location) -> Tile:
        """Get the tile type at a given location."""
        i, j = xy
        return self.state[i][j]