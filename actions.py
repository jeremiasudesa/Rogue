from typing import Union
from pygame.math import Vector2

import mapping
import pygame
import const
import random
from enemy import Enemy
import sys
import time
import music
import items
import bisect

def initLevelItems(ge, level):
    ge['door1'], ge['door2'] = items.Door(1, 2, level.downStair), items.Door(1, 0, level.upStair)
    if(level.pickaxe != None): ge['pick'] = items.Pickaxe(level.pickaxe)
    if(level.orb != None): ge['orb'] = items.Orb(level.orb)


#TODO: distinction between regular keys and number_keys
keys = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s]
number_keys = [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
dirdict = {}
for i in range(len(keys)):
    dirdict[keys[i]] = (const.DIRS[i], const.ANGLES[i])

def handle_player_dir(player, key):
    player.changeDir([dirdict[key][0][0], dirdict[key][0][1]], dirdict[key][1])

def set_pvector(player, direction, angle):
    player.changeDir(direction, angle)

def paint_posarray(lvl, posarray, tile):
    for pos in posarray:
        lvl.state[int(pos[0])][int(pos[1])] = tile

def clear_posarray(lvl, posarray):
    for pos in posarray:
        lvl.state[int(pos[0])][int(pos[1])] = mapping.AIR

def updateBakground(interface, level):
    interface.setBackground(level.tilemap)

#TURN EVERY GAME COMPONENT INTO A GLOBAL VARIABLE

def update_chunk_counter(interface, player):
    interface.drawCounter(player.chunkCounter)

def nxt_chunk(gc, level, dir):
    '''
    Handle possible next chunk directions and pass it to the chunk object itself
    '''
    if(level.curr_chunk.adj_chunks[dir[0]] == None):gc['elems']['player'].chunkCounter += 1
    level.newChunk(dir[1], dir[0])
    level.update_map_chunk(level.curr_chunk.adj_chunks[dir[0]])

def add_sprites(sprite_group, entity):
    if(type(entity) == list):
        for x in entity:
            sprite_group.add(x.sprite)
    else:
        sprite_group.add(entity.sprite)

def add_sprites_from_dict(sprite_group, entity_list):
    for entity in entity_list.values():
        add_sprites(sprite_group, entity)

def nxt_level(gc, dir):
    if(gc['level'].adj_level[dir] == None):
        gc['level'].adj_level[dir] = mapping.Level(gc['level'].rows, gc['level'].columns, gc['level'].seed+1)
        gc['level'].adj_level[dir].adj_level['d' if (dir == 'u') else 'u'] = gc['level']
    gc['level'] = gc['level'].adj_level[dir]
    gc['interface'].setBackground(gc['level'].tilemap)
    pos = gc['level'].spawn
    gc['elems']['player'].posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1]]
    update_playpos(gc)
    paint_posarray(gc['level'], gc['elems']['door1'].posarray, mapping.STAIR_DOWN)
    paint_posarray(gc['level'], gc['elems']['door2'].posarray, mapping.STAIR_UP)
    gc['elems']['player'].chunkCounter = 0

def update_item_visibility(level, item):
    """
    Update an item's visibility: items should only be visible at their origin chunk
    """
    if(level.curr_chunk.id == item.origin):
        if(not item.visible):
            item.sprite.setPos(item.pos)
            item.visible = True
    else:
        if(item.visible):
            item.sprite.setPos((-100, -100))
            item.visible = False

def update_door(level, door, type):
    """
    Updates map state representation
    """
    update_item_visibility(level, door)
    if(door.sprite.rect.center[0] < 0 and door.represented == True):
        clear_posarray(level, door.posarray)
        door.represented = False

    elif(door.sprite.rect.center[0] >= 0 and door.represented == False):
        paint_posarray(level, door.posarray, (mapping.STAIR_UP if type else mapping.STAIR_DOWN))
        door.represented = True

#TODO: generalize pickup functions, create pickup class
#PICKAXE FUNCTIONS
def update_pickaxe_sprite(player, pickaxe):
    pickaxe.angle -= 7
    pic, pac = pickaxe.sprite.rect.center, player.sprite.rect.center
    offset = Vector2(30,30)
    pickaxe.sprite.rect.center = pac + offset.rotate(pickaxe.angle)

def update_pickaxe(level, pickaxe, player):
    if(player.destructionMode):update_pickaxe_sprite(player, pickaxe)
    if(pickaxe.picked):return
    update_item_visibility(level, pickaxe)
    paint_posarray(level, pickaxe.posarray, mapping.PICKAXE)

def pick_pickaxe(level, player, pickaxe):
    pickaxe.sprite.rect.center = (player.sprite.rect.center[0]+2, player.sprite.rect.center[0]+2)
    pickaxe.picked, pickaxe.visible = True, False
    clear_posarray(level, pickaxe.posarray)
    pickaxe.sprite.setPos((-100, -100))

def use_pickaxe(player, pickaxe):
    if(pickaxe.picked == False):return
    player.destructionMode = True - player.destructionMode
    if(not player.destructionMode):
        pickaxe.sprite.setPos((-100, -100))
        pickaxe.visible = False

#VERY IMPORTANT TODO: generalize pickup functions!!!
#ORB functions
def update_orb_sprite(player, orb):
    orb.angle -= 7
    pic, pac = orb.sprite.rect.center, player.sprite.rect.center
    offset = Vector2(50,50)
    orb.sprite.rect.center = pac + offset.rotate(orb.angle)


def update_orb(level, orb, player):
    #TODO: change to check if it is in player's "using item dictionary"
    if(player.deathPower == True):update_orb_sprite(player, orb)
    if(orb.picked):return
    update_item_visibility(level, orb)
    paint_posarray(level, orb.posarray, mapping.ORB)

def get_ray(level, pos, component_id, ray, play_dir, depth):
    if(depth == 700 or level.where[pos[0]][pos[1]] != component_id):return
    ray.append(pos)
    prob = [0.85 if play_dir == const.DIRS[i] else 0.5 for i in range(len(const.DIRS))]
    curr_dir = random.choices(const.DIRS, prob)[0]
    new_pos = (pos[0] + curr_dir[0], pos[1] + curr_dir[1])
    if(level.is_walkable(new_pos)):get_ray(level, new_pos, component_id, ray, play_dir, depth+1)

def death_ray(level, interface, player):
    #fetch a set of coordinates
    arbpos = player.posarray[0]
    for i in range(50):
        ray = []
        get_ray(level, arbpos, level.where[arbpos[0]][arbpos[1]], ray, tuple(player.dir), 0)
        #show it in the inferface
        interface.showRay(ray)
        #display death ray text
        interface.clearRay(ray, level.tilemap)
        #kill the corresponding enemies
        for cell in ray:
            if(level.loc(cell) == mapping.ENEMY):
                enemy = level.locToEnemy[cell]
                enemy.hp = max(enemy.hp-1, 0)

def pick_orb(level, player, orb):
    orb.sprite.rect.center = (player.sprite.rect.center[0]+2, player.sprite.rect.center[0]+2)
    orb.picked, orb.visible = True, False
    clear_posarray(level, orb.posarray)
    orb.sprite.setPos((-100, -100))

def use_orb(level, player, orb):
    if(orb.picked == False):return
    player.deathPower = True - player.deathPower
    if(not player.deathPower):
        orb.sprite.setPos((-100, -100))
        orb.visible = False

def destroy_walls(level, player, interface):
    nxt_pos = player.nxtPosarray(player.dir)
    for x in nxt_pos:
        if(x in player.posarray or level.whereIsPos(x)[0] != 0):continue
        if(level.loc(x) != mapping.WALL):continue
        level.state[x[0]][x[1]] = mapping.AIR
        level.tilemap[x[0]][x[1]].color = mapping.colors[bisect.bisect_left(mapping.heights, 0.62)-1]
        interface.setBackground(level.tilemap)

def update_player(gc):
    update_playpos(gc)
    if(gc['elems']['player'].destructionMode):destroy_walls(gc['level'], gc['elems']['player'], gc['interface'])


def update_playpos(gc):
    """Update Player Position
    Updates the player's sprite position and the player representation in tilemap
    """
    #find next position
    nxtpos = gc['elems']['player'].nxtPosarray(gc['elems']['player'].dir)
    #check if player is trying to go outside the chunk
    dir = gc['level'].findBorder(nxtpos)
    if(dir[0] != 0):
        nxt_chunk(gc, gc['level'], dir)
        updateBakground(gc['interface'], gc['level'])
        chunkdir = [-dir[1][1], -dir[1][0]]
        nxtpos = gc['elems']['player'].nxtPosarray(dir[1])
        gc['elems']['player'].updatePos(nxtpos)
        paint_posarray(gc['level'], gc['elems']['player'].posarray, mapping.PLAYER)
        return
    #movement
    #TODO: inside definition of ge
    if(gc['elems']['player'].moving == False):return
    for pos in nxtpos:
        posloc = gc['level'].loc(pos)
        match posloc:
            case mapping.STAIR_DOWN:
                if(gc['elems']['player'].chunkCounter>10):nxt_level(gc, 'd')
            case mapping.STAIR_UP:
                nxt_level(gc, 'u')
                return
            case mapping.PICKAXE:
                pick_pickaxe(gc['level'], gc['elems']['player'], gc['elems']['pick'])
            case mapping.ORB:
                pick_orb(gc['level'], gc['elems']['player'], gc['elems']['orb'])
            case _:
                if(gc['level'].is_walkable(pos) == False):return
    clear_posarray(gc['level'], gc['elems']['player'].posarray)
    gc['elems']['player'].updatePos(nxtpos)
    paint_posarray(gc['level'], gc['elems']['player'].posarray, mapping.PLAYER)

def spawn_enemy_batch(level, player, enemy_list):
    for i in range(level.rows):
        for j in range(level.columns):
            loc1, loc2 = level.loc((i, j)), level.loc((i+1, j+1))
            if(loc1 != mapping.AIR or loc2 != mapping.AIR):continue
            chance = random.choices([1, 0], [level.enemy_probability, 1-level.enemy_probability])
            if(chance[0] == 1):
                #change const file to variables file
                const.enemies += 1
                newEnemy = Enemy(f'Global Warming, {const.enemies}', (i, j), (level.curr_chunk.id, level.seed))
                enemy_list.append(newEnemy)
                paint_posarray(level, newEnemy.posarray, mapping.ENEMY)

def create_question():
    a, b = random.randint(0, const.DIFFICULTY), random.randint(0, const.DIFFICULTY)
    return (f"What is {a} * {b}?", a*b)

#TODO: todas las funciones deberian ser de actions

def game_over(interface):
    music.play_song("end.mp3")
    interface.gameOver()
    time.sleep(8)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

#TODO (importante): hacer una funcion que se llame "get keys" para no repetir codigo o algo por el estilo

def combat(level, interface, player, enemy):
    interface.fillScreen([0, 0, 0])
    question = create_question()
    interface.createQuestionText(question[0])
    curr, currect = "", None
    done = False
    while (done == False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:          # check for key presses 
                if(event.key in number_keys):
                    curr += str(number_keys.index(event.key))
                    currect = interface.writeUserInput(curr)
                elif(event.key == pygame.K_BACKSPACE):
                    if(len(curr) == 0):continue
                    curr = curr.rstrip(curr[-1])
                    interface.clearText(currect)
                    currect = interface.writeUserInput(curr)
                if(event.key == pygame.K_RETURN):
                    if(int(curr) != question[1]):
                        game_over(interface)
                    done = True
    player.moving = 0
    interface.setBackground(level.tilemap)

def update_enemy_pos(level, interface, enemy, player):
    if(enemy == None):return
    #find next position
    nxtpos = enemy.nxtPosarray(enemy.dir)
    # check if enemy is trying to go outside the chunk
    dir = level.findBorder(nxtpos)
    if(dir[0] != 0):
        enemy.dir = Vector2(1 - 2*random.randint(0, 1), 1 - 2*random.randint(0, 1))
        return
    #movement
    for pos in nxtpos:
        posloc = level.loc(pos)
        if(posloc == mapping.PLAYER):
            combat(level, interface, player, enemy)
            clear_posarray(level, enemy.posarray)
            enemy.sprite.kill()
            enemy.hp = 0
            return
        if(level.is_walkable(pos) == False):
            enemy.dir = Vector2(1 - 2*random.randint(0, 1), 1 - 2*random.randint(0, 1))
            return
    if(enemy.moving == False):return
    clear_posarray(level, enemy.posarray)
    enemy.updatePos(nxtpos)
    paint_posarray(level, enemy.posarray, mapping.ENEMY)
    for pos in enemy.posarray:
        level.locToEnemy[tuple(pos)] = enemy

#Sonido Trueno Minecraft

def update_enemies(gc):
    enems = gc['elems']['enemies']
    while(len(enems) == 0):
        if(gc['level'].curr_chunk.killed):return
        spawn_enemy_batch(gc['level'], gc['elems']['player'], enems)
        add_sprites(gc['sprite_group'], enems)
    to_delete = []
    changedLevel = False
    for enemy_ind in range(len(enems)):
        if(enems[enemy_ind].hp == 0 or enems[enemy_ind].origin != (gc['level'].curr_chunk.id, gc['level'].seed)):
            if(enems[enemy_ind].origin != (gc['level'].curr_chunk.id, gc['level'].seed)):changedLevel = True
            to_delete.append(enemy_ind)
            continue
        update_enemy_pos(gc['level'], gc['interface'], enems[enemy_ind], gc['elems']['player'])
    for ind in to_delete[::-1]:
        clear_posarray(gc['level'], enems[ind].posarray)
        enems[ind].sprite.kill()
        gc['level'].locToEnemy.pop(enems[ind], None)
        enems.pop(ind)
    #Check if you have killed everyone
    if(len(enems) == 0 and not changedLevel):
        gc['level'].curr_chunk.killed = True
        return