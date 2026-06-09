---
name: sjtuguoxue_yuefu
version: 1.0.0
description: |
  乐府部：国学社原创古风音乐部门。提供歌单嵌入、歌曲音频引用和活动页面资源。
  当用户提到乐府、乐府部、古风音乐、和诗以歌、国学社歌曲、
  未解忆长安、聚少趁江南、大东、溯流沙 时触发。
---

# 乐府部

上海交通大学国学社乐府部，专注原创古风音乐创作与演出。

## 「和诗以歌」歌单

网易云音乐歌单，收录乐府部原创作品。

**歌单地址：** https://music.163.com/#/playlist?id=14332525936

### 曲目

| 歌曲 | 网易云 ID | 单曲嵌入 |
|------|-----------|---------|
| 聚少趁江南 | 3319155211 | `type=2&id=3319155211` |
| 未解忆长安 | 2667564747 | `type=2&id=2667564747` |
| 来春可拟共兰舟 | 2730252922 | `type=2&id=2730252922` |
| 大东 | 2626372587 | `type=2&id=2626372587` |
| 溯流沙 | 2627648742 | `type=2&id=2627648742` |
| 玉蝴蝶·秋梦 | 2626862388 | `type=2&id=2626862388` |
| 安远 | 3324911370 | `type=2&id=3324911370` |

### 网易云外链播放器嵌入

**嵌入完整歌单：**

```html
<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=450
  src="//music.163.com/outchain/player?type=0&id=14332525936&auto=1&height=430"></iframe>
```

参数说明：
- `type=0` 歌单模式（`type=2` 为单曲）
- `id=14332525936` 歌单 ID
- `auto=1` 自动播放（`auto=0` 关闭）

**嵌入单曲（推荐用于文章内配乐）：**

```html
<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width="100%" height=86
  src="//music.163.com/outchain/player?type=2&id=2626862388&auto=0&height=66"></iframe>
```

将 `id` 替换为上方曲目表中的网易云 ID 即可。

## 音频资源

歌曲音频文件托管在 GitHub，**不建议直接引用**（raw.githubusercontent.com 有 GFW 风险）。需要用音频时建议先下载到本地或上传到自有 CDN。在线使用优先用网易云 iframe 嵌入。

**仓库：** https://github.com/lyy0323/yuefu4anniv/tree/main/assets/audio

| 歌曲 | 文件名 |
|------|--------|
| 大东 | `大东.m4a` |
| 未解忆长安 | `未解忆长安.m4a` |
| 聚少趁江南 | `聚少趁江南.m4a` |
| 来春可拟共兰舟 | `来春可拟共兰舟.m4a` |
| 溯流沙 | `溯流沙.m4a` |
| 安远 | `安远.mp3` |

下载示例：

```bash
# 先 clone 或下载，不要直接在 HTML 中引用 raw.githubusercontent.com
git clone https://github.com/lyy0323/yuefu4anniv.git
# 音频文件在 assets/audio/ 目录下
```

## 乐府部四周年

**活动页面：** https://yuefu4anniv.sjtuguoxue.space

**源码仓库：** https://github.com/lyy0323/yuefu4anniv
