====================================
Simple build performance comparison
====================================

These simple python scripts are based on the idea at
https://mesonbuild.com/Simple-comparison.html

I use **ccache** and run the performance tests at least 2 times to decrease the
compile time for each build test run.

This bring into focus the performance of the buildsystem.


Setup test suite::

  clausklein$ ./gen_src.py build
  generate 2 directories containing each 4 source files

Run test suite::

  clausklein$ ./measure.py build
  Running command: rm -rf build-cmake && mkdir -p build-cmake && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER_LAUNCHER=ccache -B build-cmake
  Running command: make -C build-cmake -j 4
  Running command: make -C build-cmake -j 4
  Running command: make -C build-cmake -j 4 clean
  Running command: make -C build-cmake -j 4
  Running command: rm -rf build-cmake-ninja && mkdir -p build-cmake-ninja && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER_LAUNCHER=ccache -B build-cmake-ninja -G Ninja
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: ninja -C build-cmake-ninja -j 4 clean
  Running command: ninja -C build-cmake-ninja -j 4
  Running command: rm -rf build-meson && mkdir -p build-meson && CC='ccache gcc' meson build-meson
  Running command: ninja -C build-meson -j 4
  Running command: ninja -C build-meson -j 4
  Running command: ninja -C build-meson -j 4 clean
  Running command: ninja -C build-meson -j 4
  cmake-make
   0.865 gen
   0.518 build
   0.189 empty build
   0.095 clean
   0.566 rebuild
   2.234 overall
  cmake-ninja
   0.718 gen
   0.188 build
   0.013 empty build
   0.032 clean
   0.204 rebuild
   1.155 overall
  meson
   1.611 gen
   0.237 build
   0.013 empty build
   0.022 clean
   0.219 rebuild
   2.101 overall


The ninja based builds are the best as expected
-----------------------------------------------

One interesting point is the different size of the generated ninja build files.
The meson build generator creates only one and a simpler and clear
**build.ninja** file::

  clausklein$ find build -name '*.ninja' -ls
  81941300       48 -rw-r--r--    1 clausklein   staff   21306  8 Feb 10:17 build/buildcmakeninja/build.ninja
  81941301        8 -rw-r--r--    1 clausklein   staff    2681  8 Feb 10:17 build/buildcmakeninja/rules.ninja
  81941494       16 -rw-r--r--    1 clausklein   staff    5686  8 Feb 10:17 build/buildmeson/build.ninja
  clausklein$


And build performance with a real project
------------------------------------------

The https://github.com/open-source-parsers/jsoncpp use both, *meson* and *cmake*::

  bash-5.0$ python3 ./build_performance_measure.py
  Running command: rm -rf build-cmake-ninja && mkdir -p build-cmake-ninja && CXX=g++ cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release -G Ninja -B build-cmake-ninja
  Running command: ninja -C build-cmake-ninja
  Running command: ninja -C build-cmake-ninja
  Running command: ninja -C build-cmake-ninja clean
  Running command: ninja -C build-cmake-ninja
  Running command: rm -rf build-meson && mkdir -p build-meson && CXX='ccache g++' meson build-meson
  Running command: ninja -C build-meson
  Running command: ninja -C build-meson
  Running command: ninja -C build-meson clean
  Running command: ninja -C build-meson
  cmake-ninja
   3.755 gen
   0.739 build
   0.018 empty build
   0.044 clean
   0.721 rebuild
   5.276 overall
  meson
   1.918 gen
   1.409 build
   0.014 empty build
   0.032 clean
   1.410 rebuild
   4.784 overall
  bash-5.0$


Interesting is here: The compact *meson.build* file (only 125 lines) generates
fast a realy clear *build.ninja*, but needs more time to build (old i386 with
only 2 cores). Overall for this small project, mesonbuild is faster.

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
