from common_flags import Stat


class Flag():

    def __init__(self, f):
        self.flag_f = f

    def __del__(self):
        self.flag_f.close()

    def get_data(self):
        self.rewind()
        self.buffer = self.flag_f.readline().split()
        return self.buffer

    def set_stat(self, data):
        self.rewind()
        for i in range(0, 8):
            self.flag_f.write("{0} ".format(data[i], end=""))

    def get_requestor_id(self):
        if not self.buffer:
            return False
        return self.buffer[0]

    def get_target_id(self):
        if not self.buffer:
            return False
        return self.buffer[2]

    def is_acquired(self):
        if not self.buffer:
            return False
        return int(self.buffer[1]) == Stat.ACQUIRED

    def is_requested(self):
        if not self.buffer:
            return False
        return int(self.buffer[1]) == Stat.REQUESTED

    def is_answered(self):
        if not self.buffer:
            return False
        return int(self.buffer[1]) == Stat.ANSWERED

    def is_busy(self):
        if not self.buffer:
            return False
        return int(self.buffer[1]) == Stat.BUSY

    def rewind(self):
        self.flag_f.seek(0)
