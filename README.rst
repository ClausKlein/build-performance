====================================
Simple build performance comparison
====================================

These simple python scripts are based on the idea at
https://mesonbuild.com/Simple-comparison.html

I use **ccache** and run the performance tests at least 2 times to decrease the
compile time for each build test run.

This bring into focus the performance of the buildsystem.


Setup test suite::

  clausklein$ ./gen_src.py --outdir=generated
  generate 9 directories containing each 7 source files
  clausklein$

Run test suite::

  clausklein$ ./measure.py generated
  Running command: rm -rf build-cmake && mkdir -p build-cmake && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -B build-cmake
  Running command: make -C build-cmake -j 4
  Running command: make -C build-cmake -j 4
  Running command: make -C build-cmake -j 4 clean
  Running command: make -C build-cmake -j 4
  Running command: rm -rf build-cmake-ninja && mkdir -p build-cmake-ninja && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -B build-cmake-ninja -G Ninja
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: ninja -C build-cmake-ninja -j 4 clean
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: rm -rf build-meson && mkdir -p build-meson && CC='ccache g++' meson build-meson
  Running command: ninja -C build-meson -j 4
  Running command: ninja -C build-meson -j 4
  Running command: ninja -C build-meson -j 4 clean
  Running command: ninja -C build-meson -j 4
  cmake-make
   0.401 gen
   0.803 build
   0.200 empty build
   0.076 clean
   0.797 rebuild
   2.275 overall
  cmake-ninja
   0.609 gen
   0.468 build
   0.058 empty build
   0.120 clean
   0.456 rebuild
   1.712 overall
  meson
   1.163 gen
   0.506 build
   0.058 empty build
   0.124 clean
   0.503 rebuild
   2.353 overall
  clausklein$


The ninja based builds are the best as expected
-----------------------------------------------

One interesting point is the different size of the generated ninja build files.
The *meson* build generator creates only one and a simpler and clear
**build.ninja** file::

  clausklein$ find generated -name '*.ninja' -ls
  38100869  72 -rw-r--r-- 1 clausklein staff 34404 16 Okt 22:14 generated/build-meson/build.ninja
  38100178  24 -rw-r--r-- 1 clausklein staff 10302 16 Okt 22:14 generated/build-cmake-ninja/CMakeFiles/rules.ninja
  38100177 184 -rw-r--r-- 1 clausklein staff 91983 16 Okt 22:14 generated/build-cmake-ninja/build.ninja
  clausklein$


And build performance with a real project
------------------------------------------

The https://github.com/open-source-parsers/jsoncpp supports both, *meson* and *cmake*::

  clausklein$ ~/cmake/BuildPerformance/measure.py .
  Running command: rm -rf build-cmake && mkdir -p build-cmake && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -B build-cmake
  Running command: make -C build-cmake -j 4
  Running command: make -C build-cmake -j 4
  Running command: make -C build-cmake -j 4 clean
  Running command: make -C build-cmake -j 4
  Running command: rm -rf build-cmake-ninja && mkdir -p build-cmake-ninja && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -B build-cmake-ninja -G Ninja
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: ninja -C build-cmake-ninja -j 4 clean
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: rm -rf build-meson && mkdir -p build-meson && CC='ccache g++' meson build-meson
  Running command: ninja -C build-meson -j 4
  Running command: ninja -C build-meson -j 4
  Running command: ninja -C build-meson -j 4 clean
  Running command: ninja -C build-meson -j 4
  cmake-make
   1.704 gen
   0.858 build
   0.119 empty build
   0.116 clean
   0.706 rebuild
   3.503 overall
  cmake-ninja
   2.945 gen
   0.558 build
   0.058 empty build
   0.106 clean
   0.391 rebuild
   4.057 overall
  meson
   1.136 gen
   0.427 build
   0.054 empty build
   0.103 clean
   0.432 rebuild
   2.152 overall
  clausklein$

Interesting is here: The compact *meson.build* file (only 120 lines) generates
fast a realy clear *build.ninja*.
Overall for this small project, mesonbuild is faster.

IMHO: The winner seems https://mesonbuild.com using https://ninja-build.org and https://ccache.dev


Recources
----------

**A nice project with a dual build system: cmake and meson**

  * https://github.com/ClausKlein/jsoncpp I used it for the second performance test.

* https://medium.com/@julienjorge/an-overview-of-build-systems-mostly-for-c-projects-ac9931494444
* https://en.wikipedia.org/wiki/List_of_build_automation_software
* https://trends.google.com/trends/explore?date=all&q=bazel,meson,mpc-ace,%2Fm%2F04dl04,%2Fm%2F0cxh7f
* http://esr.ibiblio.org/?p=8581
* http://doc.cat-v.org/plan_9/4th_edition/papers/mk
* https://medium.com/windmill-engineering/bazel-is-the-worst-build-system-except-for-all-the-others-b369396a9e26


Historic
.........

* https://www.google.com/search?q=%22Recursive+Make+Considered+Harmful%22+filetype%3Apdf&oq=&aqs=
* https://manpages.debian.org/testing/mpc-ace/mpc-ace.1.en.html
