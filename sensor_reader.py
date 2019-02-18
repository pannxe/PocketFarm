from Flag import Flag
import common_flags as cf


def read_sensor():
    d_flag = Flag(open("sensor_data.flg", "w"))
    in_humi, in_temp = 66, 28
    out_humi, out_temp = 52, 35
    lumi, mois = 1, 740
    d_flag.set_stat([
        cf.Comp.INPUT, cf.Stat.ANSWERED,
        in_humi, in_temp,
        out_humi, out_temp,
        mois, lumi
    ])
    del d_flag


def ready_stat():
    ia_flag = Flag(open("ians.flg", "w"))
    ia_flag.set_stat([cf.Comp.INPUT, cf.Stat.READY, 0, 0, 0, 0, 0, 0])
    del ia_flag


def write_stat():
    ia_flag = Flag(open("ians.flg", "w"))
    ia_flag.set_stat([cf.Comp.INPUT, cf.Stat.ANSWERED, 0, 0, 0, 0, 0, 0])
    del ia_flag


print("Pocket Farm's")
print("SENSOR READER MODULE\nVERSION 1.0.0")
print("_________________________\n")
ir_flag = Flag(open("ireq.flg", "r"))
first = False
while True:
    ir_flag.get_data()
    if ir_flag.is_requested() and not first:
        print("Reading... ", end="")
        read_sensor()
        write_stat()
        print("done")
        first = True

    if ir_flag.is_acquired() and first:
        ready_stat()
        first = False
        print("acquired")
