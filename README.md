# GenShin-helper

genshin-helper是基于pyautogui开发的可以帮助你自动点击对话框过剧情的小插件
~~不会自己跑路的，只能点点对话框这样子~~

使用教程请移步B站[原神剧情小助手，自动帮你看剧情](https://www.bilibili.com/video/BV1g14y147pL)

如果不想使用默认的1920*1080的大小，需要把assets路径内chosen.png画面重新截图。

由于不同系统运行情况有所不同，且作者无力维护更多版本，大佬可以看代码自己改成符合自己需求的插件。

#### 已知的版本

| 开发者                                   | 仓库                                        | B站视频                                                                        |
|---------------------------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| [YourKlc](https://github.com/YourKlc) | https://github.com/YourKlc/GenShin-helper | [还在为原神剧情太慢而苦恼吗？自己写个工具来全自动看剧情！](https://www.bilibili.com/video/BV1Fe4y137RZ) |

## 配置文件

settings.json 是与运行有关的配置选项

```yaml
{
  "chosen_path": "assets/chosen.bmp", #chosen.bmp的路径，重新截图后可以进行修改
  "wait_after_find": 5, # 在找到图标后的等待时间，也就是自己看对话框的时间
  "wait_after_clicked": 3, # 点击之后的等待时间，避免打断对话
  "wait_not_find": 2, # 没找到对话框的冷却时间
  "skip": 0 # 快速点击选项，规律点击的时间，0为不开启，
}
```
