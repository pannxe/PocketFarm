#include <cstdio>
#include "common_flags.h"
#include "Flag.cpp"
const int self_id = CORE;

int main() {
    Flag    *r_flag = new Flag(fopen("request.flg", "r+b")),
            *b_flag = new Flag(fopen("busy.flg", "w+b"));

    while(true) {
        r_flag->get_data();

        if (r_flag->is_requested()) {
            b_flag->set_stat(self_id, BUSY);
            int id = r_flag->get_requestor_id();
            printf("Got request from %s\n  --> Processing... ", _cmp[id]);
            //
            //
            //
            r_flag->set_stat(self_id, ANSWERED, id);
            b_flag->set_stat(self_id, READY);
            printf("done\n\n");
        }
    }
    return 0;
}
