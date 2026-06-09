---
name: sjtuguoxue_yuefu
version: 1.0.0
description: |
  乐府部：国学社原创古风音乐部门。提供歌单嵌入、歌曲音频引用和活动页面资源。
  当用户提到乐府、乐府部、古风音乐、诗以歌、国学社歌曲、
  未解忆长安、聚少趁江南、大东、溯流沙 时触发。
---

# 乐府部

上海交通大学国学社乐府部，专注原创古风音乐创作与演出。

## 「诗以歌」歌单

网易云音乐歌单，收录乐府部原创作品。

**歌单地址：** https://music.163.com/#/playlist?id=14332525936

### 曲目

| 序号 | 歌曲 |
|------|------|
| 1 | 聚少趁江南 |
| 2 | 未解忆长安 |
| 3 | 来春可拟共兰舟 |
| 4 | 大东 |
| 5 | 溯流沙 |
| 6 | 玉蝴蝶·秋梦 |

### 网易云外链播放器嵌入

在公众号推文或网页中嵌入完整歌单播放器：

```html
<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=450
  src="//music.163.com/outchain/player?type=0&id=14332525936&auto=1&height=430"></iframe>
```

参数说明：
- `type=0` 歌单模式（`type=2` 为单曲）
- `id=14332525936` 歌单 ID
- `auto=1` 自动播放（`auto=0` 关闭）

## 音频资源

歌曲音频文件托管在 GitHub，可直接引用：

**仓库：** https://github.com/lyy0323/yuefu4anniv/tree/main/assets/audio

| 歌曲 | 音频地址 |
|------|---------|
| 大东 | `https://raw.githubusercontent.com/lyy0323/yuefu4anniv/main/assets/audio/大东.m4a` |
| 未解忆长安 | `https://raw.githubusercontent.com/lyy0323/yuefu4anniv/main/assets/audio/未解忆长安.m4a` |
| 聚少趁江南 | `https://raw.githubusercontent.com/lyy0323/yuefu4anniv/main/assets/audio/聚少趁江南.m4a` |
| 来春可拟共兰舟 | `https://raw.githubusercontent.com/lyy0323/yuefu4anniv/main/assets/audio/来春可拟共兰舟.m4a` |
| 溯流沙 | `https://raw.githubusercontent.com/lyy0323/yuefu4anniv/main/assets/audio/溯流沙.m4a` |
| 玉蝴蝶·秋梦 | `https://raw.githubusercontent.com/lyy0323/yuefu4anniv/main/assets/audio/玉蝴蝶·秋梦.m4a` |

HTML 中嵌入音频：

```html
<audio controls src="https://raw.githubusercontent.com/lyy0323/yuefu4anniv/main/assets/audio/大东.m4a"></audio>
```

## 乐府部四周年

**活动页面：** https://yuefu4anniv.sjtuguoxue.space

**源码仓库：** https://github.com/lyy0323/yuefu4anniv
