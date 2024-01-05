import abc

class ConsumableBlock:
    '''
    Base class for consumable blocks. Consumable blocks are blocks
    that player can step onto, then they disappear giving player some benefits
    '''

    def __init__(self, block_pos, image_name):
        '''
        Initializes ConsumableBlock object 

        Args:
            block_pos (int, int): position on map in blocks metric

            image_name (string): name of image in image container
        '''

        self.block_pos = block_pos
        self.image_name = image_name


    @abc.abstractmethod
    def on_pick_up(self, player):
        '''
        Abstract method defining what happens when player steps on block
        '''

        pass

    def is_player_on_block(self, player):
        '''
        Returns True if player stepped on block, otherwise returns False
        
        Args:
            player (Player): Player object
        
        Returns:
            True if player stepped on block
        '''

        # It checks middle of player's object so +16 is added
        if (player.player_pos[0] + 16) // 32 == self.block_pos[0] and (player.player_pos[1] + 16) // 32 == self.block_pos[1]:
            if self.on_pick_up(player):
                return True

        return False


class HealthBlock(ConsumableBlock):
    '''
    Health consumable block. Returns some health to player
    '''
    
    def __init__(self, block_pos, image_name, hp):
        '''
        Initializes HealthBlock object

        Args:
            block_pos (int, int): block position in blocks metric

            image_name (string): name of image in images container

            hp (int): how much hp is restored after stepping on the block
        '''

        super().__init__(block_pos, image_name)
        self.hp = hp


    def on_pick_up(self, player):
        '''
        Defines what happens when player steps on block

        Args:
            player (Player): Player object
        '''

        return player.add_hp(self.hp)


class WeaponBlock(ConsumableBlock): 
    '''
    Weapon consumable block. On step adds weapon to player's inventory
    '''

    def __init__(self, block_pos, image_name, weapon):
        ''' 
        Initializes WeaponBlock object

        Args:
            block_pos (int, int): block position in blocks metric

            image_name (string): image name in images container

            weapon (Weapon): weapon object
        '''

        super().__init__(block_pos, image_name)
        self.weapon = weapon


    def on_pick_up(self, player):
        '''
        Defines what happens when player steps on block
        '''

        player.add_weapon(self.weapon)

        return True


class KeyBlock(ConsumableBlock):
    '''
    Key consumable block. Keys are needed to finish level
    '''

    def __init__(self, block_pos, image_name):
        '''
        Initialize KeyBlock object

        Args:
            block_pos (int, int): block position in blocks metric

            image_name (string): name of image in images container
        '''

        super().__init__(block_pos, image_name)

    def on_pick_up(self, player):
        '''
        Defines what happens when player steps on block

        Args:  
            player (Player): Player object
        '''

        player.keys += 1

        return True


class FinishBlock(ConsumableBlock):
    '''
    Finish consumable block. On step finishes level, if player has 
    collected all keys
    '''

    def __init__(self, block_pos, image_name):
        '''
        Initializes FinishBlock object

        Args:
            block_pos (int, int): block position in blocks metric

            image_name (string): name of image in images container
        '''

        super().__init__(block_pos, image_name)

    def on_pick_up(self, player):
        '''
        Defines what happens when player steps on block

        Args:  
            player (Player): Player object
        '''

        # finished=2 means that player has finished the level and didn't die
        if player.keys >= player.keys_to_collect:
            player.finished = 2
            return True

        return False