# Orders

一个基于QuickProject.Commander的程序代写订单管理器。

## 功能

![](https://cos.rhythmlian.cn/ImgBed/c0f7fe9dd06da048960608b479cc536b.png)

- 基于Qpro自动创建项目并生成项目的README文档。
- 支持将代码打包为utf8或gbk编码的压缩包。（比如WIndows系统应该用gbk编码，则调用pack-win子命令）。

## 安装

- `pip3 install Qpro`。

- 克隆本项目至本地。

### 注册全局命令

- 在项目文件夹内执行`Qpro register-global`。

- 如果你需要Qpro提供基于fig的自动补全，可以在`~/.fig/autocomplete`文件夹下执行`Qpro gen-fig-script`；再`yarn build`应用到全局即可。

- 如果你需要Qpro提供基于zsh的tab补全，可以在`$fapth`下执行`Qpro gen-zsh-comp`自动生成补全脚本。

### 不注册全局命令

在项目文件夹下通过`qrun`调用即可。

## 使用

- 全局命令（可在任意位置运行）
  1. `orders create <项目名> <价格> <DDL>`: 创建新项目。
  2. `orders open-project <路径>`: 打开项目。
  3. `orders pack <路径> [系统]`: 打包指定系统（默认Linux）的代码压缩包。
  4. `orders pack-win <路径>`: 打包支持Windows的代码压缩包。
- 非全局命令只能在项目文件夹下执行，将上方的四种命令的`orders`换用`qrun`即可。
