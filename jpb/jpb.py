#!/usr/bin/env python3

'''
    Auto compile or execute java project by setting root mark file and given java 
    file path.

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
'''

import os
import argparse

def find_project_root(project_file, filepath, proroot='cwd'):
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
    filepath = os.path.abspath(filepath)
    if proroot == 'cwd':
        # set default project root to cwd.
        project_root = os.getcwd()
    elif proroot == 'pwd':
        # set default project root to file directory.
        project_root = os.path.dirname(filepath)
    else:
        # set default project root to pointed dir.
        project_root = os.path.abspath(proroot)
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

def get_classpath(project_root, filepath, ):
    '''
        Get standerd classpath from project dir and java file path.

    Args:
        project_root    [str]   project root dir.

        filepath        [str]   target java file path.

    return: [str]   standerd classpath of java file like `com.hello.Hello`.
    '''
    filepath = os.path.abspath(filepath)
    class_file = filepath.split(os.path.abspath(os.path.join(project_root,'%{mark}%')).split('%{mark}%')[0])[1]
    class_path = os.path.splitext(class_file)[0].replace(os.path.sep, '.')
    return class_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compile', help='choose compile mode.', action='store_true')
    parser.add_argument('-e', '--execute', help='choose execute mode.', action='store_true')
    parser.add_argument('-p', '--profile', help='project file to mark workspace. default is\
     `java.project`.', default='java.project', type=str)
    parser.add_argument('-r', '--proroot', help='point at default project root `pwd`、`cwd`\
     or given realpath. default is `cwd`.', default='cwd', type=str)
    parser.add_argument('mainfile', help='main file to build.', type=str)
    args = parser.parse_args()
    if os.path.isfile(args.mainfile):
        project_root = find_project_root(args.profile, args.mainfile, args.proroot)
        classpath = get_classpath(project_root, args.mainfile)
        if args.compile:
            print('----------java project builder (compile mode)----------')
            compile_class_file(project_root, classpath)
        if args.execute:
            print('----------java project builder (execute mode)----------')
            execute_main_class(project_root, classpath)
    else:
        print('File "%s" not found !' % args.mainfile)

if __name__ == '__main__':
    main()
