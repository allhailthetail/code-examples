// [[file:../main.org::main.cpp][main.cpp]]
// Imported libraries and headers:
#include <iostream>
#include "prog_opts.hpp"

std::string add_escape(const std::string& s) {
    std::string out {};
    for (size_t i = 0; i < s.size(); ++i) {
        if (s[i] == '\\' && (i + 1 < s.size())) {
            switch(s[i + 1]) {
                case 'a': out += '\a'; break;  // alert
                case 'b': out += '\b'; break;  // backspace
                case 'n': out += '\n'; break;  // newline
                case 't': out += '\t'; break;  // tab
                case '\\': out += '\\'; break; // literal backslash
                default: out += s[i+1]; break;
            }
        i++; // Skip because it's already been processed.
        } else { out+= s[i]; }
    }
    return out;
}

// Begin Program:
int main(int ac, char* av[]) {

    // retrieve program args:
    auto opts = get_opts(ac, av);

    // obey escapes?
    if (opts.doEscapes) {
        for (auto &word : opts.text) {
            word = add_escape(word);
        }
    }

    // add spaces between args...
    for (size_t i = 0; i < opts.text.size(); ++i) {
        std::cout << opts.text[i];
        if (i + 1 < opts.text.size()) std::cout << ' ';
    }

    if (opts.noNewline == false) {
    std::cout << '\n';
    }

    // Exit Successfully
    return 0;
 }
// main.cpp ends here
