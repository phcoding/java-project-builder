#!/usr/bin/env python3

'''
    Auto compile or execute java project by setting root mark file and given java 
    file path.

    Usage:
        `python3 jpb.py [-c|-e] target_file_name`
        `-c` means compiling mode.
        `-e` means executing mode.
'''

import os
import sys

def find_project_root(project_file, filepath):
    '''
        Find project root dir accroding to mark-file name and given java file path.

    Args:
        project_file [str]  project root mark file `java.project`.You need to create
         it in root dir.

        filepth     [str]   target compile or execute java file. The script will start
        to find mark-file from its parent dir.

    return: [str] project root dir.
    '''
    def forward_walk(filepath):
        dirname = os.path.dirname(filepath)
        if dirname != os.path.join(os.path.splitdrive(dirname)[0], os.path.sep):
            yield dirname
            yield from forward_walk(os.path.dirname(filepath))
    project_root = os.path.dirname(filepath)
    for dirname in forward_walk(filepath):
        if os.path.isfile(os.path.join(dirname, project_file)):
            project_root = dirname
            break
    return project_root

def compile_class_file(project_root, classpath):
    '''
        Compile java file associated with given classpath to class file.
    
    Args:
        project_root    [str]   jvm's workspace also project root dir.

        classpath       [str]   target classpath to compile like `com.hello.Hello`.
    
    return: [None]
    '''
    cwd_tmp = os.getcwd()
    os.chdir(project_root)
    os.system('javac -encoding UTF-8 -d . '+classpath.replace('.', os.path.sep)+'.java')
    os.chdir(cwd_tmp)

def execute_main_class(project_root, classpath):
    '''
        Execute compiled main class of project.

    Args:
        project_root    [str]   jvm's workspace.

        classpath       [str]   main class path like `com.hello.Hello`.

    return: [None]
    '''
    cwd_tmp = os.getcwd()
    os.chdir(project_root)
    os.system('java '+classpath)
    os.chdir(cwd_tmp)

def get_classpath(project_root, filepath):
    '''
        Get standerd classpath from project dir and java file path.

    Args:
        project_root    [str]   project root dir.

        filepath        [str]   target java file path.

    return: [str]   standerd classpath of java file like `com.hello.Hello`.
    '''
    class_file = filepath.split(project_root+os.sep)[1]
    class_path = os.path.splitext(class_file)[0].replace(os.path.sep, '.')
    return class_path

def show_help():
    print('''Usage: jpb    [options]    filename
Options:
    -c    only compile mode.
    -e    only execute mode.''')

def main():
    if len(sys.argv)>1:
        filepath = os.path.abspath(sys.argv[-1])
        modelist = sys.argv[1:-1]
        if(os.path.isfile(filepath)):
            project_root = find_project_root('java.project', filepath)
            classpath = get_classpath(project_root, filepath)
            if '-c' in modelist or modelist==[]:
                print('----------java Project Builder (Mode C)----------')
                compile_class_file(project_root, classpath)
            if '-e' in modelist or modelist==[]:
                execute_main_class(project_root, classpath)
        else:
            print('File "%s" not found !' % filepath)
    else:
        show_help()

if __name__ == '__main__':
    main()
