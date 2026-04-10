import tkinter as tk, random, json, os
from collections import namedtuple

W, H, FPS = 540, 780, 60
ROAD_L, ROAD_R = 85, 455
LANE_W = (ROAD_R - ROAD_L) / 3
CAR_W, CAR_H = 58, 106
SAVE_FILE = "high_score.json"

Col = namedtuple('Col', ['grass', 'road', 'edge', 'lane', 'p_car', 'o_car', 'bar', 'oil', 'tree_t', 'tree_l'])
c = Col("#567d46", "#333333", "#ffffff", "white", "#ffcc00", ["#e63946", "#a8dadc"], "#e63946", "black", "#5d2906", "#0b5345")

class RacingGame:
    def __init__(self, r):
        self.r = r
        self.r.title("Classic Racer")
        self.can = tk.Canvas(r, width=W, height=H, bg="#87CEEB", highlightthickness=0)
        self.can.pack()
        self.h_sc = self.load_sc()
        self.r.bind("<KeyPress>", self.kd)
        self.r.bind("<KeyRelease>", self.ku)
        self.reset()
        self.loop()

    def load_sc(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f: return json.load(f).get("score", 0)
            except: return 0
        return 0

    def reset(self):
        self.px, self.py = W//2-CAR_W//2, H-150
        self.obs, self.trees, self.exps = [], [], []
        self.sc, self.spd, self.fc, self.r_off = 0, 7, 0, 0
        self.lp = self.rp = False
        self.st = "play"

    def kd(self, e):
        k = e.keysym.lower()
        if k in ["left", "a"]: self.lp = True
        if k in ["right", "d"]: self.rp = True
        if self.st == "over" and k in ["r", "space"]: self.reset()

    def ku(self, e):
        k = e.keysym.lower()
        if k in ["left", "a"]: self.lp = False
        if k in ["right", "d"]: self.rp = False

    def draw_car(self, x, y, col):
        self.can.create_oval(x+5, y+CAR_H-15, x+CAR_W-5, y+CAR_H+5, fill="#222", outline="")
        self.can.create_rectangle(x+8, y+10, x+CAR_W-8, y+CAR_H-10, fill=col, outline="black", width=2)
        for gy in [y+25, y+55]:
            self.can.create_rectangle(x+15, gy, x+CAR_W-15, gy+15, fill="#dff3ff", outline="black")
        for lx in [x+10, x+CAR_W-18]:
            self.can.create_oval(lx, y+5, lx+8, y+12, fill="yellow", outline="")

    def up(self):
        if self.st != "play": return
        self.r_off = (self.r_off + self.spd) % 80
        self.fc += 1
        
        if self.lp: self.px = max(ROAD_L+10, self.px - 10)
        if self.rp: self.px = min(ROAD_R-CAR_W-10, self.px + 10)
        
        if self.fc % 25 == 0:
            self.trees.append([random.choice([10, W-70]), -120])
        if self.fc % 45 == 0:
            t, lx = random.choice(["c", "c", "b", "o"]), ROAD_L + random.randint(0, 2)*LANE_W
            if t=="c":
                self.obs.append({"t":t,"x":lx+(LANE_W-CAR_W)//2,"y":-120,"w":CAR_W,"h":CAR_H,"c":random.choice(c.o_car)})
            elif t=="b":
                self.obs.append({"t":t,"x":lx+(LANE_W-70)//2,"y":-50,"w":70,"h":30})
            elif t=="o":
                self.obs.append({"t":t,"x":lx+(LANE_W-60)//2,"y":-50,"w":60,"h":35})

        self.trees = [[x, y+self.spd] for x, y in self.trees if y < H]
        for o in self.obs[:]:
            o["y"] += self.spd
            if self.px < o["x"]+o["w"]-5 and self.px+CAR_W-5 > o["x"] and self.py < o["y"]+o["h"]-5 and self.py+CAR_H-5 > o["y"]:
                self.st = "over"
                self.exps.append({"x":self.px+CAR_W//2,"y":self.py+CAR_H//2,"f":0})
            elif o["y"] > H:
                self.obs.remove(o)
                self.sc += 1
                if self.sc > self.h_sc: self.h_sc = self.sc
                if self.sc % 10 == 0: self.spd = min(16, self.spd + 0.5)

    def draw(self):
        self.can.delete("all")
        self.can.create_rectangle(0, 0, W, H, fill=c.grass)
        self.can.create_rectangle(ROAD_L, 0, ROAD_R, H, fill=c.road, outline="")
        
        for y in range(int(self.r_off)-80, H, 40):
            col = "red" if (y//40)%2==0 else "white"
            for rx in [ROAD_L-10, ROAD_R]:
                self.can.create_rectangle(rx, y, rx+10, y+40, fill=col, outline="")
            
        for i in range(1,3):
            lx = ROAD_L+i*LANE_W
            for y in range(int(self.r_off)-80, H, 80):
                self.can.create_line(lx, y, lx, y+40, fill=c.lane, width=2)
            
        for x, y in self.trees:
            self.can.create_rectangle(x+22, y+60, x+28, y+95, fill=c.tree_t)
            for oy, r in [(y+55,25), (y+40,18), (y+15,15)]:
                self.can.create_oval(x+25-r, oy-r, x+25+r, oy+r, fill=c.tree_l, outline="#083e2f")
            
        for o in self.obs:
            if o["t"]=="c": self.draw_car(o["x"], o["y"], o["c"])
            elif o["t"]=="b":
                self.can.create_rectangle(o["x"], o["y"], o["x"]+o["w"], o["y"]+o["h"], fill="white", outline="black")
                for sx in range(0, o["w"], 15):
                    self.can.create_polygon(o["x"]+sx, o["y"], o["x"]+sx+10, o["y"], o["x"]+sx, o["y"]+o["h"], o["x"]+sx-10, o["y"]+o["h"], fill=c.bar, outline="")
            elif o["t"]=="o":
                self.can.create_oval(o["x"], o["y"], o["x"]+o["w"], o["y"]+o["h"], fill="#111")
                self.can.create_oval(o["x"]+10, o["y"]+5, o["x"]+30, o["y"]+15, fill="#333", outline="")
                
        if self.st == "play": self.draw_car(self.px, self.py, c.p_car)
        
        for ex in self.exps[:]:
            ex["f"] += 1; r = ex["f"]*7
            if ex["f"] > 15: self.exps.remove(ex)
            else: self.can.create_oval(ex["x"]-r, ex["y"]-r, ex["x"]+r, ex["y"]+r, fill="#ff4500", outline="yellow", width=2)
            
        self.can.create_text(25, 25, text=f"SCORE: {self.sc}  BEST: {self.h_sc}", fill="white", anchor="nw", font=("Arial", 14, "bold"))
        if self.st == "over":
            self.can.create_text(W//2, H//2, text="GAME OVER\nPress R or Space", fill="red", font=("Arial", 30, "bold"), justify="center")

    def loop(self):
        self.up()
        self.draw()
        self.r.after(1000//FPS, self.loop)

if __name__ == "__main__":
    rt = tk.Tk()
    rt.resizable(0,0)
    RacingGame(rt)
    rt.mainloop()
    rt.resizable(0,0)
    RacingGame(rt)
    rt.mainloop()