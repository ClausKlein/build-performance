#!/usr/bin/env python3 -tt

import sys
import os


def gen_test(outdir, num_files=10, num_dirs=10):
    gen_src_tree(outdir, num_files, num_dirs)
    gen_cmake_tree(outdir, num_files, num_dirs)
    gen_meson_tree(outdir, num_files, num_dirs)
    gen_scons_tree(outdir, num_files, num_dirs)
    # NO! gen_autotools(outdir, num_files)
    # NO! gen_premake(outdir, num_files)


def gen_premake(outdir, num_files):
    pfile = open(os.path.join(outdir, 'premake4.lua'), 'w')
    pfile.write('''
solution "Speedtest"
  configurations { "Debug", "Release"}
  location "buildpremake"

project "Speedtest"
  kind "ConsoleApp"
  language "C"
  location "buildpremake"
  files { "*.c", "*.h" }
''')


def gen_scons_tree(outdir, num_files, num_dirs):
    sfile = open(os.path.join(outdir, 'SConstruct'), 'w')
    sfile.write("env = DefaultEnvironment(CCFLAGS = '-g')\n")
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        sfile.write("SConscript('%s/SConstruct', variant_dir='buildscons/%s', duplicate=0)\n" % (subdir, subdir))
        gen_scons(os.path.join(outdir, subdir), i, num_files)


def gen_scons(outdir, target, num_files):
    sfile = open(os.path.join(outdir, 'SConstruct'), 'w')
    sfile.write("""src_files = Split('main.c""")
    for i in range(num_files):
        sfile.write(""" file%d.c""" % i)
    sfile.write("""')\nenv = Environment()\n""")
    sfile.write("env.Program('speedtest%d', source=src_files)\n" % target)


def gen_meson_tree(outdir, num_files, num_dirs):
    cfile = open(os.path.join(outdir, 'meson.build'), 'w')
    cfile.write("project('speedtest', 'c')\n")
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        cfile.write("subdir('%s')\n" % subdir)
        gen_meson(os.path.join(outdir, subdir), i, num_files)


def gen_meson(outdir, target, num_files):
    mfile = open(os.path.join(outdir, 'meson.build'), 'w')
    mfile.write("executable('speedtest%d', 'main.c'" % target)
    for i in range(num_files):
        mfile.write(""", 'file%d.c'""" % i)
    mfile.write(')\n')


def gen_autotools(outdir, num_files):
    for i in ['NEWS', 'README', 'AUTHORS', 'ChangeLog']:
        open(os.path.join(outdir, i), 'w')
    acfile = open(os.path.join(outdir, 'configure.ac'), 'w')
    acfile.write('''AC_INIT([buildtest], [1.0], [foo@example.com])
AC_PREREQ(2.69)
AM_INIT_AUTOMAKE(buildtest, 1.0)
AM_SILENT_RULES([yes])
AC_PROG_CC
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
''')
    acfile.close()
    amfile = open(os.path.join(outdir, 'Makefile.am'), 'w')
    amfile.write('''bin_PROGRAMS = speedtest
speedtest_SOURCES = main.c ''')
    for i in range(num_files):
        line = ' file%d.c' % i
        amfile.write(line)
    amfile.write('\n')


def gen_cmake_tree(outdir, num_files, num_dirs):
    cfile = open(os.path.join(outdir, 'CMakeLists.txt'), 'w')
    cfile.write("project(speedtest C)\n")
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        cfile.write("add_subdirectory(%s)\n" % subdir)
        gen_cmake(os.path.join(outdir, subdir), i, num_files)


def gen_cmake(outdir, target, num_files):
    cfile = open(os.path.join(outdir, 'CMakeLists.txt'), 'w')
    cfile.write("add_executable(testexe%d main.c\n" % target)
    for i in range(num_files):
        cfile.write('  file%d.c\n' % i)
    cfile.write(')\n')


def gen_src_tree(outdir, num_files, num_dirs):
    for i in range(num_dirs):
        subdir = 'subdir%d' % i
        os.makedirs(subdir, exist_ok=True)
        gen_src(os.path.join(outdir, subdir), num_files)


def gen_src(outdir, num_files):
    ftempl = '#include<stdio.h>\n#include"header.h"\n\nint func%d() { return 0; }\n'
    hlinetempl = "int func%d();\n"
    mainlinetempl = '  func%d();\n'
    hfile = open(os.path.join(outdir, 'header.h'), 'w')
    mainfile = open(os.path.join(outdir, 'main.c'), 'w')
    mainfile.write('''#include "header.h"
int main(int argc, char **argv) {
''')
    for i in range(num_files):
        fname = os.path.join(outdir, 'file%d.c' % i)
        fcontents = ftempl % i
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0], '<output dir>')
        sys.exit(1)
    outdir = sys.argv[1]
    gen_test(outdir)
