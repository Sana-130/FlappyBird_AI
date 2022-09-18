from asyncio.windows_utils import pipe
import bird as bd
import settings as val
import genetic_a as ga
import pygame
import random
import pickle

pygame.init()

Gener = 0
width = 660
height = 500
pipe_width = 60
is_stop=False
pipe_move_acc= 2000
last_pipe=pygame.time.get_ticks() - pipe_move_acc

updatetime=pygame.time.get_ticks()
gamestart=False

score_board_x=330
score_board_y=15
white=(255, 255, 255)
black=(0,0,0)
screen = pygame.display.set_mode((width, height))
bg_image = pygame.image.load('images/background.png')
pip_image = pygame.image.load('images/pipe.png')

space_btw_pipes=  100 #120 #170 #150 (110-clearpoint-24) (100 - clearpoint - 26) 
pipe_max_height = 300 #250 200
pipe_least_height = 60 #150 #100 #80

pip_image = pygame.transform.scale(pip_image, (pipe_width, 310))
up_pip_image = pygame.transform.rotate(pip_image, 180)
bg_image = pygame.transform.scale(bg_image, (width, height))

clear_point = 28
pygame.display.set_caption('the race')
font= pygame.font.Font('freesansbold.ttf', 25)

clock = pygame.time.Clock()

pipe_speed=-1.1
pipe_dist=250

bestBird = None

class Pipes(pygame.sprite.Sprite):
    def __init__(self, x , y,  i , pos):
        #pygame.sprite.Sprite.__init__(self)
        super().__init__()   
        self.i=i
        self.x= x
        self.pos=pos
        self.cut_off= False
        
        if pos==0:
            self.y= y
            self.image = pygame.transform.scale(up_pip_image, (pipe_width, self.y))
            self.rect= self.image.get_rect()
            self.rect.bottomleft=[self.x, self.y]
    
        elif pos==1:
            self.y= y + space_btw_pipes
            self.image =  pygame.transform.scale(pip_image, (pipe_width, height-self.y))
            self.rect= self.image.get_rect()
            self.rect.topleft=[self.x, self.y]
        

    def update(self): 
        self.rect.right = self.rect.right + pipe_speed 
        if self.rect.right < 0:
            pipe_group.remove(self)
      
    
    def off_screen(self):
        if self.rect.left <=1 and self.cut_off==False:         
            self.cut_off=True
            return True
        else:
            return False

def load_birdbrain(bird):
    file = open('save', 'rb')
    brain = pickle.load(file)
    bird.brain=brain
    file.close()


bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()

bird =bd.Bird(200, 200, False)
load_birdbrain(bird)
bird_group.add(bird)

        
def draw_pipe():
    pipe_group.draw(screen)

def move_pipe():
    pipe_group.update()
   
    
def create_pipe():
    for i in range(4, 8):
        r=random.randint(pipe_least_height, pipe_max_height)
        t=i*pipe_dist
        up_pipe=Pipes(t, r , i, 0)
        down_pipe=Pipes(t, r, i, 1)
        pipe_group.add(up_pipe, down_pipe)


def check_pipes(): 
    global last_pipe
    
    if pipe_group.sprites()[0].off_screen():
        i=4
        r=random.randint(pipe_least_height, pipe_max_height)
        t=i*pipe_dist
        up_pipe=Pipes(t, r , i, 0)
        down_pipe=Pipes(t, r, i, 1)
        pipe_group.add(up_pipe, down_pipe)
        pass


create_pipe()


current_pipe= object
samp_birds = object
pipes= object

    
def set_values():
    global current_pipe, samp_birds, pipes

    current_pipe = pipe_group.sprites()[0]
    samp_birds = bird_group.sprites()[0]
    pipes=[pipe_group.sprites()[0], pipe_group.sprites()[1]]



set_values()  

run = True 
called=False
while run:
    screen.blit(bg_image,(0,0))
    draw_pipe()
    bird_group.draw(screen)
    
        
    bird_group.update()
    for bird in bird_group:
        bird.check_score(current_pipe)
        bird.check_dist(current_pipe)
        bird.activate(pipes)
        if bird.collided :
            #bird_array.append(bird)
            bird_group.remove(bird)
        if gamestart==False and bird.collided==False:
            bird.free_fly()
        
    if gamestart==True:   
        check_pipes()
        move_pipe()

    if samp_birds!='' and current_pipe!='':
        if samp_birds.rect.left < current_pipe.rect.right and samp_birds.rect.right == current_pipe.rect.right+ clear_point:
            current_pipe = pipe_group.sprites()[2]
            pipes = [pipe_group.sprites()[2], pipe_group.sprites()[3]]
      

    text= font.render(f' Score {str(bird.score)}', True, white, black)
    textrect=text.get_rect()
    textrect.center=(score_board_x, score_board_y)
    screen.blit(text, textrect)
    pygame.display.update()
    clock.tick(60) 
    
    gamestart=True
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            #save_bestbird()  
            run = False
            pygame.quit()

        if event.type==pygame.KEYDOWN:
           pass
            
     
    