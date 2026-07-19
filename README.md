# freecad-mcp-demo

FreeCAD + Claude Desktop MCP連携による3Dモデリングデモ。

## 概要

- **ツール**: FreeCAD 1.1.1 + [freecad-mcp](https://github.com/neka-nat/freecad-mcp) + Claude Desktop
- **参考記事**: [MakeUseOf - I stopped using CAD software and let Claude design my 3D parts instead](https://www.makeuseof.com/stopped-using-cad-claude-design-3d-parts/)

## プロジェクト構成

```
├── scara_robot/
│   ├── scara_robot.FCStd   # FreeCADプロジェクト
│   ├── scara_robot.stl     # 3Dプリント用STL
│   └── scara_demo.mp4      # 動作デモ動画
└── tokyo_tower/
    └── tokyo_tower_80mm.stl  # 東京タワー（高さ80mm）STL
```

## セットアップ

```bash
# FreeCAD MCPアドオン配置
cp -r addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/v1-1/Mod/

# Claude Desktop設定 (claude_desktop_config.json)
{
  "mcpServers": {
    "freecad": {
      "command": "/opt/homebrew/bin/uvx",
      "args": ["freecad-mcp", "--only-text-feedback"]
    }
  }
}
```
