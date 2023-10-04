import RPi.GPIO as GPIO
import pygame
import time

# 集計用変数
elapsed_times = []
maxTests = 300

# GPIOピンの設定
GPIO_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)

# pygameの初期化
pygame.init()
pygame.joystick.init()

def main():
    count = 0
    try:
        # ジョイスティックの初期化
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        while count < maxTests:
            # GPIO27をLOWにする
            GPIO.output(GPIO_PIN, GPIO.LOW)
            
            # 開始時刻の記録
            start_time = time.time()

            # 入力待機
            while True:
                # イベント処理
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        # ボタンが押された場合、経過時間を計算して出力
                        elapsed_time = (time.time() - start_time) * 1000
                        elapsed_times.append(elapsed_time)
                        count += 1
                        print(f"{count:4d} current: {elapsed_time:.2f} ms  avg: {sum(elapsed_times)/len(elapsed_times):.2f} ms  min: {min(elapsed_times):.2f}  max: {max(elapsed_times):.2f} ms")
                        break
                    
                # 100ms経過してもボタンが押されなかった場合、HIGHに戻す
                if time.time() - start_time > 0.1:
                    break

            # GPIO27をHIGHに戻す
            GPIO.output(GPIO_PIN, GPIO.HIGH)
            
            # 待機
            time.sleep(0.05)

    except KeyboardInterrupt:
        # 終了処理
        GPIO.cleanup()
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        pygame.quit()

if __name__ == "__main__":
    main()
