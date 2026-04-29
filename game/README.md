# Python游戏学习项目

## 游戏列表

### 1. 贪吃蛇 (snake.py)
- **玩法**: 用WASD键控制蛇吃食物，避开边界和自身
- **学习点**: 键盘控制、碰撞检测、列表操作、游戏循环

### 2. 打砖块 (brick.py)
- **玩法**: 用A/D键控制挡板接球，击碎所有彩色砖块
- **学习点**: 多个对象管理、复杂碰撞检测、游戏状态判断

## 如何运行游戏

1. 确保安装了Python
2. 在命令行中进入项目目录：
   ```bash
   cd Desktop/python
   ```
3. 运行游戏：
   ```bash
   python snake.py    # 运行贪吃蛇
   python brick.py    # 运行打砖块
   ```

## Turtle库基础知识

- `turtle.Turtle()`: 创建一个海龟对象
- `shape()`: 设置形状
- `color()`: 设置颜色
- `goto(x, y)`: 移动到坐标
- `distance(obj)`: 计算与另一对象的距离
- `hideturtle()`: 隐藏海龟
- `write()`: 写文字
    for j in range(8):  # 每行8个砖块
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.color(colors[i])
        brick.penup()
        brick.goto(-240 + j * 70, 200 - i * 30)
        bricks.append(brick)

# 移动挡板函数
def move_left():
    x = paddle.xcor()
    if x > -250:
        paddle.setx(x - 20)

def move_right():
    x = paddle.xcor()
    if x < 250:
        paddle.setx(x + 20)

# 键盘绑定
sc.listen()
sc.onkeypress(move_left, "a")
sc.onkeypress(move_right, "d")

# 主循环
while True:
    sc.update()

    # 移动球
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # 边界碰撞检测
    if ball.xcor() > 290 or ball.xcor() < -290:
        ball.dx *= -1

    if ball.ycor() > 290:
        ball.dy *= -1

    # 挡板碰撞检测
    if (ball.ycor() < -240 and ball.ycor() > -250) and (ball.xcor() < paddle.xcor() + 50 and ball.xcor() > paddle.xcor() - 50):
        ball.sety(-240)
        ball.dy *= -1

    # 砖块碰撞检测
    for brick in bricks:
        if brick.isvisible():  # 只检测可见的砖块
            if ball.distance(brick) < 30:  # 碰撞距离
                brick.hideturtle()  # 隐藏砖块
                ball.dy *= -1
                score += 10
                pen.clear()
                pen.write("得分: {}".format(score), align="center", font=("Courier", 24, "normal"))

    # 球掉落检测（游戏结束）
    if ball.ycor() < -290:
        pen.goto(0, 0)
        pen.write("游戏结束！", align="center", font=("Courier", 24, "normal"))
        sc.update()
        time.sleep(2)
        break  # 结束游戏

    # 检查是否所有砖块都被击碎
    all_hidden = True
    for brick in bricks:
        if brick.isvisible():
            all_hidden = False
            break

    if all_hidden:
        pen.goto(0, 0)
        pen.write("恭喜通关！", align="center", font=("Courier", 24, "normal"))
        sc.update()
        time.sleep(2)
        break

    time.sleep(0.01)

sc.mainloop()</content>
<parameter name="filePath">c:\Users\123\Desktop\python\brick.py