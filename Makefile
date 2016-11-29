CC=gcc
LIBS=-lmraa

all: main.o
	$(CC) $(LIBS) -o main $^

clean:
	rm -f main main.o *~
