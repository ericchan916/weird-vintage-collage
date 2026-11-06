# 生成提示词

把括号部分换成实际内容，不把模板原样提交。中文或英文均可。所用工具不支持的参数不要写成工具参数，比例和构图可以写入提示词。

```text
Use case: compositing
Asset: one standalone [aspect ratio] raster artwork, edge-to-edge composition.

Input image map:
1–[n]: STYLE REFERENCES ONLY. Extract the cut-paper, photomontage and print grammar.
Do not copy their specific subject arrangement. Ignore all screenshot UI, captions,
play symbols, watermarks and incidental words.
[n+1]: [source object], use its [silhouette / photograph / engraving / texture].
[n+2]: [source object], ...

Required elements: [user's actual list, unchanged].
Visual anchor: [main subject].
Surreal relationship: [one specific impossible interaction].

Style: [selected branch]. Build the scene out of separately cut fragments from the
supplied element references. Keep photographic or engraved details INSIDE the
fragments and decisively cut silhouettes OUTSIDE. Let the sources keep visibly
different textures. Make overlaps and layer order legible. Selective rough paper
edges, subtle halftone, tactile paper grain and slight ink misregistration.

Layout: [foreground / middle / backdrop with a clear hierarchy].
Palette: [derived from sources or user's colors].
Keep: [identity / object features / supplied constraints, if any].
Text: none. No words, letters, numbers, labels, signatures, logos or watermark.
Avoid: smooth fantasy painting, seamless photographic scene, glossy 3D, cinematic
volumetric light, soft blend transitions, uniform illustration brushwork,
overdecorated sticker grid, screenshots, player controls, external black bars.
```

主体如果是剪纸偶戏，可将照片片段替换成 `engraved head or object fragments with flat cut-paper body sections`，强化几何拼接、平面身体和舞台底幕。不要把人偶结构无关地套在所有主题上。

## 修图时

以当前成图作为编辑目标，保留原始元素来源作为补充输入（工具允许时）。先说明保持什么，再写一项具体修改。例如：

> 保留潜水员、月球、蝴蝶、旋转楼梯和海浪，以及当前比例和配色。只把楼梯处理成独立剪片：保留踏步照片纹理，切开外部轮廓，让最上一级被头盔边缘压住。不要增添新物体或文字。

提示词写的是目标；交付结论以实际成图为准。
