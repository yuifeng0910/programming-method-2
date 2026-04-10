import tkinter as tk, random, json, os # // Khai báo thư viện giao diện, ngẫu nhiên, dữ liệu JSON và hệ thống
from collections import namedtuple # // Hỗ trợ tạo cấu trúc dữ liệu bảng màu cố định

# --- THIẾT LẬP HẰNG SỐ ---
W, H, FPS = 540, 780, 60            # // Chiều rộng, cao màn hình và tốc độ 60 khung hình/giây
ROAD_L, ROAD_R = 85, 455            # // Giới hạn biên trái và biên phải của mặt đường nhựa
LANE_W = (ROAD_R - ROAD_L) / 3      # // Độ rộng mỗi làn đường (chia mặt đường làm 3 làn)
CAR_W, CAR_H = 58, 106              # // Kích thước vật lý của xe ô tô
SAVE_FILE = "high_score.json"       # // Tên file dùng để lưu trữ điểm kỷ lục

# --- QUẢN LÝ MÀU SẮC ---
Col = namedtuple('Col', ['grass', 'road', 'edge', 'lane', 'p_car', 'o_car', 'bar', 'oil', 'tree_t', 'tree_l'])
c = Col("#567d46", "#333333", "#ffffff", "white", "#ffcc00", 
        ["#e63946", "#a8dadc"], "#e63946", "black", "#5d2906", "#0b5345") # // Gán bảng màu Hex cho vật thể

class RacingGame:
    def __init__(self, r): # // Hàm khởi tạo hệ thống khi chạy game
        self.r = r
        self.r.title("Classic Racer")
        # // Tạo Canvas để vẽ đồ họa (màu nền trời xanh)
        self.can = tk.Canvas(r, width=W, height=H, bg="#87CEEB", highlightthickness=0)
        self.can.pack()
        
        self.h_sc = self.load_sc()      # // Tải điểm cao nhất từ file JSON
        self.r.bind("<KeyPress>", self.kd)    # // Lắng nghe sự kiện nhấn phím xuống
        self.r.bind("<KeyRelease>", self.ku)  # // Lắng nghe sự kiện thả phím ra
        self.reset()                    # // Thiết lập các thông số khởi đầu
        self.loop()                     # // Bắt đầu vòng lặp cập nhật liên tục

    def load_sc(self): # // Hàm xử lý file để tải điểm kỷ lục
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f: return json.load(f).get("score", 0)
            except: return 0 # // Trả về 0 nếu file bị lỗi cấu trúc
        return 0

    def reset(self): # // Hàm thiết lập lại toàn bộ trạng thái khi chơi mới
        self.px, self.py = W//2-CAR_W//2, H-150   # // Đặt xe người chơi ở giữa làn cuối đường
        self.obs, self.trees, self.exps = [], [], [] # // Xóa danh sách vật cản, cây và nổ
        self.sc, self.spd, self.fc, self.r_off = 0, 7, 0, 0 # // Reset điểm, tốc độ và bộ đếm
        self.lp = self.rp = False       # // Reset trạng thái nhấn phím
        self.st = "play"                # // Trạng thái: "play" (đang chơi) hoặc "over" (thua)

    def kd(self, e): # // Xử lý logic khi nhấn phím (Key Down)
        k = e.keysym.lower()
        if k in ["left", "a"]: self.lp = True   # // Di chuyển trái
        if k in ["right", "d"]: self.rp = True  # // Di chuyển phải
        # // Nếu đã thua, cho phép nhấn R hoặc Space để chơi lại
        if self.st == "over" and k in ["r", "space"]: self.reset()

    def ku(self, e): # // Xử lý logic khi thả phím (Key Up)
        k = e.keysym.lower()
        if k in ["left", "a"]: self.lp = False
        if k in ["right", "d"]: self.rp = False

    def draw_car(self, x, y, col): # // Hàm vẽ ô tô (bao gồm bóng xe, thân xe, kính và đèn)
        self.can.create_oval(x+5, y+CAR_H-15, x+CAR_W-5, y+CAR_H+5, fill="#222", outline="") # // Bóng
        self.can.create_rectangle(x+8, y+10, x+CAR_W-8, y+CAR_H-10, fill=col, outline="black", width=2) # // Thân
        for gy in [y+25, y+55]: # // Cửa kính xe
            self.can.create_rectangle(x+15, gy, x+CAR_W-15, gy+15, fill="#dff3ff", outline="black")
        for lx in [x+10, x+CAR_W-18]: # // Đèn pha
            self.can.create_oval(lx, y+5, lx+8, y+12, fill="yellow", outline="")

    def up(self): # // HÀM LOGIC CHÍNH: Cập nhật vị trí và tính va chạm
        if self.st != "play": return # // Nếu thua thì dừng mọi logic di chuyển
        
        self.r_off = (self.r_off + self.spd) % 80 # // Tính độ trượt để tạo cảm giác đường đang chạy
        self.fc += 1 # // Tăng bộ đếm khung hình (frame counter)
        
        # // Cập nhật vị trí người chơi và chặn không cho ra khỏi mặt đường nhựa
        if self.lp: self.px = max(ROAD_L+10, self.px - 10)
        if self.rp: self.px = min(ROAD_R-CAR_W-10, self.px + 10)
        
        # // Tạo cây ở lề đường mỗi 25 khung hình
        if self.fc % 25 == 0:
            self.trees.append([random.choice([10, W-70]), -120])
            
        # // Tạo vật cản ngẫu nhiên mỗi 45 khung hình
        if self.fc % 45 == 0:
            t, lx = random.choice(["c", "c", "b", "o"]), ROAD_L + random.randint(0, 2)*LANE_W
            if t=="c": # // Xe địch
                self.obs.append({"t":t,"x":lx+(LANE_W-CAR_W)//2,"y":-120,"w":CAR_W,"h":CAR_H,"c":random.choice(c.o_car)})
            elif t=="b": # // Rào chắn
                self.obs.append({"t":t,"x":lx+(LANE_W-70)//2,"y":-50,"w":70,"h":30})
            elif t=="o": # // Vũng dầu
                self.obs.append({"t":t,"x":lx+(LANE_W-60)//2,"y":-50,"w":60,"h":35})

        # // Cập nhật vị trí cây trôi xuống
        self.trees = [[x, y+self.spd] for x, y in self.trees if y < H]
        
        for o in self.obs[:]: # // Duyệt danh sách vật cản
            o["y"] += self.spd # // Vật cản trôi xuống theo tốc độ game
            # // Thuật toán kiểm tra va chạm AABB (hình chữ nhật đè nhau)
            if self.px < o["x"]+o["w"]-5 and self.px+CAR_W-5 > o["x"] and \
               self.py < o["y"]+o["h"]-5 and self.py+CAR_H-5 > o["y"]:
                self.st = "over" # // Chuyển sang trạng thái thua
                self.exps.append({"x":self.px+CAR_W//2,"y":self.py+CAR_H//2,"f":0}) # // Tạo hiệu ứng nổ
            elif o["y"] > H: # // Nếu vượt qua vật cản thành công
                self.obs.remove(o)
                self.sc += 1 # // Cộng 1 điểm
                if self.sc > self.h_sc: self.h_sc = self.sc # // Cập nhật kỷ lục mới
                # // Cứ mỗi 10 điểm thì tăng tốc độ game thêm 0.5 (tối đa 16)
                if self.sc % 10 == 0: self.spd = min(16, self.spd + 0.5)

    def draw(self): # // HÀM ĐỒ HỌA: Vẽ mọi thứ lên màn hình
        self.can.delete("all") # // Xóa khung hình cũ
        self.can.create_rectangle(0, 0, W, H, fill=c.grass) # // Vẽ cỏ
        self.can.create_rectangle(ROAD_L, 0, ROAD_R, H, fill=c.road, outline="") # // Vẽ đường nhựa
        
        # // Vẽ sọc đỏ/trắng ở hai bên lề đường
        for y in range(int(self.r_off)-80, H, 40):
            col = "red" if (y//40)%2==0 else "white"
            for rx in [ROAD_L-10, ROAD_R]:
                self.can.create_rectangle(rx, y, rx+10, y+40, fill=col, outline="")
            
        # // Vẽ vạch phân làn (vạch đứt)
        for i in range(1,3):
            lx = ROAD_L+i*LANE_W
            for y in range(int(self.r_off)-80, H, 80):
                self.can.create_line(lx, y, lx, y+40, fill=c.lane, width=2)
            
        for x, y in self.trees: # // Vẽ cây xanh
            self.can.create_rectangle(x+22, y+60, x+28, y+95, fill=c.tree_t) # // Thân cây
            for oy, r in [(y+55,25), (y+40,18), (y+15,15)]: # // Tán lá
                self.can.create_oval(x+25-r, oy-r, x+25+r, oy+r, fill=c.tree_l, outline="#083e2f")
            
        for o in self.obs: # // Vẽ vật cản (xe, rào chắn, dầu)
            if o["t"]=="c": self.draw_car(o["x"], o["y"], o["c"])
            elif o["t"]=="b":
                self.can.create_rectangle(o["x"], o["y"], o["x"]+o["w"], o["y"]+o["h"], fill="white", outline="black")
                for sx in range(0, o["w"], 15): # // Vẽ họa tiết sọc trên rào chắn
                    self.can.create_polygon(o["x"]+sx, o["y"], o["x"]+sx+10, o["y"], o["x"]+sx, o["y"]+o["h"], o["x"]+sx-10, o["y"]+o["h"], fill=c.bar, outline="")
            elif o["t"]=="o": # // Vẽ vũng dầu
                self.can.create_oval(o["x"], o["y"], o["x"]+o["w"], o["y"]+o["h"], fill="#111")
                
        if self.st == "play": self.draw_car(self.px, self.py, c.p_car) # // Vẽ xe người chơi
        
        for ex in self.exps[:]: # // Vẽ hiệu ứng nổ (vòng tròn to dần)
            ex["f"] += 1; r = ex["f"]*7
            if ex["f"] > 15: self.exps.remove(ex)
            else: self.can.create_oval(ex["x"]-r, ex["y"]-r, ex["x"]+r, ex["y"]+r, fill="#ff4500", outline="yellow", width=2)
            
        # // Hiển thị bảng điểm
        self.can.create_text(25, 25, text=f"SCORE: {self.sc}  BEST: {self.h_sc}", fill="white", anchor="nw", font=("Arial", 14, "bold"))
        if self.st == "over": # // Hiển thị thông báo khi thua
            self.can.create_text(W//2, H//2, text="GAME OVER\nPress R or Space", fill="red", font=("Arial", 30, "bold"), justify="center")

    def loop(self): # // Vòng lặp chính của trò chơi (Game Loop)
        self.up()   # // Cập nhật dữ liệu
        self.draw() # // Vẽ lại màn hình
        self.r.after(1000//FPS, self.loop) # // Chờ 1/60 giây rồi lặp lại (tạo 60 FPS)

if __name__ == "__main__":
    rt = tk.Tk()
    rt.resizable(0,0) # // Khóa không cho kéo giãn cửa sổ
    RacingGame(rt) # // Chạy trò chơi
    rt.mainloop() # // giữ cửa sổ luôn mở