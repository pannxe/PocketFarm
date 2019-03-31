import common_flags as cf
from Flag import Flag
import paho.mqtt.client as mqtt
import json


def on_message(client, obj, msg):
    print("Got a payload: ", end="")
    cmd = msg.payload.decode("utf-8")
    print(cmd)
    cmd = cmd.lower()
    if cmd == "stat":
        send_stat()
    else:
        print("edit\n  Applying new configuration")
        m_in = json.loads(cmd)
        f = open("now_setting.conf", "w")
        f.write("{0} {1} {2} {3}".format (
            m_in["temp"], m_in["humi"], m_in["mois"], m_in["lumi"]
        ))
        f.close()
        print("Done\n")


def send_stat():
    print("Waiting for answer... ")
    buffer = get_answer()
    print("Finished getting answer, sending data to Line... ",)
    broker_out = {
        "in_humi": buffer[2], "in_temp": buffer[3], "out_humi": buffer[4],
        "out_temp": buffer[5], "mois": buffer[6], "lumi": buffer[7]
    }
    print(str(buffer))
    data_out = json.dumps(broker_out)
    mqttc.publish("/test2", data_out)
    print("Finished, Waiting for the next payload\n")


def get_answer():
    r_flag = Flag(open("request.flg", "r+"))
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
        a_flag = Flag(open("answer.flg", "r+"))
        print("  Getting a_flag data... ")
        a_flag.get_data()
        print("    got --> " + str(a_flag.buffer))
        print("  Getting r_flag data... ")
        r_flag.get_data()
        print("    got --> " + str(r_flag.buffer))
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
        a_flag.flag_f.close()
        a_flag.flag_f = open("request.flg", "r+")


print("Pocket Farm's")
print("LINE COMMUNICATION MODULE\nVERSION 1.0.0\n_________________________\n")
print("Initialising... ", end="")
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.username_pw_set("brsiutlc", "Rw4rcSFm_gCL")
mqttc.connect('m15.cloudmqtt.com', 17711)
mqttc.subscribe("/test1", 0)
print("Done\nWaiting for Line payload... \n")
mqttc.loop_forever()
