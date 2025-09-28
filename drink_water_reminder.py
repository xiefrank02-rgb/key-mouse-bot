import schedule
import time
from plyer import notification  # 用于跨平台通知

def job():
    # 发送系统通知
    notification.notify(
        title="喝水提醒",  # 通知标题
        message="该喝水啦！保持水分摄入，有益健康哦~",  # 通知内容
        timeout=10  # 通知显示时间（秒）
    )

def main():
    start_hour = 9
    end_hour = 21

    # 安排每天在9:45, 10:45, ..., 21:45执行提醒
    for hour in range(start_hour, end_hour + 1):
        schedule.every().day.at(f"{hour:02d}:58").do(job)  # 改为每小时的45分提醒

    while True:
        # 执行所有到期的任务
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()