CC = gcc
CFLAGS = -Wall -Wextra -g
TARGET = memsim

.PHONY: all clean test

all: $(TARGET)

$(TARGET): memsim.c
	$(CC) $(CFLAGS) -o $(TARGET) memsim.c

test: $(TARGET)
	@echo "Running tests..."
	@echo "Test 1: trace1 with 4 frames, LRU algorithm"
	./$(TARGET) trace1 4 lru quiet
	@echo "\nTest 2: trace1 with 8 frames, Clock algorithm"
	./$(TARGET) trace1 8 clock quiet
	@echo "\nTest 3: trace2 with 6 frames, LRU algorithm"
	./$(TARGET) trace2 6 lru quiet
	@echo "\nTest 4: trace3 with 4 frames, Clock algorithm"
	./$(TARGET) trace3 4 clock quiet
	@echo "\nTests completed."

clean:
	rm -f $(TARGET)