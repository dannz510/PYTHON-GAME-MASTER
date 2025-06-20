
import pygame
from .sprites import Hero
from .maps import MapParser
from ....utils import QuitGame


'''魔塔小游戏主要逻辑实现'''
class GameLevels():
    def __init__(self, cfg, resource_loader):
        self.cfg = cfg
        self.resource_loader = resource_loader
        # 游戏地图中的所有图片
        self.map_element_images = resource_loader.images['mapelements']
        # 游戏背景图片
        self.background_images = {
            'gamebg': pygame.transform.scale(resource_loader.images['gamebg'], cfg.SCREENSIZE),
            'battlebg': pygame.transform.scale(resource_loader.images['battlebg'], (932, 407)),
            'blankbg': resource_loader.images['blankbg'],
        }
        # 游戏地图解析类
        self.map_parsers_dict = {}
        self.max_map_level_pointer = 0
        self.map_level_pointer = 0
        self.loadmap()
        # 英雄类
        self.hero = Hero(
            images=resource_loader.images['hero'],
            blocksize=cfg.BLOCKSIZE,
            block_position=self.map_parser.getheroposition(),
            offset=(325, 55),
            fontpath=cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'],
            background_images=self.background_images,
            cfg=cfg,
            resource_loader=resource_loader,
        )
    '''导入地图'''
    def loadmap(self):
        if self.map_level_pointer in self.map_parsers_dict:
            self.map_parser = self.map_parsers_dict[self.map_level_pointer]
        else:
            self.map_parser = MapParser(
                blocksize=self.cfg.BLOCKSIZE, 
                filepath=self.cfg.MAPPATHS[self.map_level_pointer], 
                element_images=self.map_element_images,
                offset=(325, 55),
            )
            self.map_parsers_dict[self.map_level_pointer] = self.map_parser
    '''运行'''
    def run(self, screen):
        # 游戏主循环
        clock, is_running = pygame.time.Clock(), True
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
            key_pressed = pygame.key.get_pressed()
            move_events = []
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                move_events = self.hero.move('up', self.map_parser, screen)
            elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                move_events = self.hero.move('down', self.map_parser, screen)
            elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                move_events = self.hero.move('left', self.map_parser, screen)
            elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                move_events = self.hero.move('right', self.map_parser, screen)
            elif key_pressed[pygame.K_j] and self.hero.has_jump:
                move_events = ['jump_level']
            elif key_pressed[pygame.K_l] and self.hero.has_forecast:
                move_events = ['forecast_level']
            if not move_events: move_events = []
            # --画游戏地图
            self.map_parser.draw(screen)
            # --左侧面板栏
            font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
            font_renders = [
                self.hero.font.render(str(self.map_level_pointer), True, (255, 255, 255)),
                font.render('Game time: ' + str(pygame.time.get_ticks() // 60000) + ' Point ' + str(pygame.time.get_ticks() // 1000 % 60) + ' Second', True, (255, 255, 255)),
            ]
            rects = [fr.get_rect() for fr in font_renders]
            rects[0].topleft = (150, 530)
            rects[1].topleft = (75, 630)
            for fr, rect in zip(font_renders, rects):
                screen.blit(fr, rect)
            # --画英雄
            self.hero.draw(screen)
            self.hero.cur_scenes = [
                [font_renders[0], rects[0]], [font_renders[1], rects[1]]
            ]
            self.hero.showinfo(screen)
            # --触发游戏事件
            for event in move_events:
                if event == 'upstairs':
                    self.map_level_pointer += 1
                    self.max_map_level_pointer = max(self.max_map_level_pointer, self.map_level_pointer)
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'down')
                elif event == 'downstairs':
                    self.map_level_pointer -= 1
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'up')
                elif event == 'conversation_hero_and_fairy':
                    self.showconversationheroandfairy(screen, self.hero.cur_scenes)
                elif event in ['buy_from_shop', 'buy_from_businessman', 'buy_from_oldman']:
                    self.showbuyinterface(screen, self.hero.cur_scenes, event)
                elif event == 'jump_level':
                    ori_level = self.map_level_pointer
                    self.map_level_pointer = self.showjumplevel(screen, self.hero.cur_scenes)
                    self.loadmap()
                    if ori_level > self.map_level_pointer: self.hero.placenexttostairs(self.map_parser, 'up')
                    else: self.hero.placenexttostairs(self.map_parser, 'down')
                elif event == 'forecast_level':
                    self.showforecastlevel(screen, self.hero.cur_scenes)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
    '''显示关卡怪物信息'''
    def showforecastlevel(self, screen, scenes):
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        monsters = self.map_parser.getallmonsters()
        if len(monsters) < 1: return
        monsters_show_pointer, max_monsters_show_pointer = 1, round(len(monsters) / 4)
        show_tip_text, show_tip_text_count, max_show_tip_text_count = True, 1, 15
        return_flag = False
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        return_flag = True
                    elif event.key == pygame.K_SPACE:
                        monsters_show_pointer = monsters_show_pointer + 1
                        if monsters_show_pointer > max_monsters_show_pointer: monsters_show_pointer = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_l and return_flag:
                        return
            # --对话框
            # ----底色
            width, height = 14, 5
            left, top = self.cfg.SCREENSIZE[0] // 2 - width // 2 * self.cfg.BLOCKSIZE, self.cfg.SCREENSIZE[1] // 2 - height * self.cfg.BLOCKSIZE
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
            # ----边框
            pygame.draw.rect(screen, (199, 97, 20), (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
            # ----展示选项
            for idx, monster in enumerate(monsters[(monsters_show_pointer-1)*4: monsters_show_pointer*4]):
                id_image = self.resource_loader.images['mapelements'][monster[6]][0]
                id_image = pygame.transform.scale(id_image, (self.cfg.BLOCKSIZE - 10, self.cfg.BLOCKSIZE - 10))
                screen.blit(id_image, (left + 10, top + 20 + idx * self.cfg.BLOCKSIZE))
                text = f'Name: {monster[0]}  Life: {monster[1]}  Attack: {monster[2]}  Defense: {monster[3]}  Gold: {monster[4]}  Experience: {monster[5]}  Loss: {self.hero.winmonster(monster)[1]}'
                font_render = font.render(text, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + 15 + self.cfg.BLOCKSIZE, top + 30 + idx * self.cfg.BLOCKSIZE
                screen.blit(font_render, rect)
            # ----操作提示
            show_tip_text_count += 1
            if show_tip_text_count == max_show_tip_text_count:
                show_tip_text_count = 1
                show_tip_text = not show_tip_text
            if show_tip_text:
                tip_text = 'Spacebar'
                font_render = font.render(tip_text, True, (255, 255, 255))
                rect.left, rect.bottom = self.cfg.BLOCKSIZE * width + 30, self.cfg.BLOCKSIZE * (height + 1) + 10
                screen.blit(font_render, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
    '''显示关卡跳转'''
    def showjumplevel(self, screen, scenes):
        # 主循环
        clock, selected_level = pygame.time.Clock(), self.map_level_pointer
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return selected_level
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_level = max(selected_level - 1, 0)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_level = min(selected_level + 1, self.max_map_level_pointer)
            # --对话框
            # ----底色
            width, height = 11, 4
            left, top = self.cfg.SCREENSIZE[0] // 2 - width // 2 * self.cfg.BLOCKSIZE, self.cfg.SCREENSIZE[1] // 2 - height * self.cfg.BLOCKSIZE
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
            # ----边框
            pygame.draw.rect(screen, (199, 97, 20), (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
            # ----展示选项
            for idx in list(range(self.max_map_level_pointer+1)):
                if selected_level == idx:
                    text = f'➤No. {idx} layer'
                    font_render = font.render(text, True, (255, 0, 0))
                else:
                    text = f'➤No. {idx} layer'
                    font_render = font.render(text, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + 20 + idx // 6 * self.cfg.BLOCKSIZE * 2, top + 20 + (idx % 6) * 30
                screen.blit(font_render, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
    '''显示商店'''
    def showbuyinterface(self, screen, scenes, shop_type):
        # 购买函数
        def buy(hero, coins_cost=0, experience_cost=0, add_life_value=0, add_attack_power=0, add_defense_power=0, add_level=0, add_yellow_keys=0, add_purple_keys=0, add_red_keys=0):
            if hero.num_coins < coins_cost: return
            if hero.experience < experience_cost: return
            if add_yellow_keys < 0 and hero.num_yellow_keys < 1: return
            if add_purple_keys < 0 and hero.num_purple_keys < 1: return
            if add_red_keys < 0 and hero.num_red_keys < 1: return
            hero.num_coins -= coins_cost
            hero.experience -= experience_cost
            hero.life_value += add_life_value + 1000 * add_level
            hero.attack_power += add_attack_power + 7 * add_level
            hero.defense_power += add_defense_power + 7 * add_level
            hero.level += add_level
            hero.num_yellow_keys += add_yellow_keys
            hero.num_purple_keys += add_purple_keys
            hero.num_red_keys += add_red_keys
        # 选项定义
        # --第三层商店
        if self.map_level_pointer == 3 and shop_type == 'buy_from_shop':
            choices_dict = {
                'Increase health by 800 (25 gold)': lambda: buy(self.hero, coins_cost=25, add_life_value=800),
                'Increase Attack by 4 (25 gold)': lambda: buy(self.hero, coins_cost=25, add_attack_power=4),
                'Increases defense by 4 (25 gold)': lambda: buy(self.hero, coins_cost=25, add_defense_power=4),
                'Leave the store': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['22'][0]
        # --第十一层商店
        elif self.map_level_pointer == 11 and shop_type == 'buy_from_shop':
            choices_dict = {
                'Increase health by 4000 (100 gold coins)': lambda: buy(self.hero, coins_cost=100, add_life_value=4000),
                'Increase Attack by 20 (100 gold coins)': lambda: buy(self.hero, coins_cost=100, add_attack_power=20),
                'Increases defense by 20 (100 gold)': lambda: buy(self.hero, coins_cost=100, add_defense_power=20),
                'Leave the store': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['22'][0]
        # --第五层神秘老人
        elif self.map_level_pointer == 5 and shop_type == 'buy_from_oldman':
            choices_dict = {
                'Level Up (100 XP)': lambda: buy(self.hero, experience_cost=100, add_level=1),
                'Increase attack by 5 (30 XP points)': lambda: buy(self.hero, experience_cost=30, add_attack_power=5),
                'Increases defense by 5 (30 XP points)': lambda: buy(self.hero, experience_cost=30, add_defense_power=5),
                'Leave the store': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['26'][0]
        # --第十三层神秘老人
        elif self.map_level_pointer == 13 and shop_type == 'buy_from_oldman':
            choices_dict = {
                'Level 3 upgrade (270 XP points)': lambda: buy(self.hero, experience_cost=270, add_level=1),
                'Increases attack by 17 points (95 XP points)': lambda: buy(self.hero, experience_cost=95, add_attack_power=17),
                'Increases defense by 17 (95 XP points)': lambda: buy(self.hero, experience_cost=95, add_defense_power=17),
                'Leave the store': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['26'][0]
        # --第五层商人
        elif self.map_level_pointer == 5 and shop_type == 'buy_from_businessman':
            choices_dict = {
                'Buy 1 Yellow Key (10 Gold)': lambda: buy(self.hero, coins_cost=10, add_yellow_keys=1),
                'Buy 1 Blue Key (50 Gold)': lambda: buy(self.hero, coins_cost=50, add_purple_keys=1),
                'Buy 1 Red Key (100 Gold)': lambda: buy(self.hero, coins_cost=100, add_red_keys=1),
                'Leave the store': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['27'][0]
        # --第十二层商人
        elif self.map_level_pointer == 12 and shop_type == 'buy_from_businessman':
            choices_dict = {
                'Sell 1 Yellow Key (7 Gold)': lambda: buy(self.hero, coins_cost=-7, add_yellow_keys=-1),
                'Sell 1 Blue Key (35 Gold)': lambda: buy(self.hero, coins_cost=-35, add_purple_keys=-1),
                'Sell 1 Red Key (70 Coins)': lambda: buy(self.hero, coins_cost=-70, add_red_keys=-1),
                'Leave the store': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['27'][0]
        id_image = pygame.transform.scale(id_image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
        # 主循环
        clock, selected_idx = pygame.time.Clock(), 1
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        list(choices_dict.values())[selected_idx-1]()
                        if selected_idx == 4: return
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_idx = max(selected_idx - 1, 1)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_idx = min(selected_idx + 1, 4)
            # --对话框
            # ----底色
            width, height = 8, 3
            left, bottom = self.hero.rect.left + self.hero.rect.width // 2 - width // 2 * self.cfg.BLOCKSIZE, self.hero.rect.bottom
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, bottom + row * self.cfg.BLOCKSIZE))
            # ----边框
            pygame.draw.rect(screen, (199, 97, 20), (left - 4, bottom - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
            # ----展示选项
            for idx, choice in enumerate(['Please select:'] + list(choices_dict.keys())):
                if selected_idx == idx and idx > 0:
                    choice = '➤' + choice
                    font_render = font.render(choice, True, (255, 0, 0))
                elif idx > 0:
                    choice = '    ' + choice
                    font_render = font.render(choice, True, (255, 255, 255))
                else:
                    font_render = font.render(choice, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + self.cfg.BLOCKSIZE + 20, bottom + 10 + idx * 30
                screen.blit(font_render, rect)
            # ----展示头像
            screen.blit(id_image, (left + 10, bottom + 10))
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
    '''仙女和勇士对话'''
    def showconversationheroandfairy(self, screen, scenes):
        # 对话框指针
        conversation_pointer = 0
        # 定义所有对话
        if self.hero.has_cross:
            conversations = [
                ['Fairy, I have found the cross.'],
                ['You did a great job. Now I will start to give you', 'stronger power! Mi La Do Mi Beep...', 'Well, I have improved your current abilities!', 'Remember: If you don not have enough strength,', 'Do not go to the 21st floor. On that floor,', 'The mana of all your treasures will become useless.']
            ]
            self.hero.has_cross = False
            self.hero.life_value = int(self.hero.life_value * 4 / 3)
            self.hero.attack_power = int(self.hero.attack_power * 4 / 3)
            self.hero.defense_power = int(self.hero.defense_power * 4 / 3)
        else:
            conversations = [
                ['......'], 
                ['You woke up!'], 
                ['......', 'Who are you? Where am I?'],
                ['I am the fairy here, Just now you were', 'The monster was stunned.'],
                ['......', 'Sword, sword, where is my sword?'],
                ['Your sword was taken away by them. I only had time to', 'Rescue you.'],
                ['So, where is the princess? I am here to save her.'],
                ['The princess is still inside. You can not kill her if you go in like this.', 'The little monsters inside.'],
                ['What should I do? I promised the King I would', 'rescue the princess. What should I do now?'],
                ['Don\'t worry, I will lend you my power, and you', 'will be able to defeat those small monsters. However, you', 'must first help me find something. Find it', 'and then come back here to find me.'],
                ['Find something? Find what?'],
                ['It\'s a cross with a red gem in the middle.'],
                ['What\'s the use of that thing?'],
                ['I was originally the guardian of this tower, but not long ago,', 'a group of demons came from the north. They occupied', 'this tower and sealed my magic power inside this', 'cross. If you can bring it out of the', 'tower, my magic power will slowly recover,', 'and then I can lend you my power to', 'rescue the princess. Remember, only with my magic', 'can you open the door on the twenty-first floor.'],
                ['......', 'Alright, I\'ll give it a try.'],
                ['I just checked, your sword is on the third', 'floor, your shield is on the fifth floor, and that cross', 'is on the seventh floor. To reach the seventh floor, you must', 'first retrieve your sword and shield. Additionally, on other', 'floors of the tower, there are some swords and treasures', 'that have been stored for hundreds of years. If you obtain them,', 'they will be of great help in dealing with the monsters here.'],
                ['But how do I get in?'],
                ['I have three keys here; take them first. There', 'are many more such keys inside the tower, so you must', 'use them wisely. Go forth bravely, warrior!']
            ]
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        conversation_pointer += 1
                        if conversation_pointer >= len(conversations): return
            # --画对话框
            conversation = conversations[conversation_pointer]
            # ----勇士
            if conversation_pointer % 2 == 0:
                left, top, width, height = 510, 430, 8, 2
                pygame.draw.rect(screen, (199, 97, 20), (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
                id_image = self.hero.images['down']
            # ----仙子
            else:
                left, top, width, height = 300, 250, 8, 2
                if len(conversation) > 3: height = 3
                if len(conversation) > 5: height = 4
                if len(conversation) > 7: height = 5
                pygame.draw.rect(screen, (199, 97, 20), (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
                id_image = self.resource_loader.images['mapelements']['24'][0]
            # ----底色
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
            # ----左上角图标
            screen.blit(id_image, (left + 10, top + 10))
            # ----对话框中的文字
            for idx, text in enumerate(conversation):
                font_render = font.render(text, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + self.cfg.BLOCKSIZE + 40, top + 10 + idx * 30
                screen.blit(font_render, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)