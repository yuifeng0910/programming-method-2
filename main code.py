#AERO BLASTER: HORSE OF DOOM
import pygame, random, math, sys, os
from pygame import SRCALPHA

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
if not pygame.mixer.get_init(): pygame.mixer.init()

W,H,FPS=700,900,60
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("AERO BLASTER: HORSE OF DOOM")
clock=pygame.time.Clock()

WHITE=(255,255,255); BLACK=(10,10,10); RED=(255,70,70); YELLOW=(255,220,80)
CYAN=(100,220,255); PURPLE=(220,100,255); SILVER=(205,210,220); DARK=(120,130,145)
GREY=(70,78,96); B1=(95,70,55); B2=(130,95,70); B3=(165,125,92)

fs=pygame.font.SysFont("monospace",18,True)
fm=pygame.font.SysFont("arial",28,True)
fb=pygame.font.SysFont("arial",44,True)

PLAYER_IMG=r"C:\Users\HAI\Downloads\pl2.png"
ENEMY_IMG=r"c:\Users\HAI\Downloads\planebl.png"
BOSS_IMG=r"c:\Users\HAI\Downloads\z7718593466873_0a142d28b5623bef36d76497091803ff.jpg"
BGM=r"c:\Users\HAI\Downloads\background.wav (1).wav"
BINTRO=r"c:\Users\HAI\Downloads\boss_intro.wav.wav"
BBATTLE=r"c:\Users\HAI\Downloads\boss battle (1).wav"
EXPLO=r"c:\Users\HAI\Downloads\explosion.wav.wav"
GOVER=r"c:\Users\HAI\Downloads\game_over.wav.wav"
SHOOT=r"C:\Users\HAI\Downloads\shoot.wav"
VICTORY=r"c:\Users\HAI\Downloads\winning.wav.wav"

def ls(p,v=.5):
    try:
        if p and os.path.exists(p):
            s=pygame.mixer.Sound(p); s.set_volume(v); return s
    except: pass
def ps(s):
    try:
        if s: s.play()
    except: pass
def pm(p,l=-1,v=.4):
    try:
        if p and os.path.exists(p):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(p)
            pygame.mixer.music.set_volume(v)
            pygame.mixer.music.play(l)
    except: pass
def sm():
    try: pygame.mixer.music.stop()
    except: pass
def ss():
    try: pygame.mixer.stop()
    except: pass
def txt(t,f,c,x,y,ct=False):
    i=f.render(t,1,c)
    screen.blit(i,i.get_rect(center=(x,y)) if ct else (x,y))
def img(p,s,a=True):
    i=pygame.image.load(p)
    i=i.convert_alpha() if a else i.convert()
    return pygame.transform.scale(i,s)
def plane(size=(120,120),body=(40,40,40),can=(120,220,255)):
    sf=pygame.Surface(size,SRCALPHA); w,h=size; c=w//2
    pts=[(c,8),(c+20,32),(c+26,66),(c+12,108),(c-12,108),(c-26,66),(c-20,32)]
    pygame.draw.polygon(sf,body,pts); pygame.draw.polygon(sf,WHITE,pts,2)
    pygame.draw.polygon(sf,body,[(c-18,48),(8,78),(c-10,66)])
    pygame.draw.polygon(sf,body,[(c+18,48),(w-8,78),(c+10,66)])
    pygame.draw.ellipse(sf,can,(c-8,28,16,26))
    return sf
def asteroid_img(r):
    sf=pygame.Surface((r*2+8,r*2+8),SRCALPHA); c=r+4
    pts=[(c+math.cos(math.tau*i/12)*(r+random.randint(-6,6)),c+math.sin(math.tau*i/12)*(r+random.randint(-6,6))) for i in range(12)]
    pygame.draw.polygon(sf,B2,pts); pygame.draw.polygon(sf,B3,pts,3)
    for _ in range(5):
        pygame.draw.circle(sf,B1,(random.randint(c-r//2,c+r//2),random.randint(c-r//2,c+r//2)),random.randint(4,max(5,r//3)))
    return sf
def iss(x,y):
    g=pygame.Surface((620,300),SRCALPHA)
    pygame.draw.ellipse(g,(120,180,255,22),(40,110,540,80)); screen.blit(g,(x-310,y-150))
    pygame.draw.line(screen,WHITE,(x-180,y),(x+180,y),4)
    for i in range(-150,151,30):
        pygame.draw.line(screen,DARK,(x+i,y-10),(x+i+15,y+10),2)
        pygame.draw.line(screen,DARK,(x+i,y+10),(x+i+15,y-10),2)
    for px in (x-255,x+145):
        p=pygame.Rect(px,y-58,110,116)
        pygame.draw.rect(screen,(35,75,150),p,border_radius=4); pygame.draw.rect(screen,WHITE,p,2,border_radius=4)
        for gx in range(p.x+22,p.right,22): pygame.draw.line(screen,(120,170,255),(gx,p.y),(gx,p.bottom),1)
        for gy in range(p.y+19,p.bottom,19): pygame.draw.line(screen,(120,170,255),(p.x,gy),(p.right,gy),1)
    pygame.draw.line(screen,WHITE,(x-180,y),(x-145,y),3); pygame.draw.line(screen,WHITE,(x+145,y),(x+180,y),3)
    b=pygame.Rect(x-95,y-26,190,52); h=pygame.Rect(x-34,y-44,68,88)
    pygame.draw.rect(screen,SILVER,b,border_radius=8); pygame.draw.rect(screen,WHITE,b,2,border_radius=8)
    pygame.draw.rect(screen,GREY,h,border_radius=8); pygame.draw.rect(screen,WHITE,h,2,border_radius=8)
    for gx in range(b.x+24,b.right,24): pygame.draw.line(screen,DARK,(gx,b.y+4),(gx,b.bottom-4),1)
    for rx in (-125,88):
        m=pygame.Rect(x+rx,y-18,36,36); pygame.draw.rect(screen,DARK,m,border_radius=5); pygame.draw.rect(screen,WHITE,m,1,border_radius=5)
    for r in (pygame.Rect(x-22,y-72,44,18),pygame.Rect(x-18,y+48,36,24)):
        pygame.draw.rect(screen,DARK,r,border_radius=4); pygame.draw.rect(screen,WHITE,r,1,border_radius=4)
    pygame.draw.line(screen,WHITE,(x-8,y-72),(x-24,y-102),2); pygame.draw.line(screen,WHITE,(x+8,y-72),(x+24,y-102),2)
    pygame.draw.circle(screen,YELLOW,(x-24,y-102),3); pygame.draw.circle(screen,YELLOW,(x+24,y-102),3)
    for wx in (-16,0,16):
        pygame.draw.circle(screen,CYAN,(x+wx,y-8),5); pygame.draw.circle(screen,WHITE,(x+wx,y-8),5,1)
    p=pygame.Rect(x-120,y-14,240,20)
    pygame.draw.rect(screen,(228,232,238),p,border_radius=3); pygame.draw.rect(screen,WHITE,p,1,border_radius=3)
    txt("ISS INTERNATIONAL SPACE STATION",fs,BLACK,x,y-4,1)
class Bg:
    def __init__(s):
        s.st=[[random.randint(0,W),random.randint(0,H),random.randint(1,3)] for _ in range(140)]
        s.li=[[random.randint(0,W),random.randint(0,H),random.randint(10,24)] for _ in range(45)]
    def draw(s):
        t,m,b=(6,8,20),(18,26,46),(8,12,26)
        for y in range(H):
            k=y/(H//2) if y<H//2 else (y-H//2)/(H//2)
            c=tuple(int(t[i]+(m[i]-t[i])*k) if y<H//2 else int(m[i]+(b[i]-m[i])*k) for i in range(3))
            pygame.draw.line(screen,c,(0,y),(W,y))
        for a in s.st:
            a[1]+=a[2]
            if a[1]>H: a[0],a[1]=random.randint(0,W),0
            pygame.draw.circle(screen,(220,220,240),(a[0],a[1]),max(1,a[2]-1))
        for a in s.li:
            a[1]+=15
            if a[1]>H: a[0],a[1]=random.randint(0,W),-20
            pygame.draw.line(screen,(80,120,180),(a[0],a[1]),(a[0],a[1]+a[2]),1)
class Explosion:
    def __init__(s,x,y,m=70,c=(255,120,50)): s.x,s.y,s.r,s.m,s.c=x,y,8,m,c
    def update(s): s.r+=4
    def alive(s): return s.r<=s.m
    def draw(s):
        pygame.draw.circle(screen,s.c,(int(s.x),int(s.y)),int(s.r))
        pygame.draw.circle(screen,WHITE,(int(s.x),int(s.y)),int(s.r),1)
class Player:
    def __init__(s,sp):
        s.sp,s.x,s.y,s.v=sp,W//2,H-140,8
        s.hp=s.max_hp=100; s.hit=pygame.Rect(s.x-35,s.y-45,70,90)
    def move(s,k):
        if k["left"]: s.x-=s.v
        if k["right"]: s.x+=s.v
        if k["up"]: s.y-=s.v
        if k["down"]: s.y+=s.v
        s.x=max(60,min(W-60,s.x)); s.y=max(80,min(H-80,s.y)); s.hit=pygame.Rect(s.x-35,s.y-45,70,90)
    def draw(s):
        sh=pygame.Surface((90,35),SRCALPHA)
        pygame.draw.ellipse(sh,(0,0,0,110),(0,0,90,35))
        screen.blit(sh,(s.x-45,s.y+22)); screen.blit(s.sp,s.sp.get_rect(center=(s.x,s.y)))
class Enemy:
    def __init__(s,sp): s.sp,s.x,s.y,s.hp,s.max_hp,s.v=sp,random.randint(80,W-80),-80,3,3,4
    def rect(s): return pygame.Rect(s.x-35,s.y-45,70,90)
    def update(s): s.y+=s.v
    def draw(s):
        e=pygame.transform.rotate(s.sp,180)
        screen.blit(e,e.get_rect(center=(s.x,s.y)))
        pygame.draw.rect(screen,BLACK,(s.x-25,s.y-52,50,5))
        pygame.draw.rect(screen,RED,(s.x-25,s.y-52,int(s.hp/s.max_hp*50),5))
class Asteroid:
    def __init__(s):
        s.r=random.randint(20,40); s.base=asteroid_img(s.r); s.a=random.randint(0,360); s.rot=random.choice([-4,-3,-2,2,3,4])
        s.x=random.randint(s.r+20,W-s.r-20); s.y=-random.randint(60,220); s.vy=random.uniform(3.5,6.5); s.vx=random.uniform(-1.2,1.2)
        s.hp=s.max_hp=2 if s.r<30 else 3; s.damage=20 if s.r<30 else 35
    def rect(s): return pygame.Rect(s.x-s.r,s.y-s.r,s.r*2,s.r*2)
    def update(s): s.y+=s.vy; s.x+=s.vx; s.a=(s.a+s.rot)%360
    def draw(s):
        i=pygame.transform.rotate(s.base,s.a); screen.blit(i,i.get_rect(center=(s.x,s.y)))
class Boss:
    def __init__(s,sp=None): s.sp,s.x,s.y,s.hp,s.max_hp,s.active,s.dead,s.fr,s.ph=sp,W//2,-200,350,350,0,0,40,0
    def rect(s): return pygame.Rect(s.x-150,s.y-110,300,220)
    def update(s):
        if s.y<145: s.y+=1.4
        s.ph+=1; s.x+=math.sin(s.ph*0.03)*1.1
    def draw(s):
        if not s.active or s.dead: return
        pygame.draw.rect(screen,(25,25,30),(90,18,W-180,18),border_radius=8)
        pygame.draw.rect(screen,RED,(90,18,int((s.hp/s.max_hp)*(W-180)),18),border_radius=8)
        pygame.draw.rect(screen,WHITE,(90,18,W-180,18),2,border_radius=8)
        txt(f"BOSS: {s.hp}/{s.max_hp}",fs,WHITE,W//2,46,1)
        if s.sp: screen.blit(s.sp,s.sp.get_rect(center=(s.x,s.y)))
class Game:
    def __init__(s):
        try: s.psp=img(PLAYER_IMG,(120,120),1)
        except: s.psp=plane((120,120),(35,35,35),CYAN)
        try: s.esp=img(ENEMY_IMG,(120,120),1)
        except: s.esp=plane((120,120),(150,25,25),(255,180,180))
        try: s.bsp=img(BOSS_IMG,(300,220),0)
        except: s.bsp=None
        s.bg=Bg(); s.reset()

    def reset(s):
        ss(); sm()
        s.state="START"; s.p=Player(s.psp); s.en=[]; s.asd=[]; s.bu=[]; s.bbu=[]; s.ex=[]; s.k={"left":0,"right":0,"up":0,"down":0}
        s.score=s.frame=0; s.rate=14; s.winy=-220; s.boss=Boss(s.bsp); s.vp=s.ip=s.bp=0

    def kd(s,key):
        if key in (pygame.K_LEFT,pygame.K_a): s.k["left"]=1
        if key in (pygame.K_RIGHT,pygame.K_d): s.k["right"]=1
        if key in (pygame.K_UP,pygame.K_w): s.k["up"]=1
        if key in (pygame.K_DOWN,pygame.K_s): s.k["down"]=1
        if s.state in ("START","OVER","WON") and key==pygame.K_SPACE:
            ss(); sm(); s.reset(); s.state="PLAYING"; pm(BGM,-1,.30)

    def ku(s,key):
        if key in (pygame.K_LEFT,pygame.K_a): s.k["left"]=0
        if key in (pygame.K_RIGHT,pygame.K_d): s.k["right"]=0
        if key in (pygame.K_UP,pygame.K_w): s.k["up"]=0
        if key in (pygame.K_DOWN,pygame.K_s): s.k["down"]=0

    def boom(s,x,y,c=(255,120,50),m=70): s.ex.append(Explosion(x,y,m,c)); ps(SND_EXPLOSION)

    def over(s):
        if s.state!="OVER":
            ss(); sm(); s.state="OVER"; s.bu.clear(); s.bbu.clear(); ps(SND_GAME_OVER)

    def hurt(s,d,c=(255,80,60),r=80):
        s.p.hp=max(0,s.p.hp-d); s.boom(s.p.x,s.p.y,c,r)
        if s.p.hp<=0: s.over()

    def spawn(s):
        r=max(5,s.rate-s.score//25)
        if s.frame%r: return
        c=3 if s.score>=300 else 2 if s.score>=150 else 1
        s.bu += ([[s.p.x,s.p.y-44]] if c==1 else [[s.p.x-18,s.p.y-28],[s.p.x+18,s.p.y-28]] if c==2 else [[s.p.x,s.p.y-48],[s.p.x-32,s.p.y-12],[s.p.x+32,s.p.y-12]])
        ps(SND_SHOOT)

    def uboss(s):
        if s.score>=400 and not s.boss.active:
            ss(); sm(); s.boss.active=1; s.en.clear(); s.asd.clear()
            if not s.ip: s.ip=1; pm(BINTRO,0,.42)
        if s.boss.active and not s.boss.dead:
            s.boss.update()
            if s.boss.y>=145 and not s.bp:
                ss(); sm(); s.bp=1; pm(BBATTLE,-1,.34)
            if s.frame%s.boss.fr==0:
                for _ in range(7):
                    a=random.uniform(0.7,2.4); sp=random.uniform(5,8)
                    s.bbu.append([s.boss.x,s.boss.y+70,math.cos(a)*sp,math.sin(a)*sp])

    def hit(s,arr,x,y):
        for o in arr:
            if o.rect().collidepoint(x,y): return o

    def ubu(s):
        keep=[]
        for b in s.bu:
            b[1]-=16; used=0
            if s.boss.active and not s.boss.dead and s.boss.rect().collidepoint(b[0],b[1]):
                s.boss.hp=max(0,s.boss.hp-1); used=1
                if s.boss.hp<=0:
                    ss(); sm(); s.boss.dead=1; s.bbu.clear(); s.bu.clear(); s.en.clear(); s.asd.clear(); s.boom(s.boss.x,s.boss.y,(255,160,50),300); s.state="WON"
            if not used:
                e=s.hit(s.en,b[0],b[1])
                if e:
                    e.hp-=1; used=1
                    if e.hp<=0: s.boom(e.x,e.y,(241,196,15),90); s.score+=20; s.en.remove(e)
            if not used:
                a=s.hit(s.asd,b[0],b[1])
                if a:
                    a.hp-=1; used=1
                    if a.hp<=0: s.boom(a.x,a.y,(255,170,70),80); s.score+=10; s.asd.remove(a)
            if not used and b[1]>-50: keep.append(b)
        s.bu=keep

    def ubbu(s):
        keep=[]
        for b in s.bbu:
            b[0]+=b[2]; b[1]+=b[3]
            if s.p.hit.collidepoint(b[0],b[1]): s.hurt(20)
            elif -100<b[1]<H+20 and 0<b[0]<W: keep.append(b)
        s.bbu=keep

    def uobj(s,arr,d,c,r,lim=80):
        for o in arr[:]:
            o.update()
            if o.rect().colliderect(s.p.hit): s.hurt(d(o) if callable(d) else d,c,r); arr.remove(o)
            elif o.y>H+lim: arr.remove(o)

    def uex(s):
        s.ex=[e for e in s.ex if e.alive()]
        [e.update() for e in s.ex]

    def update(s):
        if s.state=="WON":
            if not s.vp:
                s.vp=1; ss(); ps(SND_VICTORY)
            if s.winy<H//4: s.winy+=2
            s.p.x += 2 if s.p.x<W//2 else -2 if s.p.x>W//2 else 0
            ty=s.winy+150; s.p.y += 2 if s.p.y<ty else -2 if s.p.y>ty else 0
            s.uex(); return
        if s.state!="PLAYING": s.uex(); return
        s.frame+=1; s.p.move(s.k); s.uboss(); s.spawn(); s.ubu(); s.ubbu()
        s.uobj(s.en,35,(255,80,60),100,60); s.uobj(s.asd,lambda a:a.damage,(255,130,60),110,80); s.uex()
        if not s.boss.active and s.frame%45==0: s.en.append(Enemy(s.esp))
        if not s.boss.active and s.frame%90==0: s.asd.append(Asteroid())

    def ui(s):
        pygame.draw.rect(screen,(20,20,28),(18,18,220,18),border_radius=6)
        pygame.draw.rect(screen,RED,(18,18,int(220*s.p.hp/s.p.max_hp),18),border_radius=6)
        pygame.draw.rect(screen,WHITE,(18,18,220,18),2,border_radius=6)
        txt(f"HP {s.p.hp}/{s.p.max_hp}",fs,WHITE,24,16)
        if s.state=="PLAYING": txt(f"SCORE: {s.score} | GOAL: 400",fs,WHITE,15,H-30)

    def draw(s):
        s.bg.draw()
        if s.state=="START":
            txt("AERO BLASTER: HORSE OF DOOM",fb,RED,W//2,90,1); txt(" * Press ASDW to move * ",fm,CYAN,W//2,160,1); s.p.draw()
            txt("[ SPACE ] TO TAKE OFF",fm,YELLOW,W//2,H-120,1); pygame.display.flip(); return
        if s.state=="WON":
            iss(W//2,s.winy); [e.draw() for e in s.ex]; s.p.draw()
            if s.winy>=H//4:
                txt("YOU WIN",fb,YELLOW,W//2,H//2+120,1); txt("MISSION COMPLETE",fm,WHITE,W//2,H//2+170,1); txt("[ SPACE ] TO RETRY",fs,(170,170,170),W//2,H-50,1)
            s.ui(); pygame.display.flip(); return
        s.boss.draw(); [e.draw() for e in s.en]; [a.draw() for a in s.asd]
        if s.state!="OVER":
            [pygame.draw.line(screen,YELLOW,(b[0],b[1]),(b[0],b[1]-25),4) for b in s.bu]
            for b in s.bbu:
                pygame.draw.circle(screen,PURPLE,(int(b[0]),int(b[1])),8)
                pygame.draw.circle(screen,WHITE,(int(b[0]),int(b[1])),8,1)
            [e.draw() for e in s.ex]; s.p.draw()
        else:
            txt("MISSION FAILED",fb,RED,W//2,H//2-20,1); txt("[SPACE] TO RETRY",fm,WHITE,W//2,H//2+40,1); txt(" PRESS ASDW TO MOVE",fm ,(170,170,170),W//2,H//2+80,1)
        s.ui(); pygame.display.flip()
SND_EXPLOSION=ls(EXPLO,.45)
SND_GAME_OVER=ls(GOVER,.45)
SND_SHOOT=ls(SHOOT,.18)
SND_VICTORY=ls(VICTORY,.55) or ls(r"C:\Users\HAI\Downloads\victory.wav",.35) or ls(EXPLO,.2)
def main():
    g=Game()
    while 1:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type==pygame.QUIT: ss(); sm(); pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN: g.kd(e.key)
            if e.type==pygame.KEYUP: g.ku(e.key)
        g.update(); g.draw()
if __name__=="__main__": main()
