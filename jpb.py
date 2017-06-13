#!/usr/bin/env python3

import os
import sys

def find_project_root(project_file, filepath):
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
    cwd_tmp = os.getcwd()
    os.chdir(project_root)
    os.system('javac -encoding UTF-8 -d . '+classpath.replace('.', os.path.sep)+'.java')
    os.chdir(cwd_tmp)

def execute_main_class(project_root, classpath):
    cwd_tmp = os.getcwd()
    os.chdir(project_root)
    os.system('java '+classpath)
    os.chdir(cwd_tmp)

def get_classpath(project_root, filepath):
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
