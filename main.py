import network
import socket
import time
import dht
from machine import Pin

sensor = dht.DHT11(Pin(4))

# Connect to Wi-Fi
ssid = 'xxxxxxxx'
password = 'xxxxxxxx'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    pass

print('Connected. IP:', wifi.ifconfig()[0])

# HTML template
def web_page(temp, hum):
    return """<html>
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="refresh" content="5">
                    <title>DHT11 Sensor</title>
                </head>
                <body>
                    <h1>Temperature: {} &#176;C 🌡️</h1>
                    <h2>Humidity: {} % 💧</h2>
                    <p>Auto refresh every 5 seconds 🔄</p>
                    <p>Stay cool! 😎</p>
                </body>
              </html>""".format(temp, hum)


# Start web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Web server running...')

while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        response = web_page(temp, hum)
        cl.send('HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    except OSError:
        pass
