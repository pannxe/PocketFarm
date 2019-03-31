gnome-terminal -x bash -c "./fman; exec bash" & gnome-terminal -x bash -c "python3 ./sever_comm.py; exec bash" & gnome-terminal -x bash -c "python3 ./sensor_reader.py; exec bash"


