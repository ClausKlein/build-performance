#!/usr/bin/env python

import getopt
import sys
import os

from textwrap import dedent


def gen_test(outdir, num_dirs, num_files):
    print("generate %d directories containing each %d source files at ./%s\n" %
          (num_dirs, num_files + 1, outdir))
    gen_src_tree(outdir, num_files, num_dirs)
    # XXX gen_ninja_tree(outdir, num_files, num_dirs)
    gen_cmake_tree(outdir, num_files, num_dirs)
    gen_meson_tree(outdir, num_files, num_dirs)
    # TODO gen_bazel_tree(outdir, num_files, num_dirs)
    # deprecated! gen_scons_tree(outdir, num_files, num_dirs)
    # NO! gen_autotools(outdir, num_files)
    # NO! gen_premake(outdir, num_files)


def gen_premake(outdir, num_files):
    pfile = open(os.path.join(outdir, 'premake4.lua'), 'w')
    pfile.write(dedent('''
         solution "Speedtest"
           configurations { "Debug", "Release"}
           location "buildpremake"
         
         project "Speedtest"
           kind "ConsoleApp"
           language "C"
           location "buildpremake"
           files { "*.cpp", "*.h" }
         '''))


def gen_scons_tree(outdir, num_files, num_dirs):
    sfile = open(os.path.join(outdir, 'SConstruct'), 'w')
    sfile.write("env = DefaultEnvironment(CCFLAGS = '-g')\n")
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        sfile.write(
            "SConscript('%s/SConstruct', variant_dir='buildscons/%s', duplicate=0)\n" % (subdir, subdir))
        gen_scons(os.path.join(outdir, subdir), i, num_files)


def gen_scons(outdir, target, num_files):
    sfile = open(os.path.join(outdir, 'SConstruct'), 'w')
    sfile.write("""src_files = Split('main.cpp""")
    for i in range(num_files):
        sfile.write(""" file%d.cpp""" % i)
    sfile.write("""')\nenv = Environment()\n""")
    sfile.write("env.Program('speedtest%d', source=src_files)\n" % target)


def gen_ninja_tree(outdir, num_files, num_dirs):
    cfile = open(os.path.join(outdir, 'build.ninja'), 'w')
    cwd = os.path.realpath(outdir)
    cfile.write("PWD={}\n".format(cwd))
    cfile.write(dedent('''
        rule cp
          command = cp $in $out
        
        rule cc
          depfile = $out.d
          deps = g++
          command = ccache g++ -c -I$PWD $IN -o $out $FLAGS -MMD -MT $out -MF $out.d
        
        rule link
          command = g++ -o $out $in $LINK_PATH $LINK_LIBRARIES
        
        build config: phony config.h
        build config.h: cp config.h.in
        
        '''))
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        odir = os.path.realpath(outdir)
        gen_ninja(os.path.join(odir, subdir), i, num_files, cfile)
        cfile.write("\n")

    # build bin/main0: link main0.o subdir0/file0.o subdir0/file2.o subdir0/file3.o ...
    for i in range(num_dirs):
        cfile.write("build bin/main{0}: link bin/main{0}.o ".format(i))
        subdir = 'subdir%d' % i
        odir = os.path.realpath(outdir)
        for f in range(num_files):
            cfile.write("{}/subdir{}/file{}.o ".format(odir, i, f))
        cfile.write("\n")
    cfile.write("\n")

    # build all: phony config bin/main0 bin/main1 bin/main2 ...
    cfile.write("build all: phony config ")
    for i in range(num_dirs):
        cfile.write("bin/main{} ".format(i))
    cfile.write("\ndefault all\n")


def gen_ninja(outdir, target, num_files, cfile):
    # build bin/main0.o: cc subdir0/main.cpp || config.h
    cfile.write("build bin/main%d.o: cc %s/main.cpp || config.h\n" % (target, outdir))
    cfile.write("  IN = %s/main.cpp\n" % outdir)
    for i in range(num_files):
        cfile.write("build {1}/file{0}.o: cc {1}/file{0}.cpp || config.h\n".format(i, outdir))
        cfile.write("  IN = {1}/file{0}.cpp\n".format(i, outdir))


def gen_meson_tree(outdir, num_files, num_dirs):
    cfile = open(os.path.join(outdir, 'meson.build'), 'w')
    cfile.write(dedent("""
        project('speedtest', 'cpp')
        conf_data = configuration_data()
        conf_data.set('PROJECT_VERSION', '1.2.3')
        configure_file(input : 'config.h.in',
                       output : 'config.h',
                       configuration : conf_data)
        """))
    # odir = os.path.realpath(outdir)
    # cfile.write("incdir = include_directories('%s')\n" % odir)
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        cfile.write("subdir('%s')\n" % subdir)
        gen_meson(os.path.join(outdir, subdir), i, num_files)


def gen_meson(outdir, target, num_files):
    mfile = open(os.path.join(outdir, 'meson.build'), 'w')
    # odir = os.path.relpath("..", start=outdir + "/..")
    odir = ".."
    mfile.write("incdir = include_directories('%s')\n" % odir)
    mfile.write("static_library('speedtest%d', 'main.cpp'" % target)
    for i in range(num_files):
        mfile.write(""", 'file%d.cpp'""" % i)
    mfile.write(', include_directories : incdir)\n')


def gen_bazel_tree(outdir, num_files, num_dirs):
    cfile = open(os.path.join(outdir, 'WORKSPACE'), 'w')
    # cfile.write("project('speedtest', 'cpp')\n")
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        # cfile.write("subdir('%s')\n" % subdir)
        gen_bazel(os.path.join(outdir, subdir), i, num_files)


def gen_bazel(outdir, target, num_files):
    mfile = open(os.path.join(outdir, 'BUILD'), 'w')
    mfile.write("""# load("@rules_cc//cc:defs.bzl", "cc_binary")\n\n""")
    mfile.write("""cc_binary(\n\tname = "speedtest%d",\n\tsrcs = ["main.cpp" """ % target)
    for i in range(num_files):
        mfile.write(""", "file%d.cpp" """ % i)
    mfile.write("],\n)\n")


def gen_autotools(outdir, num_files):
    for i in ['NEWS', 'README', 'AUTHORS', 'ChangeLog']:
        open(os.path.join(outdir, i), 'w')
    acfile = open(os.path.join(outdir, 'configure.ac'), 'w')
    acfile.write(dedent('''
        AC_INIT([buildtest], [1.0], [foo@example.com])
        AC_PREREQ(2.69)
        AM_INIT_AUTOMAKE(buildtest, 1.0)
        AM_SILENT_RULES([yes])
        AC_PROG_CC
        AC_CONFIG_FILES([Makefile])
        AC_OUTPUT
        '''))
    acfile.close()
    amfile = open(os.path.join(outdir, 'Makefile.am'), 'w')
    amfile.write(dedent('''
        bin_PROGRAMS = speedtest
        speedtest_SOURCES = main.cpp
        '''))
    for i in range(num_files):
        line = ' file%d.cpp' % i
        amfile.write(line)
    amfile.write('\n')


def gen_cmake_tree(outdir, num_files, num_dirs):
    cfile = open(os.path.join(outdir, 'CMakeLists.txt'), 'w')
    cfile.write(dedent("""
        cmake_minimum_required(VERSION 3.16...3.21)
        project(speedtest VERSION 1.2.3 LANGUAGES CXX)
        configure_file(
            ${CMAKE_CURRENT_SOURCE_DIR}/config.h.in
            ${CMAKE_CURRENT_BINARY_DIR}/config.h
            @ONLY
        )
        include_directories(${CMAKE_CURRENT_BINARY_DIR})
        """))
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        cfile.write("add_subdirectory(%s)\n" % subdir)
        gen_cmake(os.path.join(outdir, subdir), i, num_files)


def gen_cmake(outdir, target, num_files):
    cfile = open(os.path.join(outdir, 'CMakeLists.txt'), 'w')
    cfile.write("add_library(testlib%d STATIC main.cpp\n" % target)
    for i in range(num_files):
        cfile.write('  file%d.cpp\n' % i)
    cfile.write(')\n')
    cfile.write('set_target_properties(testlib%d PROPERTIES UNITY_BUILD ON)\n' % target)


def gen_src_tree(outdir, num_files, num_dirs):
    os.makedirs(outdir, exist_ok=True)
    # config_h = open(os.path.join(outdir, 'config.h'), 'w')
    # config_h.write("#define VERSION_STR \"0.0.0\"\n")
    config_h_in = open(os.path.join(outdir, 'config.h.in'), 'w')
    config_h_in.write("#ifdef __INTEGRITY\n  #include <integrity.h>\n#endif\n")
    config_h_in.write("#define VERSION_STR \"@PROJECT_VERSION@\"\n")
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        os.makedirs(os.path.join(outdir, subdir), exist_ok=True)
        gen_src(os.path.join(outdir, subdir), num_files)


def gen_src(outdir, num_files):
    ftempl = """
#include "header.h"

#include <cassert>
#include <iostream>
#include <string>

int func{0}() {{
    std::cout << "{0}) std::string(); ";
    std::string s("{0}");
    assert(!s.empty() && (s.length() == 1) && (s.size() == 1));
    std::cout << "s.capacity(): " << s.capacity() << std::endl; // unspecified
    return 0;
}}
"""
    hlinetempl = "int func%d();\n"
    mainlinetempl = '  func%d();\n'
    hfile = open(os.path.join(outdir, 'header.h'), 'w')
    mainfile = open(os.path.join(outdir, 'main.cpp'), 'w')
    mainfile.write(dedent('''
        #include "header.h"
        
        int main(int argc, char **argv) {
        '''))
    hfile.write("#include \"config.h\"\n\n")
    for i in range(num_files):
        fname = os.path.join(outdir, 'file%d.cpp' % i)
        fcontents = ftempl.format(i)
        hcontents = hlinetempl % i
        mcontents = mainlinetempl % i
        cfile = open(fname, 'w')
        cfile.write(fcontents)
        hfile.write(hcontents)
        mainfile.write(mcontents)
        cfile.close()
    mainfile.write('''  return 0;
}
''')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:f:o:", [
                                   "help", "dirnum=", "filenum=", "outdir="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    outdir = 'generated'
    dirnum = 9
    filenum = 7
    for o, a in opts:
        if o in ("-h", "--help"):
            print(sys.argv[0], '--dirnum=2 --filnum=3 --outdir=build')
            sys.exit()
        elif o in ("-o", "--outdir"):
            outdir = str(a)
        elif o in ("-f", "--filenum"):
            filenum = int(a)
        elif o in ("-d", "--dirnum"):
            dirnum = int(a)
        else:
            assert False, "unhandled option"
    # ...
    gen_test(outdir, dirnum, filenum)


if __name__ == '__main__':
    main()
