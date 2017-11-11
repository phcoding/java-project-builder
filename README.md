# Java Project Builder
1. describe
```
JPB(java project builder)  is a simple tool for building java project which means
you can use it to compile or execute java project only use one line command. The 
only thing you have do is to point at which source file to compile or which source
file is the main file. Hope this tool can take little convenient to you in java 
project building ! 
```
---
2. usage
```
    usage: jpb [-h] [-c] [-e] [-p PROFILE] [-r PROROOT] mainfile
    positional arguments:
      mainfile              main file to build.
    optional arguments:
      -h, --help            show this help message and exit
      -c, --compile         choose compile mode.
      -e, --execute         choose execute mode.
      -p PROFILE, --profile PROFILE
                            project file to mark workspace. default is
                            `java.project`.
      -r PROROOT, --proroot PROROOT
                            point at default project root `pwd`、`cwd` or given
                            realpath. default is `cwd`.
```
---
3. demo
+ execute compiled class file:
``` python3 jpb.py -e [class file path]```
+ compile java project:
``` python3 jpb.py -c [main file path]```
+ compile and execute project:
``` python3 jpb.py -c -e [main file path]```
