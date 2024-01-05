import pygame
import math

class Bullet:
    def __init__(self, pos, speed, solid, angle, range):
        '''
        Initialize Bullet object

        Args:
            pos (int, int): bullet's position

            speed (int): bullet speed, px per 1s

            angle (float): angle between player's weapon and bullets

            range (int): distance in px after which bullets disappear
        '''

        self.pos = pos
        self.speed = speed
        self.solid = solid
        self.angle = angle
        self.range = range
        self.distance_traveled = 0
        
    def calculate_new_pos(self, time):
        '''
        Calculates and sets new bullet's position and also removes
        bullet if it has extended its range. Returns True if bullet extended its range,
        otherwise False
        
        Args:
            time (int): time in ms
        
        Returns:
            True if bullet extended its range
        '''

        distance = time / 1000 * self.speed
        self.distance_traveled += distance
        self.pos[0] += distance * math.cos(self.angle)
        self.pos[1] += distance * math.sin(self.angle)

        if self.distance_traveled >= self.range:
            return True

        return False


class Weapon:
    def __init__(self, shooting_type, shooting_type_arg, damage, bullets_speed, bullets_per_second, bullets_solid, bullets_range):
        '''
        Initializes Weapon object

        Args:
            shooting_type (int): describes how weapon shoots bullets
                0 - line
                1 - all around
                2 - cone
            
            shooting_type_arg (int): describes how many bullets are shot at once
                only for shooting_type = 1 or 2

            damage (int): single bullet damage

            bullets_speed (int): bullet speed, px per 1s

            bullets_per_second (int): how many waves of bullets are shot per second

            bullets_solid (bool): are bullets solid, do they fly through blocks?

            bullets_range (bool): bullets range in px
        '''

        self.shooting = False
        self.shooting_type = shooting_type
        self.shooting_type_arg = shooting_type_arg
        self.damage = damage
        self.bullets_speed = bullets_speed
        self.bullets_per_second = bullets_per_second
        self.bullets_solid = bullets_solid
        self.bullets = []
        self.clock = pygame.time.Clock()
        self.clock_combined_time = 0
        self.shoot_tick_time = 10
        self.bullets_range = bullets_range


    def shoot(self, entity_pos, angle):
        '''
        Shoots new bullet from player's position at given angle
        
        Arguments:
            entity_pos (int, int): shooter position

            angle (float): angle in radians
        '''

        weapon_pos = entity_pos[:]
        # Weapon position is moved a little to right from entity
        # So it looks like bullets are shot directly from the weapon 
        weapon_pos[0] += 32
        weapon_pos[1] += 16
        # Shot single line of bullets
        if self.shooting_type == 0:
            self.bullets.append(Bullet(weapon_pos, self.bullets_speed, self.bullets_solid, angle, self.bullets_range))
        # Shot bullets all around
        elif self.shooting_type == 1:
            for i in range(self.shooting_type_arg):
                self.bullets.append(Bullet([weapon_pos[0], weapon_pos[1]], self.bullets_speed, self.bullets_solid,
                                    math.radians((i/self.shooting_type_arg) * 360), self.bullets_range))
        # Shot bullets in a cone
        elif self.shooting_type == 2:
            for i in range(-(self.shooting_type_arg // 2), (self.shooting_type_arg // 2) + 1, 1):
                self.bullets.append(Bullet([weapon_pos[0], weapon_pos[1]], self.bullets_speed, self.bullets_solid,
                                    angle + math.radians(45 * (i / self.shooting_type_arg)), self.bullets_range))


    def calculate_bullets_pos(self):
        '''
        Calculates positions for all bullets shot by weapon's object
        and removes bullet if it extended its range
        '''

        for bullet in self.bullets:
            if bullet.calculate_new_pos(self.clock_combined_time):
                self.bullets.remove(bullet)


