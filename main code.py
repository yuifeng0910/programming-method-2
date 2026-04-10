import pygame
import random
import sys

# --- CẤU HÌNH HỆ THỐNG ---
WIDTH, HEIGHT = 500, 750
FPS = 60

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 50, 50)
BLUE  = (50, 150, 255)
GOLD  = (255, 215, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sky Force: ATM Transaction Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.pixel_font = pygame.font.SysFont("Courier", 30, bold=True)
        
        # Trạng thái dựa trên sơ đồ bạn gửi
        # READ_CARD -> READ_PIN -> CHOOSE_TRANS -> PLAYING -> EJECT
        self.state = "READ_CARD"
        self.reset_game_data()

    def reset_game_data(self):
        """Khởi tạo dữ liệu máy bay chiến đấu"""
        self.player_pos = [WIDTH // 2, HEIGHT - 100]
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.frame_count = 0

    def draw_text(self, text, y, color=WHITE, center=True):
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, y)) if center else surf.get_rect(topleft=(20, y))
        self.screen.blit(surf, rect)

    # --- LOGIC CÁC TRẠNG THÁI (DỰA TRÊN SƠ ĐỒ) ---

    def state_read_card(self):
        self.screen.fill((40, 44, 52))
        self.draw_text("HỆ THỐNG ATM SKY FORCE", 100, GOLD)
        self.draw_text("Vui lòng 'Insert Card' để bắt đầu", 300)
        self.draw_text("Nhấn [SPACE] để đưa thẻ vào", 500, BLUE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "READ_PIN"

    def state_read_pin(self):
        self.screen.fill((40, 44, 52))
        self.draw_text("NHẬP MÃ PIN", 100, BLUE)
        self.draw_text("**** ", 300, WHITE)
        self.draw_text("Nhấn [ENTER] để xác nhận PIN hợp lệ", 500, WHITE)
        self.draw_text("Nhấn [ESC] để hủy (Transaction Cancel)", 550, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: self.state = "CHOOSE_TRANS"
                if event.key == pygame.K_ESCAPE: self.state = "EJECT_CARD"

    def state_choose_transaction(self):
        self.screen.fill((40, 44, 52))
        self.draw_text("CHỌN GIAO DỊCH", 100, GOLD)
        self.draw_text("1. Rút tiền nhanh", 250)
        self.draw_text("2. SKY FORCE MISSION (Start Game)", 320, BLUE)
        self.draw_text("Nhấn [2] để bắt đầu chiến dịch", 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.reset_game_data()
                self.state = "PLAYING"

    # --- TRẠNG THÁI CHƠI GAME (PIXEL ART STYLE) ---

    def state_playing(self):
        self.screen.fill((20, 30, 60)) # Nền trời đêm
        self.frame_count += 1

        # 1. Xử lý di chuyển máy bay
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_pos[0] > 40: self.player_pos[0] -= 7
        if keys[pygame.K_RIGHT] and self.player_pos[0] < WIDTH - 40: self.player_pos[0] += 7
        
        # 2. Bắn đạn (giống tia laser trong ảnh)
        if self.frame_count % 10 == 0:
            self.bullets.append([self.player_pos[0], self.player_pos[1] - 40])

        # 3. Tạo kẻ địch (Máy bay pixel trắng)
        if self.frame_count % 30 == 0:
            self.enemies.append([random.randint(50, WIDTH-50), -50])

        # Cập nhật đạn
        for b in self.bullets[:]:
            b[1] -= 15
            if b[1] < 0: self.bullets.remove(b)

        # Cập nhật kẻ địch & Va chạm
        for e in self.enemies[:]:
            e[1] += 5
            # Vẽ máy bay địch (Pixel Style)
            pygame.draw.rect(self.screen, WHITE, (e[0]-20, e[1]-10, 40, 20)) 
            pygame.draw.rect(self.screen, RED, (e[0]-5, e[1]+10, 10, 5))

            # Va chạm với người chơi
            if abs(e[0] - self.player_pos[0]) < 35 and abs(e[1] - self.player_pos[1]) < 35:
                self.state = "EJECT_CARD" # Game Over -> Kết thúc giao dịch

            if e[1] > HEIGHT: self.enemies.remove(e)

        # 4. Vẽ máy bay người chơi (Dựa trên mẫu ảnh bạn gửi)
        px, py = self.player_pos
        # Thân chính
        pygame.draw.polygon(self.screen, BLUE, [(px, py-40), (px-30, py+20), (px+30, py+20)])
        # Cánh đỏ trắng
        pygame.draw.rect(self.screen, RED, (px-50, py, 20, 30))
        pygame.draw.rect(self.screen, RED, (px+30, py, 20, 30))
        # Lửa đuôi
        if self.frame_count % 4 < 2:
            pygame.draw.circle(self.screen, GOLD, (px, py+35), 10)

        # Vẽ đạn laser
        for b in self.bullets:
            pygame.draw.line(self.screen, RED, (b[0], b[1]), (b[0], b[1]-20), 4)

        self.draw_text(f"SCORE: {self.score}", 20, GOLD, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

    def state_eject_card(self):
        self.screen.fill(BLACK)
        self.draw_text("TRANSACTION OVER", 200, RED)
        self.draw_text(f"Final Score: {self.score}", 300, WHITE)
        self.draw_text("Ejecting Card...", 400, WHITE)
        self.draw_text("Nhấn [SPACE] để quay lại màn hình đầu", 600, GOLD)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "READ_CARD"

    def run(self):
        while True:
            if self.state == "READ_CARD": self.state_read_card()
            elif self.state == "READ_PIN": self.state_read_pin()
            elif self.state == "CHOOSE_TRANS": self.state_choose_transaction()
            elif self.state == "PLAYING": self.state_playing()
            elif self.state == "EJECT_CARD": self.state_eject_card()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
