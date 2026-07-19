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

#### Step 1: モデル生成

```
スカラ型ロボットを作って
```

**生成されるパーツ構成（Part::Feature × 6）:**

| オブジェクト名 | 内容 | 寸法 |
|---|---|---|
| `Base` | ベース円柱 + ネック | φ50mm × 高さ28mm |
| `Joint1` | 第1関節モータハウジング | φ16mm × 高さ14mm |
| `Arm1` | 第1アーム（カプセル形・内部ポケット付き） | 長さ80mm × 幅18mm × 厚さ12mm |
| `Joint2` | 第2関節モータハウジング | φ14mm × 高さ12mm |
| `Arm2` | 第2アーム（カプセル形・内部ポケット付き） | 長さ60mm × 幅14mm × 厚さ10mm |
| `EndEffector` | Zスピンドル + ツールチャック | φ12mm × 高さ20mm |

> パーツを個別の `Part::Feature` として分割生成することで、
> 各パーツのPlacementを個別に変更でき、関節アニメーションが可能になる。

#### Step 2: FEM解析（任意）

左穴を固定拘束、右穴に荷重をかけてFEM解析:

```
１つの穴を固定して，もう一つの穴にM3ボルトを配置して，
そのM3ボルトの頭に30000Nの力を与えたときのFEM解析をしたい
```

**解析結果（SS400鋼材・E=210GPa・ν=0.30）:**
- 最大von Mises応力: 16.11 MPa（降伏応力245MPaの約6.6%）
- 最大変位: 0.0032 mm
- 節点数: 549 / 要素数: 1,680

#### Step 3: 動作範囲の可視化

```
動作範囲を可視化して
```

Claude.aiのチャット上にインタラクティブなビジュアライザーが表示される。
以下のパラメータをスライダーでリアルタイム変更可能:

- アーム1長 / アーム2長
- 関節1角度 / 関節2角度
- Z高さ（スピンドルストローク）
- 表示切替: 上面図 / 側面図 / 3Dアイソメ

エンドエフェクタ座標 (X, Y, Z) と到達半径がリアルタイムで更新される。

> L1=80mm・L2=60mmの場合: 最大到達半径140mm、不感帯半径20mm

#### Step 4: 動作デモ（FreeCAD連動アニメーション）

```
連続的に動作デモっぽく，座標を生成して，動かして
```

**生成される5フェーズのデモシーケンス:**

| フェーズ | 動作 | 関節1 | 関節2 | Z |
|---|---|---|---|---|
| 1 | ホーム → 展開 | 0° → 60° | 0° → 60° | 0mm |
| 2 | ピック動作 | 60° | 60° | 0 → 18 → 0mm |
| 3 | 移送 → プレース | 60° → -45° | 60° → 80° | 0 → 20 → 0mm |
| 4 | 円弧スキャン | -45° → 120° | 80° → 40° | 5mm |
| 5 | ホーム帰還 | 120° → 0° | 40° → 0° | 0mm |

補間方式: smoothstep（`ease(t) = 3t² − 2t³`）による加減速制御

> FreeCADのビューで各パーツのPlacementがリアルタイムに更新されるため、
> 視点を自由に変えながら動作を確認できる。

#### Step 5: デモ動画の保存

```
今の動作デモを動画で保存して
```

方式を聞かれたら:

```
FreeCADの連続スクリーンショット→動画変換（フレーム毎にPNG保存→ffmpegでMP4）
```

**処理フロー:**
1. デモ実行と同時に `saveImage()` で各フレームをPNG保存（1280×720px）
2. ffmpegで30fpsのH.264 MP4に変換（CRF18・高品質）
3. 出力: `~/dev/freecad/scara_robot/scara_demo.mp4`（273フレーム・約9秒・0.6MB）

> ffmpegが未インストールの場合は `brew install ffmpeg` で導入。
