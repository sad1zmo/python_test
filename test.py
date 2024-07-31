import os
import re
import sys


def extract_cmds_from_file(filepath):
    with open(filepath, 'r') as file:
        file_content = file.read()
        match = re.search(r'CMDS\s*=\s*(\[.*?\])', file_content, re.DOTALL)
        if match:
            cmds_str = match.group(1)
            cmds = eval(cmds_str)
            return cmds
    return []


def gather_all_cmds(directory):
    cmds = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                file_cmds = extract_cmds_from_file(filepath)
                if file_cmds:
                    cmds.append(filepath, file_cmds)
    if cmds:
        return sorted(cmds)
    else:
        print("Нет команд для выполнения")
        sys.exit(1)


def execute_cmds(cmds):
    unic_executed = set()
    for _, file_cmds in cmds:
        for cmd in file_cmds:
            if cmd not in unic_executed:
                print(cmd)
                os.system(cmd)
                unic_executed.add(cmd)
            else:
                print(f'Команда {cmd} уже выполнялась')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Укажите директорию для поиска")
        sys.exit(1)

    directory = sys.argv[1]
    cmds = gather_all_cmds(directory)
    execute_cmds(cmds)
