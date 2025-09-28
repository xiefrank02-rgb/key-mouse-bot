import schedule
import time
from win10toast import ToastNotifier  # 用于发送Windows通知

def job():
    # 初始化通知器
    toaster = ToastNotifier()
    # 发送系统通知
    toaster.show_toast(
        title="喝水提醒",  # 通知标题
        msg="该喝水啦！保持水分摄入，有益健康哦~",  # 通知内容
        duration=10,  # 通知显示时间（秒）
        icon_path=None,  # 可选：设置通知图标（.ico文件路径）
        threaded=True  # 多线程显示，不阻塞程序运行
    )

def main():
    start_hour = 9
    end_hour = 21

    # 安排每天在9:45, 10:45, ..., 21:45执行提醒
    for hour in range(start_hour, end_hour + 1):
        schedule.every().day.at(f"{hour:02d}:45").do(job)

    while True:
        # 执行所有到期的任务
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
