#include <cstdio>
#include <string>
#include "common_flags.h"

class Flag {
private:
    int buffer[8];
    FILE *flag_f;

public:
    Flag(std::string a, std::string b) {
        flag_f = fopen(a.c_str(), b.c_str());
    }

    ~Flag() {
        fclose(flag_f);
    }

    void refreash(std::string a, std::string b) {
        freopen(a.c_str(), b.c_str(), flag_f);
    }

    int *get_data() {
        _rewind();
        for (size_t i = 0; i < 8; i++)
            fscanf(flag_f, "%d", &buffer[i]);
        return buffer;
    }

    void set_stat(int b[8]) {
        _rewind();
        for (size_t i = 0; i < 8; i++)
            fprintf(flag_f, "%d ", b[i]);
    }

    void set_stat(int self, int stat, int id) {
        int b[] = {self, stat, id, 0, 0, 0, 0, 0};
        set_stat(b);
    }

    void set_stat(int self, int stat) {
        int b[] = {self, stat, 0, 0, 0, 0, 0, 0};
        set_stat(b);
    }

    int get_requestor_id() {
        return buffer[0];
    }

    bool is_requested() {
        return buffer[1] == REQUESTED;
    }

    bool is_answered() {
        return buffer[1] == ANSWERED;
    }

    bool is_acquired() {
        return buffer[1] == ACQUIRED;
    }

    void _rewind() {
        rewind(flag_f);
    }
};
