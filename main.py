import os
import zipfile

import colorama
from colorama import Fore, Style

index = 0


class Colored:
    """
    description:
        print colored str in terminal.
    usage:
        from colorama import Fore, Back
        print(Colored('test', Fore.Red + Back.White))
    available:
        Fore:BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
        Back:BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
        Style:BRIGHT, DIM, NORMAL, RESET_ALL
    """

    def __init__(self, message, color):
        self.message = message
        self.color = color

    def __str__(self):
        return self.color + self.message + Style.RESET_ALL


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


def print_result(key, line_number, name, line: str):
    """
    :param key: 关键字
    :param line_number: 行号
    :param name: 结果所在问价名
    :param line: 具体
    :return flag: 终止输出
    """
    if index > 10:
        a = input()
        if a == 'q' or a == 'Q':  # 如果输入q/Q，终止输出
            return True
    else:
        print()
    print(Colored(name, Fore.YELLOW),
          Colored('[{0}]'.format(line_number), Fore.GREEN),
          Colored('[{0}]:'.format(index), Fore.CYAN),
          end='', sep='')
    lines = line.split(key)
    for i, v in enumerate(lines):
        print(v, end='')
        if i != len(lines) - 1:
            print(Colored(key, Fore.RED), end='')
    return False


def search_file(key, file, parent_path):
    """
    :param key: 关键字
    :param file: 文件路径
    :param parent_path 父路径
    :return: 搜索停止
    """
    global index
    with open(file, 'r', encoding='UTF-8') as f:
        try:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1
                if line.find(key) >= 0:
                    index = index + 1
                    name = f.name.replace(parent_path + '\\', '')
                    if print_result(key, line_number, name, line.strip()):
                        return True
        except UnicodeDecodeError:  # 过滤不是UTF-8编码的文件
            pass


def search(key, path):
    global index
    index = 0
    if os.path.isdir(path):
        for file in walk_file(path):
            if search_file(key, file, path):
                return
    else:
        search_file(key, path, os.path.dirname(path))


def unzip_file(zip_path, unzip_path):
    """
    :param zip_path: zip路径
    :param unzip_path: 解压后路径
    """
    if not os.path.exists(unzip_path):
        os.makedirs(unzip_path)
    if zipfile.ZipFile(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as f:
            f.extractall(unzip_path)


def main():
    print(Colored('请输入文件或文件夹路径：', Fore.YELLOW), end='')
    # 用户输入的路径
    input_path = input()

    # 判断输入是否合法
    while os.path.isdir(input_path) or os.path.isfile(input_path):
        if os.path.isfile(input_path) and input_path.endswith('zip'):
            # 文件名 ： xxx.zip
            file_name = input_path[input_path.rindex(os.sep) + 1:]

            # 解压路径 ：D:\Projects\Python\LogTools\unzip_files\xxx
            unzip_path = os.path.join(os.getcwd(), 'unzip_files', file_name[:file_name.rindex('.')])

            # 解压文件
            unzip_file(input_path, unzip_path)
            print(Colored('文件已解压到：%s' % unzip_path, Fore.YELLOW))
            input_path = unzip_path
        while True:
            print(Colored('请输入关键字：', Fore.YELLOW), end='')
            key = input()
            if len(key) == 0:
                continue
            search(key, input_path)
    else:
        print(Colored('输入路径不合法，请重新输入：', Fore.RED), end='')


log_root = os.path.join(os.path.abspath(os.getcwd() + os.sep + '.'), 'logs')


def aop_print(*args, sep=' ', end='\n', file=None):
    print(*args, sep=sep, end=end, file=file)
    format_args = [msg.message for msg in args if isinstance(msg, Colored)]
    if not os.path.exists(log_root):
        os.makedirs(log_root)
    with open(os.path.join(log_root, 'log.txt'), 'a+', encoding='UTF-8') as f:
        print(*format_args, sep=sep, end=end, file=f)


if __name__ == '__main__':
    # 允许终端显示颜色
    colorama.init()

    # 控制流程
    main()
