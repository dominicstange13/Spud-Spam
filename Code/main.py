import pygame
import random

pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_center = screen.get_rect().center
clock = pygame.time.Clock()
currenttime = 0
mousepos = pygame.mouse.get_pos()
res = pygame.display.Info() #for debugging/coordinating objects on screen

#screen resolution referenced in code: 1920x1080

quitbutton = pygame.rect.Rect((1870,0),(50,50))
quitbuttonimage = pygame.image.load("assets/images/quitbutton.png").convert_alpha()
playbutton = pygame.rect.Rect((0,0),(600,150))
playbuttonimage = pygame.image.load("assets/images/playbutton.png").convert_alpha()
playbutton.center = (screen_center[0],950)
logo = pygame.image.load("assets/images/logo.png").convert_alpha()
logorect = logo.get_rect()

grass = pygame.image.load("assets/images/grass.png").convert_alpha()

player = pygame.rect.Rect((0,980),(200,100))
cursor = pygame.image.load("assets/images/cursor.png").convert_alpha()
cursor = pygame.transform.scale_by(cursor, 0.5)
cursorrect = cursor.get_rect()

bulletrect = pygame.rect.Rect((0,980),(50,50))
cannon = pygame.image.load("assets/images/cannon.png").convert_alpha()
potato = pygame.image.load("assets/images/potato.png").convert_alpha()

bulletmodactive = False
bulletnumber = 1
shootcd = 1000
lastshot = 0

enemypos = pygame.rect.Rect((0,0),(100,100))
enemyskins = []
enemyskin1 = pygame.image.load("assets/images/apple.png").convert_alpha()
enemyskin2 = pygame.image.load("assets/images/corn.png").convert_alpha()
enemyskin3 = pygame.image.load("assets/images/carrot.png").convert_alpha()
enemyskin4 = pygame.image.load("assets/images/blueberry.png").convert_alpha()
enemyskins.extend([enemyskin1, enemyskin2, enemyskin3, enemyskin4])

spawncd = 1500
lastspawn = 0
totalenemies = 0
roundenemies = 0
enemiesleft = 0

hp = 100
cash = 0
cashperkill = 1

running = True
inround = False
roundnum = 0

bulletreloadupgrade = pygame.image.load("assets/images/bulletreload.png").convert_alpha()
bulletnumberupgrade = pygame.image.load("assets/images/bulletnumber.png").convert_alpha()
cashperkillupgrade = pygame.image.load("assets/images/cashperkill.png").convert_alpha()
upgradeiconimages = [bulletreloadupgrade, bulletnumberupgrade, cashperkillupgrade]

roundcountfont = pygame.font.Font("assets/fonts/mainfont.ttf", 70)
enemycountfont = pygame.font.Font("assets/fonts/mainfont.ttf", 48)
hpcountfont = pygame.font.Font("assets/fonts/mainfont.ttf", 36)
cashfont = pygame.font.Font("assets/fonts/mainfont.ttf", 48)
upgradepricefont = pygame.font.Font("assets/fonts/mainfont.ttf", 24)
roundcounter = roundcountfont.render(str(roundnum), True, "Red")

class Enemy:
    def __init__(self, skin):
        self.pos = enemypos.copy()
        self.speed = 2
        self.skin = enemyskins[skin]

    def move(self):
        global roundnum
        if roundnum > 6:
            self.speed = roundnum / 2
        self.pos.y += self.speed
        self.currenty = self.pos.y

    def die(self):
        global enemiesleft
        enemies.remove(self)
        enemyposses.remove(self.pos)
        enemiesleft -= 1

class Bullet:
    def __init__(self, bulletpos):
        self.pos = bulletpos.copy()
        self.speed = 20

    def letitrip(self):
        self.currenty = self.pos.y
        if self.currenty + self.speed >= 200:
            self.pos.y -= self.speed
            self.currenty = self.pos.y

    def removebullet(self):
        bullets.remove(self)
        bulletposses.remove(self.pos)

class Upgrade:
    def __init__(self, cost, x, y):
        self.cost = cost
        self.pos = pygame.rect.Rect((x,y),(150,150))
        self.timesbought = 0

    def uptheprice(self):
        self.timesbought += 1
        self.cost = self.cost * round(1.3 ** self.timesbought)

def renderstartscreen():
    screen.blit(grass, (0,0))
    screen.blit(grass, (960,0))
    screen.blit(grass, (0,540))
    screen.blit(grass, (960,540))
    logorect.center = (playbutton.centerx,(playbutton.centery - 500))
    screen.blit(logo, logorect)
    screen.blit(quitbuttonimage, quitbutton)
    screen.blit(playbuttonimage, (playbutton.topleft))

def renderround():
    global roundcounter, roundnum, enemiesleft, hp
    screen.blit(grass, (0,0))
    screen.blit(grass, (960,0))
    screen.blit(grass, (0,540))
    screen.blit(grass, (960,540))
    roundcounter = roundcountfont.render(f"Round: {str(roundnum)}", True, "Red")
    enemycounter = enemycountfont.render(f"Enemies Left: {str(enemiesleft)}/{str(roundenemies)}", True, "Red")
    cashcounter = cashfont.render(f"${cash}", True, "yellow2")
    cashcounterrect = cashcounter.get_rect()
    hpcounter = hpcountfont.render(f"{str(hp)}/100", True, "deeppink")
    if mousepos[0] >= 100 and mousepos[0] <= 1820:
        player.centerx = mousepos[0]
    else:
        if mousepos[0] >= 100:
            player.centerx = 1820
        elif mousepos[0] <= 1820:
            player.centerx = 100
    bulletrect.centerx = mousepos[0]
    cursorrect.centerx = mousepos[0]
    cursorrect.centery = mousepos[1]
    screen.blit(cannon, ((bulletrect.x - 25), bulletrect.y))
    checkbulletcollisions()
    for b in bulletposses:
        if b.y >= 200:
            screen.blit(potato, (b.x,b.y))
    for b in bullets:
        if b.pos.y >= 200:
            b.letitrip()
        else:
            b.removebullet()
    for e in enemyposses:
        screen.blit(enemies[enemyposses.index(e)].skin, (e.x,e.y))
    for e in enemies:
        if e.pos.y >= 980:
            hp -= 20
            e.die()
        else:
            e.move()
    screen.blit(roundcounter, (0,0))
    screen.blit(enemycounter, (0,70))
    screen.blit(hpcounter, (0,1040))
    screen.blit(quitbuttonimage, quitbutton)
    cashcounterrect.topleft = (1870,0)
    for i in range(abs(len(str(cash)))):
        cashcounterrect.x -= 32
    screen.blit(cashcounter, (cashcounterrect.centerx,(cashcounterrect.centery + 50)))
    renderupgrades()
    pygame.mouse.set_visible(False)
    screen.blit(cursor, cursorrect)

def renderupgrades():
    global upgradebutton, inupgradescreen, upgradeicons, upgrades, upgradefirerate, upgradebulletnumber, upgradecashgain, upgradebg, upgradepricefont
    upgradeprices = []
    for u in upgradeicons:
        screen.blit(upgradeiconimages[upgradeicons.index(u)], u)
    for u in upgrades:
        cashvalue = upgradepricefont.render(f"${u.cost}", True, "yellow2")
        cashvalueoffset = abs(len(str(u.cost))) - 1
        screen.blit(cashvalue, ((upgradeicons[upgrades.index(u)].centerx - 10) - (5 * cashvalueoffset), upgradeicons[upgrades.index(u)].centery + 50))

def checkbuttoncollisions():
    buttons = [quitbutton, playbutton]
    for button in buttons:
        if button.collidepoint(mousepos) and button == quitbutton:
            return "quit"
        elif button.collidepoint(mousepos) and button == playbutton:
            return "play"

def spawnenemies():
    global totalenemies, roundenemies, roundnum, enemiesleft, spawncd
    if currenttime >= 1500 and totalenemies < roundenemies:
        enemypos.y = random.randint(0,100)
        enemypos.x = random.randint(0,1820)
        newenemy = Enemy(random.randint(0,3))
        enemyposses.append(newenemy.pos)
        enemies.append(newenemy)
        totalenemies += 1
    if totalenemies >= roundenemies and len(enemies) == 0:
        roundnum += 1
        spawncd = 1500 * (0.9 ** roundnum)
        roundenemies = 10 * (1.15 ** roundnum)
        roundenemies = round(roundenemies)
        enemiesleft = roundenemies
        totalenemies = 0

def checkbulletcollisions():
    global cash
    for b in bulletposses:
        bulletcollisions = b.collidelist(enemyposses)
        if bulletcollisions != -1:
            for e in enemyposses:
                enemycollisions = e.collidelist(bulletposses)
                if enemycollisions != -1:
                    screen.blit(potato, (b.x,b.y))
                    bullets[bulletposses.index(b)].removebullet()
                    enemies[bulletcollisions].die()
                    cash += cashperkill
                    enemycollisions = -1

bulletposses = []
bullets = []

enemyposses = []
enemies = []

upgradeicons = []
upgrades = []
upgradebg = pygame.rect.Rect((1120,780),(800,300))
upgradefirerate = Upgrade(5, (upgradebg.centerx - 350), upgradebg.centery - 75)
upgradebulletnumber = Upgrade(10, (upgradefirerate.pos.x + 275), upgradefirerate.pos.y)
upgradecashgain = Upgrade(15, (upgradebulletnumber.pos.x + 275), upgradefirerate.pos.y)
upgradeicons.extend([upgradefirerate.pos, upgradebulletnumber.pos, upgradecashgain.pos])
upgrades.extend([upgradefirerate, upgradebulletnumber, upgradecashgain])

while running:
    mousepos = pygame.mouse.get_pos()
    screen.fill((0,0,0))
    if not inround:
        renderstartscreen()
    else:
        currenttime = pygame.time.get_ticks()
        renderround()
        checkbuttoncollisions()
        if currenttime - lastspawn >= spawncd:
            lastspawn = currenttime
            spawnenemies()
        if hp <= 0:
            running = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            checkbuttoncollisions()
            if checkbuttoncollisions() == "quit":
                running = False
            elif checkbuttoncollisions() == "play" and not inround:
                hp = 100
                cash = 0
                bulletnumber = 1
                inround = True
                roundnum = 0
        for u in upgradeicons:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inround and u.collidepoint(mousepos):
                if upgrades[upgradeicons.index(u)] == upgradefirerate and upgradefirerate.cost <= cash:
                    cash -= upgradefirerate.cost
                    upgradefirerate.uptheprice()
                    shootcd = shootcd / 1.2
                elif upgrades[upgradeicons.index(u)] == upgradebulletnumber and upgradebulletnumber.cost <= cash:
                    cash -= upgradebulletnumber.cost
                    upgradebulletnumber.uptheprice()
                    bulletnumber += 1
                elif upgrades[upgradeicons.index(u)] == upgradecashgain and upgradecashgain.cost <= cash:
                    cash -= upgradecashgain.cost
                    upgradecashgain.uptheprice()
                    cashperkill = cashperkill * 2

    mousebuttons = pygame.mouse.get_pressed()
    if mousebuttons[0] and inround:
        if currenttime - lastshot >= shootcd:
            lastshot = currenttime
            for _ in range(bulletnumber):
                newbullet = Bullet(bulletrect)
                newbullet.pos.x -= 30 * (bulletnumber - 1)
                if bulletnumber > 1:
                    newbullet.pos.x += 75 * _
                newbullet.letitrip()
                bulletposses.append(newbullet.pos)
                bullets.append(newbullet)
                
    pygame.display.flip()
    clock.tick(60)

pygame.quit()