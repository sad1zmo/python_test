import os
import re
import sys


def extract_cmds_from_file(filepath):
    with open(filepath, 'r') as file:
        file_content = file.read()
        variable_matches = re.findall(r'CMDS\s*=\s*(\[.*?\])', file_content, re.DOTALL)
        for var_match in variable_matches:
            echo_matches = re.findall(r"'echo\s+\d+'", var_match)
        if echo_matches:
            return echo_matches
    return []


def gather_all_cmds(directory):
    cmds = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                file_cmds = extract_cmds_from_file(filepath)
                if file_cmds:
                    for cmd in file_cmds:
                        cmds.append((filepath, cmd))
    if cmds:
        return sorted(cmds)
    else:
        print("Нет команд для выполнения")
        sys.exit(1)


def execute_cmds(cmds):
    unic_executed = set()
    for _, file_cmds in cmds:
        if file_cmds not in unic_executed:
            # os.system(file_cmds.strip("'"))
            os.system(eval(file_cmds))
            unic_executed.add(file_cmds)
        else:
            print(f'Команда {file_cmds} уже выполнялась')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Укажите директорию для поиска")
        sys.exit(1)

    directory = sys.argv[1]
    cmds = gather_all_cmds(directory)
    execute_cmds(cmds)
