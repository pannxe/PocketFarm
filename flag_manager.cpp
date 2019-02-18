#include <cstdio>

#include "common_flags.h"
#include "Flag.cpp"

const int self_id = FLAG;

bool get_sensor() {
    Flag    *ir_flag = new Flag(fopen("ireq.flg", "w")),
            *ia_flag = new Flag(fopen("ians.flg", "r"));

    printf("\n    Request has sent to Sensor Reader Module... ");
    ir_flag->set_stat(self_id, REQUESTED);
    delete ir_flag;

    while(true) {
        ia_flag->get_data();
        if(ia_flag->is_answered()) {
            Flag *ir_flag = new Flag(fopen("ireq.flg", "w"));
            ir_flag->set_stat(self_id, ACQUIRED);
            printf("answer acquired\n");
            delete ir_flag;
            return true;
        }
    }
    return false;
}

int main() {
    printf("Pocket Farm's\nFLAG MANAGER MODULE\nVERSION 1.0.0\n_________________________\n");
    Flag    *r_flag = new Flag(fopen("request.flg", "r")),
            *a_flag = new Flag(fopen("answer.flg", "w+")),
            *b_flag = new Flag(fopen("busy.flg", "w"));

    bool first = false;
    printf("Waiting for request...\n");
    while(true) {
        b_flag->set_stat(self_id, READY);
        r_flag->get_data();
        if (r_flag->is_requested()) {
            first = true;
            b_flag->set_stat(self_id, BUSY);
            int id = r_flag->get_requestor_id();
            printf("Got request from %s\n  --> Processing... ", _cmp[id]);
            if(get_sensor()) {
                a_flag->set_stat(self_id, ANSWERED, id);
                printf("done\n\n");
            }
            else {
                printf("Error!");
                return 1;
            }
        }
        if (r_flag->is_acquired() && first) {
            first = false;
            printf("acquired\n\n");
        }
    }

    return 0;
}
