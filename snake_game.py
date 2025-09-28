import pygame
import sys
import random
import time

# 初始化pygame
pygame.init()

# 游戏配置
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
CELL_NUMBER = WINDOW_WIDTH // CELL_SIZE

# 颜色定义
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 设置游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# 字体设置
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        # 蛇的初始位置（身体由三个方块组成）
        self.body = [pygame.math.Vector2(5, 10), pygame.math.Vector2(4, 10), pygame.math.Vector2(3, 10)]
        self.direction = pygame.math.Vector2(1, 0)  # 初始向右移动
        self.new_block = False
    
    def draw_snake(self):
        """绘制蛇"""
        for block in self.body:
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, block_rect)
    
    def move_snake(self):
        """移动蛇"""
        if not self.new_block:
            # 复制身体列表，去掉尾部
            body_copy = self.body[:-1]
            # 在头部添加一个新的方块
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
        else:
            # 如果吃到了食物，增长身体
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
    
    def add_block(self):
        """增加蛇的身体长度"""
        self.new_block = True

class Food:
    def __init__(self):
        self.randomize()
    
    def draw_food(self):
        """绘制食物"""
        food_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
    
    def randomize(self):
        """随机生成食物位置"""
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def update(self):
        """更新游戏状态"""
        if not self.game_over:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()
    
    def draw_elements(self):
        """绘制所有元素"""
        if self.game_over:
            self.draw_game_over()
        else:
            self.food.draw_food()
            self.snake.draw_snake()
            self.draw_score()
    
    def check_collision(self):
        """检查碰撞（蛇是否吃到食物）"""
        if self.food.pos == self.snake.body[0]:
            # 重新放置食物
            self.food.randomize()
            # 确保食物不会出现在蛇身上
            for block in self.snake.body[1:]:
                if block == self.food.pos:
                    self.food.randomize()
            
            # 增加蛇的长度
            self.snake.add_block()
            # 增加分数
            self.score += 1
    
    def check_fail(self):
        """检查游戏结束条件"""
        # 检查是否撞墙
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over = True
        
        # 检查是否撞到自己
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over = True
    
    def draw_score(self):
        """绘制分数"""
        score_text = str(self.score)
        score_surface = font.render(score_text, True, WHITE)
        score_x = int(WINDOW_WIDTH - 60)
        score_y = int(WINDOW_HEIGHT - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 绘制半透明覆盖层
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # 绘制游戏结束文字
        game_over_surface = font.render("Game Over", True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30))
        screen.blit(game_over_surface, game_over_rect)
        
        # 绘制最终分数
        score_surface = font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 10))
        screen.blit(score_surface, score_rect)
        
        # 绘制重新开始提示
        restart_surface = font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        screen.blit(restart_surface, restart_rect)
    
    def reset(self):
        """重置游戏"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

def main():
    # 创建游戏主对象
    game = Main()
    
    # 设置游戏更新事件（控制蛇的移动速度）
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)  # 每150毫秒更新一次
    
    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == SCREEN_UPDATE:
                game.update()
            
            if event.type == pygame.KEYDOWN:
                # 控制蛇的方向
                if event.key == pygame.K_UP:
                    if game.snake.direction.y != 1:  # 不允许直接反向
                        game.snake.direction = pygame.math.Vector2(0, -1)
                
                if event.key == pygame.K_DOWN:
                    if game.snake.direction.y != -1:
                        game.snake.direction = pygame.math.Vector2(0, 1)
                
                if event.key == pygame.K_RIGHT:
                    if game.snake.direction.x != -1:
                        game.snake.direction = pygame.math.Vector2(1, 0)
                
                if event.key == pygame.K_LEFT:
                    if game.snake.direction.x != 1:
                        game.snake.direction = pygame.math.Vector2(-1, 0)
                
                # 重新开始游戏
                if event.key == pygame.K_SPACE and game.game_over:
                    game.reset()
        
        # 填充背景
        screen.fill(BLACK)
        
        # 绘制游戏元素
        game.draw_elements()
        
        # 更新显示
        pygame.display.update()
        
        # 控制帧率
        clock.tick(60)

if __name__ == "__main__":
    main()