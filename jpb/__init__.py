from __future__ import absolute_import
import os
import sys
import argparse
import jpb.jpblib as jpblib


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
        project_root = jpblib.find_project_root(args.profile, args.mainfile, args.proroot)
        classpath = jpblib.get_classpath(project_root, args.mainfile)
        if args.compile:
            print('----------java project builder (compile mode)----------')
            jpblib.compile_class_file(project_root, classpath)
        if args.execute:
            print('----------java project builder (execute mode)----------')
            jpblib.execute_main_class(project_root, classpath)
    elif os.path.isdir(args.mainfile):
        if args.execute:
            print('WARNING: directory as the args only support compile mode !')
        if args.compile:
            print('----------java project builder (compile mode)----------')
            for rt, dirs, files in os.walk(args.mainfile):
                for file in files:
                    if os.path.splitext(file)[1]==".java":
                        project_root = jpblib.find_project_root(args.profile, os.path.join(rt,file), args.proroot)
                        classpath = jpblib.get_classpath(project_root, os.path.join(rt,file))
                        print('-> %s' % classpath)
                        jpblib.compile_class_file(project_root, classpath)
    else:
        print('File "%s" not found !' % args.mainfile)

if __name__ == '__main__':
    sys.exit(main())
