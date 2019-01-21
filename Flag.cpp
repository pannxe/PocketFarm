#include <cstdio>
#include "common_flags.h"

#define _fread(x, y)     fread(x, sizeof(x), 1, y)
#define _fwrite(x, y)   fwrite(x, sizeof(x), 1, y)

class Flag {
private:
    FILE *flag_f;
    int buffer[8];

public:
    Flag(FILE *f) {
        flag_f = f;
    }

    ~Flag() {
        fclose(flag_f);
    }

    void get_data() {
        rewind(flag_f);
        _fread(buffer, flag_f);
    }

    void set_stat(int self, int stat, int id) {
        _rewind();
        int b[] = {self, stat, id, 0, 0, 0, 0, 0};
        fwrite(b, sizeof(b), 1, flag_f);
    }

    void set_stat(int self, int stat) {
        _rewind();
        int b[] = {self, stat, 0, 0, 0, 0, 0, 0};
        fwrite(b, sizeof(b), 1, flag_f);
    }

    void set_stat(int b[8]) {
        _rewind();
        fwrite(b, sizeof(b), 1, flag_f);
    }

    int get_requestor_id() {
        return buffer[0];
    }

    bool is_requested() {
        return buffer[1] == REQUESTED;
    }

    void _rewind() {
        rewind(flag_f);
    }
};
