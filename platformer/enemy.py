class Enemy:
    def __init__(self, image_name, block_pos, movement, hp, weapon):
        '''
        Initialize Enemy object

        image_name (string): name of image in images container

        block_pos (int, int): block position in blocks metric

        movement (EnemyMovement): EnemyMovement object

        hp (int): Enemy's health

        weapon (Weapon): Enemy's weapon
        '''

        self.image_name = image_name
        self.start_block_pos = block_pos
        self.movement = movement
        self.pos = [self.start_block_pos[0] * 32, self.start_block_pos[1] * 32]
        self.movement.enemy_pos = self.pos
        self.pos_on_screen = []
        self.hp = hp
        self.weapon = weapon
        # Is enemy more than 960px away from player
        self.is_in_bigger_sight_ = False

    def set_ai(self, ai):
        '''
        Sets ai and gives ai weapon

        Args:
            ai (Ai): Ai object
        '''

        self.ai = ai
        self.ai.weapon = self.weapon

    def is_bullet_on_enemy(self, bullet_pos):
        '''
        Returns True if bullet hit enemy, otherwise returns False
        
        Args:
            bullet_pos (int, int): bullet's position
        
        Returns:
            True if bullet has hit enemy
        '''

        if self.pos[0] <= bullet_pos[0] <= self.pos[0] + 32 and self.pos[1] <= bullet_pos[1] <= self.pos[1] + 32:
            return True
        
        return False

    def hit(self, damage):
        '''
        Substracts damage from enemy's health. Returns True if enemy's hp is lesser than 0,
        otherwise returns False
        
        Args:
            damage (int): damage
        
        Returns:
            True if enemy's hp is lesser than 0
        '''

        self.hp -= damage
        if self.hp <= 0:
            return True

        return False


    def is_in_bigger_sight(self, player_pos):
        '''
        Sets attribute is_in_bigger_sight_ to True if enemy is in player's sight
        position, otherwise sets it to False
        
        Arguments:
            player_pos (int, int): player's positon
        '''

        if abs(self.pos[0] - player_pos[0]) <= 960:
            self.is_in_bigger_sight_ = True
        else:
            self.is_in_bigger_sight_ = False