from typing import Union
from pygame.math import Vector2

import mapping
import pygame
import vars
import random
from enemy import Enemy
import sys
import time
import bisect
from actionsdir import interface_actions, level_actions, player_actions, entities_actions, items_actions, music_actions

def frame(gc, ge):
    music_actions.rand_music("end.wav")
    interface_actions.update_xp(gc['interface'], gc['elems']['player'])
    update_enemies(gc)
    update_player(gc)
    items_actions.update_door(gc['level'], ge['door1'], False)
    items_actions.update_door(gc['level'], ge['door2'], True)
    items_actions.update_pickaxe(gc['level'], ge['pick'], ge['player'])
    items_actions.update_orb(gc['level'], ge['orb'], ge['player'])
    interface_actions.render_interface(gc['interface'])

def nxt_level(gc, dir):
    ge = gc['elems']
    if(gc['level'].adj_level[dir] == None):
        gc['level'].adj_level[dir] = mapping.Level(gc['level'].rows, gc['level'].columns, gc['level'].seed+1)
        gc['level'].adj_level[dir].adj_level['d' if (dir == 'u') else 'u'] = gc['level']
    gc['level'] = gc['level'].adj_level[dir]
    gc['interface'].setBackground(gc['level'].tilemap)
    pos = gc['level'].spawn
    ge['player'].posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1]]
    update_playpos(gc)
    level_actions.paint_posarray(gc['level'], ge['door1'].posarray, mapping.STAIR_DOWN)
    level_actions.paint_posarray(gc['level'], ge['door2'].posarray, mapping.STAIR_UP)
    ge['player'].XP = 0

def death_ray(level, interface, player):
    #fetch a set of coordinates
    arbpos = player.posarray[0]
    for i in range(50):
        ray = []
        level_actions.get_ray(level, arbpos, level.where[arbpos[0]][arbpos[1]], ray, tuple(player.dir), 0)
        #show it in the inferface
        interface.showRay(ray)
        #display death ray text
        interface.clearRay(ray, level.tilemap)
        #kill the corresponding enemies
        for cell in ray:
            if(level.loc(cell) == mapping.ENEMY):
                enemy = level.locToEnemy[cell]
                enemy.hp = max(enemy.hp-1, 0)

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
    if(gc['elems']['player'].inventory['P']):destroy_walls(gc['level'], gc['elems']['player'], gc['interface'])

def update_playpos(gc):
    """Update Player Position
    Updates the player's sprite position and the player representation in tilemap
    """
    ge = gc['elems']
    #find next position
    nxtpos = ge['player'].nxtPosarray(ge['player'].dir)
    #check if player is trying to go outside the chunk
    dir = gc['level'].findBorder(nxtpos)
    if(dir[0] != 0):
        level_actions.nxt_chunk(gc, gc['level'], dir)
        interface_actions.update_background(gc['interface'], gc['level'])
        chunkdir = [-dir[1][1], -dir[1][0]]
        nxtpos = ge['player'].nxtPosarray(dir[1])
        ge['player'].updatePos(nxtpos)
        level_actions.paint_posarray(gc['level'], ge['player'].posarray, mapping.PLAYER)
        return
    #movement
    if(ge['player'].moving == False):return
    for pos in nxtpos:
        posloc = gc['level'].loc(pos)
        match posloc:
            case mapping.STAIR_DOWN:
                if(level_actions.can_open(gc['level'], ge['player'].XP)):
                    nxt_level(gc, 'd')
                    return
            case mapping.STAIR_UP:
                if(gc['level'].seed == vars.ORIGIN_CHUNK):
                    quit_or_win(ge['player'], gc['interface'])
                nxt_level(gc, 'u')
                return
            case mapping.PICKAXE:
                items_actions.pick_pickUp(gc['level'], ge['pick'], ge['player'])
            case mapping.ORB:
                items_actions.pick_pickUp(gc['level'], ge['orb'], ge['player'])
            case _:
                if(gc['level'].is_walkable(pos) == False):return
    level_actions.clear_posarray(gc['level'], ge['player'].posarray)
    ge['player'].updatePos(nxtpos)
    level_actions.paint_posarray(gc['level'], ge['player'].posarray, mapping.PLAYER)

def spawn_enemy_batch(level, player, enemy_list):
    for i in range(level.rows):
        for j in range(level.columns):
            loc1, loc2 = level.loc((i, j)), level.loc((i+1, j+1))
            if(loc1 != mapping.AIR or loc2 != mapping.AIR):continue
            chance = random.choices([1, 0], [level.enemy_probability, 1-level.enemy_probability])
            if(chance[0] == 1):
                #change const file to variables file
                vars.enemies += 1
                newEnemy = Enemy(f'Global Warming, {vars.enemies}', (i, j), (level.curr_chunk.id, level.seed))
                enemy_list.append(newEnemy)
                level_actions.paint_posarray(level, newEnemy.posarray, mapping.ENEMY)

def create_question():
    a, b = random.randint(0, vars.DIFFICULTY), random.randint(0, vars.DIFFICULTY)
    return (f"What is {a} * {b}?", a*b)

def game_over(interface):
    music_actions.play_song("end.mp3")
    interface.gameOver()
    time.sleep(8.5)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

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
                if(event.key in vars.number_keys):
                    curr += str(vars.number_keys.index(event.key))
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
            level_actions.clear_posarray(level, enemy.posarray)
            enemy.sprite.kill()
            enemy.hp = 0
            return
        if(level.is_walkable(pos) == False):
            enemy.dir = Vector2(1 - 2*random.randint(0, 1), 1 - 2*random.randint(0, 1))
            return
    if(enemy.moving == False):return
    level_actions.clear_posarray(level, enemy.posarray)
    enemy.updatePos(nxtpos)
    level_actions.paint_posarray(level, enemy.posarray, mapping.ENEMY)
    for pos in enemy.posarray:
        level.locToEnemy[tuple(pos)] = enemy

#Sonido Trueno Minecraft

def update_enemies(gc):
    ge = gc['elems']
    enems = ge['enemies']
    while(len(enems) == 0):
        if(gc['level'].curr_chunk.killed):return
        spawn_enemy_batch(gc['level'], ge['player'], enems)
        entities_actions.add_sprites(gc['sprite_group'], enems)
    to_delete = []
    changedLevel = False
    for enemy_ind in range(len(enems)):
        if(enems[enemy_ind].hp == 0 or enems[enemy_ind].origin != (gc['level'].curr_chunk.id, gc['level'].seed)):
            if(enems[enemy_ind].origin != (gc['level'].curr_chunk.id, gc['level'].seed)):changedLevel = True
            to_delete.append(enemy_ind)
            continue
        update_enemy_pos(gc['level'], gc['interface'], enems[enemy_ind], ge['player'])
    for ind in to_delete[::-1]:
        level_actions.clear_posarray(gc['level'], enems[ind].posarray)
        enems[ind].sprite.kill()
        gc['level'].locToEnemy.pop(enems[ind], None)
        enems.pop(ind)
    #Check if you have killed everyone
    if(len(enems) == 0 and not changedLevel):
        gc['level'].curr_chunk.killed = True
        return

def win_screen(interface):
    music_actions.play_song("end.mp3")
    interface.Won()
    time.sleep(8.5)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def quit_or_win(player, interface):
    if player_actions.in_inventory(player, 'T'):
        win_screen()
    else:
        game_over(interface)