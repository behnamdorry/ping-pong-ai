import pygame
import sys
import random
import time

# مقداردهی اولیه Pygame
pygame.init()

# تنظیمات صفحه
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong AI Battle - Score System")

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# فونت
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

class GameManager:
    def __init__(self):
        self.score_ai1 = 0
        self.score_ai2 = 0
        self.max_score = 3  # امتیاز برای برنده شدن
        self.round_winner = None
        self.game_state = "playing"  # playing, round_over
        self.round_start_time = 0
        self.round_delay = 3  # ثانیه تأثیر بین راندها
        self.total_wins_ai1 = 0
        self.total_wins_ai2 = 0
        
    def update_score(self, scorer):
        """به روزرسانی امتیاز و بررسی برنده"""
        if scorer == "ai1":
            self.score_ai1 += 1
        else:
            self.score_ai2 += 1
        
        # بررسی پایان راند
        if self.score_ai1 >= self.max_score or self.score_ai2 >= self.max_score:
            if self.score_ai1 >= self.max_score:
                self.round_winner = "ai1"
                self.total_wins_ai1 += 1
            else:
                self.round_winner = "ai2"
                self.total_wins_ai2 += 1
                
            self.game_state = "round_over"
            self.round_start_time = time.time()
    
    def update(self):
        """به روزرسانی وضعیت بازی"""
        if self.game_state == "round_over":
            # بررسی پایان تأثیر بین راندها
            if time.time() - self.round_start_time >= self.round_delay:
                self.reset_round()
                return True
        return False
    
    def reset_round(self):
        """بازنشانی برای راند جدید"""
        self.score_ai1 = 0
        self.score_ai2 = 0
        self.round_winner = None
        self.game_state = "playing"
    
    def get_winner_text(self):
        """متن برنده را برمی‌گرداند"""
        if self.round_winner == "ai1":
            return "AI 1 Wins the Round!"
        else:
            return "AI 2 Wins the Round!"
    
    def get_total_score_text(self):
        """متن امتیاز کلی را برمی‌گرداند"""
        return f"Total: AI1 {self.total_wins_ai1} - {self.total_wins_ai2} AI2"

def simple_ai(paddle, ball, speed):
    """هوش مصنوعی ساده دنبال کننده توپ"""
    # حرکت به سمت توپ با سرعت ثابت
    if paddle.centery < ball.centery:
        paddle.y += min(speed, ball.centery - paddle.centery)
    elif paddle.centery > ball.centery:
        paddle.y -= min(speed, paddle.centery - ball.centery)
    
    # محدود کردن به صفحه
    paddle.y = max(0, min(paddle.y, HEIGHT - paddle.height))

def predictive_ai(paddle, ball, ball_speed_x, ball_speed_y, speed):
    """هوش مصنوعی با قابلیت پیش‌بینی"""
    # فقط اگر توپ به سمت راکت می‌آید
    if (paddle == player1 and ball_speed_x > 0) or (paddle == player2 and ball_speed_x < 0):
        # پیش‌بینی موقعیت Y توپ وقتی به راکت می‌رسد
        if ball_speed_x != 0:
            # محاسبه زمان رسیدن توپ به راکت
            if paddle == player1:
                time_to_reach = (paddle.left - ball.right) / ball_speed_x
            else:
                time_to_reach = (paddle.right - ball.left) / ball_speed_x
            
            # پیش‌بینی موقعیت Y
            predicted_y = ball.centery + (ball_speed_y * time_to_reach)
            
            # تصحیح برای برخورد با دیوارها
            while predicted_y < 0 or predicted_y > HEIGHT:
                if predicted_y < 0:
                    predicted_y = -predicted_y
                else:
                    predicted_y = 2 * HEIGHT - predicted_y
            
            # حرکت به سمت موقعیت پیش‌بینی شده
            if paddle.centery < predicted_y:
                paddle.y += min(speed, predicted_y - paddle.centery)
            else:
                paddle.y -= min(speed, paddle.centery - predicted_y)
    
    # محدود کردن به صفحه
    paddle.y = max(0, min(paddle.y, HEIGHT - paddle.height))

# ایجاد اجزای بازی
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
player1 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 70, 10, 140)  # راکت راست
player2 = pygame.Rect(10, HEIGHT // 2 - 70, 10, 140)         # راکت چپ

# سرعت‌ها
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 8

# مدیر بازی
game_manager = GameManager()

# حلقه اصلی بازی
clock = pygame.time.Clock()

def reset_ball():
    """بازنشانی توپ به مرکز"""
    ball.center = (WIDTH // 2, HEIGHT // 2)
    return (7 * random.choice((1, -1)), 
            7 * random.choice((1, -1)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_manager.game_state == "round_over":
                # بازیکن می‌تواند با کلید R بازی را زودتر ادامه دهد
                game_manager.reset_round()

    if game_manager.game_state == "playing":
        # به روزرسانی هوش مصنوعی‌ها
        predictive_ai(player1, ball, ball_speed_x, ball_speed_y, player_speed)  # AI1 پیشرفته
        simple_ai(player2, ball, player_speed)  # AI2 ساده
        
        # حرکت توپ
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        
        # برخورد با دیوارهای بالا و پایین
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        
        # برخورد با راکت‌ها
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1
            # افزایش جزئی سرعت برای هیجان بیشتر
            ball_speed_x *= 1.05
            ball_speed_y *= 1.05
        
        # بررسی گل شدن
        if ball.left <= 0:
            game_manager.update_score("ai1")
            ball_speed_x, ball_speed_y = reset_ball()
        elif ball.right >= WIDTH:
            game_manager.update_score("ai2")
            ball_speed_x, ball_speed_y = reset_ball()
    
    else:  # round_over
        # به روزرسانی خودکار برای راند بعدی
        if game_manager.update():
            ball_speed_x, ball_speed_y = reset_ball()
    
    # رسم بازی
    screen.fill(BLACK)
    
    # رسم راکت‌ها و توپ
    pygame.draw.rect(screen, BLUE, player1)    # AI1 آبی
    pygame.draw.rect(screen, RED, player2)     # AI2 قرمز
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # نمایش امتیازها
    score_text = font.render(f"{game_manager.score_ai1} - {game_manager.score_ai2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    
    # نمایش امتیاز کلی
    total_score_text = font.render(game_manager.get_total_score_text(), True, GREEN)
    screen.blit(total_score_text, (WIDTH // 2 - total_score_text.get_width() // 2, 60))
    
    # نمایش پیام برنده
    if game_manager.game_state == "round_over":
        winner_text = large_font.render(game_manager.get_winner_text(), True, GREEN)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))
        
        countdown = game_manager.round_delay - int(time.time() - game_manager.round_start_time)
        countdown_text = font.render(f"Next round in: {countdown}", True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 + 50))
        
        restart_text = font.render("Press R to start immediately", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    
    # به روزرسانی صفحه
    pygame.display.flip()
    clock.tick(60)