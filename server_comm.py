import common_flags as cf
from Flag import Flag
import paho.mqtt.client as mqtt
import json


def sendStat(brokerOut):
    dataOut = json.dumps(brokerOut)
    mqttc.publish("/test2", dataOut)
    print("Finished\nWaiting for the next payload...")


def applyStat(cmd) :
    print("Applying new configuration...", end="")
    m_in = json.loads(cmd)
    with open("now_setting.conf", "w") as f :
        f.write(f"{m_in['temp']} {m_in['humi']} {m_in['mois']} {m_in['lumi']}")
    print("Done\n")


def getAnswer():
    r_flag = Flag(open("request.flg", "r+"))
    a_flag = Flag(open("answer.flg", "r+"))
    b_flag = Flag(open("busy.flg", "r+"))

    # Wait until ready
    print("Getting b_flag data... ", end="")
    b_flag.get_data()
    while b_flag.is_busy():
        b_flag.get_data()
    print("Done")
    # Request data
    print("Set r_flag to REQUESTED... ", end="")
    r_flag.set_stat([cf.Comp.LINE, cf.Stat.REQUESTED, 0, 0, 0, 0, 0, 0])
    print("Done")

    while True:
        print("  Getting a_flag data... ")
        a_flag.get_data()
        print(f"    got --> {a_flag.buffer}")
        print("  Getting r_flag data... ")
        r_flag.get_data()
        print(f"    got --> {r_flag.buffer}")
        if a_flag.is_answered() and r_flag.buffer:
            print("  Set r_flag to ACQUIRED... ", end="")
            r_flag.set_stat([cf.Comp.LINE, cf.Stat.ACQUIRED, 0, 0, 0, 0, 0, 0])
            print("Done")
            d_flag = Flag(open("sensor_data.flg", "r"))
            buffer = d_flag.get_data()
            del r_flag
            del a_flag
            del b_flag
            return buffer

def onMessage(client, obj, msg):
    cmd = msg.payload.decode("utf-8").lower()
    print(f"Got a payload: {cmd}")

    if cmd == "stat":
        print("Waiting for answer... ")
        buffer = getAnswer()
        print(f"Finished getting answer.\nBuffer : {buffer}")

        brokerOut = {
        "in_humi": buffer[2], "in_temp": buffer[3], "out_humi": buffer[4],
        "out_temp": buffer[5], "mois": buffer[6], "lumi": buffer[7]
        }
        sendStat(brokerOut)
    elif cmd == "edit":
        applyStat(cmd)

print("Pocket Farm's")
print("LINE COMMUNICATION MODULE\nVERSION 1.0.0\n_________________________\n")
print("Initialising... ", end="")
mqttc = mqtt.Client()
mqttc.on_message = onMessage
mqttc.username_pw_set("brsiutlc", "Rw4rcSFm_gCL")
mqttc.connect('m15.cloudmqtt.com', 17711)
mqttc.subscribe("/test1", 0)
print("Done\nWaiting for Line payload... \n")
mqttc.loop_forever()
