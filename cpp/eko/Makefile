CXX := g++
CXXFLAGS := -std=c++20 -O3 -I$(HOME)/.local/include
LDFLAGS := -L$(HOME)/.local/lib
LIBS := -lboost_program_options

SRC := src/main.cpp src/prog_opts.cpp
OBJ := $(SRC:.cpp=.o)

all: eko

eko: $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS) $(LIBS)

# Debug target overrides
debug: CXX = clang++
debug: CXXFLAGS = -std=c++20 -O0 -g -Wall -Wextra -I$(HOME)/.local/include
debug: clean eko

.PHONY: all debug clean
clean:
	rm -f eko src/*.o
