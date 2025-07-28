#pragma once
#include <string>
#include <vector>

struct ProgOpts{
    bool noNewline { false };
    bool doEscapes { false };
    std::vector<std::string> text {};
};

// Parse options from the command line at runtime.
// Uses boost/program_options.hpp
ProgOpts get_opts(int ac, char* av[]);
