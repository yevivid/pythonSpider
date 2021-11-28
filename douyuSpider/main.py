import re
import threading
import time

import websocket
import mysql.connector


# 将字符串数据按照斗鱼协议封装为字节流
def dy_encode(msg):
    # 头部8字节，尾部1字节，与字符串长度相加即数据长度
    # 为什么不加最开头的那个消息长度所占4字节呢？这得问问斗鱼^^
    data_len = len(msg) + 9
    # 字符串转化为字节流
    msg_byte = msg.encode('utf-8')
    # 将数据长度转化为小端整数字节流
    len_byte = int.to_bytes(data_len, 4, 'little')
    # 前两个字节按照小端顺序拼接为0x02b1，转化为十进制即689（《协议》中规定的客户端发送消息类型）
    # 后两个字节即《协议》中规定的加密字段与保留字段，置0
    send_byte = bytearray([0xb1, 0x02, 0x00, 0x00])
    # 尾部以'\0'结束
    end_byte = bytearray([0x00])
    # 按顺序拼接在一起
    data = len_byte + len_byte + send_byte + msg_byte + end_byte

    return data


# 发送登录请求消息
def login(ws, uid):
    msg = 'type@=loginreq/roomid@={}/'.format(uid)
    msg = 'type@=loginreq/roomid@={}/dfl@=/username@=visitor955293/uid@=1309578141/ver@=20190610/aver@=218101901/ct@=0/'.format(uid)
    msg_bytes = dy_encode(msg)
    ws.send(msg_bytes)



# 发送入组消息
def join_group(ws, uid):
    msg = 'type@=joingroup/username@=rieuse/password@=douyu/rid@={}/gid@=-9999/'.format(uid)
    msg = 'type@=joingroup/rid@={}/gid@=-9999/'.format(uid)
    msg_bytes = dy_encode(msg)
    ws.send(msg_bytes)


def on_message(ws, message):
    # 将字节流转化为字符串，忽略无法解码的错误（即斗鱼协议中的头部尾部）
    message = message.decode(encoding='utf-8', errors='ignore')
    # print(message)
    if "/nn@=" in message and "/txt@=" in message:
        text = re.split('/nn@=', message)
        text = re.split('/cid@=', text[1])
        text = re.split('/txt@=', text[0])
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        text.append(localtime)
        print(text)
        connect_mysql(text)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print('close')


def connect_mysql(text):
    cnx = mysql.connector.connect(user='yinianvivid', password='123456',
                                  host='127.0.0.1',
                                  database='spider')

    sql = ("INSERT INTO live (NAME,context,TIME)" + " VALUES (%s,%s,NOW())")
    data = (text[0], text[1])

    cnx.cursor().execute(sql, data)
    cnx.commit()
    cnx.close()


def keep_live(ws):
    heart_data_bytes = dy_encode("type@=mrkl/")
    ws.send(heart_data_bytes)
    time.sleep(30)


def on_open(ws):
    print('open')
    # uid = '501761'
    # uid = '74751'
    uid = '1863767'
    login(ws, uid)
    time.sleep(3)
    # 登录后发送入组消息
    join_group(ws, uid)


ws = websocket.WebSocketApp('wss://danmuproxy.douyu.com:8502/',
                            on_message=on_message, on_error=on_error,
                            on_close=on_close, on_open=on_open)

def main(ws):
    ws.run_forever()

main_thread = threading.Thread(target=main(ws))
heart_thread = threading.Thread(target=keep_live(ws))

main_thread.start()
heart_thread.start()
