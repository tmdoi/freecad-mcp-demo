# freecad-mcp-demo

FreeCAD + Claude Desktop MCP連携による3Dモデリングデモ。

## ⚠️ 注意事項

- 本リポジトリに記載のプロンプトはあくまで一例です。同一のプロンプトを入力しても、AIの応答は毎回異なる場合があります。
- 生成されるモデルの形状・寸法・動作の正確性は保証されません。実用・製造目的で使用する場合は必ず人間による検証を行ってください。
- FreeCAD・freecad-mcp・Claude Desktopのバージョンによって動作結果が異なる場合があります。

---

## 概要

- **ツール**: FreeCAD 1.1.1 + [freecad-mcp](https://github.com/neka-nat/freecad-mcp) + Claude Desktop
- **参考記事**: [MakeUseOf - I stopped using CAD software and let Claude design my 3D parts instead](https://www.makeuseof.com/stopped-using-cad-claude-design-3d-parts/)

## プロジェクト構成

```
├── scara_robot/
│   ├── scara_robot.FCStd   # FreeCADプロジェクト
│   ├── scara_robot.stl     # 3Dプリント用STL
│   └── scara_demo.mp4      # 動作デモ動画
├── tokyo_tower/
│   └── tokyo_tower_80mm.stl      # 東京タワー（高さ80mm）STL
├── unitree_go2/
│   ├── unitree_go2.FCStd         # 4脚歩行ロボット（基本版）
│   └── unitree_go2_photoref.FCStd # 実機写真を参照して造形を寄せた版
└── wall_planter/
    ├── wall_planter.FCStd         # 壁掛けプランター（3部品）
    ├── plate1_frame.stl           # プレート1: フレーム容器
    ├── plate2_liner_tray.stl      # プレート2: ライナー+ドリップトレイ
    └── usdz/                      # iPhone AR確認用USDZ
        ├── Frame.usdz
        ├── Liner.usdz
        ├── DripTray.usdz
        └── wall_planter_assembled.usdz  # 3部品アセンブル版
```

## セットアップ

### macOS

```bash
# FreeCAD (Homebrew) と uv をインストール
brew install --cask freecad
brew install uv

# FreeCAD MCPアドオン配置（FreeCAD 1.1系）
git clone https://github.com/neka-nat/freecad-mcp.git
cp -r freecad-mcp/addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/v1-1/Mod/
```

Claude Desktop設定 `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Windows 11

```powershell
# FreeCAD と uv をインストール
winget install FreeCAD.FreeCAD
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# uvx のパスを確認（設定ファイルにフルパスで記述する）
where.exe uvx
#   例: C:\Users\<ユーザー名>\.local\bin\uvx.exe

# FreeCAD MCPアドオンを取得（git未導入ならZIPで代用）
cd $env:USERPROFILE\Downloads
Invoke-WebRequest -Uri "https://github.com/neka-nat/freecad-mcp/archive/refs/heads/main.zip" -OutFile "freecad-mcp.zip"
Expand-Archive -Path "freecad-mcp.zip" -DestinationPath . -Force

# アドオン配置（%APPDATA%\FreeCAD\Mod、バージョン番号フォルダなし）
$dest = "$env:APPDATA\FreeCAD\Mod\FreeCADMCP"
New-Item -ItemType Directory -Force -Path $dest
Copy-Item -Recurse -Force "freecad-mcp-main\addon\FreeCADMCP\*" $dest
```

Claude Desktop設定 `%APPDATA%\Claude\claude_desktop_config.json`
（Claude Desktop の 設定 → 開発者 → 「設定を編集」からも開ける）:

```json
{
  "mcpServers": {
    "freecad": {
      "command": "C:\\Users\\<ユーザー名>\\.local\\bin\\uvx.exe",
      "args": ["freecad-mcp", "--only-text-feedback"]
    }
  }
}
```

#### macOS との主な違い

| 項目 | macOS | Windows 11 |
|---|---|---|
| アドオン配置先 | `~/Library/Application Support/FreeCAD/v1-1/Mod/` | `%APPDATA%\FreeCAD\Mod\`（バージョン番号なし） |
| 設定ファイル | `~/Library/Application Support/Claude/` | `%APPDATA%\Claude\` |
| uvx の指定 | `/opt/homebrew/bin/uvx` | `.exe` 付きフルパス、`\` は `\\` にエスケープ |
| JSON内パス区切り | `/` | `\\`（バックスラッシュ2つ） |

> **Windows特有のハマりどころ**
> - FreeCAD 1.1.3 などで初回起動時に「以前の設定を移行しますか？」と出たら「設定をコピー（推奨）」を選ぶとアドオンが新バージョン用ディレクトリに引き継がれる。
> - アドオンは `Mod\FreeCADMCP\InitGui.py` が直下にある状態が正解（`Mod\FreeCADMCP\FreeCADMCP\...` の二重フォルダだと認識されない）。
> - 設定ファイルを保存しても、Claude Desktop はタスクトレイに常駐したままだと再読み込みされない。トレイアイコンを右クリックして完全終了してから再起動する。
> - RPCサーバーの起動確認は PowerShell で `Test-NetConnection -ComputerName 127.0.0.1 -Port 9875`（`TcpTestSucceeded : True` なら稼働中）。

### 共通: RPCサーバーの起動

FreeCAD を起動 → ワークベンチのドロップダウンから **MCP Addon** を選択 →
ツールバーの **Start RPC Server** をクリック（**Auto-Start Server** にチェックで次回から自動起動）。
その後 Claude Desktop を再起動し、ツール一覧に `freecad` が出れば接続完了。

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

---

### Unitree GO2（4脚歩行ロボット）

#### Step 1: モデル生成

```
Unitree社 GO2の4脚歩行ロボットを書きたい
```

Claudeがweb検索で実機スペックを調べたうえで、1/10スケールのモデルを生成する。

**参照した実機スペック（Unitree GO2 標準版）:**

| 項目 | 実寸 | 1/10モデル |
|---|---|---|
| 製品サイズ | 700 × 310 × 400 mm | 70 × 31 × 40 mm |
| 重量 | 約15 kg（バッテリー込み） | ― |
| 胴体関節（Hip）可動域 | -48° 〜 48° | ― |
| 大腿関節（Thigh）可動域 | -200° 〜 90° | ― |
| 下腿関節（Calf）可動域 | -156° 〜 -48° | ― |

**生成されるパーツ構成（Part::Feature × 18）:**

| オブジェクト名 | 内容 |
|---|---|
| `Body` | 胴体シャーシ + 上部カバー（角丸） |
| `Head` | 前方ユニット + LiDAR円柱 |
| `Hip_○○` | 股関節モータ（横向き円筒）× 4 |
| `Thigh_○○` | 大腿（カプセル形状）× 4 |
| `Calf_○○` | 下腿（カプセル形状）× 4 |
| `Foot_○○` | 足先（球体・黒ゴム想定）× 4 |

`○○` は脚の位置を表す **FR / FL / RR / RL**（前右・前左・後右・後左）。

**立位姿勢:** 大腿 45°・下腿 -75°（4本の足先はすべて Z = -33.3mm で水平接地）

> SCARAと同様に各パーツを個別の `Part::Feature` に分割しているため、
> Placementを書き換えれば歩行アニメーションに拡張できる。

#### Step 2: 実機写真を参照した造形の作り込み（任意）

実機の写真を添付して、以下のように指示する。

```
黄色いパーツは前ですか？できれば，写真のような形状に似せてほしいです
```

**写真参照版（`unitree_go2_photoref.FCStd`）での変更点:**

- カラーを実機準拠のシルバーグレー基調に変更（初回生成時の黄色は実機には存在しない）
- 胴体を「下段シャーシ + 上段カウル」の2段構成にし、上面の盛り上がりを再現
- 顔を黒い前面パネル + メインカメラ + LiDARドーム + サイドセンサーの構成に変更
- 大腿を板状の厚いハウジング、下腿を下に向かって細くなるテーパー形状に変更
- 股関節・膝に円筒モータを露出させる

> 画像を添付すると、AIが自身の生成物と実機との差異を指摘したうえで修正できる。
> 形状の細部を詰める場合は、テキストだけで指示するより効率が良い。

#### 補足: fillet エラーへの対処

`Part.makeFillet()` は全エッジ一括指定で `StdFail_NotDone` エラーになることがある。
以下のようなフォールバック関数を挟むと安定する。

```python
def safe_fillet(shape, radius):
    try:
        return shape.makeFillet(radius, shape.Edges)
    except Exception:
        pass
    try:
        # 縦エッジのみに限定して再試行
        vedges = [e for e in shape.Edges
                  if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1e-3]
        return shape.makeFillet(radius, vedges)
    except Exception:
        return shape  # 失敗したら面取りなしで返す
```

---

## Tips

### FreeCADのテーマをLightに切り替える

```
FreeCADの画面モードをLightモードにしたい
```

同梱のプリファレンスパックをマージ適用する（`Insert` は既存設定を保持、`Import` は置換）。

```python
import FreeCAD as App
cfg = "/Applications/FreeCAD.app/Contents/Resources/share/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg"
App.ParamGet("User parameter:BaseApp").Parent().Insert(cfg)
```

適用後はFreeCADの再起動で完全に反映される。
GUIから操作する場合は **FreeCAD → 設定… → 一般 → テーマ**。

### 重い処理でGUIがタイムアウトする場合

OCCTのブーリアン演算やgitのpushなどで `GUI dispatch timed out after 90s` が出る場合は、
`execute_code` ではなく `execute_code_async` を使うとバックグラウンド実行になる。

---

### 壁掛けプランター（無印良品「壁にかけられる観葉植物」参照）

実機の商品ページ画像（正面・裏面）を添付し、「モデルはまだ作らず設計相談から」と伝えて、
対話的に仕様を固めてから造形した事例。

#### 設計相談で確定した仕様

| 項目 | 決定 |
|---|---|
| 植え方 | 土を直接入れる（写真踏襲） |
| 壁固定 | 裏面の鍵穴スリット（フック掛け） |
| 前面開口 | 控えめ + 土留めリップ（土こぼれ防止） |
| 排水 | ライナー底に排水穴 + ドリップトレイ |
| 防水 | コートなし（壁厚2mm + 水量管理） |
| 寸法 | 実物通り 143 × 143 × 45 mm |
| 造形ベッド | Bambu A1（256mm角） |

#### 3部品構成

| 部品 | 役割 |
|---|---|
| `Frame` | 白い外殻。前面土留めリップ、四隅の脚（壁とのすき間5mm）、裏面の鍵穴スリット + 補強ボス、底内側の水返し堰 |
| `Liner` | 土を入れるお椀。底に排水穴 φ4 × 3個 |
| `DripTray` | ライナー下の受け皿。排水を溜めて抜いて捨てられる |

> 3つの正方形（143 / 138 / 137mm角）は256角ベッドに平面展開すると収まらないため、
> 2プレートに分割。品質（防水・強度）を優先し、水を受ける面を層に沿わせる寝かせ置きを基本とした。

- **プレート1**: `Frame` 単独（寝かせ置き）
- **プレート2**: `Liner`（寝かせ置き）+ `DripTray`（薄いので立て置き）

#### スライサー設定の推奨（コートなし防水方針）

壁を3周以上、底面ソリッド層を5層以上にすると、FDMの層間からの水染みを物理的に減らせる。

#### iPhoneでのAR確認（USDZ）

STLはiOS標準ではプレビューできないため、USDZに変換すると
iPhoneのクイックルックでグリグリ回して確認でき、AR表示で原寸（14.3cm角）を壁に投影できる。

macOS標準のUSDツールでSTLを経由せず、メッシュ頂点から直接USDA→USDZを生成した。

```python
# 各パーツのメッシュ頂点・面から USDA を書き出し、usdzip で USDZ 化
import subprocess
subprocess.run(["/usr/bin/usdzip", "out.usdz", "in.usda"])
subprocess.run(["/usr/bin/usdchecker", "out.usdz"])  # 検証
```

`wall_planter_assembled.usdz` は3部品を組み立て位置に配置した完成イメージ。
AirDropまたはメッセージでiPhoneに送り、タップで3D/AR確認できる。
