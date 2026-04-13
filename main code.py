import pygame, random, math, sys, os
from pygame import SRCALPHA

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

W, H, FPS = 700, 900, 60
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Sky Force Deluxe - Compact ISS")
clock = pygame.time.Clock()

WHITE=(255,255,255); BLACK=(10,10,10); RED=(255,70,70); YELLOW=(255,220,80)
CYAN=(100,220,255); ORANGE=(255,140,60); PURPLE=(220,100,255)
SILVER=(205,210,220); DARK=(120,130,145); GREY=(70,78,96)
B1=(95,70,55); B2=(130,95,70); B3=(165,125,92)

font_s = pygame.font.SysFont("monospace", 18, bold=True)
font_m = pygame.font.SysFont("arial", 28, bold=True)
font_b = pygame.font.SysFont("arial", 44, bold=True)

PLAYER_IMG = r"C:\Users\HAI\Downloads\pl2.png"
ENEMY_IMG  = r"c:\Users\HAI\Downloads\planebl.png"
BOSS_IMG   = r"c:\Users\HAI\Downloads\z7718593466873_0a142d28b5623bef36d76497091803ff.jpg"

BGM_PATH         = r"c:\Users\HAI\Downloads\background.wav (1).wav"
BOSS_INTRO_PATH  = r"c:\Users\HAI\Downloads\boss_intro.wav.wav"
BOSS_BATTLE_PATH = r"c:\Users\HAI\Downloads\boss_battle.wav.wav"
EXPLOSION_WAV    = r"c:\Users\HAI\Downloads\explosion.wav.wav"
GAME_OVER_WAV    = r"c:\Users\HAI\Downloads\game_over.wav.wav"
HIT_WAV          = r"/mnt/data/hit.wav.wav"
SHOOT_WAV        = r"C:\Users\HAI\Downloads\shoot.wav"
VICTORY_WAV      = r"C:\Users\HAI\Downloads\victory.wav"

def load_sound(path, volume=0.5):
    try:
        if path and os.path.exists(path):
            s = pygame.mixer.Sound(path)
            s.set_volume(volume)
            return s
    except:
        pass
    return None

def play_sound(s):
    try:
        if s: s.play()
    except:
        pass

def play_music(path, loops=-1, volume=0.4):
    try:
        if path and os.path.exists(path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
    except:
        pass

def stop_music():
    try: pygame.mixer.music.stop()
    except: pass

def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    screen.blit(img, img.get_rect(center=(x, y)) if center else (x, y))

def load_img(path, size, alpha=True):
    img = pygame.image.load(path)
    img = img.convert_alpha() if alpha else img.convert()
    return pygame.transform.scale(img, size)

def fallback_plane(size=(120,120), body=(40,40,40), canopy=(120,220,255)):
    surf = pygame.Surface(size, SRCALPHA)
    w,h=size; cx=w//2
    pts=[(cx,8),(cx+20,32),(cx+26,66),(cx+12,108),(cx-12,108),(cx-26,66),(cx-20,32)]
    pygame.draw.polygon(surf, body, pts)
    pygame.draw.polygon(surf, WHITE, pts, 2)
    pygame.draw.polygon(surf, body, [(cx-18,48),(8,78),(cx-10,66)])
    pygame.draw.polygon(surf, body, [(cx+18,48),(w-8,78),(cx+10,66)])
    pygame.draw.ellipse(surf, canopy, (cx-8,28,16,26))
    return surf

def asteroid_surface(r):
    surf = pygame.Surface((r*2+8, r*2+8), SRCALPHA)
    c = r+4
    pts=[]
    for i in range(12):
        a = math.tau*i/12
        rr = r + random.randint(-6, 6)
        pts.append((c+math.cos(a)*rr, c+math.sin(a)*rr))
    pygame.draw.polygon(surf, B2, pts)
    pygame.draw.polygon(surf, B3, pts, 3)
    for _ in range(5):
        rr=random.randint(4,max(5,r//3))
        x=random.randint(c-r//2,c+r//2); y=random.randint(c-r//2,c+r//2)
        pygame.draw.circle(surf, B1, (x,y), rr)
    return surf

def draw_iss(x, y):
    glow = pygame.Surface((620, 300), SRCALPHA)
    pygame.draw.ellipse(glow, (120,180,255,22), (40, 110, 540, 80))
    screen.blit(glow, (x-310, y-150))

    # main truss
    pygame.draw.line(screen, WHITE, (x-180, y), (x+180, y), 4)
    for i in range(-150, 151, 30):
        pygame.draw.line(screen, DARK, (x+i, y-10), (x+i+15, y+10), 2)
        pygame.draw.line(screen, DARK, (x+i, y+10), (x+i+15, y-10), 2)

    # solar panels
    for px in (x-255, x+145):
        panel = pygame.Rect(px, y-58, 110, 116)
        pygame.draw.rect(screen, (35,75,150), panel, border_radius=4)
        pygame.draw.rect(screen, WHITE, panel, 2, border_radius=4)
        for gx in range(panel.x+22, panel.right, 22):
            pygame.draw.line(screen, (120,170,255), (gx, panel.y), (gx, panel.bottom), 1)
        for gy in range(panel.y+19, panel.bottom, 19):
            pygame.draw.line(screen, (120,170,255), (panel.x, gy), (panel.right, gy), 1)

    # connectors
    pygame.draw.line(screen, WHITE, (x-180, y), (x-145, y), 3)
    pygame.draw.line(screen, WHITE, (x+145, y), (x+180, y), 3)

    # main body
    body = pygame.Rect(x-95, y-26, 190, 52)
    pygame.draw.rect(screen, SILVER, body, border_radius=8)
    pygame.draw.rect(screen, WHITE, body, 2, border_radius=8)
    for gx in range(body.x+24, body.right, 24):
        pygame.draw.line(screen, DARK, (gx, body.y+4), (gx, body.bottom-4), 1)

    # center hub
    hub = pygame.Rect(x-34, y-44, 68, 88)
    pygame.draw.rect(screen, GREY, hub, border_radius=8)
    pygame.draw.rect(screen, WHITE, hub, 2, border_radius=8)

    # side modules
    for rx in (-125, 88):
        mod = pygame.Rect(x+rx, y-18, 36, 36)
        pygame.draw.rect(screen, DARK, mod, border_radius=5)
        pygame.draw.rect(screen, WHITE, mod, 1, border_radius=5)

    # top/bottom modules
    top = pygame.Rect(x-22, y-72, 44, 18)
    bot = pygame.Rect(x-18, y+48, 36, 24)
    pygame.draw.rect(screen, DARK, top, border_radius=4)
    pygame.draw.rect(screen, DARK, bot, border_radius=4)
    pygame.draw.rect(screen, WHITE, top, 1, border_radius=4)
    pygame.draw.rect(screen, WHITE, bot, 1, border_radius=4)

    # antennae
    pygame.draw.line(screen, WHITE, (x-8, y-72), (x-24, y-102), 2)
    pygame.draw.line(screen, WHITE, (x+8, y-72), (x+24, y-102), 2)
    pygame.draw.circle(screen, YELLOW, (x-24, y-102), 3)
    pygame.draw.circle(screen, YELLOW, (x+24, y-102), 3)

    # windows
    for wx in (-16, 0, 16):
        pygame.draw.circle(screen, CYAN, (x+wx, y-8), 5)
        pygame.draw.circle(screen, WHITE, (x+wx, y-8), 5, 1)

    # label plate
    plate = pygame.Rect(x-120, y-14, 240, 20)
    pygame.draw.rect(screen, (228,232,238), plate, border_radius=3)
    pygame.draw.rect(screen, WHITE, plate, 1, border_radius=3)
    draw_text("ISS INTERNATIONAL SPACE STATION", font_s, BLACK, x, y-4, center=True)

class Background:
    def __init__(self):
        self.stars = [[random.randint(0,W), random.randint(0,H), random.randint(1,3)] for _ in range(140)]
        self.lines = [[random.randint(0,W), random.randint(0,H), random.randint(10,24)] for _ in range(45)]

    def draw(self):
        top, mid, bot = (6,8,20), (18,26,46), (8,12,26)
        for y in range(H):
            t = y/(H//2) if y < H//2 else (y-H//2)/(H//2)
            c = tuple(int(top[i]+(mid[i]-top[i])*t) if y < H//2 else int(mid[i]+(bot[i]-mid[i])*t) for i in range(3))
            pygame.draw.line(screen, c, (0,y), (W,y))
        for s in self.stars:
            s[1] += s[2]
            if s[1] > H: s[0], s[1] = random.randint(0,W), 0
            pygame.draw.circle(screen, (220,220,240), (s[0], s[1]), max(1, s[2]-1))
        for l in self.lines:
            l[1] += 15
            if l[1] > H: l[0], l[1] = random.randint(0,W), -20
            pygame.draw.line(screen, (80,120,180), (l[0],l[1]), (l[0],l[1]+l[2]), 1)

class Explosion:
    def __init__(self, x, y, max_r=70, color=(255,120,50)):
        self.x, self.y, self.r, self.max_r, self.color = x, y, 8, max_r, color
    def update(self): self.r += 4
    def alive(self): return self.r <= self.max_r
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.r))
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), int(self.r), 1)

class Player:
    def __init__(self, sprite):
        self.sprite, self.x, self.y, self.speed = sprite, W//2, H-140, 8
        self.hp = self.max_hp = 100
        self.hitbox = pygame.Rect(self.x-35, self.y-45, 70, 90)
    def move(self, keys):
        if keys["left"]: self.x -= self.speed
        if keys["right"]: self.x += self.speed
        if keys["up"]: self.y -= self.speed
        if keys["down"]: self.y += self.speed
        self.x = max(60, min(W-60, self.x))
        self.y = max(80, min(H-80, self.y))
        self.hitbox = pygame.Rect(self.x-35, self.y-45, 70, 90)
    def draw(self):
        shadow = pygame.Surface((90,35), SRCALPHA)
        pygame.draw.ellipse(shadow, (0,0,0,110), (0,0,90,35))
        screen.blit(shadow, (self.x-45, self.y+22))
        screen.blit(self.sprite, self.sprite.get_rect(center=(self.x, self.y)))

class Enemy:
    def __init__(self, sprite):
        self.sprite, self.x, self.y, self.hp, self.max_hp, self.speed = sprite, random.randint(80,W-80), -80, 3, 3, 4
    def rect(self): return pygame.Rect(self.x-35, self.y-45, 70, 90)
    def update(self): self.y += self.speed
    def draw(self):
        screen.blit(self.sprite, self.sprite.get_rect(center=(self.x, self.y)))
        pygame.draw.rect(screen, BLACK, (self.x-25, self.y-52, 50, 5))
        pygame.draw.rect(screen, RED, (self.x-25, self.y-52, int(self.hp/self.max_hp*50), 5))

class Asteroid:
    def __init__(self):
        self.radius = random.randint(20, 40)
        self.base = asteroid_surface(self.radius)
        self.angle = random.randint(0, 360)
        self.rot = random.choice([-4,-3,-2,2,3,4])
        self.x = random.randint(self.radius+20, W-self.radius-20)
        self.y = -random.randint(60, 220)
        self.vy = random.uniform(3.5, 6.5)
        self.vx = random.uniform(-1.2, 1.2)
        self.hp = self.max_hp = 2 if self.radius < 30 else 3
        self.damage = 20 if self.radius < 30 else 35
    def rect(self): return pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
    def update(self):
        self.y += self.vy; self.x += self.vx; self.angle = (self.angle+self.rot) % 360
    def draw(self):
        img = pygame.transform.rotate(self.base, self.angle)
        screen.blit(img, img.get_rect(center=(self.x, self.y)))

class Boss:
    def __init__(self, sprite=None):
        self.sprite, self.x, self.y = sprite, W//2, -200
        self.hp = self.max_hp = 350
        self.active = self.dead = False
        self.fire_rate = 40
        self.phase = 0
    def rect(self): return pygame.Rect(self.x-150, self.y-110, 300, 220)
    def update(self):
        if self.y < 145: self.y += 1.4
        self.phase += 1
        self.x += math.sin(self.phase*0.03)*1.1
    def draw(self):
        if not self.active or self.dead: return
        pygame.draw.rect(screen, (25,25,30), (90,18,W-180,18), border_radius=8)
        pygame.draw.rect(screen, RED, (90,18,int((self.hp/self.max_hp)*(W-180)),18), border_radius=8)
        pygame.draw.rect(screen, WHITE, (90,18,W-180,18), 2, border_radius=8)
        draw_text(f"BOSS: {self.hp}/{self.max_hp}", font_s, WHITE, W//2, 46, center=True)
        if self.sprite: screen.blit(self.sprite, self.sprite.get_rect(center=(self.x,self.y)))

class Game:
    def __init__(self):
        try: self.player_sprite = load_img(PLAYER_IMG, (120,120), True)
        except: self.player_sprite = fallback_plane((120,120), (35,35,35), CYAN)
        try: self.enemy_sprite = load_img(ENEMY_IMG, (120,120), True)
        except: self.enemy_sprite = fallback_plane((120,120), (150,25,25), (255,180,180))
        try: self.boss_sprite = load_img(BOSS_IMG, (300,220), False)
        except: self.boss_sprite = None
        self.bg = Background()
        self.reset()

    def reset(self):
        self.state = "START"
        self.player = Player(self.player_sprite)
        self.enemies, self.asteroids, self.bullets, self.boss_bullets, self.explosions = [], [], [], [], []
        self.keys = {"left":False,"right":False,"up":False,"down":False}
        self.score = self.frame = 0
        self.base_fire_rate = 14
        self.win_anim_y = -220
        self.boss = Boss(self.boss_sprite)
        self.victory_played = self.boss_intro_played = self.boss_battle_played = False
        stop_music()

    def keydown(self, key):
        if key in (pygame.K_LEFT, pygame.K_a): self.keys["left"] = True
        if key in (pygame.K_RIGHT, pygame.K_d): self.keys["right"] = True
        if key in (pygame.K_UP, pygame.K_w): self.keys["up"] = True
        if key in (pygame.K_DOWN, pygame.K_s): self.keys["down"] = True
        if self.state in ("START","OVER","WON") and key == pygame.K_SPACE:
            self.reset(); self.state = "PLAYING"; play_music(BGM_PATH, -1, 0.30)

    def keyup(self, key):
        if key in (pygame.K_LEFT, pygame.K_a): self.keys["left"] = False
        if key in (pygame.K_RIGHT, pygame.K_d): self.keys["right"] = False
        if key in (pygame.K_UP, pygame.K_w): self.keys["up"] = False
        if key in (pygame.K_DOWN, pygame.K_s): self.keys["down"] = False

    def add_explosion(self, x, y, color=(255,120,50), max_r=70):
        self.explosions.append(Explosion(x, y, max_r, color))
        play_sound(SND_EXPLOSION)

    def set_game_over(self):
        if self.state != "OVER":
            self.state = "OVER"
            self.bullets.clear(); self.boss_bullets.clear()
            play_sound(SND_GAME_OVER); stop_music()

    def damage_player(self, dmg, color=(255,80,60), r=80):
        self.player.hp = max(0, self.player.hp-dmg)
        play_sound(SND_HIT)
        self.add_explosion(self.player.x, self.player.y, color, r)
        if self.player.hp <= 0: self.set_game_over()

    def spawn_player_bullets(self):
        rate = max(5, self.base_fire_rate - self.score//25)
        if self.frame % rate: return
        c = 3 if self.score >= 300 else 2 if self.score >= 150 else 1
        if c == 1:
            self.bullets.append([self.player.x, self.player.y-44])
        elif c == 2:
            self.bullets += [[self.player.x-18, self.player.y-28], [self.player.x+18, self.player.y-28]]
        else:
            self.bullets += [[self.player.x, self.player.y-48], [self.player.x-32, self.player.y-12], [self.player.x+32, self.player.y-12]]
        play_sound(SND_SHOOT)

    def update_boss(self):
        if self.score >= 400 and not self.boss.active:
            self.boss.active = True
            self.enemies.clear(); self.asteroids.clear()
            if not self.boss_intro_played:
                self.boss_intro_played = True
                play_music(BOSS_INTRO_PATH, 0, 0.42)

        if self.boss.active and not self.boss.dead:
            self.boss.update()
            if self.boss.y >= 145 and not self.boss_battle_played:
                self.boss_battle_played = True
                play_music(BOSS_BATTLE_PATH, -1, 0.34)
            if self.frame % self.boss.fire_rate == 0:
                for _ in range(7):
                    a = random.uniform(0.7, 2.4); s = random.uniform(5, 8)
                    self.boss_bullets.append([self.boss.x, self.boss.y+70, math.cos(a)*s, math.sin(a)*s])

    def hit_list(self, items, x, y):
        for obj in items:
            if obj.rect().collidepoint(x, y):
                return obj
        return None

    def update_bullets(self):
        new=[]
        for b in self.bullets:
            b[1] -= 16
            used = False

            if self.boss.active and not self.boss.dead and self.boss.rect().collidepoint(b[0], b[1]):
                self.boss.hp = max(0, self.boss.hp-1)
                play_sound(SND_HIT)
                used = True
                if self.boss.hp <= 0:
                    self.boss.dead = True
                    self.boss_bullets.clear(); self.bullets.clear(); self.enemies.clear(); self.asteroids.clear()
                    self.add_explosion(self.boss.x, self.boss.y, (255,160,50), 300)
                    self.state = "WON"

            if not used:
                e = self.hit_list(self.enemies, b[0], b[1])
                if e:
                    e.hp -= 1; play_sound(SND_HIT); used = True
                    if e.hp <= 0:
                        self.add_explosion(e.x, e.y, (241,196,15), 90)
                        self.score += 20; self.enemies.remove(e)

            if not used:
                a = self.hit_list(self.asteroids, b[0], b[1])
                if a:
                    a.hp -= 1; play_sound(SND_HIT); used = True
                    if a.hp <= 0:
                        self.add_explosion(a.x, a.y, (255,170,70), 80)
                        self.score += 10; self.asteroids.remove(a)

            if not used and b[1] > -50: new.append(b)
        self.bullets = new

    def update_boss_bullets(self):
        keep=[]
        for b in self.boss_bullets:
            b[0]+=b[2]; b[1]+=b[3]
            if self.player.hitbox.collidepoint(b[0], b[1]):
                self.damage_player(20)
            elif -100 < b[1] < H+20 and 0 < b[0] < W:
                keep.append(b)
        self.boss_bullets = keep

    def update_objects(self, arr, damage, color, r, limit=80):
        for obj in arr[:]:
            obj.update()
            if obj.rect().colliderect(self.player.hitbox):
                self.damage_player(damage(obj) if callable(damage) else damage, color, r)
                arr.remove(obj)
            elif obj.y > H+limit:
                arr.remove(obj)

    def update_effects(self):
        self.explosions = [e for e in self.explosions if e.alive()]
        for e in self.explosions: e.update()

    def update(self):
        if self.state == "WON":
            if not self.victory_played:
                self.victory_played = True
                play_sound(SND_VICTORY)
                stop_music()
            if self.win_anim_y < H//4: self.win_anim_y += 2
            self.player.x += 2 if self.player.x < W//2 else -2 if self.player.x > W//2 else 0
            target_y = self.win_anim_y + 150
            self.player.y += 2 if self.player.y < target_y else -2 if self.player.y > target_y else 0
            self.update_effects()
            return

        if self.state != "PLAYING":
            self.update_effects()
            return

        self.frame += 1
        self.player.move(self.keys)
        self.update_boss()
        self.spawn_player_bullets()
        self.update_bullets()
        self.update_boss_bullets()
        self.update_objects(self.enemies, 35, (255,80,60), 100, 60)
        self.update_objects(self.asteroids, lambda a: a.damage, (255,130,60), 110, 80)
        self.update_effects()

        if not self.boss.active and self.frame % 45 == 0: self.enemies.append(Enemy(self.enemy_sprite))
        if not self.boss.active and self.frame % 90 == 0: self.asteroids.append(Asteroid())

    def draw_ui(self):
        pygame.draw.rect(screen, (20,20,28), (18,18,220,18), border_radius=6)
        pygame.draw.rect(screen, RED, (18,18,int(220*self.player.hp/self.player.max_hp),18), border_radius=6)
        pygame.draw.rect(screen, WHITE, (18,18,220,18), 2, border_radius=6)
        draw_text(f"HP {self.player.hp}/{self.player.max_hp}", font_s, WHITE, 24, 16)
        if self.state == "PLAYING":
            draw_text(f"SCORE: {self.score} | GOAL: 400", font_s, WHITE, 15, H-30)

    def draw(self):
        self.bg.draw()

        if self.state == "START":
            draw_text("HIGH-LEVEL MISSION", font_b, RED, W//2, 90, center=True)
            draw_text("FLY TO SPACE", font_m, CYAN, W//2, 160, center=True)
            self.player.draw()
            draw_text("[ SPACE ] TO TAKE OFF", font_m, YELLOW, W//2, H-120, center=True)
            pygame.display.flip()
            return

        if self.state == "WON":
            draw_iss(W//2, self.win_anim_y)
            for ex in self.explosions: ex.draw()
            self.player.draw()
            if self.win_anim_y >= H//4:
                draw_text("YOU WON", font_b, YELLOW, W//2, H//2+120, center=True)
                draw_text("MISSION COMPLETE", font_m, WHITE, W//2, H//2+170, center=True)
                draw_text("[ SPACE ] TO RETRY", font_s, (170,170,170), W//2, H-50, center=True)
            self.draw_ui()
            pygame.display.flip()
            return

        self.boss.draw()
        for e in self.enemies: e.draw()
        for a in self.asteroids: a.draw()

        if self.state != "OVER":
            for b in self.bullets:
                pygame.draw.line(screen, YELLOW, (b[0],b[1]), (b[0],b[1]-25), 4)
            for b in self.boss_bullets:
                pygame.draw.circle(screen, PURPLE, (int(b[0]),int(b[1])), 8)
                pygame.draw.circle(screen, WHITE, (int(b[0]),int(b[1])), 8, 1)
            for ex in self.explosions: ex.draw()
            self.player.draw()
        else:
            draw_text("MISSION FAILED", font_b, RED, W//2, H//2-20, center=True)
            draw_text("[SPACE] TO RETRY", font_m, WHITE, W//2, H//2+40, center=True)

        self.draw_ui()
        pygame.display.flip()

SND_EXPLOSION = load_sound(EXPLOSION_WAV, 0.45)
SND_GAME_OVER = load_sound(GAME_OVER_WAV, 0.45)
SND_HIT       = load_sound(HIT_WAV, 0.35)
SND_SHOOT     = load_sound(SHOOT_WAV, 0.18) or load_sound(HIT_WAV, 0.12)
SND_VICTORY   = load_sound(VICTORY_WAV, 0.35) or load_sound(HIT_WAV, 0.20)

def main():
    game = Game()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music(); pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN: game.keydown(event.key)
            if event.type == pygame.KEYUP: game.keyup(event.key)
        game.update()
        game.draw()

if __name__ == "__main__":
    main()
