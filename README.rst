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
  Running command: rm -rf buildcmake && mkdir -p buildcmake && cd buildcmake && CC='ccache gcc' cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug ..
  Running command: cd buildcmake && make -j 2
  Running command: cd buildcmake && make -j 2
  Running command: cd buildcmake && make -j 2 clean
  Running command: cd buildcmake && make -j 2
  Running command: rm -rf buildcmakeninja && mkdir -p buildcmakeninja && cd buildcmakeninja && CC='ccache gcc' cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -G Ninja ..
  Running command: cd buildcmakeninja && ninja -j 2
  Running command: cd buildcmakeninja && ninja -j 2
  Running command: cd buildcmakeninja && ninja -j 2 clean
  Running command: cd buildcmakeninja && ninja -j 2
  Running command: rm -rf buildmeson && mkdir -p buildmeson && CC='ccache gcc' meson buildmeson
  Running command: ninja -C buildmeson -j 2
  Running command: ninja -C buildmeson -j 2
  Running command: ninja -C buildmeson -j 2 clean
  Running command: ninja -C buildmeson -j 2
  cmake-make
   1.235 gen
   0.806 build
   0.220 empty build
   0.108 clean
   0.618 rebuild
   2.988 overall
  cmake-ninja
   0.868 gen
   0.304 build
   0.016 empty build
   0.033 clean
   0.272 rebuild
   1.493 overall
  meson
   1.750 gen
   0.278 build
   0.012 empty build
   0.024 clean
   0.263 rebuild
   2.326 overall
  clausklein$


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

  Running command: rm -rf buildcmake && mkdir -p buildcmake && cd buildcmake && CC='ccache gcc' cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug ..
  Running command: cd buildcmake && make -j 2
  Running command: cd buildcmake && make -j 2
  Running command: cd buildcmake && make -j 2 clean
  Running command: cd buildcmake && make -j 2
  Running command: rm -rf buildcmakeninja && mkdir -p buildcmakeninja && cd buildcmakeninja && CC='ccache gcc' cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug -G Ninja ..
  Running command: cd buildcmakeninja && ninja -j 2
  Running command: cd buildcmakeninja && ninja -j 2
  Running command: cd buildcmakeninja && ninja -j 2 clean
  Running command: cd buildcmakeninja && ninja -j 2
  Running command: rm -rf buildmeson && mkdir -p buildmeson && CC='ccache gcc' meson buildmeson
  Running command: ninja -C buildmeson -j 2
  Running command: ninja -C buildmeson -j 2
  Running command: ninja -C buildmeson -j 2 clean
  Running command: ninja -C buildmeson -j 2
  cmake-make
   4.737 gen
   1.338 build
   0.289 empty build
   0.743 clean
   1.237 rebuild
   8.345 overall
  cmake-ninja
   4.080 gen
   0.621 build
   0.018 empty build
   0.034 clean
   0.584 rebuild
   5.338 overall
  meson
   1.996 gen
   1.161 build
   0.014 empty build
   0.021 clean
   1.151 rebuild
   4.343 overall
  bash-5.0$ pwd
  /Users/clausklein/Workspace/cpp/jsoncpp
  bash-5.0$

IMHO: The winner is https://mesonbuild.com using https://ninja-build.org and https://ccache.dev


Recources
----------

**A nice project with a dual build system: cmake and meson**

  * https://github.com/open-source-parsers/jsoncpp I used it for the second performance test.

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
