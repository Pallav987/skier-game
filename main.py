import sys
import cfg
import pygame as pg
from numpy.core.defchararray import center
import random

class SkierClass(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.direction = 0
        self.imagepaths = cfg.SKIER_IMAGE_PATHS[:-1]
        self.image = pg.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320,100]
        self.speed = [self.direction,6-abs(self.direction)*2]

    def turn(self,num):
        self.direction +=num
        self.direction = max(-2,self.direction)
        self.direction = min(2,self.direction)

        center = self.rect.center
        self.image = pg.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center=center
        self.speed=[self.direction,6-abs(self.direction)*2]
        return self.speed
    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(20,self.rect.centerx)
        self.rect.centerx = min(620,self.rect.centerx)
    
    def setFall(self):
        self.image = pg.image.load(cfg.SKIER_IMAGE_PATHS[-1])
    def SetForward(self):
        self.direction =0
        self.image = pg.image.load(self.imagepaths[self.direction])

class ObstacleClass(pg.sprite.Sprite):
    def __init__(self,img_path,location,attribute):
        pg.sprite.Sprite.__init__(self)
        self.img_path = img_path
        self.image = pg.image.load(self.img_path)
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.attribute = attribute
        self.passed = False
    
    def move(self,num):
        self.rect.centery = self.location[1] - num

def createObstacles(s,e,num=10):
    obstacles = pg.sprite.Group()
    locations =[]

    for i in range(num):
        row= random.randint(s,e)
        col = random.randint(0,9)
        location = [col*64+20, row*64+20]
        if location not in locations :
            locations.append(location)
            attribute = random.choice(list(cfg.OBSTICLE_PATHS.keys()))
            img_path = cfg.OBSTICLE_PATHS[attribute]
            obstacle = ObstacleClass(img_path,location,attribute)
            obstacles.add(obstacle)

    return obstacles

def AddObstacles(obstacles0,obstacles1):
    obstacles = pg.sprite.Group()
    for obstacle in obstacles0:
        obstacles.add(obstacle)
    for obstacle in obstacles1:
        obstacles.add(obstacle)
    return obstacles

def ShowStartInterface(screen,screensize):
    screen.fill((255,255,255))
    img = pg.image.load('resources/images/back2.jpg')
    screen.blit(img,(0,0))
    tfont = pg.font.Font(cfg.FONTPATH, screensize[0]//5)
    cfont = pg.font.Font(cfg.FONTPATH,screensize[0]//20)

    title = tfont.render(u'Skier Game',True,(255,0,0))
    content = cfont.render(u'Press any key to START',True,(255,255,255))
    trect = title.get_rect()
    trect.midtop = (screensize[0]/2,screensize[1]/5)
    crect  = content.get_rect()
    crect.midtop = (screensize[0]/2,screensize[1]/2)
    screen.blit(title,trect)
    screen.blit(content,crect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN :
                return
        pg.display.update()

def showScore(screen,score, pos=(10,10)):
    font = pg.font.Font(cfg.FONTPATH,30)
    score_text = font.render('Score: %s' % score, True, (255,0,0))
    screen.blit(score_text,pos)

def updateFrame(screen,obstacles,skier,score):
    screen.fill((255,0,255))
    img = pg.image.load('resources/images/back.jpg')
    screen.blit(img,(0,0))
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    showScore(screen,score)

    pg.display.update()

def main():
    pg.init()
    pg.mixer.init()
    pg.mixer.music.load(cfg.BGMPATH)
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)

    screen = pg.display.set_mode(cfg.SCREENSIZE)
    pg.display.set_caption('Skier Game')

    ShowStartInterface(screen,cfg.SCREENSIZE)

    skier = SkierClass()
    obstacles0 = createObstacles(20,29)
    obstacles1 = createObstacles(10,19)

    obstaclesflag =0
    obstacles = AddObstacles(obstacles0,obstacles1)

    clock = pg.time.Clock()

    distance =0
    score =0
    speed=[0,6]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    speed = skier.turn(-1)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    speed = skier.turn(1)  
        skier.move()
        distance += speed[1]
        if distance >= 640 and obstaclesflag ==0:
            obstaclesflag =1
            obstacles0 = createObstacles(20,29)
            obstacles = AddObstacles(obstacles0,obstacles1)

        if distance >=1280 and obstaclesflag==1:
            obstaclesflag =0
            distance-=1200
            for obstacle in obstacles0:
                obstacle.location[1] = obstacle.location[1]-1200
            obstacles1 = createObstacles(10,19)
            obstacles = AddObstacles(obstacles0,obstacles1)

        for obstacle in obstacles:
            obstacle.move(distance)
        hitted_obstacles = pg.sprite.spritecollide(skier,obstacles,False)

        if hitted_obstacles:
            if hitted_obstacles[0].attribute =="tree" and not hitted_obstacles[0].passed:
                score -=50
                skier.setFall()
                updateFrame(screen,obstacles,skier,score)
                pg.time.delay(1000)
                skier.SetForward()
                speed = [0,6]
                hitted_obstacles[0].passed = True
            elif hitted_obstacles[0].attribute =="flag" and not hitted_obstacles[0].passed:
                score +=10
                obstacles.remove(hitted_obstacles[0])
                 
        updateFrame(screen,obstacles,skier,score)
        clock.tick(cfg.FPS)    


if __name__=='__main__':
    main()


