# gzic_bus

华南理工大学广州国际校区校巴预约API（对应`GZIC智慧服务`小程序）
> ~~摆脱这个巨卡无比的小程序~~

## 项目介绍

- `api`文件夹为校巴相关接口的爬虫（包含校巴查看、预约、获取二维码等接口）
- `cli`文件夹为命令行脚本相关模块，可以直接运行进行预约等操作
- 整理了校巴接口的[文档](docs/%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3.md)，方便用别的语言重写

## cli使用方法

1. 安装依赖(`requests`和`questionary`)
    ```bash
    pip install -r requirements.txt
    ```

    如果你使用[`nix`](https://nixos.org/)包管理器的话，只要运行以下命令，便可以进入一个包含所有依赖（包括`python`）的环境（请确保您启用了`nix flake`, [教程](https://nixos.wiki/wiki/Flakes)）:
    ```bash
    nix develop
    ```
    
2. 运行脚本
    ```
    python main.py
    ```

3. 关于`token`
    > 校巴接口需要传递`token`作为鉴权`header`，本程序会将`token`保存为`.token`文件，首次使用将进行统一认证登陆获取`token`，之后默认读取本地文件。`token`有效期较长，不需要经常更新。

    2025.03.07更新：新增验证码登录，适应新版本SSO
    
    2025.03.10更新：新增二维码登录，会生成二维码保存在`qrcode.jpg`，使用微信扫描登录

## cli功能

- 预约校巴 
    > 非常简单的起点终点选择，而不是反应缓慢的小程序点击
    >
    > 日期的选择，只查看某一天的班次，而不是小程序的杂乱列表
    >
    > 几个回车就能马上预约到校巴，而小程序可能刚刚加载好

- 查看已预约校巴
    > 列出预约未乘坐的班次，只显示有用的信息
    >
    > 轻松取消校巴

## 后续更新方向

1. 自动预约脚本
2. 抢票脚本
