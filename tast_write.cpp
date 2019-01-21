#include <cstdio>
#include "Flag.cpp"
#include "common_flags.h"

int main() {
    int buffer[8] = {};

    while(~scanf("%d %d", &buffer[0], &buffer[1])) {
        Flag *r_flag = new Flag(fopen("request.flg", "wb"));
        printf("%s %s ", _cmp[buffer[0]], _cmd[buffer[1]]);
        for (size_t i = 2; i < 8; i++)
            printf("%d ", buffer[i]);

        printf("\n");

        r_flag->set_stat(buffer);
        delete r_flag;
    }
    return 0;
}

/*
0 0
0 1
1 2
0 2
2 1
0 3
3 3
*/
