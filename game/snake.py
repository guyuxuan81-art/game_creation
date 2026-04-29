#   算法思想：
#          先拆分再整合。界面、蛇头、蛇身、食物、得分显示、键盘控制、移动逻辑、碰撞检测等，最后整合成一个完整的游戏。
#          蛇头要求不过界、不能碰到蛇身、碰到食物得分增加。
#          蛇身要求跟随蛇头移动，吃到食物增加长度。
#          食物要求随机出现，吃到后重新生成有效位置。
#          得分显示要求实时更新，显示当前得分。


import turtle  # 用于图形界面
import time  # 用于延迟
import random  # 用于食物的随机位置

#设置屏幕
sc = turtle.Screen()  # 创建游戏窗口
sc.title("贪吃蛇")  # 标题
sc.bgcolor("white")  # 背景白色
sc.setup(width=600, height=600)  # 窗口大小
sc.tracer(0)  # 设置刷新率，0表示不自动刷新，和sc.update()配合使用


# 蛇头部分
head = turtle.Turtle()  # 创建蛇头
head.speed(0)  # 移动速度
head.shape("square")  # 正方形
head.color("black")  # 黑色
head.penup()  # 不画线
head.goto(0, 0)  # 起始位置
head.direction = "stop"  # 初始方向


# 蛇身列表
segments = []  # 蛇身段


# 食物
food = turtle.Turtle()  # 创建食物
food.speed(0)   # 最快速度
food.shape("square")  # 正方形
food.color("red")  # 红色
food.penup()
food.goto(0, 100)  # 初始位置


# 得分
score = 0  # 当前得分


# 得分显示
pen = turtle.Turtle()  # 显示得分
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()  # 隐藏笔
pen.goto(0, 260)  # 顶部位置
pen.write("得分: 0", align="center", font=("Courier", 24, "normal"))  # 初始显示


# 方向函数（蛇头移动方向不能和自己前进方向相反，否则会撞到自己）
def go_up():
    if head.direction != "down":  # 只要方向不是向下
        head.direction = "up"   # 就可以向上移动
def go_down():
    if head.direction != "up":
        head.direction = "down"
def go_left():
    if head.direction != "right":
        head.direction = "left"
def go_right():
    if head.direction != "left":
        head.direction = "right"


# 移动函数（根据方向控制x，y坐标的变化）
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)


# 重置游戏函数
def reset_game():
    head.goto(0, 0)  # 重置蛇头
    head.direction = "stop"
    for segment in segments:  # 隐藏蛇身
        segment.goto(1000, 1000) # 把蛇身移动到屏幕外
    segments.clear()  # 清空蛇身
    global score
    score = 0  # 重置得分
    pen.goto(0, 260)  # 移回顶部位置
    pen.clear()
    pen.write("得分: {}".format(score), align="center", font=("Courier", 24, "normal"))

# 键盘绑定（wasd控制）
sc.listen()
sc.onkeypress(go_up, "w")
sc.onkeypress(go_down, "s")
sc.onkeypress(go_left, "a")
sc.onkeypress(go_right, "d")

# 主循环
while True:
    sc.update()  # 更新屏幕

    # 检查边界碰撞（头坐标超出边界）
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        pen.goto(0, 0)  # 移动到屏幕中间
        pen.write("游戏结束！", align="center", font=("Courier", 24, "normal"))
        sc.update()  # 立即更新屏幕显示
        time.sleep(2)  # 暂停2秒让用户看到结束信息
        reset_game()    # 碰到边界，调用重置函数
        

    # 碰到食物后的变化（食物、身段）
    if head.distance(food) < 20: # 如果蛇头和食物距离小于20像素，认为吃到了食物
        x = random.randint(-290, 290)  # 随机新位置
        y = random.randint(-290, 290)
        food.goto(x, y)
        new_segment = turtle.Turtle()  # 新蛇身段
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)  # 添加到蛇身列表，完成增长
        score += 10  # 得分+10
        pen.clear()
        pen.write("得分: {}".format(score), align="center", font=("Courier", 24, "normal"))

    # 移动蛇身
    for i in range(len(segments) - 1, 0, -1):  # 逆序移动蛇身段，最后一个段跟随前一个段
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)  # 移动当前段到前一个段的位置
    if segments:
        segments[0].goto(head.xcor(), head.ycor())  # 第一个蛇身段跟随蛇头

    move()  # 移动蛇头

    # 检查自身碰撞
    for segment in segments:
        if segment.distance(head) < 20: # 如果蛇头和蛇身段距离小于20像素，认为碰到了自己
            pen.goto(0, 0)  # 移动到屏幕中间
            pen.write("游戏结束！", align="center", font=("Courier", 24, "normal"))
            sc.update()  # 立即更新屏幕显示
            time.sleep(2)  # 暂停2秒让用户看到结束信息
            reset_game()

    time.sleep(0.1)  # 延迟

sc.mainloop()  # 保持窗口