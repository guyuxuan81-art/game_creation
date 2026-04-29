# 






import pygame, sys
from pygame.locals import *  # 省略pygame前缀
import random
pygame.init()  # 初始化pygame




# 设置窗口大小和标题
screen = pygame.display.set_mode((400, 700))  # 创建一个400x700的窗口
pygame.display.set_caption("Russia Square") # 设置窗口标题
clock = pygame.time.Clock()  # 用于控制游戏帧率




# 主题颜色配置
THEME = {
    'I': (0, 255, 255), # 青色,‘红绿蓝’三原色
    'O': (255, 255, 0), # 黄色
    'T': (128, 0, 128), # 紫色
    'S': (0, 255, 0), # 绿色
    'Z': (255, 0, 0), # 红色
    'J': (0, 0, 255), # 蓝色
    'L': (255, 165, 0), # 橙色
    'BG': (20, 20, 20), # 背景色黑色
    'GRID': (40, 40, 40), # 网格线颜色灰色
    'BORDER': (100, 100, 100) # 边框颜色白色
}




# 这里是实际画出的方块，后面会抽象成二维列表，根据列表的值来决定该位置是否有方块，然后在draw_grid()函数中根据这个二维列表来绘制方块
def draw_block(surface, x, y, size, color): 
# 用于绘制一个方块，参数分别是：界面，x坐标，y坐标，大小，颜色
    pygame.draw.rect(surface, color, (x, y, size, size))
     # 绘制一个正方形


def draw_grid(surface, grid_x, grid_y, cols, rows, block_size):
 # 绘制网格，参数分别是：界面，网格的x坐标，网格的y坐标，网格列数，网格的行数，每个方块的大小
    width = cols * block_size
    height = rows * block_size
    pygame.draw.rect(surface, THEME['BG'], (grid_x, grid_y, width, height)) # 绘制网格背景
    for i in range(cols + 1): # 绘制竖线
        x = grid_x + i * block_size
        pygame.draw.line(surface, THEME['GRID'], (x, grid_y), (x, grid_y + height))
    for j in range(rows + 1): # 绘制横线
        y = grid_y + j * block_size
        pygame.draw.line(surface, THEME['GRID'], (grid_x, y), (grid_x + width, y))
    pygame.draw.rect(surface, THEME['BORDER'], (grid_x, grid_y, width, height), 3)





# 将棋盘格抽象成二维列表
grid = [[0 for _ in range(10)] for _ in range(20)]  
# 20*10值为0的二维列表。一般是[0 for i in range(10)]，但i没有被使用，所以用_代替，表示这个变量不重要
'''
grid = [
  [0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0],
  ...
  (共20行)
]
'''

# 将各种形状的方块放入棋盘格中，1表示有方块，0表示没有方块
PIECES = {
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)], # 横竖条2种旋转状态
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    'O': [
        [(0, 0), (1, 0), (0, 1), (1, 1)], # 正方形1种旋转状态
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)], # T形4种旋转状态
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],
    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

# 生成抽象方块
def generate_piece():
    piece_type = random.choice(list(PIECES.keys())) # 随机选择一个方块类型
    piece_rotation = random.randint(0, len(PIECES[piece_type]) - 1) 
    # 根据不同形状方块的旋转状态数量，随机选择一个旋转状态。比如L就是4种，O就是1种
    return piece_type, piece_rotation




# 生成新方块的初始状态
current_piece_type = None # 当前方块类型，初始为None，表示没有方块，后面会调用generate_piece()函数生成一个随机方块类型
current_piece_rotation = 0 # 当前方块旋转状态，初始为0，表示默认旋转状态，后面会调用generate_piece()函数生成一个随机旋转状态
current_x = 3  # 初始x
current_y = 0  # 初始y
fall_speed = 500  # 下落速度，毫秒
fall_time = 0

# 检查方块能否移动到正确位置
def can_move(piece_type, piece_rotation, x, y):
    for dx, dy in PIECES[piece_type][piece_rotation]:
        nx, ny = x + dx, y + dy # 计算方块的实际位置，ny行nx列
        if nx < 0 or nx >= 10 or ny < 0 or ny >= 20: # 边界检查
            return False
        if grid[ny][nx]: # 用到抽象网格，如果grid[ny][nx] == 1，表示这个位置已经有方块了，不能移动过去
            return False
    return True

# 固定方块到棋盘
def fix_block_to_board():
    global grid, current_piece_type, current_piece_rotation, current_x, current_y
    for dx, dy in PIECES[current_piece_type][current_piece_rotation]: 
    # 这里的type和rotation会随着spawn_new_piece()函数的调用而改变。
        nx, ny = current_x + dx, current_y + dy
        if 0 <= nx < 10 and 0 <= ny < 20:
            grid[ny][nx] = current_piece_type

# 消除已满的行
def clear_lines():
    global grid
    new_grid = [row for row in grid if 0 in row]
    lines_cleared = 20 - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [0 for _ in range(10)])
    grid = new_grid

# 生成新方块
def spawn_new_piece():
    global current_piece_type, current_piece_rotation, current_x, current_y
    current_piece_type, current_piece_rotation = generate_piece() 
    # 调用generate_piece()函数生成一个随机方块类型和旋转状态，并赋值给type和rotation给fix_block_to_board()函数和can_move()函数使用
    current_x, current_y = 3, 0
    if not can_move(current_piece_type, current_piece_rotation, current_x, current_y):
    # 将参数传入can_move()函数，检查新生成的方块是否能放在初始位置，如果不能放，说明游戏结束
        return False  # 游戏结束
    return True

# 初始化第一个方块
spawn_new_piece()

running = True
while running:
    dt = clock.tick(60)
    fall_time += dt

    # 处理事件
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if can_move(current_piece_type, current_piece_rotation, current_x - 1, current_y):
                    current_x -= 1
            elif event.key == K_RIGHT:
                if can_move(current_piece_type, current_piece_rotation, current_x + 1, current_y):
                    current_x += 1
            elif event.key == K_DOWN:
                if can_move(current_piece_type, current_piece_rotation, current_x, current_y + 1):
                    current_y += 1
            elif event.key == K_UP: # 上键旋转
                next_rotation = (current_piece_rotation + 1) % len(PIECES[current_piece_type])
                # 相当于在当前旋转状态的基础上加1，如果超过最大旋转状态数量就回到0
                if can_move(current_piece_type, next_rotation, current_x, current_y):
                # 如果旋转后的状态可以放在当前坐标，就更新旋转状态
                    current_piece_rotation = next_rotation

    # 自动下落
    if fall_time >= fall_speed: # 如果下落时间超过设定的下落速度，就尝试让方块下落一格
        if can_move(current_piece_type, current_piece_rotation, current_x, current_y + 1):
            current_y += 1
        else:
            fix_block_to_board()
            clear_lines()
            if not spawn_new_piece(): # 如果生成新方块失败，说明游戏结束
                running = False  # 游戏结束
        fall_time = 0

    # 绘制
    screen.fill((50, 50, 50))
    draw_grid(screen, 50, 50, 10, 20, 30)
    # 绘制已固定的方块
    for row in range(20):
        for col in range(10):
            if grid[row][col]:
                draw_block(screen, 50 + col * 30, 50 + row * 30, 30, THEME[grid[row][col]])
    # 绘制当前活动方块
    for dx, dy in PIECES[current_piece_type][current_piece_rotation]:
        x = current_x + dx
        y = current_y + dy
        if 0 <= x < 10 and 0 <= y < 20:
            draw_block(screen, 50 + x * 30, 50 + y * 30, 30, THEME[current_piece_type])

    pygame.display.flip()

pygame.quit()
sys.exit()