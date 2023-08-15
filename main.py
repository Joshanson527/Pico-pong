from machine import Pin, I2C, ADC
import utime
import sh1106
import random

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)

js1 = ADC(Pin(26))
js2 = ADC(Pin(27))
p1_pos = 27
p2_pos = 27
line_height = 10
display_height = 64
display_width = 128
paddle_speed = 1
ball_x = 64
ball_y = 32

oled.flip()

while True:
    ball_vx = random.choice([-1,1])
    ball_vy = random.choice([-1,1])
    ball_speed = 1
    p1_score = 0
    p2_score = 0
    p1_ready = 0
    p2_ready = 0
    game = 0

    def display_screen():
        oled.fill(0)
        oled.rect(0, 0, 128, 64, 1)
        oled.line(4, p1_pos, 4, (p1_pos + line_height), 1)
        oled.line(5, p1_pos, 5, (p1_pos + line_height), 1)
        oled.line(123, p2_pos, 123, (p2_pos + line_height), 1)
        oled.line(122, p2_pos, 122, (p2_pos + line_height), 1)
        oled.fill_rect((ball_x - 1), (ball_y - 1), 3, 3, 1)
        oled.text(str(p1_score), 32, 5, 1)
        oled.text(str(p2_score), 90, 5, 1)
        for i in range(64):
            if (i - 1) % 2 == 0:
                oled.pixel(64, i - 1, 1)
        oled.show()

    while game == 0:
        js1_state = js1.read_u16()
        js2_state = js2.read_u16()
        if js1_state == 65535 and p1_ready == 0:
            p1_ready = 1
        elif js2_state == 65535 and p2_ready == 0:
            p2_ready = 1
        
        if js1_state < 1000 and p1_ready == 1:
            p1_ready = 2
        elif js2_state < 1000 and p2_ready == 1:
            p2_ready = 2
            
        oled.fill(0)
        oled.text("PONG", 48, 0, 1)
        if p1_ready < 2: 
            oled.text("P1 - Not ready", 8, 22, 1)
        elif p1_ready == 2:
            oled.text("P1 - Ready", 8, 22, 1)
        if p2_ready < 2:
            oled.text("P2 - Not ready", 8, 32, 1)
        elif p2_ready == 2:
            oled.text("P2 - Ready", 8, 32, 1)
        oled.text("Wiggle joystick", 4, 56, 1)
        oled.show()
        
        if p1_ready == 2 and p2_ready == 2:
            game = 1

    utime.sleep(1)

    for c in range(3):
        oled.fill(0)
        oled.rect(0, 0, 128, 64, 1)
        oled.line(4, p1_pos, 4, (p1_pos + line_height), 1)
        oled.line(5, p1_pos, 5, (p1_pos + line_height), 1)
        oled.line(123, p2_pos, 123, (p2_pos + line_height), 1)
        oled.line(122, p2_pos, 122, (p2_pos + line_height), 1)
        oled.fill_rect((ball_x - 1), (ball_y - 1), 3, 3, 1)
        oled.text(str(p1_score), 32, 5, 1)
        oled.text(str(p2_score), 90, 5, 1)
        for i in range(64):
            if (i - 1) % 2 == 0:
                oled.pixel(64, i - 1, 1)
        oled.fill_rect(59, 24, 12, 13, 0)
        oled.rect(59, 24, 12, 13, 1)
        oled.text(str(3 - c), 61, 27, 1)
        oled.show()
        utime.sleep(1)

    while game == 1:
        js1_state = js1.read_u16()
        js2_state = js2.read_u16()
        
        if js1_state == 65535 and p1_pos > 1:
            p1_pos = p1_pos - paddle_speed
        
        if js1_state < 1000 and p1_pos < display_height - line_height - 1:
            p1_pos = p1_pos + paddle_speed
            
        if js2_state == 65535 and p2_pos > 0:
            p2_pos = p2_pos - paddle_speed
        
        if js2_state < 1000 and p2_pos < (display_height - line_height):
            p2_pos = p2_pos + paddle_speed
            
        if ball_x == 4 and ball_y >= p1_pos and ball_y <= (p1_pos + line_height) and ball_vx < 0:
            ball_vx = 0 - ball_vx
            if p2_score > 6:
                ball_speed = 2
            else:
                ball_speed = 1
        
        if ball_x == 120 and ball_y >= p2_pos and ball_y <= (p2_pos + line_height) and ball_vx >0:
            ball_vx = 0 - ball_vx
            if p1_score > 6:
                ball_speed = 2
            else:
                ball_speed = 1
            
        if ball_y < 3 or ball_y > 60:
            ball_vy = 0 - ball_vy
            
        ball_x = ball_x + (ball_vx * ball_speed)
        ball_y = ball_y + (ball_vy * ball_speed)
            
        display_screen()
        
        if ball_x > 124 or ball_x < 3:
            if ball_x > 124:
                p1_score = p1_score + 1
                ball_vx = -1
            else:
                p2_score = p2_score + 1
                ball_vx = 1
            display_screen()
            utime.sleep(1)
            ball_x = 64
            ball_y = 32
            ball_vy = random.choice([-1,1])
            p1_pos = 27
            p2_pos = 27
            ball_speed = 1
        if p1_score == 10 or p2_score == 10:
            game = 0
            
    oled.fill(0)
    if p1_score == 10:
        oled.text("P1 wins " + str(p1_score) + " - " + str(p2_score), 10, 10, 1)
    else:
        oled.text("P2 wins " + str(p2_score) + " - " + str(p1_score), 10, 10, 1)
    oled.show()
    utime.sleep(3)
