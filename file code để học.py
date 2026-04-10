    import tkinter as tk, random, json, os # // Khai báo thư viện đồ họa, ngẫu nhiên và lưu trữ
    from collections import namedtuple # // Thư viện hỗ trợ tạo cấu trúc dữ liệu màu sắc

    # --- CẤU HÌNH HỆ THỐNG --- # // Thiết lập các thông số cơ bản của trò chơi
    W, H, FPS = 540, 780, 60 # // Thiết lập chiều rộng, chiều cao và tốc độ khung hình
    ROAD_L, ROAD_R = 85, 455 # // Xác định biên bên trái và bên phải của mặt đường
    LANE_W = (ROAD_R - ROAD_L) / 3 # // Chia mặt đường thành 3 làn xe
    CAR_W, CAR_H = 58, 106 # // Kích thước vật lý của xe
    SAVE_FILE = "high_score.json" # // Tên file dùng để lưu trữ điểm kỷ lục

    # --- QUẢN LÝ MÀU SẮC --- # // Bảng màu cho các vật thể trong game
    Col = namedtuple('Col', ['grass', 'road', 'edge', 'lane', 'p_car', 'o_car', 'bar', 'oil', 'tree_t', 'tree_l']) # // Định nghĩa các loại màu
    c = Col("#567d46", "#333333", "#ffffff", "white", "#ffcc00", ["#e63946", "#a8dadc"], "#e63946", "black", "#5d2906", "#0b5345") # // Gán mã màu cụ thể

    class RacingGame:
        def __init__(self, r): # // Hàm khởi tạo khi bắt đầu chạy chương trình
            self.r = r; self.r.title("Classic Racer") # // Tạo cửa sổ và đặt tên game
            self.can = tk.Canvas(r, width=W, height=H, bg="#87CEEB", highlightthickness=0); self.can.pack() # // Tạo màn hình vẽ
            self.h_sc = self.load_sc() # // Tải điểm cao nhất từ bộ nhớ
            self.r.bind("<KeyPress>", self.kd); self.r.bind("<KeyRelease>", self.ku) # // Lắng nghe sự kiện phím bấm
            self.reset(); self.loop() # // Thiết lập trạng thái ban đầu và bắt đầu vòng lặp

        def load_sc(self): # // Hàm tải điểm kỷ lục
            if os.path.exists(SAVE_FILE): # // Kiểm tra nếu file lưu điểm có tồn tại
                try:
                    with open(SAVE_FILE, "r") as f: return json.load(f).get("score", 0) # // Đọc điểm từ file JSON
                except: return 0 # // Nếu file lỗi thì mặc định điểm là 0
            return 0 # // Nếu không có file thì điểm là 0

        def reset(self): # // Hàm thiết lập lại toàn bộ thông số khi chơi mới
            self.px, self.py = W//2-CAR_W//2, H-150 # // Đặt vị trí xe ở giữa làn đường
            self.obs, self.trees, self.exps = [], [], [] # // Xóa danh sách vật cản, cây cối và hiệu ứng nổ
            self.sc, self.spd, self.fc, self.r_off = 0, 7, 0, 0 # // Reset điểm, tốc độ và bộ đếm khung hình
            self.lp = self.rp = False; self.st = "play" # // Reset trạng thái phím và đặt trạng thái đang chơi

        def kd(self, e): # // Xử lý khi nhấn phím xuống
            k = e.keysym.lower() # // Lấy tên phím đang nhấn
            if k in ["left", "a"]: self.lp = True # // Nhấn A hoặc Trái: đi sang trái
            if k in ["right", "d"]: self.rp = True # // Nhấn D hoặc Phải: đi sang phải
            if self.st == "over" and k in ["r", "space"]: self.reset() # // Nếu thua, nhấn R để chơi lại

        def ku(self, e): # // Xử lý khi thả phím ra
            k = e.keysym.lower() # // Lấy tên phím vừa thả
            if k in ["left", "a"]: self.lp = False # // Ngừng di chuyển trái
            if k in ["right", "d"]: self.rp = False # // Ngừng di chuyển phải

        def draw_car(self, x, y, col): # // Hàm vẽ xe chi tiết
            self.can.create_oval(x+5, y+CAR_H-15, x+CAR_W-5, y+CAR_H+5, fill="#222", outline="") # // Vẽ bóng đổ dưới gầm xe
            self.can.create_rectangle(x+8, y+10, x+CAR_W-8, y+CAR_H-10, fill=col, outline="black", width=2) # // Vẽ thân xe chính
            for gy in [y+25, y+55]: self.can.create_rectangle(x+15, gy, x+CAR_W-15, gy+15, fill="#dff3ff", outline="black") # // Vẽ kính xe
            for lx in [x+10, x+CAR_W-18]: self.can.create_oval(lx, y+5, lx+8, y+12, fill="yellow", outline="") # // Vẽ đèn pha

        def up(self): # // Hàm cập nhật logic game
            if self.st != "play": return # // Nếu không phải đang chơi thì dừng cập nhật
            self.r_off = (self.r_off + self.spd) % 80; self.fc += 1 # // Cập nhật vạch đường và bộ đếm
            
            if self.lp: self.px = max(ROAD_L+10, self.px - 10) # // Di chuyển trái và chặn biên lề
            if self.rp: self.px = min(ROAD_R-CAR_W-10, self.px + 10) # // Di chuyển phải và chặn biên lề
            
            if self.fc % 25 == 0: self.trees.append([random.choice([10, W-70]), -120]) # // Tạo cây mới ở lề đường
            if self.fc % 45 == 0: # // Tạo chướng ngại vật mới
                t, lx = random.choice(["c", "c", "b", "o"]), ROAD_L + random.randint(0, 2)*LANE_W # // Chọn loại vật cản
                if t=="c": self.obs.append({"t":t,"x":lx+(LANE_W-CAR_W)//2,"y":-120,"w":CAR_W,"h":CAR_H,"c":random.choice(c.o_car)}) # // Thêm xe địch
                elif t=="b": self.obs.append({"t":t,"x":lx+(LANE_W-70)//2,"y":-50,"w":70,"h":30}) # // Thêm rào chắn
                elif t=="o": self.obs.append({"t":t,"x":lx+(LANE_W-60)//2,"y":-50,"w":60,"h":35}) # // Thêm vũng dầu

            self.trees = [[x, y+self.spd] for x, y in self.trees if y < H] # // Cập nhật vị trí cây trôi xuống
            for o in self.obs[:]: # // Kiểm tra từng vật cản
                o["y"] += self.spd # // Cập nhật vị trí vật cản trôi xuống
                if self.px < o["x"]+o["w"]-5 and self.px+CAR_W-5 > o["x"] and self.py < o["y"]+o["h"]-5 and self.py+CAR_H-5 > o["y"]: # // Va chạm
                    self.st = "over"; self.exps.append({"x":self.px+CAR_W//2,"y":self.py+CAR_H//2,"f":0}) # // Xử lý khi va chạm
                elif o["y"] > H: # // Nếu vượt qua vật cản an toàn
                    self.obs.remove(o); self.sc += 1 # // Xóa vật cản và tăng điểm
                    if self.sc > self.h_sc: self.h_sc = self.sc # // Cập nhật kỷ lục mới
                    if self.sc % 10 == 0: self.spd = min(16, self.spd + 0.5) # // Tăng độ khó mỗi 10 điểm

        def draw(self): # // Hàm vẽ đồ họa
            self.can.delete("all") # // Xóa màn hình cũ
            self.can.create_rectangle(0, 0, W, H, fill=c.grass) # // Vẽ cỏ
            self.can.create_rectangle(ROAD_L, 0, ROAD_R, H, fill=c.road, outline="") # // Vẽ mặt đường
            
            for y in range(int(self.r_off)-80, H, 40): # // Vẽ sọc lề đường đỏ trắng
                col = "red" if (y//40)%2==0 else "white" # // Xen kẽ màu đỏ và trắng
                for rx in [ROAD_L-10, ROAD_R]: self.can.create_rectangle(rx, y, rx+10, y+40, fill=col, outline="") # // Vẽ lề
                
            for i in range(1,3): # // Vẽ vạch phân làn
                lx = ROAD_L+i*LANE_W
                for y in range(int(self.r_off)-80, H, 80): self.can.create_line(lx, y, lx, y+40, fill=c.lane, width=2) # // Vạch đứt
                
            for x, y in self.trees: # // Vẽ cây cối
                self.can.create_rectangle(x+22, y+60, x+28, y+95, fill=c.tree_t) # // Thân cây
                for oy, r in [(y+55,25), (y+40,18), (y+15,15)]: self.can.create_oval(x+25-r, oy-r, x+25+r, oy+r, fill=c.tree_l, outline="#083e2f") # // Tán lá
                
            for o in self.obs: # // Vẽ vật cản
                if o["t"]=="c": self.draw_car(o["x"], o["y"], o["c"]) # // Xe địch
                elif o["t"]=="b": # // Rào chắn
                    self.can.create_rectangle(o["x"], o["y"], o["x"]+o["w"], o["y"]+o["h"], fill="white", outline="black") # // Khung rào
                    for sx in range(0, o["w"], 15): self.can.create_polygon(o["x"]+sx, o["y"], o["x"]+sx+10, o["y"], o["x"]+sx, o["y"]+o["h"], o["x"]+sx-10, o["y"]+o["h"], fill=c.bar, outline="") # // Sọc đỏ
                elif o["t"]=="o": # // Vũng dầu
                    self.can.create_oval(o["x"], o["y"], o["x"]+o["w"], o["y"]+o["h"], fill="#111") # // Dầu đen
                    self.can.create_oval(o["x"]+10, o["y"]+5, o["x"]+30, o["y"]+15, fill="#333", outline="") # // Bóng dầu
                    
            if self.st == "play": self.draw_car(self.px, self.py, c.p_car) # // Vẽ xe người chơi
            
            for ex in self.exps[:]: # // Vẽ hiệu ứng nổ
                ex["f"] += 1; r = ex["f"]*7 # // Vòng nổ to dần
                if ex["f"] > 15: self.exps.remove(ex) # // Xóa khi kết thúc nổ
                else: self.can.create_oval(ex["x"]-r, ex["y"]-r, ex["x"]+r, ex["y"]+r, fill="#ff4500", outline="yellow", width=2) # // Hình tròn lửa
                
            self.can.create_text(25, 25, text=f"SCORE: {self.sc}  BEST: {self.h_sc}", fill="white", anchor="nw", font=("Arial", 14, "bold")) # // Hiển thị điểm
            if self.st == "over": self.can.create_text(W//2, H//2, text="GAME OVER\nPress R", fill="red", font=("Arial", 30, "bold"), justify="center") # // Báo thua

        def loop(self): # // Vòng lặp chính
            self.up(); self.draw() # // Cập nhật và vẽ lại
            self.r.after(1000//FPS, self.loop) # // Lặp lại sau mỗi 1/60 giây

    if __name__ == "__main__": # // Chạy chương trình
        rt = tk.Tk(); rt.resizable(0,0) # // Khởi tạo cửa sổ cố định kích thước
        RacingGame(rt) # // Khởi tạo game
        rt.mainloop() # // Giữ cửa sổ luôn mở