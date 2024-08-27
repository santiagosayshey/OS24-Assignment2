#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    int pageNo;
    int modified;
    int frameNo;
    int lastUsed;
} Page;

enum repl { rand_repl, lru, clock_repl };
int createMMU(int);
int checkInMemory(int);
int allocateFrame(int);
Page selectVictim(int, enum repl);
void updatePageAccess(int, char);

const int pageoffset = 12;  /* Page size is fixed to 4 KB */
int numFrames;
Page *pages;
int *frames;
int clockHand = 0;
int currentTime = 0;

/* Creates the page table structure to record memory allocation */
int createMMU(int frameCount)
{
    numFrames = frameCount;
    pages = calloc(1 << (32 - pageoffset), sizeof(Page));
    frames = calloc(frameCount, sizeof(int));

    if (!pages || !frames) {
        free(pages);
        free(frames);
        return -1;
    }

    for (int i = 0; i < (1 << (32 - pageoffset)); i++) {
        pages[i].frameNo = -1;  // Initialize all pages with invalid frame numbers
    }

    for (int i = 0; i < numFrames; i++) {
        frames[i] = -1;
    }

    srand(time(NULL));
    return 0;
}


/* Checks for residency: returns frame no or -1 if not found */
int checkInMemory(int page_number)
{
    return pages[page_number].frameNo;
}

/* allocate page to the next free frame and record where it put it */
int allocateFrame(int page_number)
{
    for (int i = 0; i < numFrames; i++) {
        if (frames[i] == -1) {
            frames[i] = page_number;
            pages[page_number].frameNo = i;
            return i;
        }
    }
    return -1;
}

/* Selects a victim for eviction/discard according to the replacement algorithm, returns chosen frame_no */
Page selectVictim(int page_number, enum repl mode)
{
    Page victim = {0};
    int victimFrame = -1;

    switch (mode) {
        case rand_repl:
            victimFrame = rand() % numFrames;
            break;

        case lru:
            {
                int oldestTime = currentTime;
                for (int i = 0; i < numFrames; i++) {
                    int currentPage = frames[i];
                    if (pages[currentPage].lastUsed < oldestTime) {
                        oldestTime = pages[currentPage].lastUsed;
                        victimFrame = i;
                    }
                }
            }
            break;

        case clock_repl:
            while (1) {
                if (!pages[frames[clockHand]].modified) {
                    victimFrame = clockHand;
                    clockHand = (clockHand + 1) % numFrames;
                    break;
                }
                pages[frames[clockHand]].modified = 0;  // Reset the modified bit
                clockHand = (clockHand + 1) % numFrames;
            }
            break;
    }

    int victimPage = frames[victimFrame];
    victim.pageNo = victimPage;
    victim.modified = pages[victimPage].modified;
    victim.frameNo = victimFrame;

    pages[victimPage].frameNo = -1;
    // Don't reset the modified bit here, it should be done in the main loop

    frames[victimFrame] = page_number;
    pages[page_number].frameNo = victimFrame;
    pages[page_number].modified = 0;  // New page starts as unmodified

    return victim;
}


void updatePageAccess(int page_number, char rw)
{
    pages[page_number].lastUsed = currentTime++;
    if (rw == 'W') {
        pages[page_number].modified = 1;
    }
}

int main(int argc, char *argv[])
{
    char *tracename;
    int page_number, frame_no, done;
    int do_line;
    int no_events, disk_writes, disk_reads;
    int debugmode;
    enum repl replace;
    int allocated = 0;
    unsigned address;
    char rw;
    Page Pvictim;
    FILE *trace;

    if (argc < 5) {
        printf("Usage: ./memsim inputfile numberframes replacementmode debugmode \n");
        exit(-1);
    }
    else {
        tracename = argv[1];
        trace = fopen(tracename, "r");
        if (trace == NULL) {
            printf("Cannot open trace file %s \n", tracename);
            exit(-1);
        }
        numFrames = atoi(argv[2]);
        if (numFrames < 1) {
            printf("Frame number must be at least 1\n");
            exit(-1);
        }
        if (strcmp(argv[3], "lru") == 0)
            replace = lru;
        else if (strcmp(argv[3], "rand") == 0)
            replace = rand_repl;
        else if (strcmp(argv[3], "clock") == 0)
            replace = clock_repl;
        else {
            printf("Replacement algorithm must be rand/lru/clock \n");
            exit(-1);
        }

        if (strcmp(argv[4], "quiet") == 0)
            debugmode = 0;
        else if (strcmp(argv[4], "debug") == 0)
            debugmode = 1;
        else {
            printf("Debug mode must be quiet/debug \n");
            exit(-1);
        }
    }

    done = createMMU(numFrames);
    if (done == -1) {
        printf("Cannot create MMU");
        exit(-1);
    }
    no_events = 0;
    disk_writes = 0;
    disk_reads = 0;

	do_line = fscanf(trace, "%x %c", &address, &rw);
    while (do_line == 2)
    {
        page_number = address >> pageoffset;
        frame_no = checkInMemory(page_number);

        if (frame_no == -1)
        {
            disk_reads++;            /* Page fault, need to load it into memory */
            if (debugmode)
                printf("Page fault %8d \n", page_number);
            if (allocated < numFrames)
            {
                frame_no = allocateFrame(page_number);
                allocated++;
            }
            else {
                Pvictim = selectVictim(page_number, replace);
                if (Pvictim.modified)
                {
                    disk_writes++;
                    if (debugmode) printf("Disk write %8d \n", Pvictim.pageNo);
                }
                else
                    if (debugmode) printf("Discard    %8d \n", Pvictim.pageNo);
                frame_no = Pvictim.frameNo;  // Use the victim's frame for the new page
            }
        }

        updatePageAccess(page_number, rw);
        if (rw == 'R') {
            if (debugmode) printf("reading    %8d \n", page_number);
        }
        else if (rw == 'W') {
            pages[page_number].modified = 1;  // Set the modified bit
            if (debugmode) printf("writing    %8d \n", page_number);
        }
        else {
            printf("Badly formatted file. Error on line %d\n", no_events + 1);
            exit(-1);
        }

        no_events++;
        do_line = fscanf(trace, "%x %c", &address, &rw);
    }

    printf("total memory frames:  %d\n", numFrames);
    printf("events in trace:      %d\n", no_events);
    printf("total disk reads:     %d\n", disk_reads);
    printf("total disk writes:    %d\n", disk_writes);
    printf("page fault rate:      %.4f\n", (float)disk_reads / no_events);

    // Free allocated memory
    free(pages);
    free(frames);

    return 0;
}