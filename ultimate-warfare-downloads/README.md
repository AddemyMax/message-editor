# Ultimate Warfare 0.1.23 — сохранение оружия Повелителя

[Скачать полный комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.23-source.zip). Дизайн и ресурсы остаются от 0.1.21: [спереди](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-0.1.21-preview.png), [сзади](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-0.1.21-rear-preview.png).

Исправлено предположение о свободных SECONDARY/TERTIARY у исходного танка. Все занятые слоты, их оружие, предпочтения и условия ветеранов сохраняются. Миниган выбирает общий свободный дополнительный слот и получает соответствующие AI/Draw-привязки. Если свободного слота совсем нет, сборщик сохраняет исходное оружие и выдаёт его раскладку для диагностики.

Дым теперь отдельная OCLSpecialPower: локальный таймер 30 с, временное оружие через OCL/FireWeapon, без занятия слота в WeaponSet. Прежние граната, облако на 8 с, радиус 60 и подавление только врагов сохранены. Полная оригинальная SpecialPower.ini читается из игры и дополняется в частном BIG; глобальные способности и таймеры не заменяются. Укажите ближайшую точку до 180: OCL-кнопка не ведёт машину к далёкой цели и может потратить таймер вне дальности. Нативные дальность, вылет гранаты, маскировку и перезарядку нужно проверить.

Здоровье, броня, исходные пушки, скорость, физика, размер, цена, время производства, модель и Longma не менялись. Исправление DeliveryDecal из 0.1.22 включено. Один дополнительный tumbler_systems.py исправил воспроизведённую ошибку занятых слотов в извлечённой 0.1.21 с обновлённым парсером на авторском источнике; BIG собран и проверен. На настоящей установке сборку ещё нужно повторить.

Для текущей 0.1.21 можно загрузить оба исправления из её корня:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/ini-parser-0.1.22.py" -OutFile ".\tools\uwmod\ini.py" -ErrorAction Stop
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-systems-0.1.23.py" -OutFile ".\tools\uwmod\tumbler_systems.py" -ErrorAction Stop
```

Или распакуйте полный комплект отдельно и откройте PowerShell в UltimateWarfare-0.1.23. Сборка/запуск:

```powershell
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir
}
```

Новый Skirmish за обычные США, завод и Центр стратегии. Проверьте исходные пушки, миниган на пехоте, дым вблизи машины, независимые таймеры двух машин и маскировку. Генералы и автоматическое производство AI не расширены. Нужны также повреждение/уничтожение, сохранение/загрузка, FPS и регрессии кампаний/AI.

161 тест прошёл на авторских синтетических данных. Игровая проверка новой схемы ещё не выполнена. Нужны Zero Hour 1.04, Windows и Python 3.10+; Blender для сборки не нужен. Все изображения — Blender-рендеры, не игровые снимки.

SHA256 ZIP: `a3cd3513a367412f96f49c22d6553bfd0045e5131b5873c2a6580f3e1f39226e`

В ZIP нет игры, её текстур/конфигураций, чужих моделей или частного BIG. Исходные игровые файлы не изменяются. Код/документация MIT, авторские геометрия/пиксели CC0-1.0 в пределах прав автора; права на фильм и названия у правообладателей. Старые файлы сохранены.
