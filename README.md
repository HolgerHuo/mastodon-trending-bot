# Mastodon Trending Bot

![GitHub last commit](https://img.shields.io/github/last-commit/holgerhuo/mastodon-trending-bot)![GitHub release (latest by date)](https://img.shields.io/github/v/release/holgerhuo/mastodon-trending-bot)![GitHub](https://img.shields.io/github/license/holgerhuo/mastodon-trending-bot)![GitHub all releases](https://img.shields.io/github/downloads/holgerhuo/mastodon-trending-bot/total)![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/holgerhuo/mastodon-trending-bot)

A mastodon trending bot that aggregates trending tags from json api and toot with python!

用 Python 实现的定时推送Mastodon流行标签机器人

[Example 示例](https://mast.dragon-fly.club/@trends)

## Usage 用法

Clone the repository, enter the directory, change configurations file and run mtb.py using python3. You may specify a config.json adding directly to the arguments.

克隆仓库，修改配置文件，使用Python3运行mtb.py。可通过参数自定义配置文件路径

```bash
git clone https://github.com/HolgerHuo/mastodon-trending-bot.git mtb
cd mtb
pip3 install -r requirements.txt # install dependencies
vim config.json # if necessary
python3 mtb.py # or using python3 mtb path_to_config 
```

## Configurations 配置文件

```json
{
    "MTB_APP_NAME": "MastodonTrendingBot",
    "MTB_SOURCE_INSTANCE": "https://mast.dragon-fly.club",
    "MTB_DEST_INSTANCE": "https://botsin.space",
    "MTB_APP_SECURE_TOKEN": "xxxxxx",
    "MTB_STATUS_VISIBILITY": "public",
    "MTB_STATUS_BODY": "#当下流行 \n嘟嘟嘟！这是本时段 Island岛屿 的流行标签 \n要记得善用Hashtags来帮助联邦宇宙发现你的嘟文噢～ \n\n",
    "MTB_BLACKLIST_PATH": "blacklist.txt",
    "MTB_NO_TRENDS_STATUS": "#当下流行 \n当下没有流行标签哦～\n大家可以使用Hashtags帮助你的嘟文被快速发现w！"
}
```
**MTB_APP_NAME**: App name, used when tooting and displayed on web interface 机器人名称，会显示在Web界面中

**MTB_SOURCE_INSTANCE**: Trending tags source instance 获取流行信息的实例

**MTB_DEST_INSTANCE**: Toot destination instance 嘟文发送至的实例

**MTB_APP_SECURE_TOKEN**: Bot account token 机器人账户密钥 https://instance.tld/settings/applications

**MTB_STATUS_VISIBILITY**: Toot visibility 嘟文可见度 (public, unlisted)

**MTB_STATUS_BODY (Optional 可选)**:  Personalized toot body 自定义嘟文内容 

**MTB_BLACKLIST_PATH (Optional 可选)**: Specifying blacklist file path 黑名单路径

**MTB_NO_TRENDS_STATUS (Optional 可选)**: Status to post when no tags trending 无当下流行标签时的嘟文


**Blacklist 黑名单**

Write your blacklist tags one per line, or leave it empty. Recomment to write the ones used in status body

每行一条黑名单标题，推荐将嘟文正文内容中的tag拉黑。

```text
nsfw
当下流行
aaa
```

## License 许可协议

GNU GPL v3 or above



[@holgerhuo@dragon-fly.club](https://mast.dragon-fly.club/@holgerhuo)
