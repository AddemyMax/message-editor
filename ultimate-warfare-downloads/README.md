# Ultimate Warfare 0.1.25 — Цементавр

[Скачать полный комплект 0.1.25](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.25-source.zip).

Новый юнит обычного Китая: корпус/ходовая ядерной пушки, башня и боевые параметры обычного Повелителя. Модели объединяются при сборке из установленной игры, включая соседнюю папку Generals; сохраняются штатные материалы, UV и текстуры. Готовых моделей EA в исходном ZIP нет. Здоровье, броня, оружие, AI башни, физика, локомоторы, цена и время выпуска берутся у Повелителя; габариты столкновений — от ядерной пушки. Отдельных надстроек Повелителя пока нет, обычные боевые улучшения сохранены. Нужен Центр пропаганды. Новая кнопка использует иконку Повелителя; при заполненном заводе Лунма остаётся в ячейке 15, Цементавр получает 16. Исходные команды сохраняются. На CSF имя «Цементавр», для Latin-1 STR — Cementaur.

Распакуйте комплект в отдельную папку. Если скачивание через ссылку неудобно, откройте PowerShell в папке, куда хотите распаковать новый комплект, и выполните:

```powershell
$kitZip = Join-Path $env:TEMP "UltimateWarfare-0.1.25-source.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.25-source.zip" -OutFile $kitZip -ErrorAction Stop
Expand-Archive -LiteralPath $kitZip -DestinationPath "." -ErrorAction Stop
Set-Location ".\UltimateWarfare-0.1.25"
```

Из корня новой папки UltimateWarfare-0.1.25:

```powershell
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-cementaur-0.1.25.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-cementaur-0.1.25.big"
}
```

Начните новый Skirmish за обычный Китай. Постройте завод и Центр пропаганды, поставьте рядом ядерную пушку, Повелителя и Цементавра. Проверьте корпус, текстуры, посадку башни, выезд, ходовую, поворот башни и стрельбу. Сборка использует неподвижную исходную позу W3D, без развёртывания. Отдельная повреждённая модель пока не собирается; эффекты/обломки смерти остаются от Повелителя. Подробный план — docs/first-run.md.

169 автоматических тестов пройдено. Проверены rigid/skin-геометрия, отдельная иерархия, точки выстрела, колесные привязки, сохранение параметров, ячейки 15/16 и обнаружение изменения исходных моделей. Извлечённый ZIP собирает и проверяет синтетический BIG. Сравнение с 0.1.24 на одинаковых входных данных: прежние модели, текстуры и определения Лунмы/Tumbler байт-в-байт сохранены; старые выходные файлы меняются только добавлением команд и подписей. Реальных моделей игры и Windows Zero Hour в облаке нет: внешний вид, исходная поза и игровой запуск Цементавра ещё не проверены.

Нужны Windows, установленная Zero Hour 1.04 и Python 3.10+. Blender не требуется. Файлы установки не изменяются. BIG и manifest не перезаписываются; для повторной сборки задайте другое имя -Output и тот же путь -Archive. Старые версии сохранены. Коммерческие ресурсы и частный BIG не публикуются.

SHA256 ZIP: `bc9e1d7b3b03d9ff57410fdb2545063b47c2a5ce1143806d22d726e8a72bf899`
