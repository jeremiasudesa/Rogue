import random
from typing import Optional
import pygame
import player
import items
import sys
import opensimplex
import bisect
import math
import os

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

AIR, WALL, STAIR_UP, STAIR_DOWN, PLAYER = range(5)

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
    def __init__(self, rows:int, columns:int, zoom:float, seed:int, pos:int):
        self.rows, self.columns, self.zoom, self.seed, self.pos = rows, columns, zoom, seed, pos
        opensimplex.seed(self.seed)
        self.__map = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                self.__map[i][j] += (opensimplex.noise2(x = self.zoom*(i - self.pos[0]), y = self.zoom*(j - self.pos[1]))+1)/2
        
    def getMap(self):
        return self.__map

class Chunk:
    """Chunk(top_left_position: tuple):
    Arguments

    top_left_position (tuple) -- is the position of the top left tile.

    Returns an instance of a chunk.
    Every grid computation should be done in the chunk itself, it is like a level
    """
    def __init__(self, rows:int, columns:int, top_left:list, id):
        self.id = id
        #init values
        self.rows, self.columns, self.origin = rows, columns, top_left
        self.right, self.left, self.up, self.down = None, None, None, None
        #create noise
        self.noise = NoiseMap(self.rows, self.columns, 0.1, 1234, top_left)
        self.noisemap = self.noise.getMap()
        #create tilemap
        self.state = [[(WALL if self.noisemap[i][j] > 0.5 else AIR) for j in range(columns)] for i in range(rows)]
        self.tilemap = [[Tile(self.noisemap[i][j]) for j in range(columns)] for i in range(rows)]



class Level:
    """Level(rows: int, columns: int) -> Level

    Arguments

    rows (int) -- is the number of rows for the level.
    columns (int) -- is the number of columns for the level.

    Returns an instance of a level.
    """
    def __init__(self, rows: int, columns: int):
        """Initializes a dungeon level class. See class documentation."""
        self.update_map_chunk(Chunk(rows, columns, [0, 0], 0))
        self.rows, self.columns = rows, columns

    def update_map_chunk(self, chunk):
        self.curr_chunk, self.state, self.tilemap = chunk, chunk.state, chunk.tilemap
    
    def newChunk(self, dir):
        print((self.curr_chunk.origin, dir))
        new_tl = [self.curr_chunk.origin[0] + dir[0], self.curr_chunk.origin[1] + dir[1]]
        return Chunk(self.rows, self.columns, new_tl, -1)

    def rightChunk(self, dir):
        if(self.curr_chunk.right != None):return
        right_c = self.newChunk(dir)
        right_c.left = self.curr_chunk
        self.curr_chunk.right = right_c

    def leftChunk(self, dir):
        if(self.curr_chunk.left != None):
            return
        left_c = self.newChunk(dir)
        left_c.right = self.curr_chunk
        self.curr_chunk.left = left_c

    def downChunk(self, dir):
        if(self.curr_chunk.down != None):return
        down_c = self.newChunk(dir)
        down_c.up = self.curr_chunk
        self.curr_chunk.down = down_c

    def upChunk(self, dir):
        if(self.curr_chunk.up != None):return
        up_c = self.newChunk(dir)
        up_c.down = self.curr_chunk
        self.curr_chunk.up = up_c

    def whereIsPos(self, pos):
        ret = ["I"]
        if(pos[0] == self.rows):
            ret = ["D", [-self.rows+1, 0]]
        if(pos[0] == -1):
            ret = ["U", [self.rows-2, 0]]
        if(pos[1] == self.columns):
            ret = ["R", [0, -self.columns+1]]
        if(pos[1] == -1):
            ret = ["L", [0, self.columns-2]]
        return ret

    def findBorder(self, posarr):
        ret = ["I"]
        for pos in posarr:
            where = self.whereIsPos(pos)
            if(not where[0] == "I"):ret = where
        return ret

    def find_free_tile(self) -> Location:
        """Searches one by one until it finds a free tile
        """
        for i in range(self.rows):
            for j in range(self.columns):
                if(self.state[i][j] == AIR):return True
        return False

    def get_random_location(self) -> Location:
        """Compute and return a random location in the map."""
        return random.randint(0, self.columns - 1), random.randint(0, self.rows - 1)

    def add_stair_up(self, location: Optional[Location] = None):
        """Add an ascending stair tile to a given or random location in the map."""
        if location is not None:
            j, i = location
        else:
            i = random.randint(0, self.rows - 1)
            j = random.randint(0, self.columns - 1)
        self.state[i][j] = STAIR_UP

    def add_stair_down(self, location: Optional[Location] = None):
        """Add a descending stair tile to a give or random location in the map."""
        if location is not None:
            j, i = location
        else:
            i = random.randint(0, self.rows - 1)
            j = random.randint(0, self.columns - 1)
        self.state[i][j] = STAIR_DOWN

    def add_item(self, item: items.Item, location: Optional[Location] = None):
        """Add an item to a given location in the map. If no location is given, one free space is searched.
        """
        if location is None:
            j, i = self.find_free_tile()
        else:
            j, i = location
        items = self.items.get((i, j), [])
        items.append(item)
        self.items[(i, j)] = items

    def is_walkable(self, location: Location):
        """Check if a player can walk through a given location."""
        i, j = location
        return (self.state[i][j] != WALL)

    def index(self, tile: Tile) -> Location:
        """Get the location of a given tile in the map. If there are multiple tiles of that type, then only one is
        returned.

        Arguments

        tile (Tile) -- one of the known tile types (AIR, WALL, STAIR_DOWN, STAIR_UP)

        Returns the location of that tile type or raises ValueError
        """
        for i in range(self.rows):
            try:
                j = self.state[i].index(tile)
                return j, i
            except ValueError:
                pass
        raise ValueError

    def loc(self, xy: Location) -> Tile:
        """Get the tile type at a given location."""
        j, i = xy
        return self.state[i][j]

    def get_items(self, xy: Location) -> list[items.Item]:
        """Get a list of all items at a given location. Removes the items from that location."""
        j, i = xy
        if (i, j) in self.items:
            items = self.items[(i, j)]
            del(self.items[(i, j)])
        else:
            items = []
        return items

    def getTilemap(self):
        return self.tilemap

    def dig(self, xy: Location) -> None:
        """Replace a WALL at the given location, by AIR."""
        j, i = xy
        if self.state[i][j] is WALL:
            self.state[i][j] = AIR

    def is_free(self, xy: Location) -> bool:
        """Check if a given location is free of other entities."""
        # completar
        raise NotImplementedError

    def are_connected(self, initial: Location, end: Location) -> bool:
        """Check if there is walkable path between initial location and end location."""
        # completar
        raise NotImplementedError

    def get_path(self, initial: Location, end: Location) -> bool:
        """Return a sequence of locations between initial location and end location, if it exits."""
        # completar
        raise NotImplementedError