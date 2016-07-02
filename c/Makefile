CC = gcc
PATH_I = include
PATH_L = lib
FLAG_L = -lfreeglut -lglew32 -lopengl32 -lglu32

SRC = src
BUILD = bin

RM = del

.PHONY: hello clean

hello:
	$(CC) $(SRC)\hello.c -I $(PATH_I) -L $(PATH_L) $(FLAG_L) -o $(BUILD)\hello.exe
	$(BUILD)\run.bat $(BUILD)\hello.exe

clean:
	$(RM) $(BUILD)\*.exe
