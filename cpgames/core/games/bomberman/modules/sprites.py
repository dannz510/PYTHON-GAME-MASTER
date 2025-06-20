
import copy
import random
import pygame



class Wall(pygame.sprite.Sprite):
    def __init__(self, image, coordinate, blocksize, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (blocksize, blocksize))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
        self.coordinate = coordinate
        self.blocksize = blocksize

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return True



class Background(pygame.sprite.Sprite):
    def __init__(self, image, coordinate, blocksize, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (blocksize, blocksize))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
        self.coordinate = coordinate
        self.blocksize = blocksize

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return True



class Fruit(pygame.sprite.Sprite):
    def __init__(self, image, kind, coordinate, blocksize, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.kind = kind
        if self.kind == 'banana':
            self.value = 5
        elif self.kind == 'cherry':
            self.value = 10
        else:
            raise ValueError('Unknow fruit %s...' % self.kind)
        self.image = pygame.transform.scale(image, (blocksize, blocksize))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
        self.coordinate = coordinate
        self.blocksize = blocksize

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return True



class Bomb(pygame.sprite.Sprite):
    def __init__(self, image, coordinate, blocksize, digitalcolor, explode_image, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (blocksize, blocksize))
        self.explode_image = explode_image
        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize

        self.coordinate = coordinate
        self.blocksize = blocksize
   
        self.explode_millisecond = 6000 * 1 - 1
        self.explode_second = int(self.explode_millisecond / 1000)
        self.start_explode = False
   
        self.exploding_count = 1000 * 1
      
        self.harm_value = 1
 
        self.is_being = True
        self.font = pygame.font.SysFont('Consolas', 20)
        self.digitalcolor = digitalcolor

    def draw(self, screen, dt, map_parser):
        if not self.start_explode:
         
            self.explode_millisecond -= dt
            self.explode_second = int(self.explode_millisecond / 1000)
            if self.explode_millisecond < 0:
                self.start_explode = True
            screen.blit(self.image, self.rect)
            text = self.font.render(str(self.explode_second), True, self.digitalcolor)
            rect = text.get_rect(center=(self.rect.centerx-5, self.rect.centery+5))
            screen.blit(text, rect)
            return False
        else:
          
            self.exploding_count -= dt
            if self.exploding_count > 0:
                return self.__explode(screen, map_parser)
            else:
                self.is_being = False
                return False

    def __explode(self, screen, map_parser):
        explode_area = self.__calcExplodeArea(map_parser.instances_list)
        for each in explode_area:
            image = self.explode_image
            image = pygame.transform.scale(image, (self.blocksize, self.blocksize))
            rect = image.get_rect()
            rect.left, rect.top = each[0] * self.blocksize, each[1] * self.blocksize
            screen.blit(image, rect)
        return explode_area
    
    def __calcExplodeArea(self, instances_list):
        explode_area = []

        for ymin in range(self.coordinate[1], self.coordinate[1]-5, -1):
            if ymin < 0 or instances_list[ymin][self.coordinate[0]] in ['w', 'x', 'z']:
                break
            explode_area.append([self.coordinate[0], ymin])
        for ymax in range(self.coordinate[1]+1, self.coordinate[1]+5):
            if ymax >= len(instances_list) or instances_list[ymax][self.coordinate[0]] in ['w', 'x', 'z']:
                break
            explode_area.append([self.coordinate[0], ymax])
        for xmin in range(self.coordinate[0], self.coordinate[0]-5, -1):
            if xmin < 0 or instances_list[self.coordinate[1]][xmin] in ['w', 'x', 'z']:
                break
            explode_area.append([xmin, self.coordinate[1]])
        for xmax in range(self.coordinate[0]+1, self.coordinate[0]+5):
            if xmax >= len(instances_list[0]) or instances_list[self.coordinate[1]][xmax] in ['w', 'x', 'z']:
                break
            explode_area.append([xmax, self.coordinate[1]])
        return explode_area


class Hero(pygame.sprite.Sprite):
    def __init__(self, images, coordinate, blocksize, map_parser, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images[-1]
        self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
        self.coordinate = coordinate
        self.blocksize = blocksize
        self.map_parser = map_parser
        self.hero_name = kwargs.get('hero_name')

        self.health_value = 50
      
        self.bomb_cooling_time = 5000
        self.bomb_cooling_count = 0
       
        self.randommove_cooling_time = 100
        self.randommove_cooling_count = 0

    def move(self, direction):
        self.__updateImage(direction)
        if direction == 'left':
            if self.coordinate[0]-1 < 0 or self.map_parser.getElemByCoordinate([self.coordinate[0]-1, self.coordinate[1]]) in ['w', 'x', 'z']:
                return False
            self.coordinate[0] = self.coordinate[0] - 1
        elif direction == 'right':
            if self.coordinate[0]+1 >= self.map_parser.width or self.map_parser.getElemByCoordinate([self.coordinate[0]+1, self.coordinate[1]]) in ['w', 'x', 'z']:
                return False
            self.coordinate[0] = self.coordinate[0] + 1
        elif direction == 'up':
            if self.coordinate[1]-1 < 0 or self.map_parser.getElemByCoordinate([self.coordinate[0], self.coordinate[1]-1]) in ['w', 'x', 'z']:
                return False
            self.coordinate[1] = self.coordinate[1] - 1
        elif direction == 'down':
            if self.coordinate[1]+1 >= self.map_parser.height or self.map_parser.getElemByCoordinate([self.coordinate[0], self.coordinate[1]+1]) in ['w', 'x', 'z']:
                return False
            self.coordinate[1] = self.coordinate[1] + 1
        else:
            raise ValueError('Unknow direction %s...' % direction)
        self.rect.left, self.rect.top = self.coordinate[0] * self.blocksize, self.coordinate[1] * self.blocksize
        return True
  
    def randomAction(self, dt):
    
        if self.randommove_cooling_count > 0:
            self.randommove_cooling_count -= dt
        action = random.choice(['left', 'left', 'right', 'right', 'up', 'up', 'down', 'down', 'dropbomb'])
        flag = False
        if action in ['left', 'right', 'up', 'down']:
            if self.randommove_cooling_count <= 0:
                flag = True
                self.move(action)
                self.randommove_cooling_count = self.randommove_cooling_time
        elif action in ['dropbomb']:
            if self.bomb_cooling_count <= 0:
                flag = True
                self.bomb_cooling_count = self.bomb_cooling_time
        return action, flag

    def generateBomb(self, image, digitalcolor, explode_image):
        return Bomb(image=image, coordinate=copy.deepcopy(self.coordinate), blocksize=self.blocksize, digitalcolor=digitalcolor, explode_image=explode_image)
  
    def draw(self, screen, dt):
   
        if self.bomb_cooling_count > 0:
            self.bomb_cooling_count -= dt
        screen.blit(self.image, self.rect)
        return True

    def eatFruit(self, fruit_sprite_group):
        eaten_fruit = pygame.sprite.spritecollide(self, fruit_sprite_group, True, None)
        for fruit in eaten_fruit:
            self.health_value += fruit.value
   
    def __updateImage(self, direction):
        directions = ['left', 'right', 'up', 'down']
        idx = directions.index(direction)
        self.image = self.images[idx]
        self.image = pygame.transform.scale(self.image, (self.blocksize, self.blocksize))