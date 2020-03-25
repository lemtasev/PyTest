# import sys
import tkinter as tk
import math
from threading import Thread
import time


# from tkinter import messagebox


class EzClock:
    global root, __thread_time

    def __init__(self):
        self.root = tk.Tk()
        self.__init_windows()

    def __init_windows(self):
        # 设置窗口大小
        width = 400
        height = 400
        self.root.title("ezClock")
        self.root.attributes("-alpha", 0.9)  # 透明度
        self.root.protocol("WM_DELETE_WINDOW", self.__on_closing)
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2))
        # 禁止改变窗体大小
        self.root.resizable(width=False, height=False)
        cv = tk.Canvas(self.root, width=width, height=height, bg="#eeeeee")
        cv.config(highlightthickness=0)
        self.__draw_clock(cv)
        cv.pack()

    def __draw_clock(self, cv: tk.Canvas):
        length = 150  # 边长
        x0 = 200  # 圆心x
        y0 = 200  # 圆心y
        self.__draw_circle(cv, x0, y0, length, fill="black")
        self.__draw_circle(cv, x0, y0, (length - 5), fill="white")
        self.__draw_circle(cv, x0, y0, 10, fill="black")
        self.__draw_calibration(cv, x0, y0, length)
        self.__thread_time = Thread(target=self.__draw_hand, args=(cv, x0, y0, length))
        self.__thread_time.setDaemon(True)
        self.__thread_time.start()

    # 画指针
    def __draw_hand(self, cv: tk.Canvas, x0, y0, length):
        now_timestamp = int(time.time())
        lh = 0
        lm = 0
        second_hand = None
        minute_hand = None
        hour_hand = None
        while True:
            h = time.localtime(now_timestamp).tm_hour
            m = time.localtime(now_timestamp).tm_min
            s = time.localtime(now_timestamp).tm_sec
            if lh != h:
                # Hour
                if hour_hand is not None:
                    cv.delete(hour_hand)
                    print("删hour")
                x1 = math.cos((15 * h - 210) * math.pi / 180) * (length - 70) + x0
                y1 = math.sin((15 * h - 210) * math.pi / 180) * (length - 70) + y0
                hour_hand = cv.create_line((x0, y0), (x1, y1), fill="black", arrow=tk.LAST, width=8)
                print("画hour")
            if lm != m:
                # Minute
                if minute_hand is not None:
                    cv.delete(minute_hand)
                    print("删minute")
                x1 = math.cos((6 * m - 90) * math.pi / 180) * (length - 50) + x0
                y1 = math.sin((6 * m - 90) * math.pi / 180) * (length - 50) + y0
                minute_hand = cv.create_line((x0, y0), (x1, y1), fill="green", arrow=tk.LAST, width=6)
                print("画minute")
            # Second
            if second_hand is not None:
                cv.delete(second_hand)
            x1 = math.cos((6 * s - 90) * math.pi / 180) * (length - 30) + x0
            y1 = math.sin((6 * s - 90) * math.pi / 180) * (length - 30) + y0
            second_hand = cv.create_line((x0, y0), (x1, y1), fill="red", arrow=tk.LAST, width=2)

            lh = h
            lm = m
            now_timestamp += 1
            time.sleep(1)

    # 画圆
    def __draw_circle(self, cv: tk.Canvas, x0, y0, length, fill="white"):
        ox0 = x0 - length
        oy0 = y0 - length
        ox1 = x0 + length
        oy1 = y0 + length
        cv.create_oval((ox0, oy0), (ox1, oy1), fill=fill, outline="", width=3)  # 坐标是椭圆所在矩形对角线坐标

    # 画刻度
    def __draw_calibration(self, cv: tk.Canvas, x0, y0, length):
        # 画1到12点数字和大刻度
        for i in range(1, 13):
            print(i)
            degrees = i * 30 - 90
            x1 = math.cos(degrees * math.pi / 180) * (length - 30) + x0
            y1 = math.sin(degrees * math.pi / 180) * (length - 30) + y0
            cv.create_text((x1, y1), text=i, font=("黑体", 24), fill="black")
            x2 = math.cos(degrees * math.pi / 180) * (length - 15) + x0
            y2 = math.sin(degrees * math.pi / 180) * (length - 15) + y0
            x3 = math.cos(degrees * math.pi / 180) * (length - 4) + x0
            y3 = math.sin(degrees * math.pi / 180) * (length - 4) + y0
            cv.create_line((x2, y2), (x3, y3), fill="black", width=3)
        # 画60个小刻度
        for i in range(60):
            degrees = i * 6 - 90
            x2 = math.cos(degrees * math.pi / 180) * (length - 4) + x0
            y2 = math.sin(degrees * math.pi / 180) * (length - 4) + y0
            x3 = math.cos(degrees * math.pi / 180) * (length - 10) + x0
            y3 = math.sin(degrees * math.pi / 180) * (length - 10) + y0
            cv.create_line((x2, y2), (x3, y3), fill="black", width=1)

    def __on_closing(self):
        print("Stopping")
        # self.__thread_time.stop()
        # self.__thread_time.join()
        self.root.destroy()
        print("ok")
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     self.root.destroy()
        #     sys.exit()


# 入口
ezClock = EzClock()
ezClock.root.mainloop()
