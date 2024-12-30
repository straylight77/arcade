# Automatically load flags from compile_flags.txt
COMPILE_FLAGS := $(shell cat compile_flags.txt)
LINKER_FLAGS := -L/opt/homebrew/opt/sfml@2/lib -lsfml-graphics -lsfml-window -lsfml-system

# Compiler and flags
CXX := g++
CXXFLAGS := -Wall $(COMPILE_FLAGS)

# Source files
SRC := $(wildcard *.cpp)
OBJ := $(SRC:.cpp=.o)

# Output binary
TARGET := asteroids

# Build rules
$(TARGET): $(OBJ)
	$(CXX) $(OBJ) -o $@ $(CXXFLAGS) $(LINKER_FLAGS)

%.o: %.cpp
	$(CXX) -c $< -o $@ $(CXXFLAGS)

clean:
	rm -f $(OBJ) $(TARGET)

easy: $(SRC)
	$(CXX) $(SRC) -o $(TARGET) $(CXXFLAGS) $(LINKER_FLAGS)
