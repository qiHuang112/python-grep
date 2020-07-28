import colorama
import os
from termcolor import colored


def file_filter(name: str):
    """
    :param name: walk所有子文件时返回的文件名
    :return: 根据文件名筛选需要的文件
    """
    return True


def walk_file(path: str):
    """
    :param path:文件夹根目录
    :return: 根目录下所有子文件
    """
    arr = []
    for r, dirs, files in os.walk(path):
        arr += [os.path.join(r, name) for name in files if file_filter(name)]
        if len(dirs) > 0:
            for d in dirs:
                arr += walk_file(d)
    return arr


def print_result(key, line_number, name, line: str, index):
    """
    :param key: 关键字
    :param line_number: 行号
    :param name: 结果所在问价名
    :param line: 具体
    :param index: 第index个结果
    :return flag: 终止输出
    """
    if index > 10:
        a = input()
        if a == 'q' or a == 'Q':  # 如果输入q/Q，终止输出
            return True
    print(colored(name, 'cyan'), end='')
    print(colored('[{0}]'.format(line_number), 'cyan'), end='')
    print(colored(':', 'cyan'), end='')
    lines = line.split(key)
    for i, v in enumerate(lines):
        print(v, end='')
        if i != len(lines) - 1:
            print(colored(key, 'red'), end='')
    print()
    return False


def search_file(key, file):
    """
    :param key: 关键字
    :param file: 文件路径
    :return: 搜索停止
    """
    index = 0
    with open(file, 'r', encoding='UTF-8') as f:
        try:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1
                if line.find(key) >= 0:
                    index = index + 1
                    if print_result(key, line_number, f.name.split("\\")[-1], line, index):
                        return True
        except UnicodeDecodeError:  # 过滤不是UTF-8编码的文件
            pass


def search(key, path):
    if os.path.isdir(path):
        for file in walk_file(path):
            if search_file(key, file):
                return
    else:
        search_file(key, path)


def main():
    print(colored('请输入文件或文件夹路径：', color='yellow'), end='')
    # 用户输入的路径
    input_path = input()

    # 判断输入是否合法
    while os.path.isdir(input_path) or os.path.isfile(input_path):
        while True:
            print(colored('请输入关键字：', color='yellow'), end='')
            key = input()
            search(key, input_path)
    else:
        print(colored('输入路径不合法，请重新输入：', color='red'), end='')


if __name__ == '__main__':
    # 允许终端显示颜色
    colorama.init()

    # 控制流程
    main()
