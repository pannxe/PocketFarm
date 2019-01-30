#ifndef COMMON_FLAGS
    #define COMMON_FLAGS
    enum {
        REQUESTED,
        ANSWERED,
        ACQUIRED,
        BUSY,
        READY
    };
    char _cmd[5][12] = {
        "REQUESTED",
        "ANSWERED",
        "ACQUIRED",
        "BUSY",
        "READY"
    };

    enum {
        LINE,
        INPUT,
        CORE,
        OUTPUT,
        FLAG,
        NULLIUS
    };
    char _cmp[6][12] = {
        "LINE",
        "INPUT",
        "CORE",
        "OUTPUT",
        "FLAG",
        "NULLIUS"
    };
#endif
