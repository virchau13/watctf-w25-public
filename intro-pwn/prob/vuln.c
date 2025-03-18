#include <stdio.h>

void vuln() {
    volatile char buf[55];
    scanf("%s", buf);
}

int main() {
    vuln();
}
