import common_flags as cf
from Flag import Flag
import paho.mqtt.client as mqtt
import json


r_flag = Flag(open("request.flg", "r+"))
a_flag = Flag(open("answer.flg", "r"))
b_flag = Flag(open("busy.flg", "r"))


def on_message(client, obj, msg):
    if msg.payload == "stat":
        send_stat()


def send_stat():
    global mqttc
    buffer = get_answer()
    broker_out = {
        "in_humi": buffer[2], "in_temp": buffer[3], "out_humi": buffer[4],
        "out_temp": buffer[5], "mois": buffer[6], "lumi": buffer[7]
    }
    data_out = json.dumps(broker_out)
    mqttc.publish("/test2", data_out)


def get_answer():
    global r_flag, a_flag

    # Wait until ready
    b_flag.get_data()
    while b_flag.is_busy():
        b_flag.get_data

    # Request data
    r_flag.set_stat([cf.Comp.LINE, cf.Stat.REQUESTED, 0, 0, 0, 0, 0, 0])
    while True:
        a_flag.get_data()
        r_flag.get_data()
        if a_flag.is_answered() and not r_flag.is_acquired() and r_flag.buffer:
            r_flag.set_stat([cf.Comp.LINE, cf.Stat.ACQUIRED, 0, 0, 0, 0, 0, 0])
            return a_flag.buffer


def main():
    global mqttc
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.username_pw_set("brsiutlc", "Rw4rcSFm_gCL")
    mqttc.connect('m15.cloudmqtt.com', 17711)
    mqttc.subscribe("/test1", 0)
    mqttc.loop_forever


main()
