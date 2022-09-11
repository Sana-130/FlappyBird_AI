from asyncio.windows_utils import pipe
import bird as bd
import settings as val
import genetic_a as ga
import pygame
import random

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
bg_image = pygame.image.load('background.png')
pip_image = pygame.image.load('pipe.png')

space_btw_pipes=  120 #170 #150
pipe_max_height = 300 #250 200
pipe_least_height = 60 #150 #100 #80

pip_image = pygame.transform.scale(pip_image, (pipe_width, 310))
up_pip_image = pygame.transform.rotate(pip_image, 180)
bg_image = pygame.transform.scale(bg_image, (width, height))

clear_point = 22
pygame.display.set_caption('the race')
font= pygame.font.Font('freesansbold.ttf', 25)

clock = pygame.time.Clock()

pipe_speed=-1.1
pipe_dist=250


class Pipes(pygame.sprite.Sprite):
    def __init__(self, x , y,  i , pos):
        #pygame.sprite.Sprite.__init__(self)
        super().__init__()   
        self.i=i
        self.x= x
        self.pos=pos
        self.cut_off= False
        #self.down_pipe_y= self.top_pipe_y + 150
        if pos=="0":
            self.y= y
            self.image = pygame.transform.scale(up_pip_image, (pipe_width, self.y))
            self.rect= self.image.get_rect()
            self.rect.bottomleft=[self.x, self.y]
    
        elif pos=="1":
            self.y= y + space_btw_pipes
            self.image =  pygame.transform.scale(pip_image, (pipe_width, height-self.y))
            self.rect= self.image.get_rect()
            self.rect.topleft=[self.x, self.y]
        

    def update(self): 
        self.rect.right = self.rect.right + pipe_speed 

        if self.rect.right < 0:
            #remove(self)
            pipe_group.remove(self)
            #print(len(pipe_group))

      
    
    def off_screen(self):
        if self.rect.left <=1 and self.cut_off==False:         
            self.cut_off=True
            return True
        else:
            return False

bird_array=[]

bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
first = False

for i in range(val.INITIAL_POPULATION):
    bird= bd.Bird(200, 200, screen , False)
    bird_group.add(bird)
    #bird_array.append(bird)

#bird_group.add(bird)
        
def draw_pipe():
    pipe_group.draw(screen)

def move_pipe():
    pipe_group.update()
   
    
def create_pipe():
    for i in range(4, 8):
        r=random.randint(pipe_least_height, pipe_max_height)
        t=i*pipe_dist
        up_pipe=Pipes(t, r , i, "0")
        down_pipe=Pipes(t, r, i, "1")
        pipe_group.add(up_pipe, down_pipe)


def check_pipes(): 
    global last_pipe
    
    if pipe_group.sprites()[0].off_screen():
        i=4
        r=random.randint(pipe_least_height, pipe_max_height)
        t=i*pipe_dist
        up_pipe=Pipes(t, r , i, "0")
        down_pipe=Pipes(t, r, i, "1")
        pipe_group.add(up_pipe, down_pipe)
        pass

def check_birds():
    for bird in bird_group:
        if bird.collided==True:
            bird_array.append(bird)
            bird_group.remove(bird)

def generate_birds(array):
    global bird
    global called
    for i in array:
        bird = i
        bird_group.add(bird)
    #bird = bd.Bird(200, 200, screen, False )
    #bird.brain.h_weights=[[-0.10392156,  0.71058073, -0.83140582, -0.05340096, -0.19602816 ,-0.34464918],
    reset_game()

def reset_game():
    global called
    for n in pipe_group:
        pipe_group.remove(n)
    create_pipe()
    set_values()
    called=False
    #create_pipe()
    pass

create_pipe()


current_pipe= object
samp_birds = object
pipes= object

def set_values():
    global current_pipe, samp_birds, pipes

    current_pipe = pipe_group.sprites()[0]
    samp_birds = bird_group.sprites()[0]
#print(samp_birds)
    pipes=[pipe_group.sprites()[0], pipe_group.sprites()[1]]
    
set_values()
    
run = True 
called=False
while run:
    screen.blit(bg_image,(0,0))
    draw_pipe()
    if first==False:
        #first_generation()
        first=True
    bird_group.draw(screen)
    check_birds()
    
    if len(bird_group)==0 and called==False:
        #for bird in bird_array:
        #    print(bird.cls_dist)
        #print(bird_array[random.randint(0,99)].cls_dist)
        #u=ga.create_population(bird_array)
        u= ga.advanced(bird_array)
        called=True
        Gener +=1
        generate_birds(u)
        bird_array=[]
        #print("the length", len(u))
        
    bird_group.update()
    for bird in bird_group:
        bird.check_score(current_pipe)
        bird.check_dist(current_pipe)
        bird.activate(pipes)
        if bird.collided :
            bird_array.append(bird)
            bird_group.remove(bird)
        if gamestart==False and bird.collided==False:
            bird.free_fly()
        
    if gamestart==True:   
        check_pipes()
        move_pipe()

    if samp_birds!='' and current_pipe!='':
        #print('hhhs',samp_birds.rect.left, current_pipe.rect.right, samp_birds.rect.right, current_pipe.rect.right)
        if samp_birds.rect.left < current_pipe.rect.right and samp_birds.rect.right == current_pipe.rect.right+ clear_point:
            current_pipe = pipe_group.sprites()[2]
            pipes = [pipe_group.sprites()[2], pipe_group.sprites()[3]]
        #print( current_pipe.x, "change")

    collided_bird = pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
    listi = list(collided_bird)
    if listi:
        for bird in listi:
            bird.collided= True
            bird_array.append(bird)
            bird_group.remove(bird)
            listi.remove(bird)
        #bird.fall_down()
        #gamestart=False
        pass

    text= font.render(f' Score {str(bird.score)} Generation {str(Gener)} ', True, white, black)
    textrect=text.get_rect()
    textrect.center=(score_board_x, score_board_y)
    screen.blit(text, textrect)
    pygame.display.update()
    clock.tick(60) 
    
    gamestart=True
    

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  
            run = False
            pygame.quit()

        if event.type==pygame.KEYDOWN:
           pass
            #if event.key==pygame.K_SPACE and bird.collided==False:
            #    bird.jumb()
     
    