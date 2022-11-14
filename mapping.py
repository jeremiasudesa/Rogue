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
    __colors = [[0, 0, 51],[0, 94, 184], [160, 160, 160],[96, 96, 96],[32, 32, 32]]
    __heights = [-1, 0.35, 0.5, 0.65, 0.8]
    def __pickColor(self, num):
        return self.__colors[bisect.bisect_left(self.__heights, num)-1]

    def __init__(self, noise, walkable):
        self.walkable = walkable
        self.color = self.__pickColor(noise)

#create directions
directions = []
for x in range(-1, 2):
    for y in range(-1, 2):
        if(x == 0 and y == 0):
            continue
        directions.append((x, y))

AIR = 0
WALL = 1
STAIR_UP = 2
STAIR_DOWN = 3
PLAYER = 4

class Level:
    """Level(rows: int, columns: int) -> Level

    Arguments

    rows (int) -- is the number of rows for the level.
    columns (int) -- is the number of columns for the level.

    Returns an instance of a level.
    """
    def __init__(self, rows: int, columns: int):
        """Initializes a dungeon level class. See class documentation."""
        #init values
        self.rows, self.columns = rows, columns
        #create noise
        zoom = 0.1
        opensimplex.seed(1234)
        noise = [[0 for _ in range(columns)] for _ in range(rows)]
        for i in range(rows):
            for j in range(columns):
                noise[i][j] += (opensimplex.noise2(x = zoom*i, y = zoom*j)+1)/2
        #create tilemap
        self.state = [[0 for _ in range(columns)] for _ in range(rows)]
        self.tilemap = [[Tile(noise[i][j], (False if noise[i][j] > 0.5 else True)) for j in range(columns)] for i in range(rows)]

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
        j, i = location
        return self.state[i % self.rows][j % self.columns].walkable

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