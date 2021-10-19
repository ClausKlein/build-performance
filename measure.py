#!/usr/bin/env python

import sys
import os
import time
import subprocess


def gettime(command):
    if command is None:
        return 0.0
    print('Running command:', command)
    starttime = time.time()
    subprocess.check_call(command, shell=True, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    endtime = time.time()
    return endtime - starttime


def measure(cores=4):
    cmake_defaults = '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER_LAUNCHER=ccache'

    measurements = [
        # PREPARED ['bazel', 'bazel aquery //subdir0:speedtest0', 'CXX=g++ bazel build //subdir0:speedtest0', 'CXX=g++ bazel clean'],
        ['cmake-make', 'rm -rf {1} && mkdir -p {1} && cmake {0} -B {1}'.format(cmake_defaults, '../build-cmake'),
            'make -C ../build-cmake -j {}'.format(cores),
            'make -C ../build-cmake -j {} clean'.format(cores)],
        ['cmake-ninja', 'rm -rf {1} && mkdir -p {1} && cmake {0} -B {1} -G Ninja'.format(cmake_defaults, '../build-cmake-ninja'),
            'ninja -C ../build-cmake-ninja -j {}'.format(cores),
            'ninja -C ../build-cmake-ninja -j {} clean'.format(cores)],
        ['meson-ninja', 'rm -rf {0} && mkdir -p {0} && CXX=\'ccache g++\' meson --unity on {0}'.format('../build-meson-ninja'),
            'ninja -C ../build-meson-ninja -j {}'.format(cores),
            'ninja -C ../build-meson-ninja -j {} clean'.format(cores)],
        # NO! ['scons', 'rm -rf buildscons .sconsign.dblite', 'CXX=\'ccache g++\' scons -j {}'.format(cores), 'CXX=\'ccache
        # g++\' scons -j {} -c'.format(cores)],
        # NO! ['premake', 'premake4 gmake', 'make -C buildpremake -j {}'.format(cores), None],
        # NO! ['autotools', "rm -f *.o speedtest && autoreconf -vif && mkdir -p buildauto && cd buildauto && ../configure CFLAGS='-O0 -g'", 'make -C buildauto -j {}'.format(cores), None],
    ]
    results = []
    for m in measurements:
        cur = []
        results.append(cur)
        cur.append(m[0])
        conf = m[1]
        make = m[2]
        clean = m[3]
        cur.append(gettime(conf))
        cur.append(gettime(make))
        cur.append(gettime(make))
        cur.append(gettime(clean))
        cur.append(gettime(make))
    return results


def print_times(times):
    for t in times:
        print(t[0])
        print(" %.3f gen" % t[1])
        print(" %.3f build" % t[2])
        print(" %.3f empty build" % t[3])
        print(" %.3f clean" % t[4])
        print(" %.3f rebuild" % t[5])
        overall = t[1] + t[2] + t[3] + t[4] + t[5]
        print(" %.3f overall" % overall)


if __name__ == '__main__':
    src_dir = "generated"
    if len(sys.argv) != 2:
        print(sys.argv[0], '<source dir>')
    else:
        src_dir = sys.argv[1]
    os.chdir(src_dir)
    print_times(measure())
