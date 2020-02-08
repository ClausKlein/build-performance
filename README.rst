====================================
Simple build performance comparison
====================================

These simple python scripts are based on the idea at
https://mesonbuild.com/Simple-comparison.html

Setup test suite::

  clausklein$ ./gen_src.py build
  generate 2 directories containing each 3 source files

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
  Running command: rm -rf buildscons .sconsign.dblite
  Running command: CC='ccache gcc' scons -j 2
  Running command: CC='ccache gcc' scons -j 2
  Running command: CC='ccache gcc' scons -j 2 -c
  Running command: CC='ccache gcc' scons -j 2
  cmake-make
   2.637 gen
   0.718 build
   0.206 empty build
   0.718 clean
   0.718 rebuild
  cmake-ninja
   0.938 gen
   0.274 build
   0.016 empty build
   0.274 clean
   0.274 rebuild
  meson
   1.857 gen
   0.300 build
   0.011 empty build
   0.300 clean
   0.300 rebuild
  scons
   0.024 gen
   3.145 build
   1.982 empty build
   3.145 clean
   3.145 rebuild
  clausklein$


The ninja base builds are the best as expected
-----------------------------------------------

One interesting point is the different size of the generated ninja build files.
The meson build generator creates only one and a simpler and clear
**build.ninja** file::

  clausklein$ find build -name '*.ninja' -ls
  81941300       48 -rw-r--r--    1 clausklein   staff   21306  8 Feb 10:17 build/buildcmakeninja/build.ninja
  81941301        8 -rw-r--r--    1 clausklein   staff    2681  8 Feb 10:17 build/buildcmakeninja/rules.ninja
  81941494       16 -rw-r--r--    1 clausklein   staff    5686  8 Feb 10:17 build/buildmeson/build.ninja
  clausklein$


Recources
----------

* https://medium.com/@julienjorge/an-overview-of-build-systems-mostly-for-c-projects-ac9931494444
* https://en.wikipedia.org/wiki/List_of_build_automation_software
* https://trends.google.com/trends/explore?date=all&q=meson,mpc-ace,%2Fm%2F04dl04,%2Fm%2F0cxh7f
* http://esr.ibiblio.org/?p=8581
* http://doc.cat-v.org/plan_9/4th_edition/papers/mk
* https://manpages.debian.org/testing/mpc-ace/mpc-ace.1.en.html
