import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400), 0, 32)
window_title = pygame.display.set_caption("rich man")
game_over = False
score = 0
#构建背景板
background = pygame.image.load("./view/richman_sky.JPG").convert()
balloonPng = [{"name" : "black", "path" : "./view/balloon/black.png", "score": 7},
              {"name" : "bule", "path" : "./view/balloon/bule.png", "score": 1},
              {"name" : "green", "path" : "./view/balloon/green.png", "score": 1},
              {"name" : "heart", "path" : "./view/balloon/heart.png", "score": 5}]
font = pygame.font.Font(None, 32)

#准心类
class Sight(object):
    def __init__(self):
        self.x = 200
        self.y = 200
        self.image = pygame.image.load("./view/sight.png").convert_alpha()

    def move(self, mouse_x, mouse_y):
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2
    
    def restart(self, mouse_x, mouse_y):
        self.move(mouse_x, mouse_y)

class ColorBalloon(object):
    def __init__(self):
        self.restart()
        index = random.randint(0,3)        
        self.image = pygame.image.load(balloonPng[index]["path"]).convert_alpha()
        self.name = balloonPng[index]["name"]
        self.score = balloonPng[index]["score"]

    def move(self, mouse_x, mouse_y):
        if self.y <= -100:
            self.restart()
        else:
            self.y -= self.speed

    def restart(self):
        self.x = random.randint(50, 550)
        self.y = 400
        self.speed = random.uniform(0.05,0.1)

sight = Sight()
balloonList = []
for i in range(15):
    balloonList.append(ColorBalloon())

#效验是否集中气球
def checkHint(sight, balloon):    
    if (sight.x < balloon.x + 0.5 * balloon.image.get_width()) and (sight.x > balloon.x - 0.5 * balloon.image.get_width()) and (sight.y < balloon.y + 0.5 * balloon.image.get_height()) and (sight.y > balloon.y - 0.5 * balloon.image.get_height()):
        return True
    return False

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()    
    text = font.render("Score: %d" % score, 1, (0, 255, 0))
    # 将背景图画上去
    screen.blit(background, (0, 0))    
    screen.blit(text, (5, 5))
    # 获得鼠标位置
    x, y = pygame.mouse.get_pos()
    # 获取光标中心位置
    x -= sight.image.get_width() / 2
    y -= sight.image.get_height() / 2

    # 将光标画上去
    screen.blit(sight.image, (x, y))
    for balloon in balloonList:        
        screen.blit(balloon.image, (balloon.x, balloon.y))
        balloon.move(mouse_x, mouse_y)

    #将最新的坐标赋值给sight
    sight.move(mouse_x, mouse_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #监听鼠标点击且点击按钮为鼠标左键
            for balloon in balloonList:
                hintFlag = checkHint(sight, balloon)
                #集中目标
                if hintFlag:
                    score += balloon.score
                    #重新绘制气球
                    balloon.restart()

    # 刷新画面
    pygame.display.update()