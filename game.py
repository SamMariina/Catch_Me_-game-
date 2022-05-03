from tkinter import *
# импорт всплывающего окна
import tkinter.messagebox as mb
# импортируем рандом
import random
# глобальные переменные
# настройки окна
Width = 900
Height = 300
# очки для каждого игрока
player_1_score = 0
player_2_score = 0
# счет скорости
initial_speed = 20
# настройки ракеток
# ширина ракетки
pad_w = 10
# высота ракетки
pad_h = 100
# настройки мяча
# радиус мяча
ball_radius = 40
# горизонтальная скорость
ball_x_change = 20
# вертикальная скорость
ball_y_change = 0
# окно
root = Tk()
root.title("CATCH ME")
# canvas
c = Canvas(root, width=Width, height=Height, background='#30d5c8')
c.pack()
# элементы игрового поля
# левая линия
c.create_line(pad_w, 0, pad_w, Height, fill='white')
# правая линия
c.create_line(Width - pad_w, 0, Width - pad_w, Height, fill='white')
# разделитель игрового поля
c.create_line(Width / 2, 0, Width / 2, Height, fill='white')
# мяч
ball = c.create_oval(Width / 2 - ball_radius / 2,
                     Height / 2 - ball_radius / 2,
                     Width / 2 + ball_radius / 2,
                     Height / 2 + ball_radius / 2, fill='#FFFF00')
# левая ракетка
left_pad = c.create_line(pad_w / 2, 0, pad_w / 2, pad_h, width=pad_w, fill='#0000FF')
# правая ракетка
right_pad = c.create_line(Width - pad_w / 2, 0, Width - pad_w / 2, pad_h, width=pad_w, fill='#0000FF')
# текст очков
p_1_text = c.create_text(Width - Width / 6, pad_h / 4,
                         text=player_1_score,
                         font='Arial 20', fill='white')
p_2_text = c.create_text(Width / 6, pad_h / 4,
                         text=player_2_score,
                         font='Arial 20', fill='white')
# скорости ракеток
pad_speed = 20
# скорость левой ракетки
left_pad_speed = 0
# скорость правой ракетки
right_pad_speed = 0
# скорость мяча с каждым ударом
ball_speed_up = 1.00
# максимальная скорость мяча
ball_max_speed = 30
# начальная скорость мяча по горизонтали
ball_x_speed = 20
# начальная скорость мяча по вертикали
ball_y_speed = 20
# расстояние до правого края
right_line_distance = Width - pad_w


# счет
def update_score(player):
    global player_1_score, player_2_score
    if player == 'right':
        if player_1_score or player_2_score < 5:
            player_1_score += 1
            c.itemconfig(p_1_text, text=player_1_score)
        if player_1_score == 5:
            mb.showinfo("Player_1 The winner!!!")
            root.destroy()
    else:
        if player_1_score or player_2_score < 5:
            player_2_score += 1
            c.itemconfig(p_2_text, text=player_2_score)
        if player_2_score == 5:
            mb.showinfo("Player_2 The winner!!!")
            root.destroy()


# респаун
def spawn_ball():
    global ball_x_speed
    c.coords(ball, Width / 2 - ball_radius / 2,
            Height / 2 - ball_radius / 2,
            Width / 2 + ball_radius / 2,
            Height / 2 + ball_radius / 2)
    ball_x_speed = -(ball_x_speed * - initial_speed / abs(ball_x_speed))


# отскок мяча от ракеток
def bounce(action):
    global ball_x_speed, ball_y_speed
    if action == 'strike':
        ball_y_speed = random.randrange(-10, 10)
        if abs(ball_x_speed) < ball_max_speed:
            ball_x_speed *= -ball_speed_up
        else:
            ball_x_speed = -ball_x_speed
    else:
        ball_y_speed = -ball_y_speed


# функция движения мяча
def move_ball():
    global ball, right_pad, left_pad
    ball_left, ball_top, ball_right, ball_bot = c.coords(ball)
    ball_center = (ball_top + ball_bot) / 2
    # вертикальный отскок
    if ball_right + ball_x_speed < right_line_distance and ball_left + ball_x_speed > pad_w:
        c.move(ball, ball_x_speed, ball_y_speed)
    elif ball_right == right_line_distance or ball_left == pad_w:
        if ball_right > Width / 2:
            if c.coords(right_pad)[1] < ball_center < c.coords(right_pad)[3]:
                bounce('strike')
            else:
                update_score('left')
                spawn_ball()
        else:
            if c.coords(left_pad)[1] < ball_center < c.coords(left_pad)[3]:
                bounce('strike')
            else:
                update_score('right')
                spawn_ball()
    else:
        if ball_right > Width / 2:
            c.move(ball, right_line_distance - ball_right, ball_y_speed)
        else:
            c.move(ball, -ball_left + pad_w, ball_y_speed)
    if ball_top + ball_y_speed < 0 or ball_bot + ball_y_speed > Height:
        bounce('ricochet')


# функция движения ракеток
def move_pads():
    pads = {left_pad: left_pad_speed,
            right_pad: right_pad_speed}
    for pad in pads:
        c.move(pad, 0, pads[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > Height:
            c.move(pad, 0, Height - c.coords(pad)[3])


# обработка нажатия клавиш
def moveent_handler(event):
    global left_pad_speed, right_pad_speed
    if event.keysym == 'w':
        left_pad_speed = -pad_speed
    elif event.keysym == 's':
        left_pad_speed = pad_speed
    elif event.keysym == 'Up':
        right_pad_speed = -pad_speed
    elif event.keysym == 'Down':
        right_pad_speed = pad_speed


# Привязка к канвас
c.bind("<KeyPress>", moveent_handler)


# клавиши не нажаты
def stop_pad(event):
    global left_pad_speed, right_pad_speed
    if event.keysym in "ws":
        left_pad_speed = 0
    elif event.keysym in ("Up", "Down"):
        right_pad_speed = 0


c.bind("<KeyRelease>", stop_pad)


def main():
    move_ball()
    move_pads()
    # вызывает саму себя
    root.after(30, main)


# фокус на канвас (реакция на клавиши)
c.focus_set()
# запуск
main()
# запуск окна
root.mainloop()
