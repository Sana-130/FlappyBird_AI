import pygame
import nueral_network as nt
import numpy as np

bird_width=35
bird_height=29

bird1=pygame.image.load('bird1.png')
bird2=pygame.image.load('bird2.png')
bird3=pygame.image.load('bird3.png')
bird4=pygame.transform.scale(bird1, (bird_width, bird_height))
bird4_1=pygame.transform.rotate(bird4,180)
bird_images=[pygame.transform.scale(bird1, (bird_width, bird_height)) , pygame.transform.scale(bird2, (bird_width, bird_height))  , pygame.transform.scale(bird3, (bird_width, bird_height))]
pipe_dist = 250
width = 660
height = 500
pipe_gap = 120

clear_point = 22

screen = pygame.display.set_mode((width, height))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, screen , brain):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.img_list = bird_images
        self.screen = screen #pygame.display.set_mode((width, height))
        self.update_time=pygame.time.get_ticks()
        self.index=0
        self.image=self.img_list[self.index]
        self.fall_img=bird4_1
        self.rect=self.image.get_rect()
        self.vel=0
        self.rect.center=[x,y]
        self.mask=pygame.mask.from_surface(self.image)
        self.collided= False
        self.collision=False
        self.count_pipe= 0
        self.score=0
        self.cls_dist=0.0
        #self.brain= nt.NueralNetwork(4, 6, 1)
        self.fitness=0
        self.inputs=[]
        if brain:
            self.brain = brain
        else:
            self.brain = nt.NueralNetwork(3, 6, 1)

    def free_fly(self):
        animate_break=100
        self.image= self.img_list[self.index]
        if pygame.time.get_ticks()-self.update_time >= animate_break:
            self.update_time=pygame.time.get_ticks()
            self.index+=1

        if self.index>=len(self.img_list):
            self.index=0

    def update(self):
        
        self.vel+=0.2
        if self.vel > 9:
            self.vel = 9

        if self.rect.bottom < height:
            self.rect.y +=int(self.vel)  

        if self.rect.bottom >= height or self.rect.top <=0:
            self.collided= True  

        if self.collided==False:   
            #else:
            #    self.image=self.img_list[0]       
                animate_break=100
                self.image= self.img_list[self.index]
                self.image= pygame.transform.rotate(self.img_list[self.index], self.vel * -5)
                if pygame.time.get_ticks()-self.update_time >= animate_break:
                    self.update_time=pygame.time.get_ticks()
                    self.index+=1
        
                if self.index>=len(self.img_list):
                    self.index=0 
        else:
            
            self.image=pygame.transform.rotate(self.img_list[self.index], -90)
        
    def jumb(self):
        if (self.rect.top  > 35):
            self.vel=-5

    def fall_down(self):
        self.vel+=10
        
    def check_score(self, pipe):
        
        inside=False
       
        #pipe_group.sprites()[0]
        #print(bird.rect.left, '>', pipe.rect.left, self.rect.right, '<', pipe.rect.right)
        
        if self.rect.left > pipe.rect.left and self.rect.right < pipe.rect.right+1 and inside==False:
            inside=True
        if inside==True:
            if self.rect.right >= pipe.rect.right and self.collided==False:
                self.score+=1
                inside=False 

                #print("scoreee", self.score)
    
    def activate(self, pipes):

        top_pipe = pipes[0]
        btm_pipe = pipes[1]

        #horizontal top
        horizontal_dist= (top_pipe.rect.left - self.rect.right )/width #self.rect.left
        horizontal_dist2=(top_pipe.rect.right - self.rect.left)/width
        vertical_dist = (self.rect.top - top_pipe.rect.bottom)/height
        vertical_dist2=(self.rect.bottom - btm_pipe.rect.top)/height
        y_val = self.vel / height
        y_point= self.rect.y/height
        vertical_gap_dist = (top_pipe.rect.bottom + (pipe_gap/2) - self.rect.bottom)/height  
        upper_wall_dist=self.rect.top/height
        btm_wall_dist=self.rect.bottom-height/height

        '''
        horizontal_distance = (top_pipe.rect.left - self.rect.right) / width

        hor_dist=(top_pipe.rect.right - self.rect.right)/width
        
        #vertical top distance
        vert_dist =(self.rect.top - top_pipe.rect.bottom)/height
        vertical_distance = (btm_pipe.rect.top - self.rect.bottom ) / height

        y_vel = self.vel / 9
        y_point = self.rect.y / height
'''
        #if self.inputs == '':
        #self.inputs=[horizontal_distance, vertical_distance, y_vel , y_point, vert_dist, hor_dist]
        #self.inputs = [horizontal_dist, vertical_dist, y_point]
        self.inputs=[horizontal_dist, vertical_dist,vertical_dist2]
        #else:
        #    self.inputs[0] = horizontal_distance
        #    self.inputs[1] = vertical_distance
        #    self.inputs[2] = x_point
        #    self.inputs[3] = y_point

        output = self.brain.feedforward(self.inputs)
        self.decide(output)
        
    def decide(self, output):
        
        if output > 0.5:
            self.jumb()
       
        else:
            pass
        
    def check_dist(self, cls_pipe):
        
        dist = cls_pipe.rect.left - self.rect.right
        dist2 = cls_pipe.rect.right - self.rect.right
        #print(dist2)
        end_range = 248
        #end_range2=pipe_dist-62
        end_range2 = pipe_dist - clear_point
        #print(dist)
        if(dist2 >=0 and dist2 <= end_range2): #-2
            self.cls_dist = (end_range2-dist2)/end_range2
            #print("cls", self.cls_dist)
    