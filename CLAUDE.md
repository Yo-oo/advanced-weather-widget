# Advanced Weather Widget — zh_TW 翻譯工作流程

## 檔案結構

| 路徑                     | 說明                                |
| ------------------------ | ----------------------------------- |
| `translate/template.pot` | 上游原始翻譯模板（source of truth） |
| `translate/zh_TW.po`     | 正式翻譯檔，直接提交給上游          |
| `.docs/gen_zh_TW.py`     | 翻譯生成腳本（包含完整翻譯字典）    |
| `.docs/tools/`           | 發版輔助腳本（抽取上下文、跨語言比對、寫回字典），見「翻譯品質流程」 |
| `.docs/work/`            | 輔助腳本的輸出（`context.json` 等），不需版本控制 |

`.docs/` 是本地工作區，不提交到上游。腳本直接讀寫 `translate/` 下的檔案。

## 修改翻譯

所有翻譯在 `.docs/gen_zh_TW.py` 中維護：

- **單行條目**：修改 `TRANSLATIONS` dict 中對應 key 的 value
- **多行條目**：修改 `MULTILINE` dict；key 為 msgid 開頭的唯一前綴（至少涵蓋到第二行以區分重複的第一行）。
  key 盡量延伸到 msgid 結尾附近：前綴比對的特性是上游在後段增補句子時仍會命中，舊譯文會被默默沿用
- **同一 msgid、不同語意（msgctxt）**：`TRANSLATIONS` 只以 msgid 為 key，所有 context 共用同一譯文。需要區分時加進 `CTX_TRANSLATIONS`，key 為 `(msgctxt, msgid)`，優先於 `TRANSLATIONS`（例：`High`/`Low` 的每日最高／最低溫、`Dry`、`Large`、`Normal`）
- **複數條目**：`PLURAL` dict，key 為單數 msgid，只填 msgstr[0]（`nplurals=1`）

修改後執行：

```bash
python3 .docs/gen_zh_TW.py
```

輸出：

```
Written: N entries
Untranslated: 0
```

驗證格式：

```bash
msgfmt --check translate/zh_TW.po -o /dev/null
```

> **重要**：不要直接編輯 `translate/zh_TW.po`，下次執行腳本會覆蓋。所有變更都要在 `gen_zh_TW.py` 的 dict 中進行。

## 發版流程（上游更新 template.pot 後）

1. **同步上游**：`git switch translation/tools`，先 `git checkout -- translate/zh_TW.po contents/locale/` 放掉尚未 commit 的 po/.mo（上游也會改 `zh_TW.po`，不放掉 merge 會衝突），再 `git fetch --all && git merge origin/main`。commit 前再 fetch 一次：發版前 template 可能還會再改
2. **更新 `OBSOLETE`**：以 `git show main:translate/zh_TW.po` 裡的 `#~` 區塊逐字取代腳本中的 `OBSOLETE` list。沿用舊資料會漏掉新的過時條目（1.9.0 就少了 44 條）；腳本會略過 template 中已重新啟用的 msgid，避免 `msgfmt` 報重複定義
3. **執行腳本**：`python3 .docs/gen_zh_TW.py`，新條目會留空並列在 `Untranslated`
4. **翻譯新條目**：`python3 .docs/tools/extract_context.py` 產生含原始碼上下文的 `.docs/work/context.json`，翻譯完用 `apply_translations.py` 寫回字典（流程見「翻譯品質流程」）。新條目量少時直接補進 dict 即可，但仍要先看原始碼
5. **驗證**：`msgfmt --check --statistics`，並確認 `%N`、`<br>`、換行數量與原文一致；編譯 `.mo`
6. **commit**
   - `translation/tools`：只 commit `.docs/`（`.docs` 被 ignore，需 `git add -f`）。**不要** commit po/.mo
   - `git branch -f translation/update-zh_TW-<ver> main`（分支尚未 push 且無獨有 commit 時），`git switch` 過去（未 commit 的 po/.mo 會帶過去），只 commit `zh_TW.po` 與 `.mo`，訊息為 `Update zh_TW translation for <ver>`
   - 絕不從 `translation/tools` 開 PR

## 檢查是否有遺漏

腳本的 `Untranslated: N` 涵蓋單行與多行的**空白**條目，`msgfmt --statistics` 可交叉確認：

```bash
msgfmt --check --statistics translate/zh_TW.po -o /dev/null
```

**偵測不到的情況：多行條目原文被修改。** `MULTILINE` 以前綴比對，上游只改後段時仍會套用舊譯文，且不計入未翻譯。上游更新 template 後，需逐條比對多行條目的 msgid 與 msgstr 內容（行數不同是明顯訊號）：

```bash
awk '/^msgid ""$/{p=1;buf=$0"\n";next} p&&/^(msgstr|")/{buf=buf $0"\n";next} p{if(buf ~ /msgstr ""\n"/ && buf !~ /Project-Id/) print buf"----"; p=0}' translate/zh_TW.po
```

單行條目為整句完全比對，原文一改就會變成未翻譯，不會有此問題。

## Header 與過時條目

- `POT-Creation-Date` 沿用既有 `zh_TW.po` 的值（上游 msgmerge 寫入），不從 template 讀取，避免與上游不一致；`PO-Revision-Date` 每次執行都更新
- `#~` 過時條目來自 `OBSOLETE` list，需每次發版依「發版流程」第 2 步重新取自 main

編譯 .mo：

```bash
msgfmt translate/zh_TW.po -o contents/locale/zh_TW/LC_MESSAGES/plasma_applet_org.kde.plasma.advanced-weather-widget.mo
```

## 翻譯品質流程（新增字串量大時）

1.9.0 一次新增約 550 條，流程如下：

1. **先看原始碼，再翻譯。** 光看 msgid 容易錯：`10 m` 是風的測量高度（公尺），不是分鐘；`Wheel` 是設定齒輪按鈕，不是滑鼠滾輪；`Highs and lows` 是等壓線上的高低氣壓中心，不是高低溫；說明面板裡小寫開頭的條目是接在粗體按鍵名後的描述片段；雷達／衛星時間軸上的 `range` 是時間範圍。`extract_context.py` 會為每條附上前後約 7 行 QML
2. **多位 translator 獨立翻譯**（subagent，彼此看不到對方結果；約 3 組，量大時分前後半避免 context 過長），再比對：多數一致的先看，三者皆異的保留現譯並標記。Fable 需額外 usage credits，沒開時改用 Opus／Sonnet
3. **與 zh_CN 比對**，再用 `build_compare.py` **與所有語言比對**，只看「意思」出入。各語言品質不一，單一語言離群值要持保留態度（例：四種語言都把 `Wheel` 誤譯成滑鼠滾輪）
4. **審閱方式**：分批（約 14 條）以表格列出「現譯／新譯／建議」，使用者確認後才套用；有爭議的用語先上網查證，沒有證據就維持現狀；決定與依據記在 `.docs/review-<ver>.md`
5. 腳本以 msgid 為 key，同 msgid 不同 context 要用 `CTX_TRANSLATIONS`

## 翻譯原則

- 術語參考**中央氣象署**用語
- 技術縮寫保留英文：API、AQI、KDE、PM2.5、UV、HTTP
- 全形括號用於中文語境：`（）`；半形用於純英文內容：`()`
- 斜線分隔符一律用半形：`/`
- 冒號用全形：`：`
- 引用實際的 UI 標籤（設定路徑、分頁名、頁面名）時，必須與該標籤現有譯文**完全一致**，例如分頁 `Details` 是「詳細資訊」、設定頁 `Location` 是「位置」（單一儲存的地點才叫「地點」）、`Visible tabs:` 是「可見頁籤」
- shell 指令中的引號保持半形 ASCII，不要改成「」
- 省略號用 `⋯`（三點）而非 `...`

## 重要術語對照

| 英文                              | 中文           | 備註           |
| --------------------------------- | -------------- | -------------- |
| Apparent / Feels-like temperature | 體感溫度       | 中央氣象署用語 |
| Dew point                         | 露點           |                |
| Visibility                        | 能見度         |                |
| Atmospheric pressure              | 大氣壓力       |                |
| Precipitation                     | 降水量         |                |
| Geomagnetic Storm                 | 地磁風暴       |                |
| Aurora Visibility                 | 極光可見度     |                |
| Solar Wind                        | 太陽風         |                |
| Kp Index                          | Kp 指數        |                |
| X-ray Flare Class                 | X 射線閃焰等級 |                |
| Waxing Crescent                   | 眉月           |                |
| Waxing Gibbous                    | 盈凸月         |                |
| Waning Gibbous                    | 虧凸月         |                |
| Waning Crescent                   | 殘月           |                |
| First Quarter                     | 上弦月         |                |
| Last Quarter                      | 下弦月         |                |
| Rime fog                          | 霧淞           |                |
| Snow grains                       | 雪粒           | CWA 官方用語   |
| Alder                             | 榿木           | 花粉           |
| Birch                             | 白樺           | 花粉           |
| Mugwort                           | 艾草           | 花粉           |
| Ragweed                           | 豚草           | 花粉           |
| Alert / Warning                   | 警報           | 不用「警告」「警戒」 |
| All clear                         | 無警報         | 警報卡片無警報時的標籤 |
| Precipitation / Chance of precip. | 降水量 / 降水機率 | 含降雪，不只寫「降雨」 |
| Model（氣象預報模型）             | 模型           | 不用「模式」   |
| Palette                           | 調色盤         | 不用「色盤」   |
| Click / Double-click / Right-click | 點擊 / 連點兩下 / 點擊右鍵 |       |
| Previous day / Next day           | 上一天 / 下一天 | 與 Previous/Next period 一致 |
| Weather history                   | 歷史天氣       |                |
| Shortcuts                         | 快捷鍵         | KDE 繁中舊譯為「捷徑」，沒有「快速鍵」的證據 |
| Tooltip                           | 提示           | 沿用既有譯文   |
| Weather Map                       | 天氣地圖       | 互動地圖分頁，不是綜觀「天氣圖」 |
| range（雷達／衛星時間軸）         | 時間範圍       | 不是空間涵蓋範圍 |
| scale / level（G scale、Kp）      | 等級           | 色階門檻用「級距」 |
| Borders                           | 邊界           |                |
| 語言名稱                          | …語            | 阿拉伯語，不用「…文」 |
