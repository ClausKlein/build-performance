#!/usr/bin/python3 -tt

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


def measure():
    measurements = [
        # PREPARED ['bazel', 'bazel aquery //subdir0:speedtest0', 'CC=clang bazel build //subdir0:speedtest0', 'CC=clang bazel clean'],
        # TBD ['cmake-make', 'rm -rf buildcmake && mkdir -p buildcmake && cd buildcmake && CC=\'ccache gcc\' cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug ..',
        # TBD     'cd buildcmake && make -j 4', 'cd buildcmake && make -j 4 clean'],
        ['cmake-ninja', 'rm -rf buildcmakeninja && mkdir -p buildcmakeninja && cd buildcmakeninja && CC=\'ccache gcc\' cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -G Ninja ..',
            'cd buildcmakeninja && ninja -j 4', 'cd buildcmakeninja && ninja -j 4 clean'],
        ['meson', 'rm -rf buildmeson && mkdir -p buildmeson && CC=\'ccache gcc\' meson buildmeson',
            'ninja -C buildmeson -j 4', 'ninja -C buildmeson -j 4 clean'],
        # NO! ['scons', 'rm -rf buildscons .sconsign.dblite', 'CC=\'ccache gcc\' scons -j 4', 'CC=\'ccache gcc\' scons -j 4 -c'],
        # NO! ['premake', '/home/jpakkane/premake-4.4-beta4/bin/release/premake4 gmake', 'cd buildpremake && make -j 4', none],
        # NO! ['autotools', "rm -f *.o speedtest && autoreconf -vif && mkdir -p buildauto && cd buildauto && ../configure CFLAGS='-O0 -g'", 'cd buildauto && make -j 4', none],
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
