import vars

def handle_player_dir(player, key):
    player.changeDir([vars.dirdict[key][0][0], vars.dirdict[key][0][1]], vars.dirdict[key][1])

def set_pvector(player, direction, angle):
    player.changeDir(direction, angle)

def in_inventory(player, key):
    return player.inventory[key] != None

def move(player, key):
    player.moving += 1 
    player.dir = tuple(vars.DIRS[vars.keys.index(key)])
    handle_player_dir(player,key)
