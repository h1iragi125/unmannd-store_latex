from machine import Pin
import machine
import utime

hasshin = Pin(14, Pin.OUT) #14番を出力（発信）と定義
jyushin = Pin(15, Pin.IN) #15番を入力（受信）と定義

def read_distance():
    hasshin.low() #9行から13行までのコードで超音波を一瞬だけ発信
    utime.sleep_us(2)
    hasshin.high()
    utime.sleep_us(10)
    hasshin.low()
    while jyushin.value() == 0: #超音波が受信されていないとき
        start = utime.ticks_us() #現時点での稼働時間をマイクロ秒単位で返す
    while jyushin.value() == 1: #超音波が受信されているとき
        goal = utime.ticks_us() #現時点での稼働時間をマイクロ秒単位で返す
    #超音波は一瞬なので、jyushin.value()==0となり、無限ループにはならない
    passed = goal - start
    distance = float((passed * 340 * 0.0001) / 2) #cmで出力
    print(distance)

while True:
   read_distance()
   utime.sleep(1)