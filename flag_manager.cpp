#include <cstdio>

#include "common_flags.h"
#include "Flag.cpp"

const int self_id = FLAG;

int main() {
    Flag    *r_flag = new Flag(fopen("request.flg", "r")),
            *a_flag = new Flag(fopen("answer.flg", "w+")),
            *b_flag = new Flag(fopen("busy.flg", "w"));

    bool first = false;
    while(true) {
        r_flag->get_data();
        if (r_flag->is_requested()) {
            first = true;
            b_flag->set_stat(self_id, BUSY);
            int id = r_flag->get_requestor_id();
            printf("Got request from %s\n  --> Processing... ", _cmp[id]);
            //
            // system("python .\\sensors.py");
            //
            a_flag->set_stat(self_id, ANSWERED, id);
            b_flag->set_stat(self_id, READY);
            printf("done... ");
        }
        else if (r_flag->is_acquired() && first) {
            first = false;
            printf("acquired\n\n");
        }
    }
    return 0;
}
