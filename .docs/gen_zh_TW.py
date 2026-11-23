#!/usr/bin/env python3
"""Generate zh_TW.po from template.pot"""
import re, sys, os
from datetime import datetime, timezone, timedelta

_here = os.path.dirname(os.path.abspath(__file__))
_root = os.path.join(_here, '..')
_pot  = os.path.join(_root, 'translate', 'template.pot')
_out  = os.path.join(_root, 'translate', 'zh_TW.po')

with open(_pot, 'r', encoding='utf-8') as f:
    content = f.read()

TRANSLATIONS = {
    # --- Special/format strings ---
    " until dawn": " 後日出",
    "%1 %2": "%1 %2",
    "%1 - Today": "%1 - 今天",
    "%1 - Tomorrow": "%1 - 明天",
    "%1 is ending": "%1趨緩",
    "%1 is expected": "預計有%1",
    "%1 is expected to end %2.": "%1預計於%2結束。",
    "%1 is possible %2.": "%2可能有%1。",
    "%1 will be %2 with a low of %3 and a high of %4.":
        "%1 天氣將為%2，低溫 %3，高溫 %4。",
    "%1pt %2": "%1pt %2",
    "--": "--",
    "-180 to 180 (e.g. 23.3219)": "-180 至 180（例如 23.3219）",
    "-90 to 90 (e.g. 42.6977)": "-90 至 90（例如 42.6977）",
    "0 = auto (120 px per chip). Increase if values are truncated.":
        "0 = 自動（每個標籤 120 px），若數值被截斷請增加。",
    "0 = auto. Increase if items are cut off.":
        "0 = 自動，若項目被截斷請增加。",
    "1 Alert": "1 則警報",
    "3D Oxygen (Bundled)": "3D Oxygen（內建）",
    "12-hour format": "12 小時制",
    "12h": "12h",
    "24-hour format": "24 小時制",
    "24h": "24h",
    "68°F": "68°F",

    # --- A ---
    "All days show hourly forecast when opening the tab": "開啟頁籤時所有日期均顯示逐時預報",
    "All days start collapsed": "所有日期預設收折",
    "Auto-open hourly forecast:": "自動展開逐時預報：",
    "<b>Effective:</b> %1": "<b>生效時間：</b>%1",
    "<b>Headline:</b> %1": "<b>標題：</b>%1",
    "<b>Instruction:</b> %1": "<b>說明：</b>%1",
    "<b>Provider:</b> %1": "<b>資料來源：</b>%1",
    "<b>Severity:</b> %1%2": "<b>嚴重程度：</b>%1%2",
    "<b>Why OWM layers may not match RainViewer radar</b><br/><br/>OWM precipitation/cloud layers are <b>static model tiles</b> - they show a smoothed NWP (Numerical Weather Prediction) output, not actual radar returns. They represent where the model <i>thinks</i> it is raining based on interpolation between weather stations and model runs.<br/><br/>RainViewer uses <b>real weather radar composites</b> from radar stations - actual measured reflectivity updated every 2-10 minutes. This discrepancy is expected and known.":
        "<b>為何 OWM 圖層可能與 RainViewer 雷達不符</b><br/><br/>OWM 降水/雲層圖層是<b>靜態模型磚</b>，顯示的是平滑化後的數值天氣預報（NWP）輸出，而非實際雷達回波。這些圖層呈現模型根據氣象站資料與模式計算後<i>推測</i>的降雨位置。<br/><br/>RainViewer 使用來自雷達站的<b>真實氣象雷達合成圖</b>，每 2 至 10 分鐘更新一次實際量測的反射率。此差異屬預期現象，為已知情況。",
    "AI-powered weather intelligence. API key required below.":
        "AI 驅動的天氣智慧服務，請在下方填入 API 金鑰。",
    "API key is empty.": "API 金鑰為空。",
    "AQHI": "AQHI",
    "AQI": "AQI",
    "Active": "活躍",
    "Adaptive (Open-Meteo)": "自適應（Open-Meteo）",
    "Adaptive (auto-fallback)": "自適應（自動備援）",
    "Add Location Manually": "手動新增地點",
    "Add a location": "新增地點",
    "Advanced (all tabs)": "進階（所有頁籤）",
    "Afternoon": "下午",
    "Air Quality": "空氣品質",
    "Air Quality:": "空氣品質：",
    "Air quality index": "空氣品質指標",
    "Air quality is acceptable.": "空氣品質尚可。",
    "Air quality is extremely poor.": "空氣品質極差。",
    "Air quality is fair.": "空氣品質普通。",
    "Air quality is poor.": "空氣品質差。",
    "Air quality is satisfactory.": "空氣品質良好。",
    "Air quality is very poor.": "空氣品質非常差。",
    "Air quality options": "空氣品質選項",
    "All tabs": "所有頁籤",
    "Alder": "榿木",
    "Alerts": "警報",
    "Alerts:": "警報：",
    "Alt: %1 %2": "高度：%1 %2",
    "Alt: %1 m": "高度：%1 公尺",
    "Alternative provider. API key required below.":
        "備用氣象資料來源，請在下方填入 API 金鑰。",
    "Altitude (%1):": "海拔（%1）：",
    "Altitude is optional, but strongly recommended for accurate forecasts. "
    "MET Norway (met.no) uses it to correct temperature and pressure for elevation; "
    "leaving it at 0 for a mountain location will return sea-level values.":
        "海拔為選填項目，但強烈建議填入以提高預報精確度。"
        "MET Norway（met.no）會根據海拔修正溫度與氣壓；"
        "若山區地點設為 0，將回傳海平面數值。",
    "Altitude:": "海拔：",
    "An API key is required for %1. Weather data cannot be retrieved without it.":
        "%1 需要 API 金鑰，未設定則無法取得天氣資料。",
    "Animate row scrolling": "啟用列捲動動畫",
    "Apparent (feels-like) temperature": "體感溫度",
    "Apparent temperature": "體感溫度",
    "Appearance": "外觀",
    "Apply Settings?": "套用設定？",
    "Apply detected location": "套用偵測到的位置",
    "Are you sure? This is your last saved location. If you remove it, "
    "the widget will no longer show weather information.":
        "確定要刪除？這是您最後一個儲存的地點，刪除後小工具將不再顯示天氣資訊。",
    "Around midnight - ": "接近午夜 — ",
    "Atmospheric pressure": "大氣壓力",
    "Aurora Visibility": "極光可見度",
    "Auto": "自動",
    "Auto (detect on save)": "自動（儲存時偵測）",
    "Auto-detection first asks GeoClue2, the system location service, for your current position. If system location is unavailable, the widget estimates your location from your public IP address, which is usually less precise and only updates when detection runs again.":
        "自動偵測會優先透過 GeoClue2（系統定位服務）取得您的目前位置。若系統定位不可用，將根據您的公開 IP 位址估算位置，通常精確度較低，且僅在再次執行偵測時才會更新。",
    "Auto-detection is limited without QtLocation and QtPositioning. It will fall back to IP-based detection, which may be less accurate and will not update in real time as you move. If you want to improve auto-detection accuracy, please install the required packages for your distribution. For more details, see the install guide.":
        "未安裝 QtLocation 和 QtPositioning 時，自動偵測功能受限，將改用 IP 定位，精確度較低且不會隨移動即時更新。若要提升精確度，請為您的發行版安裝所需套件。詳情請參閱安裝指南。",
    "Auto-detection updated coordinates.": "自動偵測已更新座標。",
    "Automatic": "自動",
    "Automatically detect location": "自動偵測位置",
    "Available": "可用",

    # --- B ---
    "Back": "返回",
    "Badge Background Color": "徽章背景顏色",
    "Badge background:": "徽章背景：",
    "Badge opacity:": "徽章不透明度：",
    "Badge position:": "徽章位置：",
    "Badge spacing:": "徽章間距：",
    "Behavior": "行為",
    "Birch": "白樺",
    "Both  07:17 / 18:03": "兩者  07:17 / 18:03",
    "Both (sunrise & sunset)": "兩者（日出與日落）",
    "Bottom Center": "下方置中",
    "Bottom Left": "左下",
    "Bottom Right": "右下",
    "Browse…": "瀏覽⋯",
    "Bullet  •": "實心圓點  •",
    "Button guide": "按鈕說明",
    "Bz (Magnetic Field)": "Bz（磁場）",

    # --- C ---
    "CO": "CO",
    "Cancel": "取消",
    "Cancel rename": "取消重新命名",
    "Carbon Monoxide (CO)": "一氧化碳（CO）",
    "Cards": "卡片",
    "Cards (2 columns)": "卡片（2 欄）",
    "Cards height:": "卡片高度：",
    "Celsius (°C)": "攝氏（°C）",
    "Changes staged. Click the main Apply button to save.":
        "變更已暫存，點擊主套用按鈕以儲存。",
    "Checking location availability…": "正在檢查位置可用性⋯",
    "Chinese weather provider with global coverage. API key required below.":
        "中國天氣服務供應商，涵蓋全球資料，請在下方填入 API 金鑰。",
    "Choose Simple Mode Font": "選擇簡易模式字型",
    "Choose Style…": "選擇樣式⋯",
    "Choose a Panel Font": "選擇面板字型",
    "Choose a custom icon for this item": "為此項目選擇自訂圖示",
    "Choose on Map": "在地圖上選擇",
    "Choose on map": "在地圖上選擇",
    "City / location name": "城市/地點名稱",
    "Clear": "晴",
    "Clear (day)": "晴（白天）",
    "Clear (night)": "晴（夜晚）",
    "Clear night": "晴夜",
    "Clear sky": "晴空",
    "Clouds": "雲層",
    'Click \\"Test across providers\\" to check if the coordinates are serviceable '
    "by each supported weather provider. Providers requiring an API key that is not "
    "configured will be skipped.":
        '點擊「測試所有供應商」以檢查該座標是否受各支援天氣供應商服務。'
        "未設定 API 金鑰的供應商將被略過。",
    "Click on the map to select a location": "點擊地圖以選擇位置",
    "Click to configure a location": "點擊以設定位置",
    "Colorful": "彩色",
    "Colorful (KDE color icons)": "彩色（KDE 彩色圖示）",
    "Compressed": "緊湊",
    "Condition": "天氣狀況",
    "Condition Icons": "天氣狀況圖示",
    "Condition:": "天氣狀況：",
    "Configure display mode options": "設定顯示模式選項",
    "Configure icon - %1": "設定圖示 — %1",
    "Configure icon…": "設定圖示⋯",
    "Configure weather icons…": "設定天氣圖示⋯",
    "Configure…": "設定⋯",
    "Confirm rename": "確認重新命名",
    "Compass in forecast:": "預報中顯示指南針：",
    "Confirm your location": "確認您的位置",
    "Critical notifications are still shown even when Do Not Disturb is enabled, or while you're playing a game or watching a fullscreen video (if those options are enabled in System Settings → Notifications).":
        "即使啟用「勿擾」模式，或您正在遊玩遊戲或觀看全螢幕影片時（如已在系統設定 → 通知中啟用相關選項），重要通知仍然會顯示。",
    "Connection failed (HTTP %1).": "連線失敗（HTTP %1）。",
    "Connection successful! %1 key is valid.": "連線成功！%1 金鑰有效。",
    "Coordinates": "座標",
    "Current moon phase": "目前月相",
    "Current date and/or time": "目前日期及/或時間",
    "Current temperature": "目前溫度",
    "Custom": "自訂",
    "Custom (set each unit manually)": "自訂（手動設定各單位）",
    "Custom per-condition icons": "依天氣狀況自訂圖示",
    "Custom…": "自訂⋯",

    # --- D ---
    "Daily Forecast Settings": "每日預報設定",
    "Date / Time": "日期/時間",
    "Date / Time options": "日期/時間選項",
    "Date and time in header:": "標題顯示日期與時間：",
    "Date format:": "日期格式：",
    "Date/Time:": "日期/時間：",
    "Date:": "日期：",
    "Dark Sky-compatible API with US alerts. API key required below.":
        "相容 Dark Sky 的 API，含美國天氣警報，請在下方填入 API 金鑰。",
    "Dash  –": "破折號  –",
    "Data Refresh": "資料更新",
    "Dawn approaching - ": "黎明將至 — ",
    "Day": "白天",
    "Daylight over": "日照結束",
    "Default": "預設",
    "Default location (click to unset)": "預設地點（點擊取消設定）",
    "Default tab:": "預設頁籤：",
    "Dense drizzle": "濃毛雨",
    "Description": "說明",
    "Details": "詳細資訊",
    "Details Items": "詳細資訊項目",
    "Details items:": "詳細資訊項目：",
    "Details layout:": "詳細資訊版面配置：",
    "Details only": "僅顯示詳細資訊",
    "Detect / change location": "偵測/變更位置",
    "Detect / change location…": "偵測/變更位置⋯",
    "Detecting…": "偵測中⋯",
    "Dew Point": "露點",
    "Dew point temperature": "露點溫度",
    "Dew point:": "露點：",
    "Disable item": "停用項目",
    "Disabled": "已停用",
    "Discard": "捨棄",
    "Dismiss": "關閉",
    "Display": "顯示",
    "Display mode:": "顯示模式：",
    "Displaying °C and °F together": "同時顯示 °C 與 °F",
    "Dual temperature": "雙溫度",
    "Dominant pollen type and index": "主要花粉類型及指數",
    "Drag to reorder enabled items": "拖曳以重新排列已啟用的項目",
    "Drag to reorder shown items": "拖曳以重新排列顯示的項目",
    "Drizzle": "毛雨",

    # --- E ---
    "Each QWeather project has a unique API host. "
    "Find yours at console.qweather.com under your project settings.":
        "每個 QWeather 專案都有獨特的 API 主機位址，"
        "請至 console.qweather.com 的專案設定中查詢。",
    "Each notification type can be enabled independently, with its own daily time where applicable.":
        "每種通知類型可獨立啟用，並可個別設定每日觸發時間（如適用）。",
    "Edit Saved Location": "編輯已儲存的地點",
    "Edit location details": "編輯地點詳細資訊",
    "Effective": "生效時間",
    "Enable alert notifications": "啟用警報通知",
    "Enable all": "全部啟用",
    "Enable item": "啟用項目",
    "Enable or disable this item": "啟用或停用此項目",
    "Enable or disable this item on the panel": "在面板上啟用或停用此項目",
    "Enabled": "已啟用",
    "Enter Location": "輸入位置",
    "Enter Manually": "手動輸入",
    "Enter a location name and valid coordinates, then click the main Apply button.":
        "輸入地點名稱及有效座標，然後點擊主套用按鈕。",
    "Enter manually": "手動輸入",
    "Enter your OpenWeatherMap API key": "輸入您的 OpenWeatherMap API 金鑰",
    "Enter your Pirate Weather API key": "輸入您的 Pirate Weather API 金鑰",
    "Enter your QWeather API key": "輸入您的 QWeather API 金鑰",
    "Enter your StormGlass API key": "輸入您的 StormGlass API 金鑰",
    "Enter your Tomorrow.io API key": "輸入您的 Tomorrow.io API 金鑰",
    "Enter your Visual Crossing API key": "輸入您的 Visual Crossing API 金鑰",
    "Enter your WeatherAPI.com key": "輸入您的 WeatherAPI.com 金鑰",
    "Enter exact latitude, longitude, and optional elevation for a more local forecast. You can copy coordinates from OpenStreetMap, GeoNames, or Google Maps.":
        "輸入精確的緯度、經度及選填的海拔高度，以獲得更在地的預報。您可從 OpenStreetMap、GeoNames 或 Google Maps 複製座標。",
    "Enter your Weatherbit API key": "輸入您的 Weatherbit API 金鑰",
    "Error (code %1)": "錯誤（代碼 %1）",
    "Evening - ": "傍晚 — ",
    "Excellent": "優",
    "Expand all days:": "展開所有日期：",
    "Expand widget to fill available panel space": "擴展小工具以填滿面板空間",
    "Expanded cards height:": "展開卡片高度：",
    "Expires": "到期",
    "Extreme": "極端",
    "Extreme geomagnetic storm.": "極端地磁風暴。",
    "Extremely Poor": "極差",

    # --- F ---
    "First day of week:": "每週第一天：",
    "Forecast:": "預報：",
    "Friday": "星期五",
    "Fahrenheit (°F)": "華氏（°F）",
    "Failed to load weather providers": "無法載入天氣資料來源",
    "Failed: %1": "失敗：%1",
    "Fair": "普通",
    "Feels Like": "體感",
    "Feels like:": "體感：",
    "Feels like: %1": "體感：%1",
    "Fill panel": "填滿面板",
    "Fill panel:": "填滿面板：",
    "Find": "尋找",
    "First Quarter": "上弦月",
    "Flare Warning": "閃焰警告",
    "Flat Color (Bundled)": "純色（內建）",
    "Fog": "霧",
    "Font icons (default)": "字型圖示（預設）",
    "Font size:": "字型大小：",
    "Footer:": "頁尾：",
    "Forecast": "預報",
    "Forecast days:": "預報天數：",
    "Forecast only": "僅顯示預報",
    "Free Norwegian Meteorological Institute service. No API key needed.":
        "挪威氣象研究所免費服務，無需 API 金鑰。",
    "Free and open-source. No API key needed. Recommended.":
        "免費且開放原始碼，無需 API 金鑰，推薦使用。",
    "Freezing drizzle": "凍毛雨",
    "Freezing drizzle (day)": "凍毛雨（白天）",
    "Freezing drizzle (night)": "凍毛雨（夜晚）",
    "Freezing rain": "凍雨",
    "Freezing rain (day)": "凍雨（白天）",
    "Freezing rain (night)": "凍雨（夜晚）",
    "Full Moon": "滿月",
    "Future alerts": "未來警報",

    # --- G ---
    "General": "一般",
    "GPS / GeoClue2 unavailable (install qt6-qtlocation for best accuracy). Using IP-based detection.":
        "GPS / GeoClue2 不可用（安裝 qt6-qtlocation 以獲得最佳精確度），正在使用 IP 定位。",
    "GeoClue2 unavailable, trying system location…":
        "GeoClue2 無法使用，嘗試系統位置⋯",
    "Geomagnetic Storm": "地磁風暴",
    "Geomagnetic activity": "地磁活動",
    "Geomagnetic activity will be %1 (Kp %2)": "地磁活動將達%1（Kp %2）",
    "Good": "良好",
    "Grass": "禾草",

    # --- H ---
    "Headline": "標題",
    "Heavy": "大量",
    "Hourly Forecast Settings": "逐時預報設定",
    "Hourly layout:": "逐時版面：",
    "Heavy drizzle": "大毛雨",
    "Heavy rain": "大雨",
    "Heavy showers": "大陣雨",
    "Heavy snow": "大雪",
    "Heavy snow showers": "大陣雪",
    "Heavy snowfall": "大降雪",
    "Heavy thunderstorm with hail": "夾雹大雷雨",
    "Hidden": "隱藏",
    "Hide from details": "在詳細資訊中隱藏",
    "Hide prefix icon": "隱藏前綴圖示",
    "High": "高",
    "High precision forecast provider. API key required below.":
        "高精度天氣預報供應商，請在下方填入 API 金鑰。",
    "Historical and forecast data provider. API key required below.":
        "歷史與預報資料供應商，請在下方填入 API 金鑰。",
    "Horizontal": "水平",
    "How often the rows scroll to reveal the next item":
        "列捲動以顯示下一個項目的頻率",
    "Humidity": "濕度",
    "Humidity:": "濕度：",

    # --- I ---
    "IP geolocation": "IP 地理定位",
    "Icon and temperature": "圖示與溫度",
    "Icon first": "圖示優先",
    "Icon only": "僅顯示圖示",
    "Icon size:": "圖示大小：",
    "Icon source:": "圖示來源：",
    "Icon theme:": "圖示主題：",
    "Icon:": "圖示：",
    "Icons": "圖示",
    "If you have just registered a new OpenWeatherMap API key, it might take up to 2 hours for it to become active. Please try again later if it doesn't work immediately.":
        "若您剛申請了新的 OpenWeatherMap API 金鑰，可能需要最多 2 小時才會生效。若立即使用無效，請稍後再試。",
    "If this looks correct, apply it. Otherwise, choose your location manually.":
        "若資訊正確，請套用；否則請手動選擇您的位置。",
    "Imperial (°F, mph, inHg, in)": "英制（°F、mph、inHg、in）",
    'In a vertical panel, long item labels may be truncated. Consider using \\"Simple\\" '
    "mode, increasing the panel width, or reducing the font size.":
        "在垂直面板中，較長的項目標籤可能被截斷。"
        "建議改用「簡易」模式、增加面板寬度或縮小字型大小。",
    "Individual units": "個別單位",
    "Instruction": "說明",
    "Interval:": "間隔：",
    "Invalid API key (HTTP %1)": "API 金鑰無效（HTTP %1）",
    "Invalid API key. Please check and try again.":
        "API 金鑰無效，請確認後重試。",
    "Invalid response": "無效的回應",
    "Invalid response from QWeather.": "QWeather 回應無效。",
    "Item spacing:": "項目間距：",
    "Item width:": "項目寬度：",
    "Items Order:": "項目順序：",

    # --- K ---
    "KDE Icon Theme": "KDE 圖示主題",
    "KDE Symbolic": "KDE 符號圖示",
    "KDE System Icons (automatic, follows weather code)":
        "KDE 系統圖示（自動，依天氣代碼）",
    'KDE icon themes don\'t fully support many item icons. You can set your own icons by clicking \\"Set your own icons\\".':
        "KDE 圖示主題不完全支援許多項目圖示，"
        "您可以點擊「設定自訂圖示」來自行設定。",
    "Keep Changes": "保留變更",
    "Keep the changes you made to Details Items?":
        "是否保留詳細資訊項目的變更？",
    "Keep the changes you made to Panel Items?":
        "是否保留面板項目的變更？",
    "Keep the changes you made to Tooltip Items?":
        "是否保留提示項目的變更？",
    "Keep widget open": "保持小工具開啟",
    "Knots (kn)": "節（kn）",
    "Kp Index": "Kp 指數",
    "Kp index/G forecast:": "Kp 指數/G 等級預報：",

    # --- L ---
    "Last Quarter": "下弦月",
    "Lat:": "緯度：",
    "Lat: %1°": "緯度：%1°",
    "Latitude": "緯度",
    "Latitude:": "緯度：",
    "Layout": "版面配置",
    "Light": "微量",
    "Layout type:": "版面類型：",
    "Light drizzle": "輕毛雨",
    "Light freezing drizzle": "輕凍毛雨",
    "Light freezing rain": "輕凍雨",
    "Light rain": "小雨",
    "Light rain / Drizzle (day)": "小雨/毛雨（白天）",
    "Light rain / Drizzle (night)": "小雨/毛雨（夜晚）",
    "Light showers": "小陣雨",
    "Light snow": "小雪",
    "Light snow (day)": "小雪（白天）",
    "Light snow (night)": "小雪（夜晚）",
    "Light snow showers": "小陣雪",
    "Lines:": "行數：",
    "List": "清單",
    "Loading radar…": "載入雷達中⋯",
    "Loading details…": "載入詳細資訊中⋯",
    "Loading forecast…": "載入預報中⋯",
    "Loading hourly data…": "載入逐時資料中⋯",
    "Loading locations…": "載入位置中⋯",
    "Location": "位置",
    "Location '%1' is already in your saved list. You can apply the selected location, but it will not be saved again.":
        "「%1」已在您的儲存清單中，您可套用此位置，但不會重複儲存。",
    "Location Name": "地點名稱",
    "Location auto-detected.": "位置已自動偵測。",
    "Location detection is depending on system configuration and permissions.":
        "位置偵測取決於系統設定與權限。",
    "Location is available on %1.": "位置在 %1 上可用。",
    "Location is not available on %1 (HTTP %2). Try a different provider or location.":
        "位置在 %1 上不可用（HTTP %2），請嘗試其他供應商或位置。",
    "Location name": "地點名稱",
    "Location name:": "地點名稱：",
    "Location package notice": "位置套件通知",
    "Location staged. Click the main Apply button to save.":
        "位置已暫存，點擊主套用按鈕以儲存。",
    "Location:": "位置：",
    "Lon:": "經度：",
    "Lon: %1°": "經度：%1°",
    "Longitude": "經度",
    "Longitude:": "經度：",
    "Looking up location…": "查詢位置中⋯",
    "Low": "低",

    # --- M ---
    "Magnetic Field (Bz)": "磁場（Bz）",
    "Main icon style:": "主圖示樣式：",
    "Mainly clear": "大致晴朗",
    "Mainly clear (day)": "大致晴朗（白天）",
    "Mainly clear (night)": "大致晴朗（夜晚）",
    "Manual": "手動",
    "Marine and weather data provider. API key required below.":
        "海洋與天氣資料供應商，請在下方填入 API 金鑰。",
    "Metric (°C, km/h, hPa, mm)": "公制（°C、km/h、hPa、mm）",
    "Mild symptoms in highly sensitive individuals.":
        "對花粉極度敏感者可能出現輕微症狀。",
    "Minimal to no risk.": "風險極低或無風險。",
    "Minimum height:": "最小高度：",
    "Minimum width:": "最小寬度：",
    "Minor geomagnetic storm.": "輕度地磁風暴。",
    "Misc": "其他",
    "Mod": "中量",
    "Mode:": "模式：",
    "Monday": "星期一",
    "Moderate": "中度",
    "Moderate drizzle": "中等毛雨",
    "Moderate geomagnetic storm.": "中度地磁風暴。",
    "Moderate rain": "中雨",
    "Moderate rain showers": "中等陣雨",
    "Moderate snowfall": "中等降雪",
    "Moon": "月亮",
    "Moon Phase": "月相",
    "Moon mode:": "月亮模式：",
    "Moon phase and moonrise/moonset": "月相與月出/月落",
    "Moon phase mode:": "月相模式：",
    "Moon phase only": "僅顯示月相",
    "Moon phase options": "月相選項",
    "Moon phase, moonrise & moonset": "月相、月出及月落",
    "Moon:": "月亮：",
    "Moonrise": "月出",
    "Moonrise & moonset only": "僅顯示月出與月落",
    "Moonrise icon:": "月出圖示：",
    "Moonrise only": "僅顯示月出",
    "Moonrise/Moonset": "月出/月落",
    "Moonrise:": "月出：",
    "Moonset": "月落",
    "Moonset icon:": "月落圖示：",
    "Moonset only": "僅顯示月落",
    "Moonset:": "月落：",
    "Most allergy sufferers will experience discomfort.":
        "多數過敏患者將感到不適。",
    "Morning": "上午",
    "Mugwort": "艾草",
    "Multiple lines (tall panel)": "多行（高面板）",

    # --- N ---
    "NOAA Kp index and geomagnetic activity": "NOAA Kp 指數與地磁活動",
    "NO₂": "NO₂",
    'Need the coordinates for a place? You can look them up at '
    '<a href=\\"https://www.mapcoordinates.net/\\">mapcoordinates.net</a>.':
        "需要查詢某地的座標？可至 "
        '<a href=\\"https://www.mapcoordinates.net/\\">mapcoordinates.net</a> 搜尋。',
    "Network error": "網路錯誤",
    "New Moon": "新月",
    "Night": "夜晚",
    "Nitrogen Dioxide (NO₂)": "二氧化氮（NO₂）",
    "No": "否",
    "No details data": "無詳細資訊資料",
    "No forecast data": "無預報資料",
    "No geomagnetic storm activity.": "無地磁風暴活動。",
    "No info": "無資料",
    "No information": "無資料",
    "No location set": "未設定位置",
    "No saved locations. Save the current location to quickly switch between places.":
        "尚無儲存的地點，儲存目前位置以便快速切換地點。",
    "No weather stations found for '%1'": "未找到「%1」的氣象站",
    "None": "無",
    "None Selected": "未選取",
    "Normal": "正常",
    "Not available (HTTP %1)": "無法使用（HTTP %1）",
    "Notifications": "通知",
    "Notify about upcoming rain/storms": "即將降雨/雷雨通知",
    "Notify with today's UV forecast": "今日紫外線指數預報通知",
    "Notify with today's forecast": "今日天氣預報通知",
    "Notify with today's geomagnetic activity forecast": "今日地磁活動預報通知",
    "Notify with tomorrow's forecast": "明日天氣預報通知",
    "Not tested": "未測試",
    "Note: size may be reduced if the panel is not thick enough.":
        "注意：若面板不夠厚，大小可能會縮減。",
    "Now: %1%2": "目前：%1%2",
    "Number of item rows visible at once. Resize the panel height in KDE settings to match.":
        "一次可見的項目列數，請在 KDE 設定中調整面板高度以配合。",

    # --- O ---
    "OK": "確定",
    "Olive": "橄欖",
    "Only the clicked day expands": "僅點擊的日期展開",
    "Open install guide": "開啟安裝指南",
    "Open radar in browser": "在瀏覽器中開啟雷達",
    "Opens today's hourly forecast automatically (or the next available day)": "自動展開今日逐時預報（或下一個可用日期）",
    "Open-Meteo (recommended, free)": "Open-Meteo（推薦，免費）",
    "OpenWeatherMap (Key Required)": "OpenWeatherMap（需要金鑰）",
    "OpenWeatherMap API Key:": "OpenWeatherMap API 金鑰：",
    "Options": "選項",
    "Orange": "橙色",
    "Overcast": "陰",
    "Ozone (O₃)": "臭氧（O₃）",
    "O₃": "O₃",

    # --- P ---
    "PM10": "PM10",
    "PM2.5": "PM2.5",
    "Panel": "面板",
    "Panel Items": "面板項目",
    "Panel display settings": "面板顯示設定",
    "Panel font:": "面板字型：",
    "Panel items settings": "面板項目設定",
    "Panel items:": "面板項目：",
    "Particulate Matter (PM10)": "懸浮微粒（PM10）",
    "Particulate Matter (PM2.5)": "細懸浮微粒（PM2.5）",
    "Partly cloudy": "多雲",
    "Partly cloudy (day)": "多雲（白天）",
    "Partly cloudy (night)": "多雲（夜晚）",
    "Pick an exact spot on the map for a more local forecast, such as your neighborhood block or a specific landmark.":
        "在地圖上選取精確位置以獲得更在地的預報，例如您所在的街區或特定地標。",
    "Phase + moonrise & moonset": "月相＋月出與月落",
    "Phase + upcoming rise/set": "月相＋即將月出/月落",
    "Pipe  |": "直線  |",
    "Pirate Weather (Key Required)": "Pirate Weather（需要金鑰）",
    "Pirate Weather API Key:": "Pirate Weather API 金鑰：",
    "Pollen": "花粉",
    "Pollen data not available for this location.": "此地點無花粉資料。",
    "Pollen options": "花粉選項",
    "Pollen:": "花粉：",
    "Poor": "差",
    "Pause": "暫停",
    "Play": "播放",
    "Postpone %1 min": "延後 %1 分鐘",
    "Precip sum:": "降水總量：",
    "Precip Sum": "降水總量",
    "Precip. Sum:": "降水總量：",
    "Preview: 20°C": "預覽：20°C",
    "Primary unit shown first (e.g. °C / °F)": "主要單位顯示在前（例如 °C / °F）",
    "Precipitation": "降水量",
    "Precipitation Sum": "降水總量",
    "Precipitation rate (mm/h)": "降水率（mm/h）",
    "Precipitation:": "降水量：",
    "Prefix style:": "前綴樣式：",
    "Pressure": "氣壓",
    "Pressure forecast:": "氣壓預報：",
    "Pressure:": "氣壓：",
    "Provider": "供應商",
    "Provider availability": "供應商可用性",
    "Provider website:": "供應商網站：",
    "Provider:": "供應商：",
    "Provider: %1": "供應商：%1",

    "Radar": "雷達",
    "Radar only": "僅顯示雷達",
    "Radar provider: <a href='https://www.rainviewer.com/'>Rain Viewer</a><br/><br/>The widget uses the free RainViewer API, which provides the past 2 hours of weather radar data in 10-minute intervals. Radar forecast is not supported.<br/><br/>Rain Viewer does not guarantee the availability of radar data. They do not conclude contracts with owners of this data. The reason is that the owners can ask them to remove their data from Rain Viewer, change the format, or stop sharing the data. They are trying to keep radar data for as long as possible, but sometimes the owners just stop providing the images.":
        "雷達資料來源：<a href='https://www.rainviewer.com/'>Rain Viewer</a><br/><br/>本小工具使用免費的 RainViewer API，提供過去 2 小時、每 10 分鐘間隔的氣象雷達資料。不支援雷達預報。<br/><br/>Rain Viewer 不保證雷達資料的可用性。他們不與資料擁有者簽訂合約，原因是擁有者可能隨時要求移除資料、更改格式或停止共享。他們會盡力維持雷達資料的持續供應，但有時擁有者會直接停止提供影像。",
    "Radar:": "雷達：",
    "Real-time": "即時",
    "Recent": "最近",
    "Region default": "地區預設",
    "Region default (long)": "地區預設（長格式）",
    "Region default (short)": "地區預設（短格式）",

    # --- Q ---
    "QWeather (Key Required)": "QWeather（需要金鑰）",
    "QWeather API Host:": "QWeather API 主機：",
    "QWeather API Key:": "QWeather API 金鑰：",
    "QWeather error (code %1). Check your API key.":
        "QWeather 錯誤（代碼 %1），請檢查您的 API 金鑰。",
    "QtLocation and QtPositioning are not installed": "未安裝 QtLocation 和 QtPositioning",
    "QtWebEngine is not installed": "未安裝 QtWebEngine",
    "Quiet": "平靜",

    # --- R ---
    "Ragweed": "豚草",
    "Rain": "雨",
    "Rain (day)": "雨（白天）",
    "Rain (night)": "雨（夜晚）",
    "Rain showers": "陣雨",
    "Rain/Storm": "降雨/雷雨",
    "Recommended - e.g. 560": "建議值 — 例如 560",
    "Red": "紅色",
    "Refresh": "重新整理",
    "Refresh weather automatically": "自動更新天氣",
    "Relative humidity %": "相對濕度 %",
    "Relative humidity percentage": "相對濕度百分比",
    "Reload radar": "重新載入雷達",
    "Remove last location?": "移除最後一個地點？",
    "Remove saved location": "移除已儲存的地點",
    "Rename location": "重新命名地點",
    "Repeat reminder every:": "重複提醒間隔：",
    "Requesting location via GeoClue2…": "透過 GeoClue2 請求位置⋯",
    "Requesting location… (%1)": "請求位置中⋯（%1）",
    "Reset": "重設",
    "Reset All to Defaults": "全部重設為預設值",
    "Reset to default": "重設為預設值",
    "Rime fog": "霧淞",
    "Round values:": "數值四捨五入：",

    # --- S ---
    "SO₂": "SO₂",
    "Saved locations": "已儲存的地點",
    "Shadow Color": "陰影顏色",
    "Shadow color:": "陰影顏色：",
    "Saturday": "星期六",
    "Secondary unit shown first (e.g. °F / °C)": "次要單位顯示在前（例如 °F / °C）",
    "Scroll animation:": "捲動動畫：",
    "Scroll interval (sec):": "捲動間隔（秒）：",
    "Search by city or place name. Results show the location name, region, and country, and are suitable for general city-level forecasts rather than exact street-level placement.":
        "依城市或地點名稱搜尋。結果顯示位置名稱、地區及國家，適合一般城市層級預報，而非精確的街道位置。",
    "Search Location": "搜尋位置",
    "Search a weather station to set your location":
        "搜尋氣象站以設定您的位置",
    "Search for a location or choose it on the map.":
        "搜尋位置或在地圖上選擇。",
    "Search location": "搜尋位置",
    "Search location…": "搜尋位置⋯",
    "Separator:": "分隔符號：",
    "Shadow intensity:": "陰影強度：",
    "Serious risk; avoid outdoor activities.": "嚴重風險，請避免戶外活動。",
    "Set <b>%1</b> as your default location?":
        "將 <b>%1</b> 設為預設地點？",
    "Set Location…": "設定位置⋯",
    "Set as default location": "設為預設地點",
    "Set as default?": "設為預設？",
    "Set your own icons…": "設定自訂圖示⋯",
    "Severe geomagnetic storm.": "嚴重地磁風暴。",
    "Severities:": "嚴重程度：",
    "Show Radar tab in widget": "在小工具中顯示雷達頁籤",
    "Show Today:": "顯示今天：",
    "Show both units:": "顯示兩種單位：",
    "Show in:": "顯示於：",
    "Show my location": "顯示我的位置",
    "Show / hide the prefix icon": "顯示/隱藏前綴圖示",
    "Show / hide the prefix icon on the panel": "在面板上顯示/隱藏前綴圖示",
    "Show in details": "在詳細資訊中顯示",
    "Show or hide this detail item": "顯示或隱藏此詳細資訊項目",
    "Show pollen types in expanded view:": "在展開檢視中顯示花粉類型：",
    "Show pollutants in expanded view:": "在展開檢視中顯示污染物：",
    "Show prefix icon": "顯示前綴圖示",
    "Show space weather items in expanded view:":
        "在展開檢視中顯示太空天氣項目：",
    "Show temperature unit:": "顯示溫度單位：",
    "Show update time and provider": "顯示更新時間與供應商",
    "Show/hide key": "顯示/隱藏金鑰",
    "Show:": "顯示：",
    "Showers": "陣雨",
    "Showing primary unit only": "僅顯示主要單位",
    "Showing ° only": "僅顯示 °",
    "Showing °C / °F after values": "在數值後顯示 °C / °F",
    "Shown": "已顯示",
    "Simple": "簡易",
    "Simple Mode Items": "簡易模式項目",
    "Simple Widget": "簡易小工具",
    "Simple chips:": "簡易標籤：",
    "Simple (icon + temperature)": "簡易（圖示＋溫度）",
    "Simple display mode settings": "簡易顯示模式設定",
    "Single line (all items at once)": "單行（同時顯示所有項目）",
    "Size:": "大小：",
    "Skipped - API key not configured": "已略過 — 未設定 API 金鑰",
    "Slight rain": "微雨",
    "Slight rain showers": "微陣雨",
    "Slight snow showers": "微陣雪",
    "Slight snowfall": "微量降雪",
    "Small circle  ⚬": "小圓圈  ⚬",
    "Stats items:": "統計標籤：",
    "Strip": "條帶",
    "Sunday": "星期日",
    "Snow": "雪",
    "Snow (day)": "雪（白天）",
    "Snow (night)": "雪（夜晚）",
    "Snow Cover": "積雪覆蓋",
    "Snow Cover:": "積雪覆蓋：",
    "Snow depth (cm/in)": "積雪深度（公分/英吋）",
    "Snow grains": "雪粒",
    "Snow showers": "陣雪",
    "Solar Wind": "太陽風",
    "Space": "太空",
    "Space Weather": "太空天氣",
    "Space Weather:": "太空天氣：",
    "Space weather options": "太空天氣選項",
    "Standard provider. API key required below.":
        "標準天氣供應商，請在下方填入 API 金鑰。",
    "Storm": "風暴",
    "StormGlass (Key Required)": "StormGlass（需要金鑰）",
    "StormGlass API Key:": "StormGlass API 金鑰：",
    "Strong": "強烈",
    "Strong geomagnetic storm.": "強烈地磁風暴。",
    "Sulfur Dioxide (SO₂)": "二氧化硫（SO₂）",
    "Sunrise / Sunset:": "日出/日落：",
    "Sunrise/sunset markers:": "日出/日落標記：",
    "Swap order:": "交換順序：",
    "Sun rise & set times": "日出與日落時間",
    "Sun times mode:": "日出日落模式：",
    "Sun times options": "日出日落選項",
    "Sunrise": "日出",
    "Sunrise and sunset times": "日出與日落時間",
    "Sunrise icon:": "日出圖示：",
    "Sunrise only": "僅顯示日出",
    "Sunrise only  07:17": "僅日出  07:17",
    "Sunrise/Sunset": "日出/日落",
    "Sunrise:": "日出：",
    "Sunset": "日落",
    "Sunset icon:": "日落圖示：",
    "Sunset only": "僅顯示日落",
    "Sunset only   18:03": "僅日落   18:03",
    "Sunset:": "日落：",
    "Switch location": "切換位置",
    "Symbolic": "符號圖示",
    "Symbolic (Bundled)": "符號圖示（內建）",
    "Symbolic (follows theme colour)": "符號圖示（跟隨主題色彩）",
    "System tray": "系統匣",
    "System tray display settings": "系統匣顯示設定",
    "System tray icon settings": "系統匣圖示設定",
    "System Tray Badge Background Color": "系統匣徽章背景顏色",
    "System location unavailable, trying IP geolocation…":
        "系統位置無法使用，嘗試 IP 地理定位⋯",

    # --- T ---
    "Temperature": "溫度",
    "Temperature Color": "溫度顏色",
    "Temperature color:": "溫度顏色：",
    "Temperature badge": "溫度徽章",
    "Temperature first": "溫度優先",
    "Temperature only": "僅顯示溫度",
    "Temperature shadow:": "溫度陰影：",
    "Temperature:": "溫度：",
    "The auto-detected location is already in your saved list.":
        "自動偵測到的位置已在您的儲存清單中。",
    "This location is already in your saved list.":
        "此位置已在您的儲存清單中。",
    "Time format:": "時間格式：",
    "Time:": "時間：",
    "To unlock additional map layers (Rain, Clouds, Temperature, Wind, Pressure): disable Adaptive mode from the 'Provider' tab, select OpenWeatherMap as your weather provider, and enter your API key above. When you are ready, you can enable Adaptive mode again.":
        "若要解鎖其他地圖圖層（雨量、雲層、溫度、風速、氣壓）：請在「供應商」分頁停用自適應模式，選擇 OpenWeatherMap 作為天氣供應商，並在上方填入 API 金鑰。完成後可再次啟用自適應模式。",
    "Test API Key": "測試 API 金鑰",
    "Test across providers": "測試所有供應商",
    "Testing connection…": "測試連線中⋯",
    "Testing…": "測試中⋯",
    "Text labels (Temperature, Wind…)": "文字標籤（溫度、風速⋯）",
    "Text will follow the system font and expand to fill the available space.":
        "文字將跟隨系統字型並展開以填滿可用空間。",
    "The Radar tab requires the QtWebEngine package, which is not installed on this system.":
        "雷達頁籤需要 QtWebEngine 套件，但此系統尚未安裝。",
    "The geomagnetic (Kp/G) forecast is only available up to 3 days ahead":
        "地磁（Kp/G）預報最多提供未來 3 天的資料",
    "The condition icon will automatically reflect the current weather using "
    "your KDE system icon theme. No customisation is needed.":
        "天氣狀況圖示將自動使用您的 KDE 系統圖示主題反映目前天氣，無需自訂。",
    "The map picker requires the QtLocation and QtPositioning packages, which are not installed on this system.":
        "地圖選取器需要 QtLocation 和 QtPositioning 套件，但此系統尚未安裝。",
    "Theme default": "主題預設",
    "Thunderstorm": "雷雨",
    "Thunderstorm (day)": "雷雨（白天）",
    "Thunderstorm (night)": "雷雨（夜晚）",
    "Thunderstorm with hail": "夾雹雷雨",
    "Thunderstorm with hail (day)": "夾雹雷雨（白天）",
    "Thunderstorm with hail (night)": "夾雹雷雨（夜晚）",
    "Thunderstorm, heavy hail (day)": "夾雹大雷雨（白天）",
    "Thunderstorm, heavy hail (night)": "夾雹大雷雨（夜晚）",
    "Timed out": "逾時",
    "Timezone:": "時區：",
    "Today": "今天",
    "Today's weather": "今日天氣",
    "Today's total precipitation (mm/in)": "今日累積降水量（mm/英吋）",
    "Tomorrow": "明天",
    "Tomorrow forecast": "明日預報",
    "Tonight": "今晚",
    "Tomorrow.io (Key Required)": "Tomorrow.io（需要金鑰）",
    "Tomorrow.io API Key:": "Tomorrow.io API 金鑰：",
    "Tooltip": "提示",
    "Tooltip Items": "提示項目",
    "Tooltip height:": "提示高度：",
    "Tooltip items": "提示項目",
    "Tooltip items settings": "提示項目設定",
    "Tooltip items:": "提示項目：",
    "Tooltip width:": "提示寬度：",
    "Tooltip:": "提示：",
    "Top Center": "上方置中",
    "Top Left": "左上",
    "Top Right": "右上",
    "Treat alert notifications as critical": "將警報通知設為重要通知",
    "Truncate (single line)": "截斷（單行）",

    # --- U ---
    "UV Index": "紫外線指數",
    "UV Index:": "紫外線指數：",
    "UV index": "紫外線指數",
    "UV index forecast:": "紫外線指數預報：",
    "UV will be %1 (%2)": "紫外線指數將達 %1（%2）",
    "Ultraviolet index": "紫外線指數",
    "Unable to detect location. All methods failed.":
        "無法偵測位置，所有方法均失敗。",
    "Unit preset:": "單位預設：",
    "Units": "單位",
    "Unknown": "未知",
    "Unknown location": "未知位置",
    "Unpin widget": "取消釘選小工具",
    "Unsettled": "不穩定",
    "Upcoming (auto)": "即將（自動）",
    "Upcoming (next sunrise or sunset)": "即將（下一次日出或日落）",
    "Upcoming rise/set only": "僅顯示即將的升降",
    "Update timed out. Click the refresh button to retry.": "更新逾時，請點擊重新整理按鈕重試。",
    "Updated %1": "已於 %1 更新",
    "Updating…": "更新中⋯",
    "Use 24-hour format:": "使用 24 小時制：",
    "Use region defaults": "使用地區預設",
    "Use KDE locale settings": "使用 KDE 語系設定",
    "Use manual location": "使用手動位置",
    "Uses KDE system icons by default. Click the button to customise each item's icon.":
        "預設使用 KDE 系統圖示，點擊按鈕以自訂各項目的圖示。",

    # --- V ---
    "V.Poor": "非常差",
    "Values are rounded to whole numbers": "數值四捨五入為整數",
    "Values show decimal places": "數值顯示小數位",
    "Vertical": "垂直",
    "Very High": "非常高",
    "Very Poor": "非常差",
    "Violent rain showers": "劇烈陣雨",
    "Visibility": "能見度",
    "Visibility distance": "能見距離",
    "Visibility:": "能見度：",
    "Visible tabs:": "可見頁籤：",
    "Visual Crossing (Key Required)": "Visual Crossing（需要金鑰）",
    "Visual Crossing API Key:": "Visual Crossing API 金鑰：",

    # --- W ---
    "Waning Crescent": "殘月",
    "Waning Gibbous": "虧凸月",
    "Waxing Crescent": "眉月",
    "Waxing Gibbous": "盈凸月",
    "We detected your coordinates: <b>%1°, %2°</b>.":
        "已偵測到您的座標：<b>%1°、%2°</b>。",
    "We detected your location as: <b>%1</b>.":
        "已偵測到您的位置為：<b>%1</b>。",
    "Weather Provider": "天氣供應商",
    "Weather Widget": "天氣小工具",
    "Weather alert": "天氣警報",
    "Weather alerts": "天氣警報",
    "Weather condition text": "天氣狀況文字",
    "Weather icon + condition text": "天氣圖示＋狀況文字",
    "Weather icon style:": "天氣圖示樣式：",
    "Weather icon theme:": "天氣圖示主題：",
    "Weather provider:": "天氣供應商：",
    "WeatherAPI.com (Key Required)": "WeatherAPI.com（需要金鑰）",
    "WeatherAPI.com API Key:": "WeatherAPI.com API 金鑰：",
    "Weatherbit (Key Required)": "Weatherbit（需要金鑰）",
    "Weatherbit API Key:": "Weatherbit API 金鑰：",
    "Website": "網站",
    "Widget": "小工具",
    "Widget Size": "小工具大小",
    "Widget panel area:": "小工具面板區域：",
    "Wind": "風",
    "Wind speed + direction": "風速＋風向",
    "Wind speed and direction": "風速與風向",
    "Wind speed:": "風速：",
    "Wind:": "風：",
    "Wrap to next line": "折行",

    'You can see date/time format reference at: <a href=\\"https://doc.qt.io/qt-6/qml-qtqml-qt.html#formatDateTime-method\\">Qt documentation</a>':
        '您可在以下位置查閱日期/時間格式參考：<a href=\\"https://doc.qt.io/qt-6/qml-qtqml-qt.html#formatDateTime-method\\">Qt 文件</a>',

    # --- X/Y/Z ---
    "X-ray Flare Class": "X 射線閃焰等級",
    "Yellow": "黃色",
    "Yes": "是",
    "Yes, remove it": "是，移除",
    "You may need to increase the widget's width to see all the selected information":
        "您可能需要增加小工具的寬度，以顯示所有已選取的資訊",
    "Zoom in": "放大",
    "Zoom out": "縮小",

    # --- lowercase / units ---
    "a decrease from yesterday": "較昨日減少",
    "a few clouds": "少雲",
    "an increase from yesterday": "較昨日增加",
    "clear skies": "晴空",
    "cloudy skies": "多雲",
    "drizzle": "毛毛雨",
    "e.g. Sofia, Bulgaria": "例如：保加利亞索非亞",
    "extreme": "極端",
    "feet": "英尺",
    "fog": "霧",
    "freezing rain": "凍雨",
    "from %1": "自 %1 起",
    "ft": "英尺",
    "high": "高",
    "in the next few hours": "未來數小時內",
    "left": "後日落",
    "low": "低",
    "m": "公尺",
    "met.no (free)": "met.no（免費）",
    "meters": "公尺",
    "minor": "輕微",
    "minutes": "分鐘",
    "moderate": "中度",
    "overcast skies": "陰天",
    "px": "px",
    "px height": "px 高度",
    "px width": "px 寬度",
    "quiet": "平靜",
    "rain": "雨",
    "severe": "嚴重",
    "showers": "陣雨",
    "showers and thunderstorms": "雷陣雨",
    "similar to yesterday": "與昨日相近",
    "snow": "雪",
    "snow showers": "陣雪",
    "strong": "強烈",
    "system location": "系統位置",
    "this afternoon": "今日下午",
    "this morning": "今日上午",
    "this night": "今夜",
    "thunderstorms": "雷雨",
    "until %1": "至 %1",
    "until dawn": "後日出",
    "very high": "非常高",
    "your location": "您的位置",

    # --- New in 1.7.0 template: alerts, radar, units ---
    "API error": "API 錯誤",
    "Alerts provider:": "警報供應商：",
    "Alerts provider: <a href='https://alerts.kde.org/'>FOSS Public Alert Server</a><br/><br/>KDE's FOSS Public Alert Server collects official severe-weather warnings in CAP format from agencies worldwide and matches them to your exact location. Alert notifications work the same as with the native provider.":
        "警報資料來源：<a href='https://alerts.kde.org/'>FOSS Public Alert Server</a><br/><br/>KDE 的 FOSS Public Alert Server 匯集全球各機構以 CAP 格式發布的官方劇烈天氣警報，並比對至您的確切位置。警報通知的運作方式與原生供應商相同。",
    "Alerts provider: <a href='https://librewxr.net/'>LibreWXR</a><br/><br/>LibreWXR is a free, open-source weather API that aggregates official CAP alerts worldwide (WMO Severe Weather Information Centre, NOAA NWS, and others) and matches them to your exact location. Alert notifications work the same as with the native provider.":
        "警報資料來源：<a href='https://librewxr.net/'>LibreWXR</a><br/><br/>LibreWXR 是一款免費、開源的天氣 API，匯集全球官方 CAP 警報（WMO 劇烈天氣資訊中心、NOAA NWS 等）並比對至您的確切位置。警報通知的運作方式與原生供應商相同。",
    "Alerts provider: <a href='https://www.meteoalarm.org/'>EUMETNET MeteoAlarm</a> + <a href='https://www.weather.gov/'>NOAA NWS</a><br/><br/>European locations use the official MeteoAlarm feeds (38 countries), US locations use the NOAA National Weather Service alerts API, with met.no MetAlerts as a fallback. If your weather provider delivers its own alerts (e.g. WeatherAPI.com, Pirate Weather), those are used directly.":
        "警報資料來源：<a href='https://www.meteoalarm.org/'>EUMETNET MeteoAlarm</a>＋<a href='https://www.weather.gov/'>NOAA NWS</a><br/><br/>歐洲地區使用官方 MeteoAlarm 警報（涵蓋 38 國），美國地區使用 NOAA 國家氣象局警報 API，並以 met.no MetAlerts 作為備援。若您的天氣供應商本身提供警報（例如 WeatherAPI.com、Pirate Weather），則直接使用其警報資料。",
    "Avalanche": "雪崩",
    "BBC Weather (free)": "BBC Weather（免費）",
    "Black and White": "黑白",
    "Coastal event": "沿海事件",
    "Connection failed": "連線失敗",
    "Dark map": "深色地圖",
    "EXTREME": "極端",
    "FOSS Public Alert Server": "FOSS Public Alert Server",
    "Flood": "洪水",
    "Forest fire": "森林火災",
    "Free BBC Weather service (data from the Met Office). No API key needed.":
        "免費的 BBC Weather 服務（資料來自 Met Office），無需 API 金鑰。",
    "Glow intensity:": "光暈強度：",
    "High temperature": "高溫",
    "Icon glow:": "圖示光暈：",
    "LibreWXR": "LibreWXR",
    "Loading frames": "載入影格中",
    "Loading frame…": "載入影格中⋯",
    "Loading…": "載入中⋯",
    "Low temperature": "低溫",
    "MINIMAL": "極輕微",
    "MINOR": "輕微",
    "MODERATE": "中度",
    "MeteoAlarm + NOAA NWS (Native)": "MeteoAlarm＋NOAA NWS（原生）",
    "No data": "無資料",
    "No radar data": "無雷達資料",
    "No satellite data": "無衛星資料",
    "Not supported": "不支援",
    "Notify about upcoming snow": "即將下雪時通知",
    "Per alert type:": "依警報類型：",
    "Postpone": "延後",
    "Purple": "紫色",
    "QWeather provides hourly forecasts for up to 168 hours (7 days). Daily forecast is still available for this date.":
        "QWeather 提供最長 168 小時（7 天）的逐時預報。此日期仍可查看每日預報。",
    "Radar + Satellite": "雷達＋衛星",
    "Radar color scheme:": "雷達色彩配置：",
    "Radar provider:": "雷達供應商：",
    "Radar provider: <a href='https://librewxr.net/'>LibreWXR</a><br/><br/>LibreWXR is a free, open-source weather radar API. It combines real radar composites from NOAA, Canadian, and European sources with a global model fallback, and provides the past 2 hours of radar data plus a short nowcast. It also offers a free satellite (infrared) layer.<br/><br/>Layer mode, radar color scheme, and motion arrows are selected directly in the Radar tab. The map follows your Plasma light/dark theme automatically.":
        "雷達資料來源：<a href='https://librewxr.net/'>LibreWXR</a><br/><br/>LibreWXR 是一款免費、開源的天氣雷達 API。它整合 NOAA、加拿大及歐洲的真實雷達合成資料，並以全球模式作為備援，提供過去 2 小時的雷達資料及短期即時預報，同時也提供免費的衛星（紅外線）圖層。<br/><br/>圖層模式、雷達色彩配置與移動箭頭可直接在「雷達」分頁中選擇。地圖會自動跟隨您的 Plasma 淺色/深色主題。",
    "Rain Viewer": "Rain Viewer",
    "Repeat reminder until dismissed": "重複提醒直到關閉為止",
    "SEVERE": "嚴重",
    "Satellite": "衛星",
    "Show precipitation motion arrows": "顯示降水移動箭頭",
    "Snow is ending": "降雪趨緩",
    "Snow is expected": "預計降雪",
    "Snow is expected to end %1.": "降雪預計於%1結束。",
    "Snow is possible %1.": "%1可能降雪。",
    "Snow/Ice": "降雪/結冰",
    "Thunderstorms": "雷雨",
    "UNKNOWN": "未知",
    "Updated just now": "剛剛更新",
    "Weather Alerts": "天氣警報",
    "Wind arrows": "風向箭頭",
    "Disable a type to silence it, or give it its own repeat interval. The interval is used only when 'Repeat reminder until dismissed' is on.":
        "停用某類型即可將其靜音，或個別設定其重複提醒間隔。此間隔僅在開啟「重複提醒直到關閉為止」時才會生效。",
    "Each alert is shown only once, without Dismiss and Postpone buttons.":
        "每則警報僅顯示一次，且不含「關閉」與「延後」按鈕。",
    "Switch between the light and dark map style. Until first toggled, the map follows the Plasma theme.":
        "切換地圖的淺色與深色樣式。在首次切換之前，地圖會跟隨 Plasma 主題。",

    # --- Units ---
    "cm": "公分",
    "grains/m³": "粒/立方公尺",
    "hPa": "百帕",
    "in": "英寸",
    "in/h": "英寸/小時",
    "inHg": "英寸汞柱",
    "km": "公里",
    "km/h": "公里/小時",
    "km/s": "公里/秒",
    "kn": "節",
    "m/s": "公尺/秒",
    "mg/m³": "毫克/立方公尺",
    "mi": "英里",
    "mm": "公釐",
    "mm/h": "公釐/小時",
    "mmHg": "毫米汞柱",
    "mph": "英里/小時",
    "tonight": "今晚",
    "µg/m³": "微克/立方公尺",

    # --- New in 1.7.1 template: GPU/Wayland workaround, map background, panel color ---
    "Active - GPU compositing is currently disabled for the radar map in this session.":
        "已生效──此工作階段的雷達地圖 GPU 合成功能已停用。",
    "Carto Dark Matter (dark)": "Carto Dark Matter（深色）",
    "Carto Positron (light)": "Carto Positron（淺色）",
    "Check Status": "檢查狀態",
    "Checking…": "檢查中⋯",
    "Color by temperature:": "依溫度上色：",
    "Color the panel temperature with the same cold to hot scale as the forecast curve, instead of a fixed color.":
        "面板溫度改用與預報曲線相同的冷熱漸層上色，而非固定顏色。",
    "CyclOSM (cycling)": "CyclOSM（自行車）",
    "Humanitarian (HOT)": "Humanitarian (HOT)",
    "Log Out Now…": "立即登出⋯",
    "Map background": "地圖底圖",
    "Not available: the selected base map already has a fixed light or dark style.":
        "無法使用：所選底圖本身已固定為淺色或深色樣式。",
    "OpenStreetMap (standard)": "OpenStreetMap（標準）",
    "OpenTopoMap (topographic)": "OpenTopoMap（地形）",
    "Saved, but not active yet - log out and back in for it to take effect.":
        "已儲存但尚未生效──登出再登入即可套用。",
    "The workaround script wasn't found on disk. Try toggling the option off and on again.":
        "找不到解決方案的指令碼檔案，請嘗試將選項關閉後再重新開啟。",
    "Workaround radar map crashes on hybrid-GPU systems (EXPERIMENTAL)":
        "解決混合 GPU 系統的雷達地圖當機問題（實驗性）",

    # --- New in 1.7.2 template: upcoming-alert heads-up, LibreWXR self-hosted server ---
    "<b>Starts:</b> %1": "<b>開始時間：</b>%1",
    "Geomagnetic activity is expected to be %1 (Kp %2)": "地磁活動預計為 %1（Kp %2）",
    "Large": "較大",
    "Leave this empty to use the public server. Set it to your own address if you run a self-hosted LibreWXR instance.":
        "留空以使用公用伺服器。若您自行架設 LibreWXR 執行個體，請填入其位址。",
    "LibreWXR server:": "LibreWXR 伺服器：",
    "Notify about upcoming alerts before they start": "警報即將生效前通知",
    "Sends a single, low-priority heads-up as soon as a future alert is published (e.g. \\\"Heat warning starts tomorrow at 11:00\\\"). The normal alert notification above still fires separately once it actually becomes active.":
        "只要有尚未生效的警報發布，就會立即傳送一則低優先順序的預先通知（例如：「高溫警報將於明天 11:00 生效」）。上方的一般警報通知仍會在警報實際生效時另外觸發。",
    "UV index will be %1 (%2)": "紫外線指數將達 %1（%2）",
    "Upcoming: %1": "即將生效：%1",
    "%1 there will be %2 with a low of %3 and a high of %4.": "%1天氣將為%2，低溫：%3，高溫：%4。",

    # --- New in 1.8.0 template: AEMET, AQI standards, alert sounds, icon theme sync, LibreWXR options ---
    "256 px": "256 px",
    "512 px": "512 px",
    "AEMET - Spain only (Key Required)": "AEMET（僅限西班牙，需要金鑰）",
    "AEMET API Key:": "AEMET API 金鑰：",
    "AEMET error (code %1). Check your API key.": "AEMET 錯誤（代碼 %1），請檢查您的 API 金鑰。",
    "AEMET only covers Spain - this location has no coverage.": "AEMET 僅涵蓋西班牙，此地點不在服務範圍內。",
    'AEMET only covers locations in Spain - other locations show \\"Failed\\" rather than switching provider (it\'s intentionally left out of Adaptive Mode too, since it\'s the one provider here with its own request limit). There is a limit on the number of requests to the AEMET API per minute, so don\'t click the refresh button too many times, as you may hit the limit and have to wait at least 1 minute before making another request.A failed request retries automatically once.<br/><br/>Fields AEMET doesn\'t publish at all - pressure, visibility, snow cover, and a daily accumulated precipitation total - show as \\"N/A\\" here rather than a bug. UV is a daily figure only, not hour-by-hour, and wind can be missing for days further out where AEMET\'s own forecast confidence drops off.<br/><br/>Free key: <a href=\'https://opendata.aemet.es/centrodedescargas/altaUsuario\'>opendata.aemet.es</a>. New keys expire 3 months after creation (AEMET\'s policy, changed July 2026) - you\'ll need to request a new one when that happens.<br/><br/>Please don\'t refresh too often, as AEMET has a request limit per minute. If you hit it, you\'ll have to wait at least 1 minute before making another request.':
        "AEMET 僅涵蓋西班牙境內的地點，其他地點會顯示「失敗」，而不會切換至其他供應商（AEMET 也刻意不納入自適應模式，因為它是這裡唯一有自身請求限制的供應商）。AEMET API 每分鐘的請求次數有上限，請勿頻繁點擊重新整理按鈕，否則可能達到上限，須等待至少 1 分鐘才能再次請求。請求失敗時會自動重試一次。<br/><br/>AEMET 完全未提供的欄位（大氣壓力、能見度、積雪覆蓋及每日累積降水量）在此會顯示為「N/A」，並非程式錯誤。UV 僅提供每日數值，沒有逐時資料；較遠日期的風況也可能因 AEMET 本身預報可信度下降而缺漏。<br/><br/>免費金鑰：<a href='https://opendata.aemet.es/centrodedescargas/altaUsuario'>opendata.aemet.es</a>。新金鑰在建立 3 個月後到期（AEMET 自 2026 年 7 月起的政策），屆時需重新申請。<br/><br/>請勿過於頻繁重新整理，AEMET 每分鐘有請求次數限制。若達到上限，須等待至少 1 分鐘才能再次請求。",
    "AEMET provides hourly forecasts for up to 48 hours. Daily forecast is still available for this date.":
        "AEMET 僅提供最多 48 小時的逐時預報，此日期仍可查看每日預報。",
    "AEMET: request failed - retrying automatically.": "AEMET：請求失敗，正在自動重試。",
    "AEMET: request limit reached - retrying automatically in a minute.": "AEMET：已達請求上限，將於一分鐘後自動重試。",
    "AEMET: request limit reached for the moment. This will retry automatically - please wait a minute.":
        "AEMET：目前已達請求上限，將自動重試，請稍候一分鐘。",
    "Air Quality index standard:": "空氣品質指標標準：",
    "Air quality is acceptable; there may be a risk for people unusually sensitive to air pollution.":
        "空氣品質尚可接受；對空氣污染特別敏感的族群可能有健康風險。",
    "Air quality is satisfactory, and air pollution poses little or no risk.":
        "空氣品質令人滿意，空氣污染幾乎不構成風險。",
    "Alert sound:": "警報音效：",
    "All files (*)": "所有檔案 (*)",
    "Already-passed hours are removed from today's hourly forecast": "從今日逐時預報中移除已過去的時段",
    "Already-passed hours for today stay in place, greyed out, instead of being removed":
        "今日已過去的時段保留並以灰色顯示，而不移除",
    "Animate the wind on the map (Open-Meteo)": "在地圖上以動畫顯示風場（Open-Meteo）",
    "Apply everywhere": "全部套用",
    "Apply icon theme": "套用圖示主題",
    "Apply only here": "僅套用於此處",
    "Arrows": "箭頭",
    "Audio files (*.wav *.ogg *.oga *.mp3 *.flac)": "音訊檔案 (*.wav *.ogg *.oga *.mp3 *.flac)",
    "Auto (device)": "自動（依裝置）",
    "Automatic (based on location)": "自動（依地點）",
    "Automatic uses US AQI worldwide, switching to European CAQI or Canadian AQHI based on your location's country.":
        "自動模式在全球使用美國 AQI，並依地點所在國家切換為歐洲 CAQI 或加拿大 AQHI。",
    "Avoid strenuous outdoor activities.": "避免從事劇烈戶外活動。",
    "Balanced (10 to 20 fps)": "平衡（10 至 20 fps）",
    "CAQI": "CAQI",
    "Canadian AQHI (1-10+)": "加拿大 AQHI（1-10+）",
    "Choose Alert Sound": "選擇警報音效",
    "Consider reducing or rescheduling strenuous outdoor activities if you experience symptoms such as coughing or throat irritation.":
        "若出現咳嗽或喉嚨不適等症狀，請考慮減少或改期進行劇烈戶外活動。",
    "Couldn't play that sound file: %1": "無法播放此音效檔：%1",
    "Default (built-in siren)": "預設（內建警報聲）",
    "Economy (8 to 10 fps)": "省電（8 至 10 fps）",
    "Enter your AEMET API key": "輸入您的 AEMET API 金鑰",
    "European CAQI (0-100+)": "歐洲 CAQI（0-100+）",
    "Everyone may begin to experience health effects; sensitive groups may experience more serious effects.":
        "所有人可能開始出現健康影響；敏感族群可能出現較嚴重的影響。",
    "Font icons": "字型圖示",
    "Format:": "格式：",
    "Hazardous": "危害",
    "Health alert: everyone may experience more serious health effects.": "健康警報：所有人可能出現較嚴重的健康影響。",
    "Health warning of emergency conditions: everyone is more likely to be affected.":
        "緊急狀況健康警告：所有人都更可能受到影響。",
    "High Risk": "高風險",
    "Highlight snow and wintry precipitation with a distinct color": "以不同顏色標示降雪及冬季降水",
    "Ideal air quality for outdoor activities.": "空氣品質適合戶外活動。",
    "Invalid response from AEMET.": "AEMET 回應無效。",
    "KDE Icon Theme (Colorful)": "KDE 圖示主題（彩色）",
    "KDE Icon Theme (Symbolic)": "KDE 圖示主題（符號）",
    "Low Risk": "低風險",
    "Members of sensitive groups may experience health effects; the general public is less likely to be affected.":
        "敏感族群可能出現健康影響；一般大眾較不易受影響。",
    "Meteocons (Bundled)": "Meteocons（內建）",
    "Moderate Risk": "中度風險",
    "N/A": "N/A",
    "Negative spacing pulls panel items closer together than their natural gap and can make icons or text overlap.":
        "負間距會讓面板項目比原本的間隔更靠近，可能導致圖示或文字重疊。",
    "Off - the workaround script has been removed, so it won't load on your next login. This session already started with GPU compositing disabled though, and your system isn't systemd-managed, so there's no way to clear that live - it stays disabled (including anything you open freshly in this session) until you log out and back in.":
        "已關閉──解決方案指令碼已移除，下次登入時不會再載入。不過此工作階段啟動時已停用 GPU 合成，且您的系統並非由 systemd 管理，因此無法即時清除該設定──在登出再登入之前都會維持停用（包括在此工作階段中新開啟的任何程式）。",
    "Off - the workaround script has been removed, so it won't load on your next login. This session already started with GPU compositing disabled though, so it stays that way (and anything already open, like a terminal, keeps showing the old value) until you log out and back in.":
        "已關閉──解決方案指令碼已移除，下次登入時不會再載入。不過此工作階段啟動時已停用 GPU 合成，因此在登出再登入之前都會維持此狀態（已開啟的程式，例如終端機，也會繼續顯示舊值）。",
    "Off - the workaround script has been removed, so it won't load on your next login. Your system uses systemd, so anything launched fresh from here on may already reflect the cleared value - but anything already open (like a terminal you still have up) keeps showing the old one regardless, and a full log out and back in is the only guaranteed way to clear it everywhere.":
        "已關閉──解決方案指令碼已移除，下次登入時不會再載入。您的系統使用 systemd，因此之後新啟動的程式可能已套用清除後的值；但已開啟的程式（例如仍開著的終端機）無論如何都會繼續顯示舊值，唯有完整登出再登入才能確保全面清除。",
    "Official Spanish meteorological agency - Spain locations only! API key required below.":
        "西班牙官方氣象機構，僅限西班牙地點！請在下方填入 API 金鑰。",
    "OpenFreeMap Dark": "OpenFreeMap Dark",
    "OpenFreeMap Fiord (dark)": "OpenFreeMap Fiord（深色）",
    "OpenFreeMap Liberty (light)": "OpenFreeMap Liberty（淺色）",
    "OpenFreeMap Positron (light)": "OpenFreeMap Positron（淺色）",
    "OpenStreetMap (dark)": "OpenStreetMap（深色）",
    "Overlay detected storm cells on the map": "在地圖上疊加偵測到的對流胞",
    "Palette:": "色彩配置：",
    "Panel › Icon theme": "面板 › 圖示主題",
    "Panel › Multi-line layout › Main icon style": "面板 › 多行版面 › 主圖示樣式",
    "Panel › Simple layout › Weather icon style": "面板 › 簡易版面 › 天氣圖示樣式",
    "Plays a sound alongside the notification for alerts of that severity. A switch greyed out here means that severity is turned off above, so it never notifies - with or without sound. By default only Red and Purple play a sound.":
        "針對該嚴重程度的警報，在通知時一併播放音效。此處呈灰色的開關，表示該嚴重程度已在上方關閉，因此不會發出通知（無論有無音效）。預設僅紅色與紫色會播放音效。",
    "Precip probability:": "降雨機率：",
    "Radar Settings": "雷達設定",
    "Read-only while Adaptive mode is on - turn it off above to choose a specific provider.":
        "自適應模式開啟時為唯讀，請在上方關閉後再選擇特定供應商。",
    "Reduce or reschedule strenuous outdoor activities, especially if you experience symptoms.":
        "請減少或改期進行劇烈戶外活動，尤其是出現症狀時。",
    "Settings where this theme is not available keep their current theme.": "不支援此主題的設定將保留目前的主題。",
    "Show WMO alerts on the map": "在地圖上顯示 WMO 警報",
    "Show air quality standards:": "顯示空氣品質標準：",
    "Show motion arrows on the map": "在地圖上顯示移動箭頭",
    "Show past weather info for today:": "顯示今日已過時段的天氣資訊：",
    "Show the wind at about 3000 m (700 hPa), the flow that steers the rain, instead of the surface wind at 10 m":
        "顯示約 3000 公尺高空（700 hPa）引導降雨移動的氣流，而非 10 公尺高的地面風",
    "Show tile options: smoothing, snow mask, format and tile size": "顯示圖磚選項：平滑化、降雪遮罩、格式及圖磚大小",
    "Smooth (12 to 30 fps)": "流暢（12 至 30 fps）",
    "Smooth radar tile edges": "平滑化雷達圖磚邊緣",
    "Smoothing": "平滑化",
    "Snow mask": "降雪遮罩",
    "Sounds:": "音效：",
    "Storm cells": "對流胞",
    "System tray › Icon theme": "系統匣 › 圖示主題",
    "System tray › Simple layout › Weather icon style": "系統匣 › 簡易版面 › 天氣圖示樣式",
    "Test": "測試",
    "The Radar tab can animate the wind as moving particles (switch it on there). The wind data comes from <a href='https://open-meteo.com/'>Open-Meteo</a>, independently of the LibreWXR server. This sets the frame rate: lower it on a slow computer, raise it if strong winds look jerky.":
        "雷達分頁可將風場以移動粒子的動畫呈現（請在該處開啟）。風場資料來自 <a href='https://open-meteo.com/'>Open-Meteo</a>，與 LibreWXR 伺服器無關。此處設定影格率：電腦效能較差時可調低，強風動畫不順暢時可調高。",
    "These settings only apply when the widget is placed in a panel or the system tray - they have no effect on the desktop.":
        "這些設定僅在小工具放置於面板或系統匣時套用，對桌面上的小工具無效。",
    "Tile size:": "圖磚大小：",
    "Tooltip › Icon theme": "提示 › 圖示主題",
    "Turn off all three switches above to pick a single standard here instead.": "關閉上方全部三個開關，即可改在此處選擇單一標準。",
    "Turn on any combination to show them side by side instead of a single standard below.":
        "開啟任意組合即可並列顯示，而非使用下方的單一標準。",
    "US AQI (0-500)": "美國 AQI（0-500）",
    "USG": "敏感族群不健康",
    "Unhealthy": "不健康",
    "Unhealthy for Sensitive Groups": "對敏感族群不健康",
    "V.High": "非常高",
    "V.Unhealthy": "非常不健康",
    "Very High Risk": "非常高風險",
    "Very Unhealthy": "非常不健康",
    "Weather Alerts Provider": "天氣警報供應商",
    "Widget › Details › Icon theme": "小工具 › 詳細資訊 › 圖示主題",
    "Widget › General › Weather icon theme": "小工具 › 一般 › 天氣圖示主題",
    "Wind animation:": "風場動畫：",
    "Winds": "風場",
    "Winds aloft": "高空風",
    "You selected <b>%1</b>. Apply it to every icon theme setting where it is available?":
        "您選擇了 <b>%1</b>，是否套用到所有支援此主題的圖示主題設定？",
    "already set": "已設定",
    "not available - left unchanged": "不支援，維持不變",
    "selected here": "於此處選取",
    "will be changed": "將變更",
    "Clouds: %1": "雲量：%1",
    # --- 1.9.0 additions ---
    "%1 %":
        "%1 %",
    "%1 %2 / 3 h":
        "%1 %2 / 3 小時",
    "%1 (Default)":
        "%1（預設）",
    "%1 GB":
        "%1 GB",
    "%1 MB":
        "%1 MB",
    "%1 ahead":
        "前進 %1",
    "%1 back":
        "後退 %1",
    "%1 h":
        "%1 小時",
    "%1 h %2":
        "%1 小時 %2 分",
    "%1 min":
        "%1 分鐘",
    "%1 of %2":
        "%1 / %2",
    "%1 per day":
        "每天 %1",
    "%1 px":
        "%1 px",
    "%1. Right-click to copy or paste it, drag it onto another level.":
        "%1。點擊右鍵可複製或貼上此顏色，或將它拖曳到其他級距。",
    "%1. Right-click to copy or paste it.":
        "%1。點擊右鍵可複製或貼上。",
    "%1/%2 · %3 fps":
        "%1/%2 · %3 fps",
    "%1: %2/%3":
        "%1：%2/%3",
    "%1: options":
        "%1：選項",
    "%1: request limit reached (HTTP %2) — trying again later":
        "%1：已達請求上限（HTTP %2），稍後重試",
    "%1: the API key was rejected (HTTP %2)":
        "%1：API 金鑰遭拒（HTTP %2）",
    "%1h":
        "%1 小時",
    "%1h %2m":
        "%1 小時 %2 分",
    "%1m":
        "%1 分",
    "0 h":
        "0 小時",
    "1 d":
        "1 天",
    "10 m":
        "10 公尺",
    "12 h":
        "12 小時",
    "12 hours back to now, every hour.":
        "過去 12 小時至現在，每小時一張。",
    "2 d":
        "2 天",
    "2 hours back to 1 hour ahead, every 10 minutes. It stays so when a longer range is set.":
        "過去 2 小時至未來 1 小時，每 10 分鐘一張。設定較長的時間範圍時仍維持如此。",
    "2 to 6 km: they often come before rain.":
        "2 至 6 公里：常出現在降雨之前。",
    "3 d":
        "3 天",
    "3 hours. In the range of the satellite one hour, in that of the radar 10 minutes, while they are on: the button shows it. It stops on their first and last image.":
        "預設每步 3 小時。開啟衛星或雷達時，在其涵蓋時段內分別為每步 1 小時與 10 分鐘，按鈕上會顯示步長。逐步切換會停在該圖層的第一張與最後一張影像。",
    "4 d":
        "4 天",
    "5 d":
        "5 天",
    "6 d":
        "6 天",
    "700 hPa":
        "700 hPa",
    "8 d":
        "8 天",
    ": ":
        "：",
    "A graph for each detail; point at a day to see its value in all of them":
        "每項資料各一張圖表；指向某一天即可在所有圖表中查看其數值",
    "A graph for each detail; point at an hour to see its value in all of them":
        "每項資料各一張圖表；指向某個小時即可在所有圖表中查看其數值",
    "A layer stops where its data stops.":
        "圖層會在其資料結束處停止。",
    "A palette has 2 to 12 colors.":
        "調色盤需有 2 至 12 種顏色。",
    "A southward field (negative Bz) lets the solar wind couple with Earth's magnetic field.":
        "磁場朝南（Bz 為負）時，太陽風能與地球磁場耦合。",
    "AEMET only covers Spain — choose another weather provider or a location in Spain.":
        "AEMET 僅涵蓋西班牙 — 請選擇其他天氣資料來源，或西班牙境內的地點。",
    "AOD":
        "AOD",
    "Add a color":
        "新增顏色",
    "Air %1":
        "氣溫 %1",
    "Air pressure brought to sea level, in hPa. Blue and purple: lows (clouds, rain, wind). Orange and red: highs (settled weather, fog in winter).":
        "換算至海平面的氣壓，單位為 hPa。藍色與紫色：低壓（雲、雨、風）。橙色與紅色：高壓（天氣穩定，冬季易起霧）。",
    "Air quality":
        "空氣品質",
    "Air quality (CAMS)":
        "空氣品質（CAMS）",
    "Air temperature at 2 m. Play a whole day: the land warms up in the afternoon and cools down at night, the sea hardly changes. A sharp edge that moves is a front.":
        "離地 2 公尺的氣溫。播放一整天：陸地午後增溫、夜間降溫，海面則幾乎不變。移動中的明顯交界就是鋒面。",
    "Albanian":
        "阿爾巴尼亞語",
    "Alert Language":
        "警報語言",
    "Alerts are shown in the language the issuing authority uses for your country.":
        "警報會以您所在國家發布機關所使用的語言顯示。",
    "All":
        "全部",
    "All clear":
        "無警報",
    "Also notify about routine test alerts":
        "也通知例行測試警報",
    "Animate the scenes of the expanded cards":
        "展開的卡片會播放場景動畫",
    "Animations:":
        "動畫：",
    "Another palette has this name.":
        "已有其他調色盤使用此名稱。",
    "Applies everywhere: panel, tooltip, widget header, Details, Forecast, Radar and History. Where space is tight (forecast and history lists, alerts), \\\"Region default (long)\\\" is shown in its short form.":
        "套用於所有位置：面板、提示、小工具標題、詳細資訊、預報、雷達與歷史。空間有限處（預報與歷史清單、警報）會以簡短形式顯示「地區預設（長格式）」。",
    "Arabic":
        "阿拉伯語",
    "At the bottom left of the map, small: the pictures loaded out of those of the range, and the pictures per second at most. Under them, the models: the global one, then the finer regional ones drawn over it in this view.":
        "地圖左下角的小字：已載入影像數 / 範圍內影像總數，以及每秒最多影像數。其下方為模型：先是全球模型，再於此視野中疊加其上的較精細區域模型。",
    "Atmosphere rim":
        "大氣邊緣光",
    "Average":
        "平均",
    "Back to now":
        "回到現在",
    "Basque":
        "巴斯克語",
    "Black":
        "黑色",
    "Blue":
        "藍色",
    "Blue-red":
        "藍紅",
    "Blur under the panels":
        "面板下方模糊",
    "Bosnian":
        "波士尼亞語",
    "Bottom":
        "底部",
    "Cache cleared.":
        "快取已清除。",
    "Calm":
        "無風",
    "Catalan":
        "加泰隆尼亞語",
    "Celestial bodies":
        "天體",
    "Chance of precip.":
        "降水機率",
    "Chance of precipitation":
        "降水機率",
    "Change over the last 3 hours, worked out from the readings the widget has collected. The open ring on the dial marks the pressure 3 hours ago.":
        "過去 3 小時的變化，根據小工具收集的讀數計算。錶盤上的空心圓環標示 3 小時前的氣壓。",
    "Change the color":
        "變更顏色",
    "Change the color (replaces the colors of the G scale)":
        "變更顏色（取代 G 等級的顏色）",
    "Change the colors":
        "變更顏色",
    "Change…":
        "變更⋯",
    "Choose the alert language for each saved location. If an alert is not published in that language, its native language is shown instead.":
        "為每個已儲存的地點選擇警報語言。若警報未以該語言發布，則改為顯示其原始語言。",
    "Choose the color of the graph":
        "選擇圖表顏色",
    "Choose the day":
        "選擇日期",
    "Clean style":
        "簡潔樣式",
    "Clear Cache":
        "清除快取",
    "Clearing…":
        "正在清除⋯",
    "Click":
        "點擊",
    "Click a day to show its hourly forecast. Double-click the graph to zoom in":
        "點擊某天可顯示其逐時預報。連點兩下圖表可放大",
    "Click on the icon":
        "點擊圖示",
    "Click to hide the hourly forecast":
        "點擊以隱藏逐時預報",
    "Click to show the hourly forecast":
        "點擊以顯示逐時預報",
    "Cloud cover":
        "雲量",
    "Coasts and borders":
        "海岸線與邊界",
    "Coasts and borders width":
        "海岸線與邊界寬度",
    "Cold":
        "寒冷",
    "Coldest night":
        "最冷的一夜",
    "Color":
        "顏色",
    "Color legend on the map":
        "在地圖上顯示色彩圖例",
    "Colors":
        "顏色",
    "Colors - %1":
        "顏色 - %1",
    "Comfortable":
        "舒適",
    "Compact":
        "精簡",
    "Cool":
        "涼爽",
    "Copy color":
        "複製顏色",
    "Could not reach Open-Meteo. Check your connection and try again.":
        "無法連線至 Open-Meteo。請檢查網路連線後再試一次。",
    "Croatian":
        "克羅埃西亞語",
    "Ctrl + / Ctrl −":
        "Ctrl + / Ctrl −",
    "Ctrl + double click":
        "Ctrl + 連點兩下",
    "Ctrl held over the map":
        "在地圖上按住 Ctrl",
    "Custom range…":
        "自訂範圍⋯",
    "Daily details":
        "每日詳細資料",
    "Daily graph order:":
        "每日圖表順序：",
    "Daily layout:":
        "每日版面配置：",
    "Data is available from %1 until yesterday.":
        "可查詢 %1 至昨天的資料。",
    "Date":
        "日期",
    "Date and Time":
        "日期與時間",
    "Date and time":
        "日期與時間",
    "Date and time formats are set in Misc → Date and Time.":
        "日期與時間格式可在「其他 → 日期與時間」中設定。",
    "Day and night":
        "晝夜",
    "Days":
        "日期清單",
    "Debug":
        "除錯",
    "Debug mode:":
        "除錯模式：",
    "Deep":
        "深",
    "Default colors and limits":
        "預設顏色與級距",
    "Default order":
        "預設順序",
    "Delete":
        "刪除",
    "Density":
        "密度",
    "Detailed log output is on":
        "已開啟詳細記錄輸出",
    "Detect location":
        "偵測位置",
    "Dew point":
        "露點",
    "Double click on the icon":
        "連點兩下圖示",
    "Double-click: radar range":
        "連點兩下：雷達時間範圍",
    "Double-click: satellite range":
        "連點兩下：衛星時間範圍",
    "Download the forecast layers in the background":
        "在背景下載預報圖層",
    "Drag to change the order of the tabs":
        "拖曳以變更分頁順序",
    "Drag to reorder the graphs, or use the edit button to change a color":
        "拖曳以重新排列圖表，或使用編輯按鈕變更顏色",
    "Dry":
        "乾燥",
    "Dust":
        "沙塵",
    "Dutch":
        "荷蘭語",
    "E":
        "東",
    "Each level must go higher than the one before.":
        "每個級距都必須高於前一個。",
    "Each new forecast run is downloaded as it comes out, so the map opens without waiting. Useful on a slow connection; it downloads even if you never open the map, so leave it off on a metered one.":
        "每次有新的預報模型結果發布就會立即下載，讓地圖開啟時不必等待。適合網路較慢時使用；即使您從未開啟地圖也會下載，因此使用計量付費網路時請保持關閉。",
    "Each temperature must be higher than the one before.":
        "每個溫度都必須高於前一個。",
    "Edit temperature palette":
        "編輯溫度調色盤",
    "Edit wind palette":
        "編輯風速調色盤",
    "Edit…":
        "編輯⋯",
    "Embedded radar paused":
        "內嵌雷達已暫停",
    "End":
        "End",
    "End date":
        "結束日期",
    "Esc":
        "Esc",
    "Every (hPa)":
        "間距（hPa）",
    "Extreme heat":
        "酷熱",
    "Failed: %1 — retrying…":
        "失敗：%1 — 正在重試⋯",
    "Falling":
        "下降",
    "Falling quickly":
        "快速下降",
    "Falling slowly":
        "緩慢下降",
    "Falling very rapidly":
        "急遽下降",
    "Feels like":
        "體感溫度",
    "Finnish":
        "芬蘭語",
    "First picture":
        "第一張影像",
    "Fold the layer column":
        "收合圖層欄",
    "Folded":
        "收合時",
    "Forecast layout:":
        "預報版面配置：",
    "Format":
        "格式",
    "Format and Tiles":
        "格式與圖磚",
    "Freezing":
        "嚴寒",
    "French":
        "法語",
    "Fresh breeze":
        "清風",
    "Full":
        "完整",
    "Full screen (F11)":
        "全螢幕（F11）",
    "Gale":
        "大風",
    "Galician":
        "加利西亞語",
    "Gentle breeze":
        "微風",
    "German":
        "德語",
    "Give the palette a name.":
        "請為調色盤命名。",
    "Globe":
        "地球儀",
    "Globe glow:":
        "地球光暈：",
    "Glow of the atmosphere around the globe (globe button on the map). Lower it if the day side looks washed out.":
        "地球周圍的大氣光暈（地圖上的地球按鈕）。若日間側看起來過白，請調低此值。",
    "Graphs":
        "圖表",
    "Graphs style:":
        "圖表樣式：",
    "Greek":
        "希臘語",
    "Green":
        "綠色",
    "Green dot":
        "綠點",
    "Grey-blue band":
        "灰藍色帶",
    "Gusts":
        "陣風",
    "H and L at the centers, followed from one picture to the next.":
        "高壓 H 與低壓 L 標示於中心位置，並逐張影像追蹤其移動。",
    "Half":
        "一半",
    "Header:":
        "標頭：",
    "Hebrew":
        "希伯來語",
    "Height":
        "高度",
    "High %1 · Low %2":
        "最高 %1 · 最低 %2",
    "Highs and lows":
        "高低氣壓中心",
    "Historical values are reanalysis data on a roughly 10 km grid, so they can differ from nearby station readings.":
        "歷史數值為約 10 公里網格的再分析資料，因此可能與鄰近測站的觀測值不同。",
    "History":
        "歷史",
    "History:":
        "歷史：",
    "Home":
        "Home",
    "Home / End":
        "Home / End",
    "Hot":
        "炎熱",
    "Hourly forecast for %1":
        "%1 的逐時預報",
    "Hourly graph order:":
        "逐時圖表順序：",
    "How dark the deep night is on the radar map when day and night are shown (button on the map).":
        "顯示晝夜時（地圖上的按鈕），雷達地圖上深夜區域的暗度。",
    "How far ahead":
        "向未來多遠",
    "How far back":
        "向過去多遠",
    "How to read the weather maps":
        "如何判讀天氣地圖",
    "Humid":
        "潮濕",
    "Hungarian":
        "匈牙利語",
    "Hurricane":
        "颶風",
    "Ice pellets":
        "冰珠",
    "In force until then: %1.":
        "Plasma 重新啟動前仍使用：%1。",
    "Interpolated pictures":
        "插補影像",
    "Irish":
        "愛爾蘭語",
    "Isobars":
        "等壓線",
    "Italian":
        "義大利語",
    "KDE Plasma was started with MangoHud injected into it. The overlay can crash the whole desktop shell when the web-based radar starts, so the radar was not loaded.":
        "KDE Plasma 啟動時被注入了 MangoHud。網頁式雷達啟動時，此疊加層可能導致整個桌面 shell 當掉，因此未載入雷達。",
    "Keys":
        "按鍵",
    "Kinds shown":
        "顯示的類型",
    "Kp index (G scale)":
        "Kp 指數（G 等級）",
    "Kp index/G":
        "Kp 指數/G",
    "Last 30 days":
        "過去 30 天",
    "Last 7 days":
        "過去 7 天",
    "Last 90 days":
        "過去 90 天",
    "Last month":
        "上個月",
    "Last picture":
        "最後一張影像",
    "Layers":
        "圖層",
    "Leave full screen (F11 or Esc)":
        "離開全螢幕（F11 或 Esc）",
    "Levels shown":
        "顯示的雲層",
    "Light air":
        "軟風",
    "Light breeze":
        "輕風",
    "Lightning":
        "閃電",
    "Lines":
        "線條",
    "Load embedded radar anyway":
        "仍要載入內嵌雷達",
    "Loading of the layers":
        "圖層載入狀態",
    "Location search by %1 · Map data © %2":
        "地點搜尋由 %1 提供 · 地圖資料 © %2",
    "Logs every API request (address without keys, HTTP status, time taken, size, what came back), the provider fallback chain, caches, timers and how long the widget needs to load everything. Every line starts with [Advanced Weather Widget - <component>].\\nView it with: journalctl --user -f | grep \\\"Advanced Weather Widget\\\". \\nPlease enable only when you experience issues with the widget.":
        "記錄每個 API 請求（不含金鑰的位址、HTTP 狀態、耗時、大小、回傳內容）、天氣來源備援鏈、快取、計時器，以及小工具載入所有資料所需的時間。每行皆以 [Advanced Weather Widget - <component>] 開頭。\n檢視方式：journalctl --user -f | grep \"Advanced Weather Widget\"。\n請僅在小工具發生問題時啟用。",
    "Loop (L)":
        "循環（L）",
    "Loop: off, stops at the end":
        "循環：關閉，播放到結尾即停止",
    "Loop: on":
        "循環：開啟",
    "Luxembourgish":
        "盧森堡語",
    "Macedonian":
        "馬其頓語",
    "Magenta band":
        "洋紅色帶",
    "Maltese":
        "馬爾他語",
    "Map Cache":
        "地圖快取",
    "Map controls:":
        "地圖控制項：",
    "Map icon theme:":
        "地圖圖示主題：",
    "Map tiles already seen stay on disk, so they are not downloaded a second time. A new size applies the next time Plasma starts.":
        "已看過的地圖圖磚會保留在磁碟上，不會重複下載。新的大小會在下次啟動 Plasma 時生效。",
    "Marks under the line":
        "時間軸下方的標記",
    "Maximum size:":
        "大小上限：",
    "Mean":
        "平均",
    "Mean temperature":
        "平均氣溫",
    "Medium":
        "中",
    "Mid":
        "中層",
    "Minor":
        "輕微",
    "Moderate breeze":
        "和風",
    "Mouse wheel":
        "滑鼠滾輪",
    "Muted":
        "柔和",
    "N":
        "北",
    "NE":
        "東北",
    "NW":
        "西北",
    "Native language of the alert (Default)":
        "警報原始語言（預設）",
    "Native language:":
        "原始語言：",
    "Near gale":
        "疾風",
    "New temperature palette":
        "新增溫度調色盤",
    "New wind palette":
        "新增風速調色盤",
    "New…":
        "新增⋯",
    "Next day":
        "下一天",
    "Next period":
        "下一段期間",
    "Night darkness:":
        "夜間暗度：",
    "Night lights":
        "夜間燈光",
    "Night lights density":
        "夜間燈光密度",
    "No active alerts":
        "目前無有效警報",
    "No data is available for this period yet. The most recent days can take up to about five days to appear.":
        "此期間尚無資料。最近幾天的資料最多可能需要約五天才會出現。",
    "No data yet":
        "尚無資料",
    "No snow":
        "無積雪",
    "No warnings in effect":
        "目前無生效中的警報",
    "Off":
        "關閉",
    "Off (warnings and errors are always logged)":
        "關閉（警告與錯誤一律會記錄）",
    "Off: no data-point dots are shown.":
        "關閉：不顯示資料點。",
    "One compact graph; point at a day to see all the other details":
        "單一精簡圖表；指向某一天即可查看其他所有細節",
    "One compact graph; point at an hour to see all the other details":
        "單一精簡圖表；指向某一小時即可查看其他所有細節",
    "One step ahead (→)":
        "前進一步（→）",
    "One step back (←)":
        "後退一步（←）",
    "Opacity: %1 %":
        "不透明度：%1 %",
    "Opacity: %1 % (Shift + wheel)":
        "不透明度：%1 %（Shift + 滾輪）",
    "Open":
        "展開時",
    "Open the layer column":
        "展開圖層欄",
    "Open-Meteo is rate limiting requests. Please try again in a little while.":
        "Open-Meteo 正在限制請求頻率。請稍後再試。",
    "Oppressive":
        "悶熱",
    "Options: right click":
        "選項：點擊右鍵",
    "Orange dot":
        "橘色圓點",
    "Orange warning":
        "橙色警報",
    "Order of the layers":
        "圖層順序",
    "Page Up / Page Down (or Ctrl + arrow)":
        "Page Up / Page Down（或 Ctrl + 方向鍵）",
    "Palette name":
        "調色盤名稱",
    "Panel opacity":
        "面板不透明度",
    "Paste color":
        "貼上顏色",
    "Peak %1":
        "峰值 %1",
    "Pictures loaded / pictures in the range<br>Pictures per second at most, set in the settings of the column":
        "已載入影像數 / 範圍內影像數<br>每秒最多影像數，可於圖層欄設定中調整",
    "Pictures per second":
        "每秒影像數",
    "Plasma theme":
        "Plasma 主題",
    "Play or pause":
        "播放或暫停",
    "Play or pause (Space)":
        "播放或暫停（空白鍵）",
    "Point at a day to see its details. Double-click the graph, or hold Ctrl and scroll the mouse wheel, to zoom in.":
        "指向某一天即可查看詳細資料。連點兩下圖表，或按住 Ctrl 並捲動滑鼠滾輪，即可放大。",
    "Pollutant":
        "污染物",
    "Precip sum":
        "降水總量",
    "Precipitation (rain, snow)":
        "降水（雨、雪）",
    "Precipitation hours":
        "降水時數",
    "Precipitation sum":
        "降水總量",
    "Prepare the radar in advance":
        "預先準備雷達",
    "Prepare widget in advance:":
        "預先準備小工具：",
    "Pressure tendency":
        "氣壓趨勢",
    "Preview:":
        "預覽：",
    "Previous day":
        "上一天",
    "Previous period":
        "上一段期間",
    "Quarter":
        "四分之一",
    "Rain and snow":
        "雨夾雪",
    "Range":
        "時間範圍",
    "Range limited to %1 days":
        "範圍上限為 %1 天",
    "Range limited to %1 days: if the chosen range is longer, the end date is set automatically (for example, start date %2 gives end date %3).":
        "範圍限制為 %1 天：若所選範圍較長，結束日期會自動設定（例如開始日期為 %2 時，結束日期為 %3）。",
    "Red warning":
        "紅色警報",
    "Regional models":
        "區域模型",
    "Relative humidity":
        "相對濕度",
    "Relative humidity at 2 m: how close the air is to being saturated. Brown: dry (under 30 %, fire risk). Sand and green: usual. Blue: near 100 % (fog, low clouds, rain). It goes up at night and down in the afternoon even when the air keeps the same water. For the water itself, see the dew point.":
        "2 公尺高度的相對濕度：空氣接近飽和的程度。棕色：乾燥（低於 30 %，有火災風險）。沙色與綠色：一般。藍色：接近 100 %（霧、低雲、降雨）。即使空氣中的水氣含量不變，濕度也會在夜間升高、午後降低。若要看水氣本身，請參考露點。",
    "Remove":
        "移除",
    "Resolution while playing":
        "播放時的解析度",
    "Restore":
        "還原縮放",
    "Right click on the icon":
        "在圖示上點擊右鍵",
    "Rising":
        "上升",
    "Rising quickly":
        "快速上升",
    "Rising slowly":
        "緩慢上升",
    "Rising very rapidly":
        "急遽上升",
    "Romansh":
        "羅曼什語",
    "Routine tests (for example \\\"Required Weekly Test\\\") are ignored: no notification and no sound.":
        "例行測試（例如「Required Weekly Test」）會被忽略：不顯示通知，也不播放音效。",
    "Routine tests (for example \\\"Required Weekly Test\\\") will show a notification, but never play an alert sound.":
        "例行測試（例如「Required Weekly Test」）會顯示通知，但絕不播放警報音效。",
    "S":
        "南",
    "SE":
        "東南",
    "SW":
        "西南",
    "Scottish Gaelic":
        "蘇格蘭蓋爾語",
    "Sea level pressure":
        "海平面氣壓",
    "Select a location to see its weather history":
        "選擇地點以查看其歷史天氣",
    "Select day":
        "選擇日期",
    "Select end date":
        "選擇結束日期",
    "Select start date":
        "選擇開始日期",
    "Separated":
        "分開",
    "Serbian":
        "塞爾維亞語",
    "Settings":
        "設定",
    "Settings: pictures per second, resolution while playing,<br>coasts and borders, Sun, Moon and night lights, dark map, see-through panels":
        "設定：每秒影像數、播放時的解析度、<br>海岸線與邊界、太陽、月亮與夜間燈光、深色地圖、半透明面板",
    "Shift + mouse wheel on the icon":
        "在圖示上按 Shift + 滑鼠滾輪",
    "Shortcuts":
        "快捷鍵",
    "Show dots for every day":
        "顯示每天的資料點",
    "Show dots for every hour":
        "顯示每小時的資料點",
    "Show in daily forecast:":
        "在每日預報中顯示：",
    "Show in forecast:":
        "在預報中顯示：",
    "Show in hourly forecast:":
        "在逐時預報中顯示：",
    "Single day…":
        "單日⋯",
    "Size":
        "大小",
    "Slider":
        "滑桿",
    "Slovak":
        "斯洛伐克語",
    "Slovenian":
        "斯洛維尼亞語",
    "Small":
        "小",
    "Smooth":
        "連續漸層",
    "Smooth (20 to 30 fps)":
        "流暢（20 至 30 fps）",
    "Snowfall":
        "降雪量",
    "Spanish":
        "西班牙語",
    "Speed":
        "速度",
    "Speed x%1":
        "速度 x%1",
    "Standard":
        "標準",
    "Start date":
        "開始日期",
    "Static scenes":
        "靜態場景",
    "Steady":
        "穩定",
    "Strong breeze":
        "強風",
    "Strong gale":
        "烈風",
    "Strongest gust":
        "最強陣風",
    "Strongest wind":
        "最強風速",
    "Sunshine":
        "日照",
    "Swedish":
        "瑞典語",
    "Tabs & Header Behavior":
        "分頁與標頭行為",
    "Tabs order:":
        "分頁順序：",
    "Tabs position:":
        "分頁位置：",
    "Temperature and chance of precip.":
        "溫度與降水機率",
    "Temperature bands:":
        "溫度色帶：",
    "Temperature color":
        "溫度顏色",
    "Temperature high":
        "最高溫度",
    "Temperature low":
        "最低溫度",
    "Temperature low/high":
        "最低/最高溫度",
    "Temperature opacity:":
        "溫度不透明度：",
    "Temperature palette:":
        "溫度調色盤：",
    "Tendency: collecting data":
        "趨勢：正在收集資料",
    "The CAMS forecast. The colors follow the European Air Quality Index: cyan good, green fair, yellow moderate, red poor, dark red very poor, purple extremely poor. The scale is logarithmic: each band covers a wider range than the one before.":
        "CAMS 預報。顏色依據歐洲空氣品質指數：青色為良好、綠色為尚可、黃色為中等、紅色為差、暗紅色為很差、紫色為極差。刻度為對數尺度：每個色階涵蓋的範圍都比前一個更寬。",
    "The Details, Forecast and History tabs are built in the background after startup and stay built when the widget is closed, so it opens at once. This uses more memory for the whole session, and the History tab loads its data at startup.":
        "「詳細資訊」、「預報」與「歷史」分頁會在啟動後於背景建構，並在小工具關閉後保持建構狀態，因此開啟時能立即顯示。這會讓整個工作階段多使用一些記憶體，且「歷史」分頁會在啟動時載入資料。",
    "The Radar tab opens at once on the most recent radar image, and the animation plays at once. It uses about 200 MB more memory: leave it off on a computer with little memory.":
        "「雷達」分頁會立即開啟並顯示最新的雷達影像，動畫也會立即播放。這會多使用約 200 MB 記憶體：記憶體不多的電腦請保持關閉。",
    "The cache is full: the oldest images make room for the new ones. If the map downloads areas it has already shown again, choose a larger size.":
        "快取已滿：最舊的影像會被新影像取代。若地圖重複下載已顯示過的區域，請選擇較大的大小。",
    "The cache will be cleared the next time the map opens.":
        "快取將在下次開啟地圖時清除。",
    "The chart needs the Qt Graphs or the KDE Quick Charts QML module.":
        "圖表需要 Qt Graphs 或 KDE Quick Charts QML 模組。",
    "The colored layers share the map, one at a time: temperature, pressure, humidity, dew point, air quality. The column lists the layers as they are stacked on the map, the top one first; the order is set with the button left of the settings. The wind always goes over the others.":
        "彩色圖層共用同一張地圖，一次只顯示一個：溫度、氣壓、濕度、露點、空氣品質。欄中依圖層在地圖上的堆疊順序由上而下列出；順序可用設定左側的按鈕調整。風永遠疊在其他圖層之上。",
    "The global model, then the finer regional<br>ones drawn over it in this view":
        "全球模型，再於此視野中<br>疊上更精細的區域模型",
    "The infrared picture of the clouds, from LibreWXR: the colder the top, the higher and whiter the cloud.":
        "來自 LibreWXR 的雲層紅外線影像：雲頂越冷，雲越高、越白。",
    "The isobars join the points of equal pressure. The wind blows almost along them, counterclockwise around a low in the northern hemisphere. The closer they are, the stronger the wind.":
        "等壓線連接氣壓相同的各點。風幾乎沿著等壓線吹，在北半球繞低壓逆時針旋轉。等壓線越密，風越強。",
    "The layer column":
        "圖層欄",
    "The line":
        "時間軸",
    "The lines flow with the wind, their color is the speed (the wind palette of the settings). By default: white when calm, green and blue for a breeze, yellow and orange for a strong wind, red and violet for a storm. Where the lines bunch up and turn, the weather changes.":
        "線條隨風流動，顏色代表風速（設定中的風速調色盤）。預設：無風為白色，微風為綠色與藍色，強風為黃色與橙色，風暴為紅色與紫色。線條聚集並轉向之處，天氣會有變化。",
    "The map could not be loaded. Check your internet connection.":
        "無法載入地圖。請檢查網路連線。",
    "The map needs QtWebEngine, which is not installed. You can still search for a location above.":
        "地圖需要 QtWebEngine，但尚未安裝。您仍可在上方搜尋地點。",
    "The map page needs WebGL, which this graphics setup does not offer.":
        "地圖頁面需要 WebGL，但目前的圖形環境不支援。",
    "The same keys in every language. They work while the Weather Map tab is shown.":
        "所有語言皆使用相同的按鍵。顯示天氣地圖分頁時有效。",
    "The temperature at which dew forms. It tells how much water the air really holds. Under 10 °C the air feels dry, at 13 to 16 °C you notice it, from 18 °C it is muggy, from 21 °C oppressive, from 24 °C tropical. When the night cools down to the dew point, dew or fog forms.":
        "水氣凝結成露的溫度，可看出空氣實際含有多少水氣。低於 10 °C 時空氣感覺乾燥，13 至 16 °C 時開始有感覺，18 °C 起悶濕，21 °C 起悶熱，24 °C 起如熱帶般濕熱。夜間降溫至露點時，就會形成露水或霧。",
    "The thin button on its left edge opens or folds it. The map stays where it is when the column opens over it.":
        "其左緣的細長按鈕可開啟或收合此欄。欄在地圖上方展開時，地圖位置不會移動。",
    "The two clocks: how far back and how far ahead":
        "兩個時鐘：向過去多遠、向未來多遠",
    "The weather maps cannot play here":
        "此處無法播放天氣地圖",
    "The whiter, the more of the sky is covered. With the three levels ticked you see the model's total cover, without counting twice the clouds over each other.":
        "越白代表天空被雲覆蓋得越多。勾選三個層次時，會顯示模型的總雲量，不會重複計算上下重疊的雲。",
    "The widget collects pressure readings as it updates; about an hour of readings is needed to work out the trend.":
        "小工具會在更新時蒐集氣壓讀數；約需一小時的讀數才能算出趨勢。",
    "The wind is drawn over the map, so over every layer wherever it is in this list: its place here orders the column of the tab only.":
        "風繪製於地圖之上，因此無論它在此清單中的位置為何，都會覆蓋所有圖層：它在此處的位置只決定分頁中欄的排列順序。",
    "Theme":
        "跟隨主題",
    "There are no saved locations yet. Save a location on the Location page to choose its alert language.":
        "尚無已儲存的地點。請在「位置」頁面儲存地點後，再選擇其警報語言。",
    "Thick":
        "粗",
    "Thin":
        "細",
    "This month":
        "本月",
    "This year":
        "今年",
    "Tiles":
        "圖磚",
    "Time":
        "時間",
    "Time line":
        "時間軸",
    "Tip: double-click the graph, or hold Ctrl and scroll the mouse wheel, to zoom in":
        "提示：連點兩下圖表，或按住 Ctrl 並捲動滑鼠滾輪，即可放大",
    "Top":
        "頂部",
    "Total":
        "總雲量",
    "Total: %1":
        "總計：%1",
    "Try again":
        "重試",
    "Turkish":
        "土耳其語",
    "UV":
        "UV",
    "Until":
        "直到",
    "Use the alert's native language":
        "使用警報的原始語言",
    "Use the built-in color":
        "使用內建顏色",
    "Use the built-in colors":
        "使用內建顏色",
    "Used:":
        "已使用：",
    "Values on the lines":
        "線上數值",
    "Very deep":
        "非常深",
    "Very high":
        "非常高",
    "Very humid":
        "非常潮濕",
    "Violent storm":
        "暴風",
    "Vivid":
        "鮮豔",
    "W":
        "西",
    "Warm":
        "溫暖",
    "Warmest day":
        "最熱的一天",
    "Warning":
        "警報",
    "Weather Map":
        "天氣地圖",
    "Weather Map (Bundled)":
        "天氣地圖（內建）",
    "Weather Maps":
        "天氣地圖",
    "Weather Maps / Radar":
        "天氣地圖 / 雷達",
    "Weather Maps / Radar is turned off, so these settings are read-only. Turn it on in Appearance › Widget › General › Visible tabs.":
        "天氣地圖 / 雷達已關閉，因此這些設定為唯讀。請於「外觀 › 小工具 › 一般 › 可見頁籤」中開啟。",
    "Weather history is unavailable (HTTP %1).":
        "無法取得歷史天氣資料（HTTP %1）。",
    "Weather maps":
        "天氣地圖",
    "WebP or PNG, 256 or 512 px. The satellite follows them too.":
        "WebP 或 PNG，256 或 512 px。衛星圖層也會套用相同設定。",
    "Welsh":
        "威爾斯語",
    "Wet snow":
        "濕雪",
    "Wettest day":
        "降水量最多的一天",
    "What falls in the three hours around the time shown, in mm/h. Rain goes from blue to green, yellow, red and magenta as it gets heavier; snow is lilac and violet; the dangerous kinds (ice) have colors of their own. Under 0.05 mm/h nothing is drawn.":
        "所示時間前後三小時內的降水強度，單位為 mm/h。降雨隨雨勢增強，由藍色依序變為綠色、黃色、紅色與洋紅色；降雪為淡紫色與紫羅蘭色；危險類型（冰）有各自的顏色。低於 0.05 mm/h 時不繪製。",
    "What the weather radars see falling, from LibreWXR. After now it is LibreWXR's nowcast, paler on the time line. In its range the time line slows down to its 10 minute steps.":
        "來自 LibreWXR 的天氣雷達所見降水。現在之後為 LibreWXR 的臨近預報，在時間軸上顏色較淡。在其時間範圍內，時間軸會放慢為 10 分鐘間隔。",
    "Wheel":
        "齒輪",
    "White":
        "白色",
    "Width":
        "寬度",
    "Width of the bands":
        "色帶寬度",
    "Wind color":
        "風速顏色",
    "Wind palette:":
        "風速調色盤：",
    "Yellow warning":
        "黃色警報",
    "Yesterday":
        "昨天",
    "Zoom in (or double-click the graph, or hold Ctrl and scroll the mouse wheel)":
        "放大（或連點兩下圖表，或按住 Ctrl 並捲動滑鼠滾輪）",
    "a click or a drag shows the picture under the pointer, and pauses.":
        "點擊或拖曳即可顯示指標下方的影像，並暫停播放。",
    "a picture straight from a forecast file.":
        "直接來自預報檔案的影像。",
    "a picture worked out between two files.":
        "由兩個檔案之間推算而得的影像。",
    "about 3000 m: the flow that carries the clouds and the rain, stronger and smoother. Only the global model is drawn: the regional models hold the 10 m wind only.":
        "約 3000 公尺：帶動雲與雨的氣流，更強也更平穩。僅繪製全球模型：區域模型僅提供 10 公尺風。",
    "about 7 days back to 5 days ahead. Further on the CAMS forecast stops and the pictures stay empty.":
        "約回溯 7 天至未來 5 天。再往後 CAMS 預報即停止，影像會是空白。",
    "about 7 days back to 6 days ahead.":
        "過去約 7 天至未來 6 天。",
    "above %1 %2":
        "高於 %1 %2",
    "above 6 km: thin veils of ice, the sun still gets through.":
        "6 公里以上：薄薄的冰晶雲幕，陽光仍可穿透。",
    "at":
        "於",
    "average":
        "平均",
    "back to now.":
        "回到現在。",
    "closes this panel, then leaves full screen.":
        "關閉此面板；再按一次則離開全螢幕。",
    "full screen on or off.":
        "開啟或關閉全螢幕。",
    "h":
        "小時",
    "how hazy the air is (smoke, dust).":
        "空氣的混濁程度（煙霧、沙塵）。",
    "how many degrees each color band covers.":
        "每個色帶涵蓋的度數。",
    "how the rain moves now. They are the same on every picture: they are not the wind of the time shown.":
        "雨目前的移動方式。每張影像都相同：並非所示時間的風。",
    "its options and its color legend, which can be hidden.":
        "其選項與可隱藏的色彩圖例。",
    "its options too.":
        "同樣開啟其選項。",
    "its options, at the left of the icon.":
        "其選項，位於圖示左側。",
    "lists the days of the range. The mouse wheel over the date goes to the next or previous day.":
        "列出範圍內的每一天。在日期上滾動滑鼠滾輪可切換至下一天或上一天。",
    "on the radar or the satellite: both at once.":
        "在雷達或衛星上：同時顯示兩者。",
    "on, the animation plays round again from the start; off, it stops on the last picture.":
        "開啟時，動畫會從頭重新播放；關閉時，停在最後一張影像。",
    "on, the finer models (about 2 km) are drawn over the global one where they cover the map: the valleys, the heights and the coasts come out. Off, only the global model (about 25 km) is read: about three times less to download there.":
        "開啟時，在較精細的模型（約 2 公里）涵蓋地圖之處，會疊繪在全球模型之上：山谷、高地與海岸的細節都能呈現。關閉時僅讀取全球模型（約 25 公里）：這些地區的下載量約減少為三分之一。",
    "on, the finer models (about 2 km: AROME, ICON-D2, HRRR...) are drawn over the global one where they cover the map: a truer wind in the mountains and along the coasts. Off, only the global model (about 25 km) is read: about three times less to download there. No effect at 700 hPa.":
        "開啟時，在較精細的模型（約 2 公里：AROME、ICON-D2、HRRR⋯）涵蓋地圖之處，會疊繪在全球模型之上：山區與海岸的風更為貼近實際。關閉時僅讀取全球模型（約 25 公里）：這些地區的下載量約減少為三分之一。對 700 hPa 無效。",
    "one per picture, colored once loaded, red when it failed.":
        "每張影像一個，載入後上色，失敗時為紅色。",
    "one step back or ahead, as the buttons of the time bar.":
        "如同時間列上的按鈕，後退或前進一步。",
    "opens the list of choices. It also gives the range of the radar or of the satellite, which stays when another layer is switched on.":
        "開啟選項清單。清單中也提供雷達或衛星的時間範圍，開啟其他圖層時此範圍會保留。",
    "play or pause.":
        "播放或暫停。",
    "rain, snow, wet snow, rain and snow, freezing rain, freezing drizzle, ice pellets.":
        "雨、雪、濕雪、雨夾雪、凍雨、凍毛毛雨、冰珠。",
    "scrolls the column.":
        "捲動圖層欄。",
    "shown":
        "顯示中",
    "snow in colors of its own.":
        "降雪以專屬顏色呈現。",
    "softens the edges of the rain.":
        "柔化降雨的邊緣。",
    "switch radar, satellite, wind, isobars, precipitation, clouds, temperature, pressure, humidity, dew point, air quality on or off.":
        "開啟或關閉雷達、衛星、風、等壓線、降水、雲、溫度、氣壓、濕度、露點、空氣品質。",
    "switches the isobars on or off.":
        "開啟或關閉等壓線。",
    "switches the layer on or off.":
        "開啟或關閉圖層。",
    "the Saharan dust.":
        "撒哈拉沙塵。",
    "the UV index of the day.":
        "當日的 UV 指數。",
    "the button left of the settings: drag a layer by its handle to stack it, the first one on top; its switch takes it out of the column or puts it back.":
        "設定左側的按鈕：拖曳圖層把手即可堆疊，第一個位於最上層；其開關可將圖層移出此欄或放回。",
    "the first or last picture.":
        "第一張或最後一張影像。",
    "the loop on or off.":
        "開啟或關閉循環播放。",
    "the next or previous choice, shown in a bubble while it changes.":
        "下一個或上一個選項，變更時會顯示於氣泡中。",
    "the next or previous speed, from the keyboard or the keypad.":
        "下一個或上一個速度，可用鍵盤或數字鍵盤。",
    "the next or previous speed.":
        "下一個或上一個速度。",
    "the next speed: x1, x2, x3, then x1 again.":
        "下一個速度：x1、x2、x3，再回到 x1。",
    "the opacity of the layer, from 0 to 100 %.":
        "圖層的不透明度，從 0 到 100%。",
    "the opacity, shown in a bubble while it changes and drawn as the bar under the icon.":
        "不透明度，變更時顯示於氣泡中，並繪製為圖示下方的長條。",
    "the palette of the radar.":
        "雷達的調色盤。",
    "the palettes of the widget settings, where they can be made and changed.":
        "小工具設定中的調色盤，可在該處建立與修改。",
    "the pollutants.":
        "污染物。",
    "the pressure between two lines: 2, 4 or 8 hPa. Zoomed in close, a line comes between two.":
        "兩條線之間的氣壓差：2、4 或 8 hPa。放大檢視時，兩條線之間會再多一條。",
    "the pressure written on the lines, in three sizes.":
        "標示在線上的氣壓值，有三種大小。",
    "the previous or next picture from a forecast file.":
        "預報檔案中的上一張或下一張影像。",
    "the radar alone, on its range. A click on the satellite then adds it. The same double click gives back the layers from before.":
        "僅顯示雷達，並改用雷達的時間範圍。此時點擊衛星即可加入衛星。再連點兩下即可還原先前的圖層。",
    "the range of the radar, paler for its nowcast.":
        "雷達的時間範圍，臨近預報部分顏色較淡。",
    "the range of the satellite.":
        "衛星的時間範圍。",
    "the recent strikes.":
        "近期的雷擊。",
    "the same steps.":
        "相同的步進。",
    "the satellite alone, on its range. A click on the radar then adds it.":
        "僅顯示衛星，並改用衛星的時間範圍。此時點擊雷達即可加入雷達。",
    "the storms tracked.":
        "追蹤中的雷暴。",
    "the theme's (white on a dark map, black on a light one) or a color of your choice.":
        "主題顏色（深色地圖為白色，淺色地圖為黑色）或您自選的顏色。",
    "the warnings in force.":
        "生效中的警報。",
    "the wind and the temperature under the pointer.":
        "指標所在位置的風與溫度。",
    "the wind you feel, shaped by the relief.":
        "您實際感受到的風，受地形影響。",
    "thin, normal or thick.":
        "細、一般或粗。",
    "under about 2 km: grey days, fog, drizzle.":
        "約 2 公里以下：陰天、霧、毛毛雨。",
    "up to":
        "至",
    "zoom in or out.":
        "放大或縮小。",
    "×%1":
        "×%1",
}

# Special multi-line entries keyed by a unique marker
MULTILINE = {
    "Individual dropdowns are editable only in Custom mode.":
        '""\n'
        '"各下拉選單只能在「自訂」模式下個別編輯。\\n"\n'
        '"其他預設模式會自動設定單位。"',
    "Install it for your distribution:\\n  •":
        '""\n'
        '"請為您的發行版安裝對應套件：\\n"\n'
        '"  • Fedora / RHEL / Arch: qt6-qtlocation\\n"\n'
        '"  • openSUSE: qt6-location\\n"\n'
        '"  • Debian / Kubuntu / KDE Neon: qml6-module-qtlocation 和 qml6-module-qtpositioning\\n"\n'
        '"\\n"\n'
        '"您仍可搜尋位置或手動輸入座標。自動偵測將改用 IP 備援繼續運作，但精確度可能較低，且不會隨移動即時更新。"',
    "Install it for your distribution:\\n-":
        '""\n'
        '"請為您的發行版安裝對應套件：\\n"\n'
        '"- Fedora / RHEL: qt6-qtwebengine\\n"\n'
        '"- openSUSE / Arch: qt6-webengine\\n"\n'
        '"- Debian / Kubuntu / KDE Neon: qml6-module-qtwebengine"',
    # Key covers the 3rd line so a future msgid change is reported instead of silently reusing a stale translation
    "Providers are tried in order until one succeeds:\\nOpen-Meteo  →  BBC Weather  →  met.no  →  Pirate Weather  →  Visual Crossing  →  Tomorrow.io  →  StormGlass  →  Weatherbit  →  QWeather  →  OpenWeatherMap  →  WeatherAPI.com\\n If you want to choose a specific provider":
        '""\n'
        '"依序嘗試各供應商，直到成功為止：\\n"\n'
        '"Open-Meteo  →  BBC Weather  →  met.no  →  Pirate Weather  →  Visual Crossing  →  Tomorrow.io  →  StormGlass  →  Weatherbit  →  QWeather  →  OpenWeatherMap  →  WeatherAPI.com\\n"\n'
        '"若要選擇特定供應商，請關閉自適應模式。\\n"\n'
        '"Open-Meteo 永遠優先嘗試——免費且無需 API 金鑰。AEMET 刻意不列入此清單，因為它僅涵蓋西班牙，不適合全球使用。"',
    "Weather-alert severity levels, from lowest to highest:":
        '""\n'
        '"天氣警報嚴重程度等級，由低至高：\\n"\n'
        '"\\n"\n'
        '"🟡 黃色 — 輕微：請留意天氣狀況。\\n"\n'
        '"🟠 橙色 — 中度：請做好準備。\\n"\n'
        '"🔴 紅色 — 嚴重：請採取行動。\\n"\n'
        '"🟣 紫色 — 極端：極度危險，請立即採取行動。\\n"\n'
        '"\\n"\n'
        '"關閉某等級即可停止接收該嚴重程度的警報通知。"',
    # Key reaches the sentence added in 1.8.0 so later msgid edits surface as untranslated
    "<b>Hybrid-GPU / NVIDIA PRIME + Wayland crash workaround</b><br/><br/>On some hybrid-GPU laptops running Wayland, the Radar tab's embedded browser view can crash the whole Plasma shell the moment it first paints, due to a driver-level conflict between the two GPUs. This option disables GPU-accelerated compositing inside that browser view to avoid it.<br/><br/>Only enable this if you're actually experiencing that crash - it costs some rendering performance on the radar map.<br/><br/><b>This needs a log out and back in to take effect</b>, since it has to be set before Plasma starts. It also applies to the whole session, so any other app that embeds a Chromium-based browser view will pick up the same setting. Turning it back off later needs the same log out/in to fully clear it too.":
        '""\n'
        '"<b>混合 GPU / NVIDIA PRIME + Wayland 當機解決方案</b><br/><br/>在部分執行 Wayland 的混合 GPU 筆電上，由於兩張 GPU 之間存在驅動程式層級的衝突，雷達分頁內嵌的瀏覽器畫面在首次繪製時可能導致整個 Plasma shell 當機。此選項會停用該瀏覽器畫面內的 GPU 加速合成功能，以避免這個問題。<br/><br/>只有在您實際遇到這個當機問題時才建議開啟──這會犧牲雷達地圖的一些繪圖效能。<br/><br/><b>此設定需要登出再登入才會生效</b>，因為必須在 Plasma 啟動前就設定好。此設定也會套用到整個工作階段，因此任何其他內嵌 Chromium 瀏覽器畫面的應用程式，都會套用相同設定。之後若要關閉，同樣需要登出再登入才能完全清除。\\n"\n'
        '"        <br/><br/>若啟用此選項，將會建立以下檔案：~/.config/plasma-workspace/env/advanced-weather-widget-radar-gpu-workaround.sh"',
}

# Obsolete entries (removed from template.pot); generated as #~ blocks at end of .po
# Format: list of (msgid_po_lines, msgstr_po_lines) — each is a list of raw PO quoted strings
OBSOLETE = [
    # Copied verbatim from upstream msgmerge output (main zh_TW.po, 1.9.0)
    (
        "\"12-hour format\"",
        "\"12 \u5c0f\u6642\u5236\"",
    ),
    (
        "\"12h\"",
        "\"12h\"",
    ),
    (
        "\"24-hour format\"",
        "\"24 \u5c0f\u6642\u5236\"",
    ),
    (
        "\"24h\"",
        "\"24h\"",
    ),
    (
        "\"256 px\"",
        "\"256 px\"",
    ),
    (
        "\"512 px\"",
        "\"512 px\"",
    ),
    (
        "\"All tabs\"",
        "\"\u6240\u6709\u9801\u7c64\"",
    ),
    (
        "\"Animate the wind on the map (Open-Meteo)\"",
        "\"\u5728\u5730\u5716\u4e0a\u4ee5\u52d5\u756b\u986f\u793a\u98a8\u5834\uff08Open-Meteo\uff09\"",
    ),
    (
        "\"Arrows\"",
        "\"\u7bad\u982d\"",
    ),
    (
        "\"Auto (device)\"",
        "\"\u81ea\u52d5\uff08\u4f9d\u88dd\u7f6e\uff09\"",
    ),
    (
        "\"Behavior\"",
        "\"\u884c\u70ba\"",
    ),
    (
        "\"Black and White\"",
        "\"\u9ed1\u767d\"",
    ),
    (
        "\"Date and time in header:\"",
        "\"\u6a19\u984c\u986f\u793a\u65e5\u671f\u8207\u6642\u9593\uff1a\"",
    ),
    (
        "\"Date:\"",
        "\"\u65e5\u671f\uff1a\"",
    ),
    (
        "\"Details only\"",
        "\"\u50c5\u986f\u793a\u8a73\u7d30\u8cc7\u8a0a\"",
    ),
    (
        "\"Forecast only\"",
        "\"\u50c5\u986f\u793a\u9810\u5831\"",
    ),
    (
        "\"Format:\"",
        "\"\u683c\u5f0f\uff1a\"",
    ),
    (
        "\"Future alerts\"",
        "\"\u672a\u4f86\u8b66\u5831\"",
    ),
    (
        "\"Highlight snow and wintry precipitation with a distinct color\"",
        "\"\u4ee5\u4e0d\u540c\u984f\u8272\u6a19\u793a\u964d\u96ea\u53ca\u51ac\u5b63\u964d\u6c34\"",
    ),
    (
        "\"Keep the radar loaded in the background\"",
        "\"\u5728\u80cc\u666f\u4fdd\u6301\u96f7\u9054\u5df2\u8f09\u5165\"",
    ),
    (
        "\"Kp index/G forecast:\"",
        "\"Kp \u6307\u6578/G \u7b49\u7d1a\u9810\u5831\uff1a\"",
    ),
    (
        "\"Overlay detected storm cells on the map\"",
        "\"\u5728\u5730\u5716\u4e0a\u758a\u52a0\u5075\u6e2c\u5230\u7684\u5c0d\u6d41\u80de\"",
    ),
    (
        "\"Palette:\"",
        "\"\u8272\u5f69\u914d\u7f6e\uff1a\"",
    ),
    (
        "\"Particle width:\"",
        "\"\u7c92\u5b50\u5bec\u5ea6\uff1a\"",
    ),
    (
        "\"Precip probability:\"",
        "\"\u964d\u96e8\u6a5f\u7387\uff1a\"",
    ),
    (
        "\"Precip sum:\"",
        "\"\u964d\u6c34\u7e3d\u91cf\uff1a\"",
    ),
    (
        "\"Pressure forecast:\"",
        "\"\u6c23\u58d3\u9810\u5831\uff1a\"",
    ),
    (
        "\"Radar + Satellite\"",
        "\"\u96f7\u9054\uff0b\u885b\u661f\"",
    ),
    (
        "\"Radar only\"",
        "\"\u50c5\u986f\u793a\u96f7\u9054\"",
    ),
    (
        "\"Show Radar tab in widget\"",
        "\"\u5728\u5c0f\u5de5\u5177\u4e2d\u986f\u793a\u96f7\u9054\u9801\u7c64\"",
    ),
    (
        "\"Show WMO alerts on the map\"",
        "\"\u5728\u5730\u5716\u4e0a\u986f\u793a WMO \u8b66\u5831\"",
    ),
    (
        "\"Show motion arrows on the map\"",
        "\"\u5728\u5730\u5716\u4e0a\u986f\u793a\u79fb\u52d5\u7bad\u982d\"",
    ),
    (
        "\"Show the wind at about 3000 m (700 hPa), the flow that steers the rain, instead of the surface wind at 10 m\"",
        "\"\u986f\u793a\u7d04 3000 \u516c\u5c3a\u9ad8\u7a7a\uff08700 hPa\uff09\u5f15\u5c0e\u964d\u96e8\u79fb\u52d5\u7684\u6c23\u6d41\uff0c\u800c\u975e 10 \u516c\u5c3a\u9ad8\u7684\u5730\u9762\u98a8\"",
    ),
    (
        "\"Show tile options: smoothing, snow mask, format and tile size\"",
        "\"\u986f\u793a\u5716\u78da\u9078\u9805\uff1a\u5e73\u6ed1\u5316\u3001\u964d\u96ea\u906e\u7f69\u3001\u683c\u5f0f\u53ca\u5716\u78da\u5927\u5c0f\"",
    ),
    (
        "\"Smooth radar tile edges\"",
        "\"\u5e73\u6ed1\u5316\u96f7\u9054\u5716\u78da\u908a\u7de3\"",
    ),
    (
        "\"Snow mask\"",
        "\"\u964d\u96ea\u906e\u7f69\"",
    ),
    (
        "\"The radar map is prepared in the background after login and stays ready while the popup is closed, so the Radar tab opens at once. It uses more memory and starts QtWebEngine with Plasma.\"",
        "\"\u96f7\u9054\u5730\u5716\u6703\u5728\u767b\u5165\u5f8c\u65bc\u80cc\u666f\u6e96\u5099\uff0c\u4e26\u5728\u5f48\u51fa\u8996\u7a97\u95dc\u9589\u6642\u4fdd\u6301\u5c31\u7dd2\uff0c\u56e0\u6b64\u96f7\u9054\u5206\u9801\u53ef\u7acb\u5373\u958b\u555f\u3002\u9019\u6703\u4f54\u7528\u8f03\u591a\u8a18\u61b6\u9ad4\uff0c\u4e26\u96a8 Plasma \u4e00\u8d77\u555f\u52d5 QtWebEngine\u3002\"",
    ),
    (
        "\"Tile size:\"",
        "\"\u5716\u78da\u5927\u5c0f\uff1a\"",
    ),
    (
        "\"UV index forecast:\"",
        "\"\u7d2b\u5916\u7dda\u6307\u6578\u9810\u5831\uff1a\"",
    ),
    (
        "\"Winds\"",
        "\"\u98a8\u5834\"",
    ),
    (
        "\"Winds aloft\"",
        "\"\u9ad8\u7a7a\u98a8\"",
    ),
    (
        "\"You may need to increase the widget's width to see all the selected information\"",
        "\"\u60a8\u53ef\u80fd\u9700\u8981\u589e\u52a0\u5c0f\u5de5\u5177\u7684\u5bec\u5ea6\uff0c\u4ee5\u986f\u793a\u6240\u6709\u5df2\u9078\u53d6\u7684\u8cc7\u8a0a\"",
    ),
    (
        "\"Update timed out. Click the refresh button to retry.\"",
        "\"\u66f4\u65b0\u903e\u6642\uff0c\u8acb\u9ede\u64ca\u91cd\u65b0\u6574\u7406\u6309\u9215\u91cd\u8a66\u3002\"",
    ),
    (
        "\"Smooth (12 to 30 fps)\"",
        "\"\u6d41\u66a2\uff0812 \u81f3 30 fps\uff09\"",
    ),
    (
        "\"\"\n\"<b>Hybrid-GPU / NVIDIA PRIME + Wayland crash workaround</b><br/><br/>On some hybrid-GPU laptops running Wayland, the Radar tab's embedded browser view can crash the whole Plasma shell the moment it first paints, due to a driver-level conflict between the two GPUs. This option disables GPU-accelerated compositing inside that browser view to avoid it.<br/><br/>Only enable this if you're actually experiencing that crash - it costs some rendering performance on the radar map.<br/><br/><b>This needs a log out and back in to take effect</b>, since it has to be set before Plasma starts. It also applies to the whole session, so any other app that embeds a Chromium-based browser view will pick up the same setting.\\n\"\n\"                <br/><br/>If you enable this option, the following file will be created in: ~/.config/plasma-workspace/env/advanced-weather-widget-radar-gpu-workaround.sh\"",
        "\"\"\n\"<b>\u6df7\u5408 GPU / NVIDIA PRIME + Wayland \u7576\u6a5f\u89e3\u6c7a\u65b9\u6848</b><br/><br/>\u5728\u90e8\u5206\u57f7\u884c Wayland \u7684\u6df7\u5408 GPU \u7b46\u96fb\u4e0a\uff0c\u7531\u65bc\u5169\u5f35 GPU \u4e4b\u9593\u5b58\u5728\u9a45\u52d5\u7a0b\u5f0f\u5c64\u7d1a\u7684\u885d\u7a81\uff0c\u96f7\u9054\u5206\u9801\u5167\u5d4c\u7684\u700f\u89bd\u5668\u756b\u9762\u5728\u9996\u6b21\u7e6a\u88fd\u6642\u53ef\u80fd\u5c0e\u81f4\u6574\u500b Plasma shell \u7576\u6a5f\u3002\u6b64\u9078\u9805\u6703\u505c\u7528\u8a72\u700f\u89bd\u5668\u756b\u9762\u5167\u7684 GPU \u52a0\u901f\u5408\u6210\u529f\u80fd\uff0c\u4ee5\u907f\u514d\u9019\u500b\u554f\u984c\u3002<br/><br/>\u53ea\u6709\u5728\u60a8\u5be6\u969b\u9047\u5230\u9019\u500b\u7576\u6a5f\u554f\u984c\u6642\u624d\u5efa\u8b70\u958b\u555f\u2500\u2500\u9019\u6703\u72a7\u7272\u96f7\u9054\u5730\u5716\u7684\u4e00\u4e9b\u7e6a\u5716\u6548\u80fd\u3002<br/><br/><b>\u6b64\u8a2d\u5b9a\u9700\u8981\u767b\u51fa\u518d\u767b\u5165\u624d\u6703\u751f\u6548</b>\uff0c\u56e0\u70ba\u5fc5\u9808\u5728 Plasma \u555f\u52d5\u524d\u5c31\u8a2d\u5b9a\u597d\u3002\u6b64\u8a2d\u5b9a\u4e5f\u6703\u5957\u7528\u5230\u6574\u500b\u5de5\u4f5c\u968e\u6bb5\uff0c\u56e0\u6b64\u4efb\u4f55\u5176\u4ed6\u5167\u5d4c Chromium \u700f\u89bd\u5668\u756b\u9762\u7684\u61c9\u7528\u7a0b\u5f0f\uff0c\u90fd\u6703\u5957\u7528\u76f8\u540c\u8a2d\u5b9a\u3002\\n\"\n\"                <br/><br/>\u82e5\u555f\u7528\u6b64\u9078\u9805\uff0c\u5c07\u6703\u5efa\u7acb\u4ee5\u4e0b\u6a94\u6848\uff1a~/.config/plasma-workspace/env/advanced-weather-widget-radar-gpu-workaround.sh\"",
    ),
    (
        "\"Colorful\"",
        "\"\u5f69\u8272\"",
    ),
    (
        "\"KDE Symbolic\"",
        "\"KDE \u7b26\u865f\u5716\u793a\"",
    ),
    (
        "\"\"\n\"Providers are tried in order until one succeeds:\\n\"\n\"Open-Meteo  \u2192  BBC Weather  \u2192  met.no  \u2192  Pirate Weather  \u2192  Visual Crossing  \u2192  Tomorrow.io  \u2192  StormGlass  \u2192  Weatherbit  \u2192  QWeather  \u2192  OpenWeatherMap  \u2192  WeatherAPI.com\\n\"\n\"Open-Meteo is always tried first - it is free and requires no API key.\"",
        "\"\"\n\"\u4f9d\u5e8f\u5617\u8a66\u5404\u4f9b\u61c9\u5546\uff0c\u76f4\u5230\u6210\u529f\u70ba\u6b62\uff1a\\n\"\n\"Open-Meteo  \u2192  BBC Weather  \u2192  met.no  \u2192  Pirate Weather  \u2192  Visual Crossing  \u2192  Tomorrow.io  \u2192  StormGlass  \u2192  Weatherbit  \u2192  QWeather  \u2192  OpenWeatherMap  \u2192  WeatherAPI.com\\n\"\n\"Open-Meteo \u6c38\u9060\u512a\u5148\u5617\u8a66--\u514d\u8cbb\u4e14\u7121\u9700 API \u91d1\u9470\u3002\"",
    ),
    (
        "\"Radar color scheme:\"",
        "\"\u96f7\u9054\u8272\u5f69\u914d\u7f6e\uff1a\"",
    ),
    (
        "\"Symbolic\"",
        "\"\u7b26\u865f\u5716\u793a\"",
    ),
    (
        "\"To unlock additional map layers (Rain, Clouds, Temperature, Wind, Pressure): disable Adaptive mode, select OpenWeatherMap as your weather provider, and enter your API key above. When you are ready, you can enable Adaptive mode again.\"",
        "\"\u82e5\u8981\u89e3\u9396\u5176\u4ed6\u5730\u5716\u5716\u5c64\uff08\u96e8\u91cf\u3001\u96f2\u5c64\u3001\u6eab\u5ea6\u3001\u98a8\u901f\u3001\u6c23\u58d3\uff09\uff1a\u8acb\u505c\u7528\u81ea\u9069\u61c9\u6a21\u5f0f\uff0c\u9078\u64c7 OpenWeatherMap \u4f5c\u70ba\u5929\u6c23\u4f9b\u61c9\u5546\uff0c\u4e26\u5728\u4e0a\u65b9\u586b\u5165 API \u91d1\u9470\u3002\u5b8c\u6210\u5f8c\u53ef\u518d\u6b21\u555f\u7528\u81ea\u9069\u61c9\u6a21\u5f0f\u3002\"",
    ),
    (
        "\"Update timed out. Tap to retry.\"",
        "\"\u66f4\u65b0\u903e\u6642\uff0c\u9ede\u64ca\u91cd\u8a66\u3002\"",
    ),
    (
        "\"%1 ending\"",
        "\"%1\u8da8\u7de9\"",
    ),
    (
        "\"%1 expected\"",
        "\"\u9810\u8a08\u6709%1\"",
    ),
    (
        "\"%1 expected to end %2.\"",
        "\"%1\u9810\u8a08\u65bc%2\u7d50\u675f\u3002\"",
    ),
    (
        "\"%1 possible %2.\"",
        "\"%2\u53ef\u80fd\u6709%1\u3002\"",
    ),
    (
        "\"Carto Dark Matter (dark)\"",
        "\"Carto Dark Matter\uff08\u6df1\u8272\uff09\"",
    ),
    (
        "\"Carto Positron (light)\"",
        "\"Carto Positron\uff08\u6dfa\u8272\uff09\"",
    ),
    (
        "\"Dash  -\"",
        "\"\u7834\u6298\u865f  -\"",
    ),
    (
        "\"Not supported\"",
        "\"\u4e0d\u652f\u63f4\"",
    ),
    (
        "\"Show precipitation motion arrows\"",
        "\"\u986f\u793a\u964d\u6c34\u79fb\u52d5\u7bad\u982d\"",
    ),
    (
        "\"Snow ending\"",
        "\"\u964d\u96ea\u8da8\u7de9\"",
    ),
    (
        "\"Snow expected\"",
        "\"\u9810\u8a08\u964d\u96ea\"",
    ),
    (
        "\"Snow expected to end %1.\"",
        "\"\u964d\u96ea\u9810\u8a08\u65bc %1 \u7d50\u675f\u3002\"",
    ),
    (
        "\"Snow possible %1.\"",
        "\"%1\u53ef\u80fd\u964d\u96ea\u3002\"",
    ),
    (
        "\"in the next hours\"",
        "\"\u5728\u672a\u4f86\u6578\u5c0f\u6642\u5167\"",
    ),
]

# Translations that depend on msgctxt: (msgctxt, msgid) -> msgstr.
# Only needed where one msgid has different meanings in different contexts;
# otherwise TRANSLATIONS (keyed by msgid alone) applies to every context.
CTX_TRANSLATIONS = {
    ("@label daily maximum temperature", "High"): "最高溫",
    ("@label daily minimum temperature", "Low"): "最低溫",
    ("@label no precipitation at that place", "Dry"): "無降水",
    ("isobar lines", "Normal"): "一般",
    ("text size", "Large"): "大",
}

# Plural entries (msgid_plural / msgstr[N]), keyed by the singular msgid.
# Chinese has no grammatical plural (nplurals=1), so only msgstr[0] is kept.
PLURAL = {
    "Updated %1 day ago": "%1 天前更新",
    "Updated %1 hour ago": "%1 小時前更新",
    "Updated %1 minute ago": "%1 分鐘前更新",
    "%1 day has no data yet": "%1 天尚無資料",
    "%1 snowy day": "%1 個降雪日",
    "%1 wet day": "%1 個降水日",
    "and %1 more alert": "還有 %1 則警報",
}


def extract_msgid_text(entry):
    """Extract the raw msgid value (without quotes) from an entry block."""
    lines = entry.split('\n')
    collecting = False
    parts = []
    for line in lines:
        if line.startswith('msgid '):
            val = line[6:]
            parts.append(val)
            collecting = True
        elif collecting:
            if line.startswith('"'):
                parts.append(line)
            else:
                break
    if not parts:
        return None
    # Join and strip outer quotes (multiline or single)
    joined = '\n'.join(parts)
    if joined == '""':
        return ''
    # Decode the PO string
    result = []
    for p in parts:
        # strip surrounding quotes
        inner = p[1:-1]  # remove leading " and trailing "
        result.append(inner)
    return ''.join(result)


def translate_entry(entry):
    """Return the entry with msgstr filled in."""
    raw_lines = entry.split('\n')

    # Find msgid text
    msgid_text = extract_msgid_text(entry)
    if msgid_text is None or msgid_text == '':
        return entry  # header or empty

    # Decode escape sequences for lookup
    decoded = msgid_text.replace('\\n', '\n').replace('\\"', '"')

    # Plural entries: msgid_plural / msgstr[N]. Only msgstr[0] is kept (nplurals=1).
    if any(line.startswith('msgstr[') for line in raw_lines):
        plural_translation = PLURAL.get(msgid_text)
        po_translation = (
            plural_translation.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            if plural_translation is not None else ''
        )
        # Always collapse to a single msgstr[0] slot (nplurals=1), translated or not,
        # to match the zh_CN/ja_JP convention rather than the pot's default 2-slot form.
        result = []
        for line in raw_lines:
            if line.startswith('msgstr[0]'):
                result.append(f'msgstr[0] "{po_translation}"')
            elif line.startswith('msgstr[1]'):
                continue
            else:
                result.append(line)
        return '\n'.join(result)

    # Look up in CTX_TRANSLATIONS first (same msgid, different msgctxt), then TRANSLATIONS
    _cm = next((l for l in raw_lines if l.startswith('msgctxt "')), None)
    ctx_text = _cm[9:-1] if _cm else None
    translation = CTX_TRANSLATIONS.get((ctx_text, msgid_text)) if ctx_text else None
    if translation is None:
        translation = TRANSLATIONS.get(msgid_text)

    # If not found, try MULTILINE by startswith match (supports duplicate first lines)
    if translation is None:
        ml_key = next((k for k in MULTILINE if msgid_text.startswith(k)), None)
        if ml_key in MULTILINE:
            # Use prebuilt multiline msgstr
            ml = MULTILINE[ml_key]
            result = []
            in_msgstr = False
            for line in raw_lines:
                if line.startswith('msgstr'):
                    result.append('msgstr ' + ml)
                    in_msgstr = True
                elif in_msgstr and line.startswith('"'):
                    pass  # skip old empty lines
                else:
                    if in_msgstr and not line.startswith('"'):
                        in_msgstr = False
                    result.append(line)
            return '\n'.join(result)

    if translation is None:
        return entry  # leave untranslated

    # Re-encode translation as PO string
    po_translation = translation.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

    # Replace msgstr "" with filled value
    result = []
    replaced = False
    for line in raw_lines:
        if not replaced and line == 'msgstr ""':
            result.append(f'msgstr "{po_translation}"')
            replaced = True
        else:
            result.append(line)
    return '\n'.join(result)


def _pot_creation_date():
    # Keep the date already in zh_TW.po (set upstream by msgmerge) so the header
    # stays untouched; fall back to template.pot only when there's no existing file.
    pat = r'"POT-Creation-Date: ([^\\]+)\\n"'
    if os.path.exists(_out):
        with open(_out, 'r', encoding='utf-8') as f:
            m = re.search(pat, f.read())
        if m:
            return m.group(1)
    m = re.search(pat, content)
    return m.group(1) if m else 'YEAR-MO-DA HO:MI+ZONE'

def _revision_date():
    tz_8 = timezone(timedelta(hours=8))
    return datetime.now(tz_8).strftime('%Y-%m-%d %H:%M+0800')

def build_header():
    return (
        '# Advanced Weather Widget - Traditional Chinese (zh_TW) translation\n'
        '# Copyright (C) 2026\n'
        '# This file is distributed under the same license as the Advanced Weather Widget package.\n'
        '# Yo , 2026.\n'
        '#\n'
        '#, fuzzy\n'
        'msgid ""\n'
        'msgstr ""\n'
        '"Project-Id-Version: Advanced Weather Widget\\n"\n'
        '"Report-Msgid-Bugs-To: https://github.com/pnedyalkov91/advanced-weather-widget/issues\\n"\n'
        f'"POT-Creation-Date: {_pot_creation_date()}\\n"\n'
        f'"PO-Revision-Date: {_revision_date()}\\n"\n'
        '"Last-Translator: Yo\\n"\n'
        '"Language-Team: \\n"\n'
        '"Language: zh_TW\\n"\n'
        '"MIME-Version: 1.0\\n"\n'
        '"Content-Type: text/plain; charset=UTF-8\\n"\n'
        '"Content-Transfer-Encoding: 8bit\\n"\n'
        '"Plural-Forms: nplurals=1; plural=0;\\n"'
    )


raw_entries = re.split(r'\n\n+', content.strip())

translated = [build_header()]
untranslated = []

for i, entry in enumerate(raw_entries[1:], 1):
    msgid_text = extract_msgid_text(entry)
    if msgid_text == '':
        continue  # skip original header
    result = translate_entry(entry)
    translated.append(result)
    # Track untranslated
    # Flag as untranslated only if msgstr "" is NOT followed by a continuation line
    if re.search(r'msgstr ""(?:\n(?!")|$)', result) and msgid_text:
        untranslated.append((i, msgid_text[:60]))

output = '\n\n'.join(translated) + '\n'

# Append obsolete entries as #~ blocks
if OBSOLETE:
    obsolete_lines = []
    _active = {extract_msgid_text(e) for e in raw_entries[1:]}
    for msgid_po, msgstr_po in OBSOLETE:
        # skip entries that upstream has since re-activated in template.pot
        if msgid_po.startswith('"') and msgid_po.endswith('"') and '\n' not in msgid_po \
                and msgid_po[1:-1] in _active:
            continue
        for line in ('msgid ' + msgid_po).split('\n'):
            obsolete_lines.append('#~ ' + line)
        for line in ('msgstr ' + msgstr_po).split('\n'):
            obsolete_lines.append('#~ ' + line)
        obsolete_lines.append('')
    output += '\n' + '\n'.join(obsolete_lines)

with open(_out, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Written: {len(translated)} entries")
print(f"Untranslated: {len(untranslated)}")
if untranslated:
    for idx, text in untranslated[:20]:
        print(f"  [{idx}] {text}")
