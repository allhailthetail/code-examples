// Description: Parses args to tidy key-value pairs using boost libs
#include "prog_opts.hpp"
#include <boost/program_options.hpp>
#include <iostream>

namespace po = boost::program_options;

ProgOpts get_opts(int ac, char* av[]) {

    // Holds the options in our custom struct,
    //   since we only need basic functionality right now...
    ProgOpts opts {};

    po::options_description desc("Allowed options");
    desc.add_options()
        // long-short value pairs go here. ORDER MATTERS!
        ("help,h", "produce help message")

        ("escapes,e", po::bool_switch(&opts.doEscapes),
         "enable interpretation of backslash escapes")

        ("no-newline,n", po::bool_switch(&opts.noNewline),
         "do not output the trailing newline")

        ("text", po::value<std::vector<std::string>>(&opts.text),
         "Text to echo...")
    ;

    po::variables_map vm {};

    // Positional argument binding
    po::positional_options_description pd; pd.add("text", -1);

    // Parsing begins here, feeds into vm variable.
    po::store(po::command_line_parser(ac, av)
              .options(desc)
              .positional(pd)
              .run(),
              vm);

    // Must be called after values are stored...
    po::notify(vm);

    // if help is called as a flag, display help and return to caller:
    if (vm.count("help")) {
        std::cout << desc << '\n';
        return {};
    }

    return opts;
}
