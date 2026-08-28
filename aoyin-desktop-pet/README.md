# 敖尹 Live2D 桌宠

一个以**真正的 Live2D Cubism 模型**为核心的跨平台桌宠概念版，支持 Windows 与 macOS。它不是用 SVG / CSS 拼出来的角色：人物身体、脸部、眼睛、呼吸、物理摆动与动作均由 `.moc3` 模型和 Cubism Runtime 驱动。

> 非官方、非商业同人项目。与《恋与深空》、叠纸或 Infold Games 无关联。程序不打包任何游戏模型、贴图、声音、截图或 UI。

## 已完成

- 透明、无边框、始终置顶的桌宠窗口；
- Windows x64 与 macOS Universal（Intel + Apple Silicon）构建；
- Live2D 视线追踪、呼吸、眨眼、头部与身体微动、物理摆动；
- 独立的**摘下 / 戴回眼镜动作**：预备、眯眼、头部后仰、手部跟随、眼镜离面、动作顶点与回落；
- 眼镜摘下后保持无眼镜状态，再次触发会戴回；
- 双击眼镜或按 `G` 触发；按 `Z` 休息；
- 托盘菜单、右键菜单、窗口拖动、隐藏、点击穿透；
- 纯本地运行，不上传屏幕内容，不联网请求模型；
- 自动生成双平台安装包的 GitHub Actions。

## Live2D 实现说明

核心人物使用 Live2D 官方 Haruto 示例的 `.moc3`、物理和动作数据作为运动骨架，并重新制作了同人化配色、服装纹理与人类发型层。眼镜是跟随 `ParamAngleX/Y/Z` 的独立附件层，同时驱动 Cubism 眼睛、头部与身体参数完成摘戴动作。

这样处理是有意为之：编译后的 `.moc3` 不能诚实地凭空增加一个眼镜 ArtMesh；真正把眼镜做进模型，需要在 Live2D Cubism Editor 中持有并编辑原始 `.cmo3` 工程后重新导出。当前方案保留了真正的 Live2D 主体，同时让概念版能够完整演示可摘眼镜交互。

## 本地运行

### 1. 准备依赖

- Rust stable
- Python 3.11+
- macOS 12+，或 Windows 10/11（需要 WebView2）

```bash
python -m pip install -r requirements-assets.txt
python scripts/bootstrap_assets.py
python scripts/validate_project.py
```

### 2. 开发运行

```bash
cargo install tauri-cli --version '^2' --locked
cargo tauri dev
```

### 3. 打包

```bash
# Windows
cargo tauri build

# macOS Universal
rustup target add aarch64-apple-darwin x86_64-apple-darwin
cargo tauri build --target universal-apple-darwin
```

安装包位于 `src-tauri/target/**/release/bundle/`。

## 操作

| 操作 | 结果 |
|---|---|
| 双击眼镜 / `G` | 摘下或戴回眼镜 |
| `Z` | 进入或退出休息状态 |
| 鼠标移动 | 视线与头部跟随 |
| 长按或拖动 | 移动桌宠窗口 |
| 右键 | 打开动作菜单 |
| 托盘菜单 | 显示、摘眼镜、休息、退出 |

## 资产重建

`scripts/bootstrap_assets.py` 会从上游获取可再分发的 Live2D 示例骨架和运行时，并在本地生成：敖尹同人配色纹理、发型和眼镜等附件、跨平台图标，以及资产校验清单。这使源码分支不必直接提交第三方二进制模型。

## 许可与声明

程序代码使用 MIT License。Live2D 示例模型、Cubism Core 和第三方运行库仍受各自条款约束，详见 [NOTICE.md](NOTICE.md)。在公开发布安装包或进行任何商业使用前，请重新核对上游条款。
