import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import math

EA, I2, I1, EB, I4, I3 = (13, 19, 26, 16, 20, 21)  # 定义引脚
FREQUENCY = 50  # PWM波的频率为50Hz
# 初始化GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.output([EA, I2, EB, I3], GPIO.LOW)
GPIO.output([I1, I4], GPIO.HIGH)

center = 320  # 定义图像的标准中点center
# 打开摄像头，图像尺寸640*480（长*高），opencv存储值为480*640（行*列）
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 初始化PWM
pwma = GPIO.PWM(EA, FREQUENCY)
pwmb = GPIO.PWM(EB, FREQUENCY)
pwma.start(0)  # 此时ENA引脚持续产生占空比为0的PWM输出
pwmb.start(0)  # 此时ENB引脚持续产生占空比为0的PWM输出

count = 0
while 1:
    count += 1
    # 读取图片
    ret, frame = cap.read()  # 摄像头读取图像

    # 转换颜色空间为HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 提取橙色部分
    lower_orange = np.array([0, 50, 50])
    upper_orange = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # 进行形态学操作，去除背景噪声和连接断开的线段
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    # 将橙色部分变成黑色
    dst = cv2.bitwise_not(closing)
    dst = cv2.dilate(dst, None, iterations = 2)  # 膨胀，使黑区域变大

    color = dst[420]  # 单看第420行的像素值
    black_count = np.sum(color == 0)  # 找到黑色的像素点个数
    black_index = np.where(color == 0)  # 找到黑色的像素点索引

    # 防止black_count=0的报错
    if black_count == 0:
        continue

    # 找到黑色像素的中心点位置
    center = (black_index[0][black_count - 1] + black_index[0][0]) / 2

    # 计算出该黑色像素的中心点位置与标准中心点的偏移量
    direction = center - 320

    print(direction)
    if count == 1:
        cmd = input()  # 使小车在输入口令后能立即开始行驶

    # 摄像头无法捕捉到黑线时小车停止
    if abs(direction) > 320:
        pwma.ChangeDutyCycle(0)
        pwmb.ChangeDutyCycle(0)

    #根据偏向角度，调整车速和转向
    else:
        DirectionMAX = 60  # 设置小车的最大偏移量
        DutyMAX = 19.2     # 占空比的最大值，可以理解为小车速度的峰值
        DutyMIN = 18.3     # 占空比的最小值
        turn_angle = 0.089 # 转弯系数，控制转弯幅度

        # 如果direction偏离太多，就将其限制在区间内
        if direction > DirectionMAX:
            direction = DirectionMAX
        if direction < -DirectionMAX:
            direction = -DirectionMAX

        # 建立线性模型，调整小车的速度和转向角度
        k = (DutyMIN - DutyMAX) / DirectionMAX  # k为线性模型的斜率
        SetDuty = k * abs(direction) + DutyMAX  # abs(direction)表示方向的偏移，偏的越多，速度越慢，呈线性关系
        delta = direction * turn_angle          # delta为左右轮的占空比之差，同样偏得越多，需要转的角度越大

        # 根据左右转向的不同情况，给左右轮分别设置不同的占空比
        if delta < 0:
            DutyA = SetDuty-delta
            DutyB = SetDuty
        else:
            DutyA = SetDuty
            DutyB = SetDuty+delta
        pwma.ChangeDutyCycle(DutyA)
        pwmb.ChangeDutyCycle(DutyB)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 释放清理
cap.release()
cv2.destroyAllWindows()
pwma.stop()
pwmb.stop()
GPIO.cleanup()


