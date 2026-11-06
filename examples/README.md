# 示例与验证

这组实验使用相同的五个元素：老式潜水员、蝴蝶、月球、旋转楼梯和海浪。素材通过实际检索获得，作为图像输入交给生成工具；生成时使用的用户参考截图不随仓库分发。

| 版本 | 图片 | 视觉方向 |
|---|---|---|
| A，默认 | [摄影杂志拼贴](../assets/style-reference-a.png) | 保留照片与版画纹理，用尺度错位和遮挡连接场景 |
| B，可选 | [平面剪纸偶戏](paper-puppet.png) | 身体压成黑色纸片，头盔和楼梯保留细节 |

两张均为内置图像工具实际生成的 1254 × 1254 PNG。A 被用户选为更接近目标的方向。B 经一次针对身体材质的修正，去掉过重的写实衣褶和发亮的关节铆钉。

## 素材来源

| 元素 | 来源与署名 | 检索时记录的使用条件 |
|---|---|---|
| 老式潜水员 | [Library of Congress，cph.3a50953](https://www.loc.gov/pictures/resource/cph.3a50953/)，摄影者未核实 | 详细条目访问受限，许可未核实 |
| 蓝闪蝶 | [Smithsonian National Museum of Natural History，EO400819](https://naturalhistory.si.edu/object/nmnheducation_11016396) | 来源记录写明 Creative Commons Zero |
| 月球 | [NASA Science：Moon Mosaic](https://science.nasa.gov/resource/moon-mosaic/)，NASA Scientific Visualization Studio，Ernie Wright (USRA) | [SVS 原页](https://svs.gsfc.nasa.gov/5001/)给出署名要求，未概括为 CC0 |
| 旋转楼梯 | [Charles Roscoe Savage，经 Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SpiralstaircaseSLT3b18940u.jpg)，Library of Congress cph.3b18940 | 来源文件页标为 Public Domain Mark 1.0 |
| 海浪 | [葛饰北斋《神奈川冲浪里》，The Met，JP10](https://www.metmuseum.org/art/collection/search/36491) | 来源藏品页标为 Public Domain |

以上记录来自 2026-11-06 的检索，逐项元数据和图片直链见 [sources.input.json](sources.input.json)。仓库包含生成的示例图，没有重新分发下载的五张原始素材。

## 验证范围

- Skill 结构校验通过；示例图均已打开检查，五个元素可辨，没有看见字幕、文字或播放器界面。
- 下载脚本已完成五张真实图片下载，并通过六项行为检查：原始字节与尺寸保持、拒绝 HTML 冒充图片、部分失败返回非零、已有输出不覆盖、重复 ID 提前拒绝、路径越界 ID 拒绝。
- 此处是单组题材的出图实验，没有执行 OCR 或多组重复生成，不代表不同题材都能达到同样效果。
