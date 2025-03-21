#include <errno.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <linux/limits.h>

char path[PATH_MAX] = {'\0'};
FILE *current_file = NULL;
// Provide a nicer diagnostic
// if the file was opened in read-only mode.
// (Writing to a read-only file would otherwise error with 'Bad file descriptor'.)
bool file_is_readonly = false; 

void clear_path() {
    path[0] = '\0';
    current_file = NULL;
    file_is_readonly = false;
}

bool startswith(char *str, char *prefix) {
    return strncmp(str, prefix, strlen(prefix)) == 0;
}

void do_open_command(char *user_path) {
    if(realpath(user_path, path) == NULL) {
        perror("could not resolve path");
        clear_path();
        return;
    }
    if(strncmp(path, "/secret.txt", strlen("/secret.txt")) == 0) {
        puts("accessing /secret.txt not allowed");
        clear_path();
        return;
    }
    current_file = fopen(path, "r+");
    if(current_file == NULL) {
        if(errno == EACCES) {
            // Let them try opening it for reading anyway
            current_file = fopen(path, "r");
            if(current_file == NULL) {
                perror("Failed opening file for reading");
                clear_path();
                return;
            }
            file_is_readonly = true;
            return;
        }
        perror("Failed opening file");
        clear_path();
        return;
    }
    file_is_readonly = false;
}

char *HELP_TEXT = 
    "Available commands:\n"
    "open <path>\n"
    "   Open the file located at <path>.\n"
    "   e.g. open /readme.txt - open the file located at `/readme.txt`.\n"
    "   Note: Due to repeated incidents, I have patched this program\n"
    "   to disallow access to `/secret.txt`. THIS PROGRAM WILL NOT LET YOU READ THE SECRETS.\n"
    "set <pos> <new_value>\n"
    "   Change the value at position <position> of the file into the byte <new_value>.\n"
    "   <new_value> should be specified in hexadecimal.\n"
    "   e.g. set 192 3a - set position 192 of the file to the byte 0x3a.\n"
    "get <pos>\n"
    "   Print the byte value at position <pos> as hexadecimal.\n"
    "   e.g. get 192 - get the byte at position 192 of the file.\n"
    "status\n"
    "   Print the current file path, if any.\n"
    "time\n"
    "   Print the current time.\n"
    ;

void do_help() {
    puts(HELP_TEXT);
}

void do_set(uint64_t filepos, char byte) {
    if(current_file == NULL) {
        puts("You're not editing any files currently");
        return;
    }
    if(file_is_readonly) {
        puts("Can't change the contents of a readonly file");
        return;
    }
    if(fseek(current_file, filepos, SEEK_SET) < 0) {
        perror("failed seek");
        return;
    }
    if(fputc(byte, current_file) < 0) {
        perror("failed write");
    }
}

void do_status() {
    if (path[0] == '\0') {
        puts("No files open.");
    } else {
        printf("You are editing %s\n", path);
    }
}

void do_time() {
    system("date +'%I:%M:%S %p, %A %d %B'");
}

void do_get(uint64_t filepos) {
    if(current_file == NULL) {
        puts("You're not editing any files currently");
        return;
    }
    if(fseek(current_file, filepos, SEEK_SET) < 0) {
        perror("failed seek");
        return;
    }
    int ret;
    if((ret = fgetc(current_file)) < 0) {
        if(feof(current_file)) {
            puts("File is too small");
            return;
        }
        perror("failed read");
        return;
    }
    printf("%02x\n", ret);
}

int main() {
    puts("Welcome to HEX (HEX Editor Xtended) v7.5");
    puts("Run 'help' for help");

    char *filepath = malloc(256);
    uint64_t filepos = 0;
    unsigned int byte_to_set = 0;

    char *line = NULL;
    size_t line_memlen = 0;
    ssize_t line_readlen = 0;

    while(!feof(stdin)) {
        printf("> ");
        fflush(stdout);


        if((line_readlen = getline(&line, &line_memlen, stdin)) < 0) {
            if(feof(stdin)) break;
            perror("failure reading line");
            continue;
        }

        if(startswith(line, "status")) {
            do_status();
            continue;
        }

        if(startswith(line, "time")) {
            do_time();
            continue;
        }

        if(startswith(line, "help")) {
            do_help();
            continue;
        }

        if(startswith(line, "open")) {
            if(sscanf(line, "open %255s", filepath) <= 0) {
                printf("invalid command format for `open`\n");
                continue;
            }
            do_open_command(filepath);
            continue;
        }

        if(startswith(line, "set")) {
            if(sscanf(line, "set %lu %x", &filepos, &byte_to_set) <= 0) {
                printf("invalid command format for `set`\n");
                continue;
            }
            do_set(filepos, (char)byte_to_set);
            continue;
        }

        if(startswith(line, "get")) {
            if(sscanf(line, "get %lu", &filepos) <= 0) {
                printf("invalid command format for `get`\n");
                continue;
            }
            do_get(filepos);
            continue;
        }

        printf("unknown command: %s\n", line);
    }

    free(line);
}
