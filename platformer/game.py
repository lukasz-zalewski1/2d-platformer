import os

import pygame

from pathlib import Path

import ai
import enemy
import enemy_movement
import events
import graphics
import map
import player
import player_movement
import weapon


class Game:
    '''
    Main program class. Contains and initializes all of game main objects
    '''

    def __init__(self):
        pygame.init()

        self.map_path = (Path(__file__).parent.parent).joinpath('maps')
        self.__load_map_list(self.map_path)
        self.current_map = 0


    def __load_map_list(self, path):
        '''
        Load maps from given directory. Maps naming convention is
        'map{map number starting from 0}.map'

        Args:
            path (string): path to map's directory
        '''

        self.maps = [map_ for map_ in os.listdir(path) if map_.find('.map') != -1]


    def __load_next_map(self):
        '''
        Cleans all information from previous map and loads new one
        '''

        self.player = player.Player()
        self.enemies = []
        self.map_ = map.Map(self.player)
        self.map_.load(f'{self.map_path}\\map{str(self.current_map)}.map')
        self.__load_enemies()
        self.graphics = graphics.Graphics(self.player, self.enemies, self.map_, self.current_map, len(self.maps))
        self.movement = player_movement.Movement(self.player, self.enemies, self.map_, self.graphics)
        self.event_handler = events.EventHandler(
            self.player, self.enemies, self.map_, self.graphics, self.movement)


    def __load_enemies(self):
        '''
        Loads all enemies from map's object and runs their AIs
        '''

        for enemy_info in self.map_.enemy_list:
            enemy_ = enemy.Enemy(enemy_info[0], [enemy_info[1], enemy_info[2]], 
                          enemy_movement.EnemyMovement(True, self.map_, enemy_info[3], enemy_info[4], enemy_info[5], enemy_info[6]),
                          enemy_info[7],
                          weapon.Weapon(enemy_info[8], enemy_info[9], enemy_info[10], enemy_info[11], enemy_info[12], enemy_info[13], enemy_info[14]))
            enemy_.set_ai(ai.EnemyAI(self.player, enemy_.movement, enemy_info[15], enemy_info[16]))
            self.enemies.append(enemy_)


    def play(self):
        '''
        Starts the game. Basically it loads all available maps till player finished them all
        '''

        while self.current_map < len(self.maps):
            self.__load_next_map()
            self.event_handler.event_loop()
            if self.player.finished > 1:
                self.current_map += 1


if __name__ == '__main__':
    game = Game()
    game.play()
