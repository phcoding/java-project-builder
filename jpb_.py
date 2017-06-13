#!/usr/bin/env python3

import os
import sys
import json

def scan_packages(folder_name):
    packages = []
    for root, dirs, files in os.walk(folder_name):
        if not root in (folder_name, files):
            packages.append(root.split(folder_name+os.sep,1)[1].replace(os.sep, '.'))
    return packages

def load_config(filename):
    project_root = os.path.dirname(filename)
    try:
        with open(filename, 'r') as fp:
            project_conf = json.loads(fp.read())
    except (IOError, json.JSONDecodeError):
        project_conf = {
            "project_name": os.path.split(project_root)[1],
            "packages": scan_packages(project_root),
            "main_class": ""
            }
    if len(project_conf.get('packages'))==0:
        project_conf['packages'] = scan_packages(project_root)
    return project_root, project_conf

def show_help():
    print('''Usage:\tjpb\tproj_filename''')

def main():
    if len(sys.argv)>1:
        project_filename = sys.argv[-1]
        modelist = sys.argv[1:-1]
        if(os.path.isfile(project_filename)):
            project_root, project_config = load_config(project_filename)
            cwd_tmp = os.getcwd()
            os.chdir(project_root)
            if '-c' in modelist or modelist==[]:
                print('----------java Project Builder (Mode C)----------')
                for package in project_config.get('packages'):
                    print('Compiling package "'+package.replace('.', os.sep)+'"')
                    os.system('javac -encoding UTF-8 -d . '+package.replace('.', os.sep)+os.sep+'*.java')
            if '-e' in modelist or modelist==[]:
                os.system('java '+project_config.get('main_class'))
            os.chdir(cwd_tmp)
    else:
        show_help()

if __name__ == '__main__':
    main()