#!/usr/bin/env python3 -tt

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
        ['cmake-make', 'rm -rf buildcmake && mkdir -p buildcmake && cd buildcmake && CC=clang cmake -DCMAKE_BUILD_TYPE=Debug ..',
            'cd buildcmake && make -j 2'],
        ['cmake-ninja', 'rm -rf buildcmakeninja && mkdir -p buildcmakeninja && cd buildcmakeninja && CC=clang cmake -DCMAKE_BUILD_TYPE=Debug -G Ninja ..',
            'cd buildcmakeninja && ninja -j 2'],
        ['meson', 'rm -rf buildmeson && mkdir -p buildmeson && CC=clang meson buildmeson',
            'ninja -C buildmeson -j 2'],
        # ['scons', None, 'scons -j 2'], ['premake', '/home/jpakkane/premake-4.4-beta4/bin/release/premake4 gmake', 'cd buildpremake && make -j 2'],
        ## ['autotools', "rm -f *.o speedtest && autoreconf -vif && mkdir -p buildauto && cd buildauto && ../configure CFLAGS='-O0 -g'", 'cd buildauto && make -j 2'],
    ]
    results = []
    for m in measurements:
        cur = []
        results.append(cur)
        cur.append(m[0])
        conf = m[1]
        make = m[2]
        cur.append(gettime(conf))
        cur.append(gettime(make))
        cur.append(gettime(make))
    return results


def print_times(times):
    for t in times:
        print(t[0])
        print(" %.3f gen" % t[1])
        print(" %.3f build" % t[2])
        print(" %.3f empty build" % t[3])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0], '<output dir>')
    os.chdir(sys.argv[1])
    print_times(measure())
