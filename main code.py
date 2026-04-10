import tkinter as tk
import random
import math

# --- CẤU HÌNH ---
W, H = 540, 780
FPS = 60

Col = {
    "bg": "#02050a",
    "p_cockpit": "#00f2fe",
    "p_body": "#1c1c1c",
    "p_wing": "#cc0000",
    "laser": "#ffff00",
    "b_laser": "#ff00ff", # Màu đạn Boss (Hồng)
    "e_body": "#4a4e69",
    "rock": "#3d2b1f",
    "rock_crack": "#261a13",
    "ally_hp": "#2ecc71"
}

class BossGoliath:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x, self.y = W//2, 100
        self.hp = 200 # Máu Boss cực lớn
        self.max_hp = 200
        self.fire_rate = 60 # Boss bắn mỗi 60 frame

    def draw(self):
        # Thanh máu Boss trên cùng
        self.canvas.create_rectangle(50, 20, W-50, 30, fill="black", outline="white")
        self.canvas.create_rectangle(50, 20, 50 + ((self.hp/self.max_hp)*(W-100)), 30, fill="#e74c3c", outline="")
        self.canvas.create_text(W//2, 45, text=f"BOSS GOLIATH: {self.hp} HP", fill="white", font=("Impact", 12))

        # Thân Boss khổng lồ (Vẽ dạng khối 3D phức tạp)
        self.canvas.create_rectangle(self.x-120, self.y-50, self.x+120, self.y+50, fill="#2c3e50", outline="white", width=3)
        self.canvas.create_rectangle(self.x-80, self.y+50, self.x+80, self.y+80, fill="#34495e", outline="white", width=2)
        # 2 Cánh pháo hai bên
        self.canvas.create_polygon(self.x-120, self.y, self.x-180, self.y+30, self.x-120, self.y+60, fill="#1a1a1b", outline="white")
        self.canvas.create_polygon(self.x+120, self.y, self.x+180, self.y+30, self.x+120, self.y+60, fill="#1a1a1b", outline="white")
        # 3 Động cơ hạt nhân nhấp nháy
        for i in [-60, 0, 60]:
            col = random.choice(["#ff4500", "#ff8c00"])
            self.canvas.create_oval(self.x+i-15, self.y-70, self.x+i+15, self.y-40, fill=col, outline="")

class InfiniteSkyForce:
    def __init__(self, root):
        self.root = root
        self.root.title("Sky Force: Boss Goliath")
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
        self.base_fire_rate = 15
        self.bullet_count = 1
        self.enemy_speed = 4
        self.win_anim_y = H + 300 
        self.last_rock_x = -100 
        self.keys = {"left": False, "right": False, "up": False, "down": False}
        
        # Khởi tạo Boss
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

    def create_explosion(self, x, y, color="#ff4500", mr=50):
        self.explosions.append({"x": x, "y": y, "r": 5, "max_r": mr, "color": color})

    def draw_player(self, x, y):
        f_col = random.choice(["#00f2fe", "#ffffff", "#4facfe"])
        self.canvas.create_oval(x-7, y+35, x+7, y+65, fill=f_col, outline="")
        self.canvas.create_polygon(x, y-45, x+50, y+20, x, y+10, x-50, y+20, fill=Col["p_body"], outline="white")
        self.canvas.create_rectangle(x-40, y+5, x-20, y+10, fill=Col["p_wing"], outline="")
        self.canvas.create_rectangle(x+20, y+5, x+40, y+10, fill=Col["p_wing"], outline="")
        self.canvas.create_oval(x-6, y-25, x+6, y-5, fill=Col["p_cockpit"])

    def draw_enemy(self, x, y):
        self.canvas.create_rectangle(x-35, y-15, x+35, y+15, fill=Col["e_body"], outline="black", width=2)
        # ... (Vẽ địch chi tiết hơn...)
        self.canvas.create_rectangle(x-12, y-30, x+12, y-15, fill="#ff4d4d")
        self.canvas.create_oval(x-28, y+2, x-18, y+20, fill="#ffd700", outline="")
        self.canvas.create_oval(x+18, y+2, x+28, y+20, fill="#ffd700", outline="")

    def draw_rock(self, x, y):
        self.canvas.create_oval(x-38, y-38, x+38, y+38, fill=Col["rock"], outline=Col["rock_crack"], width=3)
        self.canvas.create_oval(x-15, y-15, x+5, y+5, fill=Col["rock_crack"], outline="")

    def draw_ally(self, x, y):
        self.canvas.create_rectangle(x-40, y-5, x+40, y+5, fill="#1abc9c", outline="white")
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#ecf0f1", outline="#2980b9", width=2)

    def spawn_objects(self):
        if self.state != "PLAYING": return
        self.enemy_speed = 4 + (self.score // 70)
        spawn_interval = max(20, 50 - (self.score // 40))

        if self.frame % spawn_interval == 0:
            rand = random.random()
            new_x = random.randint(60, W-60)
            if abs(new_x - self.last_rock_x) < 80: new_x = (new_x + 150) % (W - 120) + 60

            if rand < 0.12: # Ít thiên thạch
                self.objects.append({"t": "rock", "x": new_x, "y": -80, "hp": 999, "s": self.enemy_speed - 1})
                self.last_rock_x = new_x 
            elif rand < 0.85: # Kẻ địch
                hp = 3 + (self.score // 70)
                self.objects.append({"t": "enemy", "x": new_x, "y": -60, "hp": hp, "max_hp": hp, "s": self.enemy_speed})
            else: # Đồng minh
                self.objects.append({"t": "ally", "x": new_x, "y": -60, "hp": 2, "max_hp": 2, "s": self.enemy_speed})

    def update(self):
        if self.state == "WON":
            if self.win_anim_y > H//2: self.win_anim_y -= 1.5
            if self.py > self.win_anim_y + 120: self.py -= 0.5
            return

        if self.state != "PLAYING" : return
        self.frame += 1

        # --- LOGIC BOSS BẮN ĐẠN ---
        if self.boss.hp > 0 and self.frame % self.boss.fire_rate == 0:
            # Boss bắn 5 tia đạn hồng random hướng xuống
            for i in range(5):
                angle = random.uniform(math.pi/4, 3*math.pi/4) # Random hướng từ 45đ đến 135đ
                speed = random.uniform(5, 9) # Tốc độ random
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                self.b_bullets.append([self.boss.x, self.boss.y+80, dx, dy])

        # Cập nhật đạn Boss
        for bb in self.b_bullets[:]:
            bb[0] += bb[2] # Di chuyển x
            bb[1] += bb[3] # Di chuyển y
            # Va chạm đạn Boss với người chơi
            if abs(bb[0] - self.px) < 35 and abs(bb[1] - self.py) < 35:
                self.create_explosion(self.px, self.py, "red", mr=70)
                self.state = "OVER"
            if bb[1] > H or bb[0] < 0 or bb[0] > W: self.b_bullets.remove(bb)

        # TIẾN HÓA ĐẠN NGƯỜI CHƠI THEO MỐC (GIỮ NGUYÊN)
        fire_boost = self.score // 20
        current_fire_rate = max(5, self.base_fire_rate - fire_boost)
        if self.score >= 300: self.bullet_count = 3
        elif self.score >= 150: self.bullet_count = 2
        else: self.bullet_count = 1

        # Di chuyển người chơi
        if self.keys["left"] and self.px > 60: self.px -= 9
        if self.keys["right"] and self.px < W-60: self.px += 9
        if self.keys["up"] and self.py > 60: self.py -= 9
        if self.keys["down"] and self.py < H-60: self.py += 9

        # Người chơi bắn đạn
        if self.frame % current_fire_rate == 0:
            if self.bullet_count == 1: self.bullets.append([self.px, self.py-40])
            elif self.bullet_count == 2:
                self.bullets.append([self.px-20, self.py-30]); self.bullets.append([self.px+20, self.py-30])
            elif self.bullet_count == 3:
                self.bullets.append([self.px, self.py-50]); self.bullets.append([self.px-35, self.py-10]); self.bullets.append([self.px+35, self.py-10])

        for b in self.bullets[:]:
            b[1] -= 16
            
            # Đạn trúng Boss
            if self.boss.hp > 0 and abs(b[0] - self.boss.x) < 120 and abs(b[1] - self.boss.y) < 80:
                self.boss.hp -= 1
                self.bullets.remove(b)
                self.score += 5 # Bắn trúng boss được điểm
                if self.boss.hp <= 0:
                    self.create_explosion(self.boss.x, self.boss.y, "orange", mr=200)
                    self.state = "WON"
                    self.score += 1000 # Điểm thưởng thắng Boss
                    self.objects.clear(); self.bullets.clear(); self.b_bullets.clear()
            elif b[1] < -50: self.bullets.remove(b)

        # Xử lý Vật thể và va chạm (Giữ nguyên logic)
        for o in self.objects[:]:
            o["y"] += o["s"]
            for b in self.bullets[:]:
                if abs(o["x"] - b[0]) < 38 and abs(o["y"] - b[1]) < 38:
                    if b in self.bullets: self.bullets.remove(b)
                    o["hp"] -= 1
                    if o["hp"] <= 0:
                        self.create_explosion(o["x"], o["y"], "#ffcc00")
                        if o["t"] == "enemy": self.objects.remove(o); self.score += 20
                        elif o["t"] == "ally": self.objects.remove(o); self.score -= 150
            if abs(o["x"] - self.px) < 50 and abs(o["y"] - self.py) < 50:
                self.create_explosion(self.px, self.py, "red", mr=70)
                self.state = "OVER"
            if o["y"] > H + 100: self.objects.remove(o)

        for ex in self.explosions[:]:
            ex["r"] += 5
            if ex["r"] > ex["max_r"]: self.explosions.remove(ex)

        self.spawn_objects()

    def draw(self):
        self.canvas.delete("all")
        if self.state == "START":
            self.canvas.create_text(W//2, H//3, text="SKY FORCE\nBOSS GOLIATH", fill=Col["p_cockpit"], font=("Impact", 45), justify="center")
            self.canvas.create_text(W//2, H//2+50, text="Né đạn Boss & Tiêu diệt Goliath (200 HP)\n300đ: Bắn 3 tia | Giữ nguyên tiến hóa", fill="white", font=("Arial", 14), justify="center")
            self.canvas.create_text(W//2, H-120, text="[ SPACE TO START MISSION ]", fill="#ffff00", font=("Arial", 18, "bold"))
            return

        if self.boss.hp > 0: self.boss.draw() # Vẽ Boss

        if self.state == "WON":
            ty = self.win_anim_y
            self.canvas.create_rectangle(W//2-80, ty, W//2+80, ty+200, fill="#1c1c1c", outline="white", width=3)
            self.canvas.create_oval(W//2-50, ty-50, W//2+50, ty+50, fill=Col["p_cockpit"], outline="white")
            self.canvas.create_text(W//2, H//3, text="MISSION COMPLETE", fill="#2ecc71", font=("Impact", 45))
            self.canvas.create_text(W//2, H//3+60, text="Vũ trụ đã bình yên!", fill="white", font=("Arial", 16))

        # Vẽ Chướng ngại vật
        for o in self.objects:
            if o["t"] == "enemy": self.draw_enemy(o["x"], o["y"])
            elif o["t"] == "rock": self.draw_rock(o["x"], o["y"])
            elif o["t"] == "ally": self.draw_ally(o["x"], o["y"])
            if o["t"] != "rock":
                hp_color = "red" if o["t"] == "enemy" else Col["ally_hp"]
                self.canvas.create_rectangle(o["x"]-25, o["y"]-40, o["x"]+25, o["y"]-36, fill="black")
                self.canvas.create_rectangle(o["x"]-25, o["y"]-40, o["x"]-25+(o["hp"]/o["max_hp"]*50), o["y"]-36, fill=hp_color)

        # Vẽ đạn
        for b in self.bullets: self.canvas.create_line(b[0], b[1], b[0], b[1]-25, fill=Col["laser"], width=4)
        for bb in self.b_bullets: self.canvas.create_oval(bb[0]-8, bb[1]-8, bb[0]+8, bb[1]+8, fill=Col["b_laser"], outline="white") # Đạn Boss hồng
        
        for ex in self.explosions: self.canvas.create_oval(ex["x"]-ex["r"], ex["y"]-ex["r"], ex["x"]+ex["r"], ex["y"]+ex["r"], fill=ex["color"], outline="white")

        # Vẽ người chơi
        if self.state != "OVER": self.draw_player(self.px, self.py)
        else: self.canvas.create_text(W//2, H//2, text="MISSION FAILED\n[SPACE] TO RESPOND", fill="#ff4757", font=("Impact", 35), justify="center")
        
        # Dashboard
        self.canvas.create_text(15, H-30, text=f"SCORE: {self.score} | Lửa delay: {self.base_fire_rate - (self.score//20)}", fill="white", anchor="nw", font=("Arial", 10))

    def run(self):
        self.update(); self.draw()
        self.root.after(1000//FPS, self.run)

if __name__ == "__main__":
    rt = tk.Tk(); rt.resizable(False, False)
    InfiniteSkyForce(rt); rt.mainloop()
