#include <cstdio>
#include "Flag.cpp"
#include "common_flags.h"

int main() {
    Flag *r_flag = new Flag(fopen("request.flg", "w+")),
         *a_flag = new Flag(fopen("answer.flg", "r"));

    while(true) {
        int *buffer = a_flag->get_data();
        r_flag->get_data();
        if (a_flag->is_answer() && !r_flag->is_acquired()) {
            for (size_t i = 0; i < 8; i++) {
                printf("%d ", buffer[i]);
            }
            printf("\n");
            r_flag->set_stat(NULLIUS, ACQUIRED);
        }
    }
    return 0;
}
