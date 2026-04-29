# 打砖块游戏
# 游戏规则：用挡板接住球，击碎所有砖块
# 算法思想

import turtle
import time

# 设置屏幕
sc = turtle.Screen()
sc.title("打砖块游戏")
sc.bgcolor("black")
sc.setup(width=600, height=600)
sc.tracer(0)

# 挡板
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.color("white")
paddle.penup()
paddle.goto(0, -250)

# 球
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, -240)
ball.dx = 3  # x方向速度
ball.dy = 3  # y方向速度

# 得分
score = 0

# 得分显示
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("得分: 0", align="center", font=("Courier", 24, "normal"))

# 创建砖块
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]

for i in range(5):  # 5行砖块
    for j in range(8):  # 每行8个砖块
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.color(colors[i])
        brick.penup()
        brick.goto(-240 + j * 70, 200 - i * 30)
        bricks.append(brick)

# 移动挡板函数，
def move_left():
    x = paddle.xcor()
    if x > -250:    # 挡板不能移出左边界
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

    # 边界碰撞转向(左右上边界)
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

sc.mainloop()