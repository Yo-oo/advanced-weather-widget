# Advanced Weather Widget — zh_TW 翻譯工作流程

## 檔案結構

| 路徑                     | 說明                                |
| ------------------------ | ----------------------------------- |
| `translate/template.pot` | 上游原始翻譯模板（source of truth） |
| `translate/zh_TW.po`     | 正式翻譯檔，直接提交給上游          |
| `.docs/gen_zh_TW.py`     | 翻譯生成腳本（包含完整翻譯字典）    |

`.docs/` 是本地工作區，不提交到上游。腳本直接讀寫 `translate/` 下的檔案。

## 修改翻譯

所有翻譯在 `.docs/gen_zh_TW.py` 中維護：

- **單行條目**：修改 `TRANSLATIONS` dict 中對應 key 的 value
- **多行條目**（目前 6 個）：修改 `MULTILINE` dict；key 為 msgid 開頭的唯一前綴（至少涵蓋到第二行以區分重複的第一行）。
  key 盡量延伸到 msgid 結尾附近：前綴比對的特性是上游在後段增補句子時仍會命中，舊譯文會被默默沿用

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

## 新增條目（上游更新 template.pot 後）

重新執行腳本，未翻譯的條目會保留為空白 `msgstr ""`，並在輸出列出。
將新條目補進 `TRANSLATIONS` dict，再執行一次腳本即可。

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
- `#~` 過時條目來自 `OBSOLETE` list，目前照抄上游 msgmerge 產生的內容

編譯 .mo：

```bash
msgfmt translate/zh_TW.po -o contents/locale/zh_TW/LC_MESSAGES/plasma_applet_org.kde.plasma.advanced-weather-widget.mo
```

## 翻譯原則

- 術語參考**中央氣象署**用語
- 技術縮寫保留英文：API、AQI、KDE、PM2.5、UV、HTTP
- 全形括號用於中文語境：`（）`；半形用於純英文內容：`()`
- 斜線分隔符一律用半形：`/`
- 冒號用全形：`：`
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
