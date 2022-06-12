from QuickProject.Commander import Commander
from QuickProject import QproDefaultConsole, QproErrorString, QproInfoString
from QuickStart_Rhy import remove
from subprocess import run
import os

app = Commander(True)

def external_EXEC(command: str, failed_to_exit: bool = True):
    with open(os.devnull, 'w') as f:
        res = run(command.split(), stdout=f, stderr=f).returncode
        if res:
            QproDefaultConsole.print(QproErrorString, '未知错误')
            if failed_to_exit:
                exit(0)


def random_password():
    import random
    import string
    return ''.join(random.sample(string.punctuation.replace('"', '') + string.ascii_letters + string.digits, 12))


@app.command()
def create(name: str, price: int, DDL: str):
    """
    创建一个新的项目
    """
    os.system('Qpro create ' + name)
    import json
    with open('./' + name + '/project_configure.json', 'r') as f:
        config = json.load(f)
    with open(f'{name}/README.md', 'w') as f:
        print('# ' + name, file=f)
        print('| 项目信息 | 内容 |\n|:---|:---|', file=f)
        print('| 价格 | ' + str(price) + '元 |', file=f)
        print('| DDL | ' + DDL + ' |', file=f)
        print('\n## 进度', file=f)
        print('- [x] 创建项目', file=f)
        print('- [ ] 程序开发', file=f)
        print('- [ ] 测试', file=f)
        print('- [ ] 完成', file=f)
        print('\n## 关于本项目\n', file=f)
        print('### `project_configure.json`文件是什么？', file=f)
        print('- 项目中的`project_configure.json`是[Qpro工具](https://rhythmlian.cn/2020/02/14/QuickProject/)的配置表，你可以在[配置表](https://rhythmlian.cn/2020/02/14/QuickProject/#配置表)处查看文件中各项参数的意义。', file=f)
        print('- 如果你不用Qpro工具，可以直接将`project_configure.json`和`template`文件夹删除，注意记好编译和运行指令即可。', file=f)
        print('- 如果你使用Qpro，则编译指令可以通过`qrun -b`来调用，运行是`qrun`，编译且运行`qrun -br`。', file=f)
        print('\n### 其他注意项', file=f)
        print('- <font><b>!!!提交代码时请注意删除本文件!!!</b></font>', file=f)
        print('## 文档', file=f)
        print('### 前置操作', file=f)
        print('### 编译', file=f)
        print('- 用Qpro', file=f)
        print('```shell\nqrun -b\n```', file=f)
        print('- 不用Qpro', file=f)
        print(f'```shell\n{config["compile_tool"]}\n```', file=f)
        print('### 运行', file=f)
        print('- 用Qpro', file=f)
        print('```shell\nqrun\n```', file=f)
        print('- 不用Qpro', file=f)
        print(f'```shell\n{config["executable_filename"]}\n```', file=f)


@app.command()
def open_project(name: str):
    """
    打开项目
    """
    external_EXEC('code ' + name)


@app.command()
def pack(path: str, system: str = 'linux'):
    """
    *nix：压缩指定项目
    """
    password = random_password()

    if system == 'win':
        if os.path.exists(f'{path}.7z'):
            remove(f'{path}.7z')
        external_EXEC(f'7zz a {path}.7z {path} -p{password} -mmt')
    else:
        if os.path.exists(f'{path}.{system}.7z'):
            remove(f'{path}.{system}.7z')
        external_EXEC(f'7zz a {path}.{system}.7z {path} -p{password} -mmt')
    import pyperclip
    pyperclip.copy(password)
    
    QproDefaultConsole.print(QproInfoString, f'压缩完成，密码为："{password}" 已复制到剪贴板')
    external_EXEC('qs f .')
    with open('README.md', 'w') as f:
        package_name = f'{path}.7z' if system == 'win' else f'{path}.{system}.7z'
        print('# 说明', file=f)
        print(f'- 压缩包: {package_name}', file=f)
        print(f'- 密码: {password}', file=f)
        print('\n## 无法解压？', file=f)
        print('- 请使用7zip解压，并将密码复制到解压程序中', file=f)
        print('- 如果没有7zip，请下载下方安装包:', file=f)
        print('  - [点此下载Windows安装包](https://www.7-zip.org/a/7z2107-x64.exe)', file=f)
        print('  - [点此下载Linux安装包](https://www.7-zip.org/a/7z2107-linux-x64.tar.xz)', file=f)
        print('  - [点此下载Mac安装包](https://www.7-zip.org/a/7z2107-mac.tar.xz)', file=f)


@app.command()
def pack_win(path: str, exclude: str = ''):
    """
    Windows：将目录转换为GBK编码并打包为7z文件
    """
    os.mkdir(f'{path}.win')
    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            src_path = os.path.join(root, _dir)
            dst_path = os.path.join(root.replace(path, f'{path}.win'), _dir)
            os.mkdir(dst_path)
        for file in files:
            if file == path or file in exclude:
                continue
            src_path = os.path.join(root, file)
            dst_path = src_path.replace(path, f'{path}.win')
            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    with open(dst_path, 'w', encoding='gbk') as f2:
                        f2.write(f.read())
            except:
                os.system('cp ' + src_path + ' ' + dst_path)
                QproDefaultConsole.print(QproErrorString, f'文件 {src_path} 转换失败')
    app.real_call('pack', f'{path}.win', 'win')
    remove(f'{path}.win')


if __name__ == '__main__':
    app()
