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
```

Claude Desktop設定 (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "freecad": {
      "command": "/opt/homebrew/bin/uvx",
      "args": ["freecad-mcp", "--only-text-feedback"]
    }
  }
}
```

---

## プロンプト集

### 東京タワー（3Dプリント用・高さ80mm）

```
３Dプリンタで印刷する高さ80mmの東京タワーの３次元モデルを生成して
```

**生成される構造:**
- 4本の主脚（根元28mm広がり → 頂点に向かってテーパー、40セグメント近似）
- 水平リング13段（高さ4, 8, 12, 18, 24, 30, 36, 42, 50, 58, 66, 74, 78mm）
- X字斜め材（各段間・全4面）
- 展望台1（高さ28mm ≒ 実物150m相当）
- 展望台2（高さ50mm ≒ 実物250m相当）
- アンテナ（先端コーン付き・8mm）

**出力サイズ:** X=41.7mm × Y=41.7mm × Z=90.8mm（アンテナ含む）

**STLエクスポート:**

```
~/Downloadsにstlファイルとして保存して
```

**印刷時の注意:**
- サポート材を有効にすること（脚の細い部分）
- 推奨レイヤー高さ: 0.1〜0.15mm

---

### SCARAロボット

```
スカラ型ロボットを作って
```

**動作デモ（連続アニメーション）:**

```
連続的に動作デモっぽく，座標を生成して，動かして
```

**デモ動画の保存（フレームキャプチャ → MP4）:**

```
今の動作デモを動画で保存して（FreeCADの連続スクリーンショット→ffmpegでMP4変換）
```
