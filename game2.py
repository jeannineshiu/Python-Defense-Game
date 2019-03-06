# 1 - Import library
import pygame
from pygame.locals import *
import math
import random


# 2 - Initialize the game 初始化pygame，设置展示窗口
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
keys = [False, False, False, False] #记录几个按键的情况：WASD。
playerpos=[100,100]
acc=[0,0] #跟踪玩家的精度 射出的箭头数和被击中的獾的数量
arrows=[] #跟踪箭头
badtimer=100 #定时器為新建獾
badtimer1=0
badguys=[[640,100]]
healthvalue=194
pygame.mixer.init() #為加载和播放声音


# 3 - Load images
player = pygame.image.load("resources/images/rabbitQ.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/food3.png")
arrow = pygame.image.load("resources/images/egg.png")
badguyimg1 = pygame.image.load("resources/images/cat.png")
badguyimg=badguyimg1 #複製圖片
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0) #让背景音乐一直播放
pygame.mixer.music.set_volume(0.25)



# 4 - keep looping through
running = 1  #跟踪游戏是否结束
exitcode = 0 #跟踪玩家是否胜利
while running:
    badtimer-=1

    
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    
    for x in range(int(width/grass.get_width()+1)):  #調整背景圖片大小
        for y in range(int(height/grass.get_height()+1)):
            screen.blit(grass,(x*100,y*100))  #screen.blit()
            
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345))
    #screen.blit(player,playerpos)
    # 6.1 - Set player position and rotation
    position = pygame.mouse.get_pos()  #移動鼠標使其轉向
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    # 6.2 - Draw arrows
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*10 #10是箭头的速度
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        #如果箭頭超出視窗範圍就刪除箭頭
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
        #根据相应的旋转画出箭頭
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
            
    # 6.3 - Draw badgers
    
    #一段時間後新增獾
    if badtimer==0:
        badguys.append([640, random.randint(50,430)])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    #如果獾超出視窗範圍就刪除獾
    for badguy in badguys:
        if badguy[0]<-64:
            badguys.pop(index)
        badguy[0]-=7
        # 6.3.1 - Attack castle
        badrect=pygame.Rect(badguyimg.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        #讓獾碰到城堡後消失並減少玩家生命值
        if badrect.left<64:
            hit.play() #music
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        #6.3.2 - Check for collisions
        #當箭頭射到獾，删除獾，删除箭头，并且精确度加1
        index1=0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect): #PyGame内建功能检查两矩形是否交叉
                enemy.play() #music
                acc[0]+=1
                badguys.pop(index)
                arrows.pop(index1)
            index1+=1

        # 6.3.3 - Next bad guy
        index+=1
    #畫出所有獾
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    # 6.4 - Draw clock
    #计时记录城堡存活下来的时间
    font = pygame.font.Font(None, 24) #字體大小24
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext, textRect)

    # 6.5 - Draw health bar
    #全红色的生命值条
    screen.blit(healthbar,(5,5))
    #根据城堡的生命值往生命条里面添加绿色
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))


    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0)
        if event.type == pygame.KEYDOWN: #按下
            if event.key==K_w:
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True
        if event.type == pygame.KEYUP: #放開
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
        if event.type==pygame.MOUSEBUTTONDOWN: #點擊滑鼠
            shoot.play()  #music
            position=pygame.mouse.get_pos()
            acc[1]+=1
            #箭头旋转角度
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])

    # 9 - Move player  按鍵後反應
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5

    #10 - Win/Lose check
    #检查是否时间到了
    if pygame.time.get_ticks()>=90000:
        running=0
        exitcode=1
    #检查城堡是否被摧毁了
    if healthvalue<=0:
        running=0
        exitcode=0
    #计算精准度
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
    else:
        accuracy=0
        
# 11 - Win/lose display        
if exitcode==0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()




            
