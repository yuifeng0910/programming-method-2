import tkinter as tk
import random
import math

# --- CẤU HÌNH HỆ THỐNG ---
W, H = 640, 780
FPS = 60

Col = {
    "bg": "#02050a",
    "p_cockpit": "#00f2fe",
    "p_body": "#2c3e50",
    "p_wing": "#e74c3c",
    "laser": "#ffff00",
    "b_laser": "#ff00ff", 
    "e_body": "#4b4b4b",
    "e_wing": "#8e44ad",
    "rock": "#3d2b1f",
    "ally_hp": "#2ecc71",
    "station": "#bdc3c7",
    "gold": "#f1c40f"
}

class BossGoliath:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x, self.y = W//2, -250
        self.hp = 400 
        self.max_hp = 400
        self.fire_rate = 55
        self.active = False
        self.dead = False

    def update(self):
        if self.active and not self.dead and self.y < 130:
            self.y += 1.5

    def draw(self):
        if not self.active or self.dead: return
        # Thanh HP Boss
        self.canvas.create_rectangle(100, 20, W-100, 32, fill="#1a1a1a", outline="#ffffff", width=2)
        self.canvas.create_rectangle(100, 20, 100 + ((self.hp/self.max_hp)*(W-200)), 32, fill="#c0392b", outline="")
        self.canvas.create_text(W//2, 45, text=f"BOSS GOLIATH: {self.hp} HP", fill="white", font=("Fixedsys", 11, "bold"))
        # Thân Boss
        self.canvas.create_rectangle(self.x-130, self.y-60, self.x+130, self.y+40, fill="#2c3e50", outline="white", width=2)
        for s in [-1, 1]:
            self.canvas.create_polygon(self.x+s*130, self.y-20, self.x+s*190, self.y+30, self.x+s*130, self.y+70, fill="#1a1a1b", outline="red")

class InfiniteSkyForce:
    def __init__(self, root):
        self.root = root
        self.root.title("Nhiệm vụ: Phạm Tuân bay lên vũ trụ an toàn")
        self.canvas = tk.Canvas(root, width=W, height=H, bg=Col["bg"], highlightthickness=0)
        self.canvas.pack()
        self.setup_game()
        self.root.bind("<KeyPress>", self.keydown)
        self.root.bind("<KeyRelease>", self.keyup)
        self.run()

    def setup_game(self):
        self.state = "START" 
        self.px, self.py = W//2, H-120
        self.bullets, self.b_bullets, self.objects, self.explosions = [], [], [], []
        self.score, self.frame = 0, 0
        self.base_fire_rate = 14
        self.win_anim_y = -300 
        self.keys = {"left": False, "right": False, "up": False, "down": False}
        self.boss = BossGoliath(self.canvas)

    def keydown(self, e):
        k = e.keysym.lower()
        if k in ["left", "a"]: self.keys["left"] = True
        if k in ["right", "d"]: self.keys["right"] = True
        if k in ["up", "w"]: self.keys["up"] = True
        if k in ["down", "s"]: self.keys["down"] = True
        if self.state in ["START", "OVER", "WON"] and e.keysym == "space":
            self.setup_game(); self.state = "PLAYING"

    def keyup(self, e):
        k = e.keysym.lower()
        if k in ["left", "a"]: self.keys["left"] = False
        if k in ["right", "d"]: self.keys["right"] = False
        if k in ["up", "w"]: self.keys["up"] = False
        if k in ["down", "s"]: self.keys["down"] = False

    def create_explosion(self, x, y, color="#ff4500", mr=60):
        self.explosions.append({"x": x, "y": y, "r": 5, "max_r": mr, "color": color})

    def draw_player(self, x, y):
        flame = random.choice(["#00f2fe", "#ffffff"])
        self.canvas.create_polygon(x-10, y+30, x, y+60, x+10, y+30, fill=flame)
        self.canvas.create_polygon(x, y-45, x+45, y+20, x, y+5, x-45, y+20, fill=Col["p_body"], outline="white")
        self.canvas.create_oval(x-7, y-25, x+7, y-5, fill=Col["p_cockpit"], outline="white")

    def draw_enemy(self, x, y, hp=1, m_hp=1):
        self.canvas.create_rectangle(x-30, y-15, x+30, y+10, fill=Col["e_body"], outline="white")
        self.canvas.create_polygon(x-30, y-5, x-50, y+15, x-30, y+15, fill=Col["e_wing"], outline="black")
        self.canvas.create_polygon(x+30, y-5, x+50, y+15, x+30, y+15, fill=Col["e_wing"], outline="black")
        self.canvas.create_rectangle(x-25, y-35, x+25, y-31, fill="#1a1a1a")
        self.canvas.create_rectangle(x-25, y-35, x-25+(hp/m_hp*50), y-31, fill="#ff4d4d", outline="")

    def draw_ally(self, x, y, hp=100, m_hp=100):
        self.canvas.create_rectangle(x-40, y-5, x+40, y+5, fill="#1abc9c", outline="white")
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#ecf0f1", outline="#2980b9", width=2)
        self.canvas.create_rectangle(x-25, y-25, x+25, y-21, fill="#1a1a1a")
        self.canvas.create_rectangle(x-25, y-25, x-25+(hp/m_hp*50), y-21, fill=Col["ally_hp"], outline="")

    def update(self):
        if self.state == "WON":
            # Hoạt cảnh trạm vũ trụ hạ xuống
            if self.win_anim_y < H//3: self.win_anim_y += 2
            # Máy bay tự động bay vào trạm
            if self.py > self.win_anim_y + 40: self.py -= 3
            if self.px < W//2: self.px += 2
            elif self.px > W//2: self.px -= 2
            return

        if self.state != "PLAYING" : return
        self.frame += 1

        if self.score >= 400 and not self.boss.active:
            self.boss.active = True
            self.objects.clear()

        if self.boss.active and not self.boss.dead:
            self.boss.update()
            if self.boss.hp > 0 and self.frame % self.boss.fire_rate == 0:
                for _ in range(5):
                    ang = random.uniform(0.6, 2.5)
                    s = random.uniform(5, 8)
                    self.b_bullets.append([self.boss.x, self.boss.y+60, math.cos(ang)*s, math.sin(ang)*s])

        # Đạn Boss
        for bb in self.b_bullets[:]:
            bb[0] += bb[2]; bb[1] += bb[3]
            if abs(bb[0]-self.px)<35 and abs(bb[1]-self.py)<35: self.state = "OVER"
            if bb[1]>H or bb[1]<-100 or bb[0]<0 or bb[0]>W:
                if bb in self.b_bullets: self.b_bullets.remove(bb)

        # Di chuyển
        if self.keys["left"] and self.px > 50: self.px -= 8
        if self.keys["right"] and self.px < W-50: self.px += 8
        if self.keys["up"] and self.py > 50: self.py -= 8
        if self.keys["down"] and self.py < H-50: self.py += 8

        # Bắn đạn
        rate = max(5, self.base_fire_rate - (self.score // 25))
        if self.frame % rate == 0:
            bc = 3 if self.score >= 300 else (2 if self.score >= 150 else 1)
            if bc == 1: self.bullets.append([self.px, self.py-40])
            elif bc == 2: self.bullets.extend([[self.px-18, self.py-30], [self.px+18, self.py-30]])
            else: self.bullets.extend([[self.px, self.py-50], [self.px-35, self.py-10], [self.px+35, self.py-10]])

        # Update Đạn người chơi
        for b in self.bullets[:]:
            b[1] -= 16
            if self.boss.active and not self.boss.dead:
                if abs(b[0]-self.boss.x)<130 and abs(b[1]-self.boss.y)<70:
                    self.boss.hp -= 1
                    if b in self.bullets: self.bullets.remove(b)
                    if self.boss.hp <= 0:
                        self.boss.dead = True
                        self.b_bullets.clear() # XÓA HẾT ĐẠN BOSS KHI CHẾT
                        self.create_explosion(self.boss.x, self.boss.y, "orange", 300)
                        self.state = "WON"
                    continue
            if b[1] < -50:
                if b in self.bullets: self.bullets.remove(b)

        # Update Vật thể
        for o in self.objects[:]:
            o["y"] += o["s"]
            for b in self.bullets[:]:
                if abs(o["x"]-b[0])<45 and abs(o["y"]-b[1])<45:
                    if b in self.bullets: self.bullets.remove(b)
                    o["hp"] -= 1
                    if o["hp"] <= 0:
                        self.create_explosion(o["x"], o["y"], "#f1c40f" if o["t"]=="enemy" else "#2ecc71")
                        self.score += 20 if o["t"]=="enemy" else -100
                        if o in self.objects: self.objects.remove(o)
                        break
            if o in self.objects and abs(o["x"]-self.px)<45 and abs(o["y"]-self.py)<45:
                if o["t"] != "ally": self.state = "OVER"
            if o in self.objects and o["y"] > H + 100: self.objects.remove(o)

        for ex in self.explosions[:]:
            ex["r"] += 4
            if ex["r"] > ex["max_r"]: self.explosions.remove(ex)
        
        if not self.boss.active:
            if self.frame % 45 == 0:
                nx = random.randint(100, W-100)
                rand = random.random()
                if rand < 0.15: self.objects.append({"t": "rock", "x": nx, "y": -80, "hp": 999, "s": 4})
                elif rand < 0.93: self.objects.append({"t": "enemy", "x": nx, "y": -60, "hp": 3+(self.score//100), "max_hp": 3+(self.score//100), "s": 5})
                else: self.objects.append({"t": "ally", "x": nx, "y": -60, "hp": 100, "max_hp": 100, "s": 4})

    def draw(self):
        self.canvas.delete("all")
        if self.state == "START":
            self.canvas.create_text(W//2, 80, text="NHIỆM VỤ CẤP CAO", fill="#ff4757", font=("Impact", 45))
            self.canvas.create_text(W//2, 160, text="Giúp Phạm Tuân bay lên vũ trụ an toàn", fill="#00f2fe", font=("Fixedsys", 18, "bold"))
            self.canvas.create_rectangle(60, 220, W-60, 360, outline="red", width=2, fill="#1a0000")
            self.draw_enemy(120, 290); self.canvas.create_text(180, 260, text="KẺ THÙ (MÁU ĐỎ)", fill="#ff4d4d", anchor="nw", font=("Arial", 16, "bold"))
            self.canvas.create_rectangle(60, 380, W-60, 520, outline=Col["ally_hp"], width=2, fill="#001a00")
            self.draw_ally(120, 450); self.canvas.create_text(180, 420, text="ĐỒNG MINH (MÁU XANH)", fill=Col["ally_hp"], anchor="nw", font=("Arial", 16, "bold"))
            self.canvas.create_text(W//2, H-100, text="NHẤN [ SPACE ] ĐỂ CẤT CÁNH", fill="#f1c40f", font=("Fixedsys", 22, "bold"))
            return

        if self.state == "WON":
            # Vẽ trạm vũ trụ
            tx, ty = W//2, self.win_anim_y
            self.canvas.create_rectangle(tx-200, ty-40, tx+200, ty+10, fill=Col["station"], outline="white", width=2)
            self.canvas.create_rectangle(tx-50, ty+10, tx+50, ty+60, fill="#34495e", outline="white")
            self.canvas.create_text(tx, ty-15, text="TRẠM VŨ TRỤ QUỐC TẾ (ISS)", fill="black", font=("Arial", 12, "bold"))
            if self.win_anim_y >= H//3:
                self.canvas.create_text(W//2, H//2+100, text="BẠN ĐÃ CHIẾN THẮNG!", fill=Col["gold"], font=("Impact", 40))
                self.canvas.create_text(W//2, H//2+160, text="PHẠM TUÂN ĐÃ CẬP BẾN AN TOÀN", fill="white", font=("Fixedsys", 16))
                self.canvas.create_text(W//2, H-50, text="NHẤN [ SPACE ] ĐỂ CHƠI LẠI", fill="#555", font=("Fixedsys", 12))

        self.boss.draw()
        for o in self.objects:
            if o["t"]=="enemy": self.draw_enemy(o["x"], o["y"], o["hp"], o["max_hp"])
            elif o["t"]=="rock": self.canvas.create_oval(o["x"]-35, o["y"]-35, o["x"]+35, o["y"]+35, fill=Col["rock"])
            else: self.draw_ally(o["x"], o["y"], o["hp"], o["max_hp"])
        
        for b in self.bullets: self.canvas.create_line(b[0], b[1], b[0], b[1]-25, fill=Col["laser"], width=4)
        for bb in self.b_bullets: self.canvas.create_oval(bb[0]-8, bb[1]-8, bb[0]+8, bb[1]+8, fill=Col["b_laser"], outline="white")
        for ex in self.explosions: self.canvas.create_oval(ex["x"]-ex["r"], ex["y"]-ex["r"], ex["x"]+ex["r"], ex["y"]+ex["r"], fill=ex["color"], outline="white")

        if self.state != "OVER": self.draw_player(self.px, self.py)
        else: self.canvas.create_text(W//2, H//2, text="MISSION FAILED\n[SPACE] TO RETRY", fill="#ff4757", font=("Impact", 40))
        
        if self.state == "PLAYING":
            self.canvas.create_text(15, H-30, text=f"SCORE: {self.score} | GOAL: 400", fill="white", anchor="nw", font=("Fixedsys", 12))

    def run(self):
        try:
            self.update(); self.draw()
            self.root.after(1000//FPS, self.run)
        except: pass

if __name__ == "__main__":
    rt = tk.Tk(); rt.resizable(False, False)
    InfiniteSkyForce(rt); rt.mainloop()
