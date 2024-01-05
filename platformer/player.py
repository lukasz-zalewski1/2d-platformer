class Player:
    def __init__(self):
        '''
        Initializes player object
        '''

        self.finished = 0
        # Player starts in middle of screen
        self.player_pos = [0, 448]
        self.player_pos_on_screen = [0, 448]
        self.weapon = None
        # It means that player has no weapon selected
        self.current_weapon = -1
        self.weapons = []
        self.keys = 0
        self.keys_to_collect = 0


    def set_starting_hp(self, hp):
        '''
        Sets starting health for player
        
        Args:
            hp (int): starting health
        '''

        self.max_hp = hp
        self.hp = self.max_hp


    def add_weapon(self, weapon):
        '''
        Adds weapon to player's inventory if player does not already
        have it
        
        Args:
            weapon (Weapon): weapon to add
        '''

        self.weapons.append(weapon)
        if not self.weapon:
            self.current_weapon = 0
            self.weapon = self.weapons[self.current_weapon]

    def add_hp(self, hp):
        '''
        Adds health to player if he has not maximum health. Returns
        True if he wasn't at full health, otherwise returns False
        
        Args:
            hp (int): health to add
        
        Returns:
            True if player hadn't maximum health
        '''

        if self.hp == self.max_hp:
            return False
        else:
            self.hp += hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            return True

    def change_weapon(self, next):
        '''
        Switches to next or previous weapon
        
        Args:
            next (bool): True for next weapon, False for previous
        '''

        if len(self.weapons) > 0:
            if self.current_weapon >= 0:
                if next:
                    self.current_weapon += 1
                    if self.current_weapon >= len(self.weapons):
                        self.current_weapon = 0
                else:
                    self.current_weapon -= 1
                    if self.current_weapon < 0:
                        self.current_weapon = len(self.weapons) - 1
            
            self.weapon = self.weapons[self.current_weapon]


    def calculate_player_pos_on_screen(self, map_size):
        '''
        Calculates player's position on screen
        
        Args:
            map_size (int): map's length in blocks
        '''

        # 320 is half of screen
        # 32 is block size
        # When player exceeds half of screen player_pos and 
        # player_pos_on_screen are different
        if (self.player_pos[0] <= 320):
            self.player_pos_on_screen[0] = self.player_pos[0]
        elif (self.player_pos[0] >= map_size*32 - 320):
            self.player_pos_on_screen[0] = 640 - \
                (map_size*32 - self.player_pos[0])
        else:
            self.player_pos_on_screen[0] = 320


    def is_bullet_on_player(self, bullet_pos):
        '''
        Returns True if bullet collides with player, otherwise returns False
        
        Args:
            bullet_pos (int, int): bullet's position
        
        Returns:
            True if bullet collides
        '''

        if self.player_pos[0] <= bullet_pos[0] <= self.player_pos[0] + 32 and self.player_pos[1] <= bullet_pos[1] <= self.player_pos[1] + 32:
            return True
        
        return False


    def hit(self, damage):
        '''
        Damages player and returns True if player's hp is lower or equal to 0, 
        otherwise returns False
        
        Arguments:
            damage (int): damage dealt
        
        Returns:
            True if player's hp is lower than 0
        '''

        self.hp -= damage
        if self.hp <= 0:
            return True

        return False


    def die(self):
        '''
        Sets finished attribute to 1. Basically it means player has died
        '''
        
        self.finished = 1