import pygame, sys, json, os, time, random

from win32api import GetSystemMetrics


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100,-16, 2, 512)
pygame.init()

screen_info = pygame.display.Info()
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Galactic Cruiser')
misha = pygame.image.load("Assets/misha.png").convert_alpha()
pygame.display.set_icon(misha)
clock = pygame.time.Clock()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.speed = 600
        self.image = pygame.Surface((int(screen_width//22), int(screen_height//120)))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center =(x, y))
        self.direction = direction
        # self.shoot_cooldown = 0
    def update(self):
        baller = random.randint(1, 4)
        self.rect.x += (self.direction*self.speed*dt) 
        if self.rect.left > screen_width:
            self.kill()
        if baller > 1:
            if pygame.sprite.spritecollide(self, meteori_group, True):
                
                self.kill()
        else:
            if pygame.sprite.spritecollide(self, meteori_group, False):
                
                self.kill()

bullet_group = pygame.sprite.Group()

class meteori(pygame.sprite.Sprite):
    
    def __init__(self, x, y, one_rect, two_rect= None):
        super().__init__()
        self.speed = random.randint(300, 1500)
        self.image = pygame.image.load("Assets/rock.png").convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))
        self.health = 3
        self.point = 0
        self.one = one_rect
        self.two = two_rect
        self.check_one = False
        self.check_two = False

    def update(self):
        self.check_collision()
        self.rect.x -= (self.speed * dt)
        if self.rect.right < 0:
            self.kill()

    def check_collision(self):
        if pygame.sprite.spritecollide(self, bullet_group, True):
            # self.health -= 1
            # if self.health == 0:
            
            self.kill()
            self.point = 100
        if pygame.sprite.spritecollide(self, playone_group, True):
            
            self.kill()
        if pygame.sprite.spritecollide(self, playtwo_group, True):
            self.kill()

        return self.point

    
    def player_collision(self):
        if self.rect.collidepoint(self.one):
            self.check_one = True
        if self.two != None:
            if self.rect.collidepoint(self.two):
                self.check_two = True
        
        return self.check_one, self.check_two
            

class PlayerOne(pygame.sprite.Sprite):
    def __init__(self, mete, x, y):
        super().__init__()
        self.image = pygame.Surface((int(screen_width*0.1091), int(screen_height*0.2)))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 3
        self.group = mete
        self.velocity = 400
        self.ball = True
        
    def update(self):
        self.collide()
        self.move()
    
    def move(self):
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_UP]:
            self.rect.y -= (self.velocity * dt)
        if keys[pygame.K_DOWN]:
            self.rect.y +=(self.velocity * dt)
        if keys[pygame.K_LEFT]:
            self.rect.x -= (self.velocity * dt)
        if keys[pygame.K_RIGHT]:
            self.rect.x += (self.velocity * dt)
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right>= screen_width:
            self.rect.right = screen_width
        
    def collide(self):
        if pygame.sprite.spritecollide(self, meteori_group, False):
            self.health -= 1
            self.kill()
        # if self.health == 0:
        #     self.kill()

playone_group = pygame.sprite.Group()

x = 0
y = 0
meteori_group = pygame.sprite.Group()

class PlayerTwo(pygame.sprite.Sprite):
    def __init__(self, mete, x, y):
        super().__init__()
        self.image = pygame.Surface((int(screen_width*0.1091), int(screen_height*0.2)))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 3
        self.group = mete
        
    def update(self):
        self.collide()
        self.move()
    
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.rect.y += -400 * dt
        if keys[pygame.K_s]:
            self.rect.y += 400 * dt
        if keys[pygame.K_a]:
            self.rect.x += -400 * dt
        if keys[pygame.K_d]:
            self.rect.x += 400 * dt

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right>= screen_width:
            self.rect.right = screen_width
        

        
    def collide(self):
        if pygame.sprite.spritecollide(self, meteori_group, False):
            self.health -= 1
            self.kill()

playtwo_group = pygame.sprite.Group()

ballin = 1
hit1, hit2 = False, False
health = 3
cooldown = 0
point = 0
def DisplayScore():
    
    current_time = int((pygame.time.get_ticks() - start_time)//10*ballin)
    time_surface = menu_font.render(str(current_time), True, 'White')
    time_rect = time_surface.get_rect(center=(int(screen_width*0.225)+int(screen_width//2.7),int(screen_height//12)))
    score_surface = menu_font.render("Score:", True, 'White')
    score_rect = score_surface.get_rect(midleft=(int(screen_width//110)+int(screen_width//2.7), int(screen_height//12)))
    screen.blit(time_surface, time_rect)
    screen.blit(score_surface, score_rect)
    return current_time


Volume = {
    'sfx': 5,
    'music' : 5
}

with open('soundsv.txt') as check_volume:
    Volume = json.load(check_volume)

levels_completed = {
    'one' : False,
    'two' : False,
    'three' : False,
    'four' : False
}

# with open('level_complete.txt') as check_level:
#     levels_completed = json.load(check_level)



music_volume = Volume['music']
sfx_volume = Volume['sfx']

background = pygame.image.load('Assets/Background.png').convert_alpha()
back_surf = background.get_rect(topleft=(0,0))

cross = pygame.image.load('Assets/cross.png').convert_alpha()

back_sign = pygame.image.load('Assets/backsign.png').convert_alpha()

logo = pygame.image.load('Assets/loaf studio logo.png').convert_alpha()
balls = pygame.image.load('Assets/balls.jpg').convert_alpha()

play_one = pygame.image.load('Assets/spase.png').convert_alpha()
play_two = pygame.image.load('Assets/spacesgio.png').convert_alpha()

logo_font = pygame.font.Font('Assets/Gugi-Regular.ttf', 100)
menu_font = pygame.font.Font('Assets/IBMPlexSans-Medium.ttf', 50)
change_font = pygame.font.Font('Assets/IBMPlexSans-Medium.ttf', 75)

die = True

start_surf = menu_font.render('Start Game', True, 'White')

setting_surf = menu_font.render('Settings', True, 'White')

level_surf = menu_font.render('Levels', True, 'White')

credit_surf = menu_font.render('Credits', True, 'White')

logo_surface = logo_font.render('Galactic Cruiser', True, 'White')

uami_surf = menu_font.render('Uami', True, 'White')

loafy_surf = menu_font.render('Loaf', True, 'White')

prog_sound_surf = menu_font.render('Programmer & Sound Designer...', True, 'White')

artist_surf = menu_font.render('Artist...', True, 'White')

fan_mention = menu_font.render('And all of our fans...', True, 'White')

music_surface = menu_font.render('Music Volume', True, 'White')

sfx_surf = menu_font.render('SFX Volume', True, 'White')

mus_vol_surf = menu_font.render(str(int(music_volume//10)), True, 'White')

sfx_vol_surf = menu_font.render(str(int(sfx_volume//10)), True, 'White')

plus_surf = change_font.render('+', True, 'White')

minus_surf = change_font.render('-', True, 'White')

level_one = logo_font.render('1', True, 'White')
level_two = logo_font.render('2', True, 'White')
level_three = logo_font.render('3', True, 'White')
level_four = logo_font.render('4', True, 'White')

Quit_surf = menu_font.render('Quit The Level?', True, 'White')
select_surf = menu_font.render('Two Player Mode?', True, 'White')
yes_surf = menu_font.render('Yes', True, 'White')
no_surf = menu_font.render('No', True, 'White')




background = pygame.transform.scale(background, (screen_width, screen_height))
logo = pygame.transform.scale(logo, (screen_width, screen_height))
play_one = pygame.transform.scale(play_one, (screen_width * 0.1091, screen_height*0.2))
play_two = pygame.transform.scale(play_two, (screen_width * 0.1091, screen_height*0.2))

Quit_rect = Quit_surf.get_rect(topleft=(int(screen_width*0.34545455), int(screen_height//4)))
select_rect = select_surf.get_rect(topleft=(int(screen_width//22)*8, int(screen_height*0.3)))
yes_rect = yes_surf.get_rect(topleft=(int(screen_width//55)*21, int(screen_height//2)))
no_rect = no_surf.get_rect(topleft=(int(screen_width//11)*6, int(screen_height//2)))
level_rect = level_surf.get_rect(midtop=(int(screen_width//2), int(screen_height*0.02)))
level_one_rect = level_one.get_rect(topleft=(int(screen_width*0.2), int(screen_height*0.4)))
level_two_rect = level_two.get_rect(topleft=(int(screen_width*0.4), int(screen_height*0.4)))
level_three_rect = level_three.get_rect(topleft=(int(screen_width*0.6), int(screen_height*0.4)))
level_four_rect = level_four.get_rect(topleft=(int(screen_width*0.8), int(screen_height*0.4)))
fan_mention_rect = fan_mention.get_rect(topleft=(int(screen_width//22), int(screen_height*0.55)))
minus_rect_one = minus_surf.get_rect(topleft=((int(screen_width * 0.7727273)), int(screen_height*0.22)))
minus_rect_two = minus_surf.get_rect(topleft=((int(screen_width*0.7727273)), int(screen_height*0.35)))
uami_rect = uami_surf.get_rect(topleft=((int(screen_width * 0.818181818182)), int(screen_height*0.25)))
loafy_rect = loafy_surf.get_rect(topleft=((int(screen_width*0.8227273)), int(screen_height*0.4)))
credit_rect = credit_surf.get_rect(midtop=(int(screen_width//2), int(screen_height*0.625)))
plus_rect_one = plus_surf.get_rect(topleft=((int(screen_width * 0.8686364)), int(screen_height*0.22)))
plus_rect_two = plus_surf.get_rect(topleft=((int(screen_width*0.8686364)), int(screen_height*0.35)))
sfx_vol_rect = sfx_vol_surf.get_rect(topleft=((int(screen_width*0.955)-150), int(screen_height*0.38)))
prog_sound_rect = prog_sound_surf.get_rect(topleft=(int(screen_width//22), int(screen_height*0.25)))
logo_rect = logo_surface.get_rect(midtop=(int(screen_width//2), int(screen_height//12)))
backs_rect = back_sign.get_rect(topleft=(int(screen_width*0.025), int(screen_height//24)))
sfx_rect = sfx_surf.get_rect(topleft=(int(screen_width//22), int(screen_height*0.4)))
mus_vol_rect = mus_vol_surf.get_rect(topleft=((int(screen_width * 0.8186364)), int(screen_height*0.25)))
balls_rect = balls.get_rect(center=(screen_width/2, screen_height/2))
cross_rect = cross.get_rect(topleft=(int(screen_width*0.925), int(screen_height//24)))
start_rect = start_surf.get_rect(midtop=(int(screen_width//2), int(screen_height*0.375)))
music_rect = music_surface.get_rect(topleft=(int(screen_width//22), int(screen_height*0.25)))
artist_rect = artist_surf.get_rect(topleft=(int(screen_width//22), int(screen_height*0.4)))
setting_rect = setting_surf.get_rect(midtop=(int(screen_width//2), int(screen_height*0.5)))

player_one = play_one.get_rect(topleft=(int(screen_width//22), int(screen_height*0.2)))
player_two = play_two.get_rect(topleft=(int(screen_width//22), int(screen_height*0.5)))

Fullscreen = False



logo_mode = True
start_mode = False
setting_mode = False
credits_mode = False
level_select_mode = False
level_one_mode = False
level_two_mode = False
level_three_mode = False
level_four_mode = False
escape_mode = False
select_platers = False
endless_mode = False
end_mode = False


menu_timer = pygame.USEREVENT + 1
pygame.time.set_timer(menu_timer, 1000)

metoer_timer_1 = pygame.USEREVENT + 2
pygame.time.set_timer(metoer_timer_1, 500)

metoer_timer_2 = pygame.USEREVENT + 3
pygame.time.set_timer(metoer_timer_1, 750)

metoer_timer_3 = pygame.USEREVENT + 4
pygame.time.set_timer(metoer_timer_1, 1000)

metoer_timer_4 = pygame.USEREVENT + 5
pygame.time.set_timer(metoer_timer_1, 400)

mamamam = pygame.USEREVENT + 6
pygame.time.set_timer(mamamam, 60000)

previous_time = time.time()
screen_movement = 0
backspeed = 800
previous_state = ''

one_x = 0
one_y = 0

two_x = 0
two_y = 0

to_menu = True
to_level = False
two_mode = False
selected = False
Value =1 
start_time = 0
shoot = True

while True:
    
    music_volume = Volume['music']
    sfx_volume = Volume['sfx']
    dt = time.time() - previous_time
    previous_time = time.time()
    
    pygame.mixer.music.set_volume(music_volume)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('level_complete.txt','w') as check_level:
                json.dump(levels_completed, check_level)
            with open('soundsv.txt', 'w') as check_volume:
                json.dump(Volume, check_volume)

            pygame.quit()
            sys.exit()
        
                
                
        if logo_mode:
            screen.fill((86,31,1))
            screen.blit(logo, (0,0))
            if event.type == menu_timer:
                start_mode = True
                logo_mode = False
        elif start_mode:
            screen.fill('Black')
            screen.blit(background, back_surf)
            screen.blit(logo_surface, logo_rect)
            screen.blit(start_surf, start_rect)
            screen.blit(setting_surf, setting_rect)
            screen.blit(credit_surf, credit_rect)
            screen.blit(cross, cross_rect)

            pos = pygame.mouse.get_pos()
            if cross_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    with open('level_complete.txt','w') as check_level:
                        json.dump(levels_completed, check_level)
                    with open('soundsv.txt', 'w') as check_volume:
                        json.dump(Volume, check_volume)

                    pygame.quit()
                    sys.exit()
            elif logo_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Balls")
            elif start_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_mode = False
                    select_platers = True
                    
            elif setting_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_mode = False
                    setting_mode = True
            elif credit_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_mode = False
                    credits_mode = True
            
            
        elif select_platers:
            pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, 'Black', pygame.Rect(int((screen_width*0.5)//2), ((screen_height*0.5)//2), int(screen_width*0.5), int(screen_height*0.5)))
            screen.blit(select_surf, select_rect)
            screen.blit(yes_surf, yes_rect)
            screen.blit(no_surf, no_rect)
            if yes_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    two_mode = True
                    selected = True
                    Value = 2

            if no_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    two_mode = False
                    selected =  True
                    Value = 1

            if selected:
                endless_mode = True
                select_platers = False
                selected = False
                to_level = True
                start_time = pygame.time.get_ticks()

        elif setting_mode:
            pos = pygame.mouse.get_pos()
            sfx_vol_surf = menu_font.render(str(int(sfx_volume)), True, 'White')
            mus_vol_surf = menu_font.render(str(int(music_volume)), True, 'White')
            screen.fill("Black")
            screen.blit(background, back_surf)
            screen.blit(setting_surf, (int(screen_width*0.409091),int(screen_height//12)))
            screen.blit(back_sign, backs_rect)
            screen.blit(music_surface, music_rect)
            
            screen.blit(mus_vol_surf, mus_vol_rect)
            
            screen.blit(plus_surf, plus_rect_one)
            
            screen.blit(minus_surf, minus_rect_one)
            
            if backs_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_mode = True
                    setting_mode = False
            elif plus_rect_one.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if music_volume<10:
                        music_volume += 1
            elif plus_rect_two.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sfx_volume<10:
                        sfx_volume += 1
            elif minus_rect_one.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if music_volume > 0:
                        music_volume -= 1
            elif minus_rect_two.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sfx_volume>0:
                        sfx_volume -= 1
            Volume['music'] = music_volume
            Volume['sfx'] = sfx_volume
            

        elif credits_mode:
            pos = pygame.mouse.get_pos()
            screen.fill("Black")
            screen.blit(background, back_surf)
            screen.blit(credit_surf, (int(screen_width*0.40909091),int(screen_height//12)))
            screen.blit(back_sign, backs_rect)
            screen.blit(prog_sound_surf, prog_sound_rect)
            screen.blit(artist_surf, artist_rect)
            screen.blit(uami_surf, uami_rect)
            screen.blit(loafy_surf, loafy_rect)
            screen.blit(fan_mention, fan_mention_rect)
            screen.blit(loafy_surf, (int(screen_width*0.823182), int(screen_height*0.55)))
            if backs_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_mode = True
                    credits_mode = False

        # elif level_select_mode:
        #     pos = pygame.mouse.get_pos()
        #     screen.fill("Black")
        #     screen.blit(background, back_surf)
        #     screen.blit(back_sign, backs_rect)
        #     screen.blit(level_surf, level_rect)
        #     screen.blit(level_one, level_one_rect)
        #     if levels_completed['one']:
        #         screen.blit(level_two, level_two_rect)
        #     if levels_completed['two']:
        #         screen.blit(level_three, level_three_rect)
        #     if levels_completed['three']:
        #         screen.blit(level_four, level_four_rect)

        #     if backs_rect.collidepoint(pos):
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             start_mode = True
        #             level_select_mode = False
        #     elif level_one_rect.collidepoint(pos):
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             level_one_mode = True
        #             level_select_mode = False
        #             to_level = True
        #     elif level_two_rect.collidepoint(pos):
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             if levels_completed['one']:
        #                 level_two_mode = True
        #                 level_select_mode = False
        #                 to_level = True
        #     elif level_three_rect.collidepoint(pos):
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             if levels_completed['two']:
        #                 level_three_mode = True
        #                 level_select_mode = False
        #                 to_level = True
        #     elif level_four_rect.collidepoint(pos):
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             if levels_completed['three']:
        #                 level_four_mode = True
        #                 level_select_mode = False
        #                 to_level = True
            

        # elif level_one_mode:
        #     pos = pygame.mouse.get_pos()
            

        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             level_one_mode = False
        #             escape_mode = True
        #             previous_state = '1'
            
            
            
        # elif level_two_mode:
        #     pos = pygame.mouse.get_pos()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             level_two_mode = False
        #             escape_mode = True
        #             previous_state = '2'

        # elif level_three_mode:
        #     pos = pygame.mouse.get_pos()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             level_three_mode = False
        #             escape_mode = True
        #             previous_state = '3'

        # elif level_four_mode:
        #     pos = pygame.mouse.get_pos()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             level_four_mode = False
        #             escape_mode = True
        #             previous_state = '4'

        elif endless_mode:
            choiceslist = [screen_height*0.1,screen_height*0.25, screen_height*0.55, screen_height*0.8, screen_height*0.9]
            
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    endless_mode = False
                    escape_mode = True

            if event.type == metoer_timer_1:
                y = random.choice(choiceslist)
                if play_two:
                    mete = meteori(screen_width*1.3, y, play_one, play_two)
                else:
                    mete = meteori(screen_width*1.3, y, play_one)
                meteori_group.add(mete)
                point += mete.check_collision()
            if event.type == metoer_timer_2:
                y = random.choice(choiceslist)
                if play_two:
                    mete = meteori(screen_width*1.3, y, play_one, play_two)
                else:
                    mete = meteori(screen_width*1.3, y, play_one)
                meteori_group.add(mete)
                point += mete.check_collision()
            if event.type == metoer_timer_3:
                y = random.choice(choiceslist)
                if play_two:
                    mete = meteori(screen_width*1.3, y, play_one, play_two)
                else:
                    mete = meteori(screen_width*1.3, y, play_one)
                meteori_group.add(mete)
                point += mete.check_collision()
            if event.type == metoer_timer_4:
                y = random.choice(choiceslist)
                if play_two:
                    mete = meteori(screen_width*1.3, y, play_one, play_two)
                else:
                    mete = meteori(screen_width*1.3, y, play_one)
            if event.type == mamamam:
                ballin += 1

        elif escape_mode:
            pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, 'Black', pygame.Rect(int((screen_width*0.5)//2), ((screen_height*0.5)//2), int(screen_width*0.5), int(screen_height*0.5)))
            screen.blit(Quit_surf, Quit_rect)
            screen.blit(yes_surf, yes_rect)
            screen.blit(no_surf, no_rect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # if previous_state == '1':
                    #     level_one_mode = True
                    # elif previous_state == '2':
                    #     level_two_mode = True
                    # elif previous_state == '3':
                    #     level_three_mode = True
                    # elif previous_state == '4':
                    #     level_four_mode = True

                    endless_mode = True
                    escape_mode = False

            if yes_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if previous_state == '1':
                    #     level_one_mode = False
                    # elif previous_state == '2':
                    #     level_two_mode = False
                    # elif previous_state == '3':
                    #     level_three_mode = False
                    # elif previous_state == '4':
                    #     level_four_mode = False
                    escape_mode = False
                    start_mode = True
                    to_menu = True
            elif no_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if previous_state == '1':
                    #     level_one_mode = True
                    # elif previous_state == '2':
                    #     level_two_mode = True
                    # elif previous_state == '3':
                    #     level_three_mode = True
                    # elif previous_state == '4':
                    #     level_four_mode = True
                    endless_mode = True
                    escape_mode = False
            
        elif end_mode:
            pos = pygame.mouse.get_pos()
            screen.fill("Black")
            screen.blit(background, back_surf)
            screen.blit(back_sign, backs_rect)
            screen.blit(logo_surface, logo_rect)
            score_surface = menu_font.render('Score:     ' + str(score), True, 'White')
            score_rect = score_surface.get_rect(midbottom=(int(screen_width//2), int(screen_height//2)))
            screen.blit(score_surface, score_rect)
            if backs_rect.collidepoint(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    end_mode = False
                    start_mode = True

    if endless_mode:
        
        if to_level:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('Assets/Battle muse.wav')
            pygame.mixer.music.set_volume(music_volume/10)
            pygame.mixer.music.play(-1)
            player_one = play_one.get_rect(topleft=(int(screen_width//22), int(screen_height*0.2)))
            player_two = play_two.get_rect(topleft=(int(screen_width//22), int(screen_height*0.5)))
            meteori_group = pygame.sprite.Group()
            health = 3
            health_two = 3
            bullet_group = pygame.sprite.Group()
            playone_group = pygame.sprite.Group()
            number = PlayerOne(meteori_group,int(screen_width//22), int(screen_height*0.2))
            playone_group.add(number)
            bum = PlayerTwo(meteori_group, int(screen_width//22), int(screen_height*0.5))
            playtwo_group.add(bum)
            to_level = False

        screen.fill('Black')
        screen.blit(background, (screen_movement, 0))
        screen.blit(background, (screen_width+screen_movement, 0))
        if screen_movement <= -screen_width:
            screen.blit(background, (screen_width+screen_movement, 0))
            screen_movement = 0
        screen_movement -= backspeed * dt
        
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            one_y = -400
        if keys[pygame.K_DOWN]:
            one_y = 400
        if keys[pygame.K_LEFT]:
            one_x = -400
        if keys[pygame.K_RIGHT]:
            one_x = 400
        if keys[pygame.K_w]:
            two_y = -400
        if keys[pygame.K_s]:
            two_y = 400
        if keys[pygame.K_a]:
            two_x = -400
        if keys[pygame.K_d]:
            two_x = 400
        # if keys[pygame.K_c]:
        #     shoot = True

        if cooldown == 0:
            
            
            if two_mode:
                bullet2 = Bullet(player_two.centerx + (0.6*player_two.size[0]), player_two.centery, 1)
                bullet_group.add(bullet2)

        
        if cooldown > 0:
            cooldown -= 1

        player_one.y += one_y * dt
        one_y = 0
        if player_one.top <= 0:
            player_one.top = 0
        if player_one.bottom >= screen_height:
            player_one.bottom = screen_height
        

        
        player_one.x += one_x * dt
        one_x = 0
        if player_one.left <= 0:
            player_one.left = 0
        if player_one.right >= screen_width:
            player_one.right = screen_width
        

        meteori_group.update()
        bullet_group.update()
        playone_group.update()
        playtwo_group.update()
        

        
        

        if playone_group:
            
            if cooldown == 0:
                cooldown = 40
                bullet1 = Bullet(player_one.centerx + (0.6*player_one.size[0]), player_one.centery, 1)
                bullet_group.add(bullet1)
                if playtwo_group and two_mode:
                    bullet2 = Bullet(player_two.centerx + (0.6*player_two.size[0]), player_two.centery, 1)
                    bullet_group.add(bullet2)

            
            bullet_group.draw(screen)
            
            screen.blit(play_one, player_one)

        

        if (not playone_group and not two_mode) or (not playone_group and not playtwo_group):
            endless_mode = False
            end_mode = True
            to_menu = True
            pygame.mixer.music.fadeout(2000)
        elif not playone_group and two_mode:
            if die:
                bullet_group = pygame.sprite.Group()
                die = False
            if cooldown == 0:
                cooldown = 40
                bullet2 = Bullet(player_two.centerx + (0.6*player_two.size[0]), player_two.centery, 1)
                bullet_group.add(bullet2)
            bullet_group.draw(screen)
        
        elif not playtwo_group and playone_group:
            if die:
                bullet_group = pygame.sprite.Group()
                die = False
            

        if two_mode:
            player_two.y += two_y * dt
            two_y = 0
            if player_two.top <= 0:
                player_two.top = 0
            if player_two.bottom >= screen_height:
                player_two.bottom = screen_height

            player_two.x += two_x * dt
            two_x = 0
            if player_two.left <= 0:
                player_two.left = 0
            if player_two.right >= screen_width:
                player_two.right = screen_width
            if playtwo_group:
                
                screen.blit(play_two, player_two)
        meteori_group.draw(screen)
        score = DisplayScore()
        
            
    else:
        if to_menu:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('Assets/Menu.wav')
            pygame.mixer.music.set_volume(music_volume/10)
            pygame.mixer.music.play(-1)
            to_menu = False

    
    pygame.display.update()
    clock.tick(60)