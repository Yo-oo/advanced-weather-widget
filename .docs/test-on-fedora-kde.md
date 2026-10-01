# 在 Fedora KDE Live 測試翻譯

本地工作文件，不提交上游。

## 環境準備

- macOS + [UTM](https://mac.getutm.app)
- [Fedora KDE Plasma ISO](https://fedoraproject.org/spins/kde)（Apple Silicon 選 AArch64，Intel 選 x86_64）
- UTM 共享資料夾（選用）：`~/Downloads/others/linux/shared_folder/`

## 首次安裝流程

```bash
# 1. 安裝工具（sudo 密碼為空，直接 Enter）
sudo dnf install gettext git -y

# 2. clone 指定 branch
git clone -b translation/fix-zh_TW https://github.com/你的fork/advanced-weather-widget.git
cd advanced-weather-widget

# 3. 編譯 .mo
sh translate/scripts/build.sh

# 4. 安裝 widget（注意：必須加 --type Plasma/Applet）
kpackagetool6 --type Plasma/Applet --install .

# 5. 重啟 Plasma
killall plasmashell && kstart plasmashell
```

## 切換 branch 後更新

```bash
git fetch origin
git checkout <branch>
sh translate/scripts/build.sh
kpackagetool6 --type Plasma/Applet --upgrade .
killall plasmashell && kstart plasmashell
```

## 切換語系

System Settings → Region & Language → Language → 新增 Chinese (Traditional) → 套用 → 重新登入。

或快速測試（不需重新登入）：

```bash
LANG=zh_TW.UTF-8 plasmashell --replace &
```

## 常見問題

**widget 沒出現在元件清單**

- 確認使用 `--type Plasma/Applet`，預設會裝到錯誤的 `kpackage/generic/`
- 若裝錯位置，先手動刪除再重裝：
  ```bash
  rm -rf ~/.local/share/plasma/plasmoids/org.kde.plasma.advanced-weather-widget
  kpackagetool6 --type Plasma/Applet --install .
  ```

**確認安裝位置**

```bash
ls ~/.local/share/plasma/plasmoids/ | grep weather
```
