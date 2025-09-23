import tkinter as tk
import time
import schedule
from datetime import datetime

def show_reminder():
    # 创建弹窗
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    tk.messagebox.showinfo("喝水提醒", "喝水时间到了！")

def job():
    show_reminder()

def main():
    start_hour = 9
    end_hour = 21

    # 安排每天在9:45, 10:45, ..., 21:45执行提醒
    for hour in range(start_hour, end_hour + 1):
        schedule.every().day.at(f"{hour:02d}:05").do(job)

    while True:
        # 执行所有到期的任务
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    import tkinter.messagebox
    main()
