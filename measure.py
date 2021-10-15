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
    cmake_defaults = '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER_LAUNCHER=ccache'

    measurements = [
        # PREPARED ['bazel', 'bazel aquery //subdir0:speedtest0', 'CC=clang bazel build //subdir0:speedtest0', 'CC=gcc bazel clean'],
        #XXX ['cmake-make', 'rm -rf {1} && mkdir -p {1} && cmake {0} -B {1}'.format(cmake_defaults, 'build-cmake'), 'make -C build-cmake -j {}'.format(cores), 'make -C build-cmake -j {} clean'.format(cores)],
        ['cmake-ninja', 'rm -rf {1} && mkdir -p {1} && cmake {0} -B {1} -G Ninja'.format(cmake_defaults, 'build-cmake-ninja'),
            'ninja -C build-cmake-ninja -j {}'.format(cores), 'ninja -C build-cmake-ninja -j {} clean'.format(cores)],
        #XXX ['meson', 'rm -rf {0} && mkdir -p {0} && CC=\'ccache gcc\' meson {0}'.format('build-meson'), 'ninja -C build-meson -j {}'.format(cores), 'ninja -C build-meson -j {} clean'.format(cores)],
        # NO! ['scons', 'rm -rf buildscons .sconsign.dblite', 'CC=\'ccache gcc\' scons -j {}'.format(cores), 'CC=\'ccache gcc\' scons -j {} -c'.format(cores)],
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
    if len(sys.argv) != 2:
        print(sys.argv[0], '<output dir>')
    os.chdir(sys.argv[1])
    print_times(measure())
