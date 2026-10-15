# Ultimate Warfare 0.1.30 — единая тяжёлая броня Бэтмобиля

Вместо умножения исходных сопротивлений назначается единый коэффициент боевого урона 5% для DEFAULT и всех явно заданных боевых типов во всех ArmorSet Tumbler. Это 95% снижение входящего обычного боевого урона, включая SMALL_ARMS/GATTLING, снаряды, ракеты, взрывы, огонь и другие типы. Различия исходного урона/скорострельности оружия сохраняются; одинаков коэффициент защиты. Здоровье, ракеты, миниган, основные пушки, дым, скорость и цена прежние. Лечение/STATUS и служебные типы сохраняют исходные коэффициенты; прямой скриптовый урон, обходящий броню движка, по-прежнему её обходит. Остальные юниты не правятся.

[Полный комплект 0.1.30](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.30-source.zip). Для вашей текущей 0.1.28/29 из корня мода:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-rockets-0.1.30.py" -OutFile ".\tools\uwmod\tumbler_rockets.py" -ErrorAction Stop
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-armor-0.1.30.json" -OutFile ".\content\units\tumbler.json" -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.30.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.30.big"
}
```

После запуска нового BIG начните новый Skirmish и сравните попадания пулемёта Humvee, китайского Gattling, танковых пушек и ракет. Не переносите старые сохранения для первого сравнения. Модель и ракеты прежние.

186 автоматических тестов пройдены, включая исходную уязвимость SMALL_ARMS=300%/GATTLING=180%, нормализуемую до 5%, все наборы брони и сохранение здоровья. На извлечённой 0.1.28 замена только двух файлов собирает корректный синтетический BIG без DEFAULT в исходной броне. Полный 0.1.30 ZIP даёт тот же BIG. Игровой результат новой брони ещё не проверен в Windows. Режим множителя поддерживается для старых манифестов без armor_damage_percent.

SHA256 ZIP: `e986dd5ea1dce5be8b4854173c01ec9e52123e1fb947f9c442c5411790902c35`.

## Предыдущие обновления

# Ultimate Warfare 0.1.29 — исправление необязательного DEFAULT брони

В 0.1.28 сборщик ошибочно требовал DEFAULT в каждой исходной таблице брони. В SAGE это необязательное поле: ArmorTemplate начинает со 100% для всех типов. Исправление следует этому правилу, учитывает порядок DEFAULT/повторных переопределений и сохраняет специальные воздействия/лечение при усилении боевой брони втрое. Ракетная установка, модели и другие параметры не менялись. Переустановка игры не требуется.

[Полный комплект 0.1.29](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.29-source.zip). Для текущей папки 0.1.28 достаточно одного файла:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-rockets-0.1.29.py" -OutFile ".\tools\uwmod\tumbler_rockets.py" -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.29.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.29.big"
}
```

183 теста пройдены, включая отсутствие DEFAULT, пустую броню и порядок сбросов/переопределений. На извлечённой 0.1.28 воспроизведена исходная ошибка, затем замена единственного модуля позволила собрать и проверить синтетический BIG. Полный ZIP 0.1.29 также собирается на этих входных данных. Оригинальные таблицы брони остаются неизменными; усиление применяется только к частным таблицам Tumbler. Native-сборка/игровой запуск на установке пользователя после исправления ещё не проверены.

SHA256 ZIP: `cf15759f0ab78a3a104a8ba1830ac733b3fa95d5027a0c2dba906a752104ba0d`.

## Предыдущее обновление

# Ultimate Warfare 0.1.28 — Бэтмобиль: броня ×3 и кормовые ракеты

[Скачать полный комплект 0.1.28](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.28-source.zip). [Рендер авторской модели сзади](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-rockets-0.1.28-rear.png) — Blender, не снимок SAGE.

Боевая броня Tumbler усилена втрое: новые частные Armor снижают получаемый боевой урон до 1/3 прежнего, здоровье остаётся прежним. Лечение, STATUS и служебные воздействия сохраняют старые коэффициенты. Основные пушки, миниган, дым, скорость, цена, время производства и прочие юниты сохранены.

Сзади — четыре небольшие ракеты на отдельной поворотной установке. Урон, снаряд и эффекты взяты по ссылкам из локального обычного дополнительного оружия Scorpion. Дальность 360, залп 4, интервал 250 мс, перезарядка 12 с. Установка доступна сразу и автоматически ищет наземные цели; не занимает три оружейных слота машины и не требует новой кнопки. Визуальные ракеты связаны с боезапасом. Атаки установки раскрывают маскировку. Родительская команда атаки может вести машину ближе, на дальность основных пушек; дальность ракет проверяйте на остановленной машине. Автоматический выбор целей установки независим от пушек.

Распакуйте комплект отдельно в UltimateWarfare-0.1.28. Если ссылку скачать неудобно, выполните в PowerShell в папке, где хотите получить новый комплект:

```powershell
$kitZip = Join-Path $env:TEMP "UltimateWarfare-0.1.28-source.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.28-source.zip" -OutFile $kitZip -ErrorAction Stop
Expand-Archive -LiteralPath $kitZip -DestinationPath "." -ErrorAction Stop
Set-Location ".\UltimateWarfare-0.1.28"
```

Затем из новой папки:

```powershell
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir
}
```

Начните новый Skirmish за обычные США, постройте завод и Центр стратегии. Проверьте крепление установки, четыре выстрела, исчезновение/возврат ракет при перезарядке, раскрытие/возврат маскировки, повреждения и уничтожение носителя. Подробный план — docs/first-run.md. Игровая проверка 0.1.28 на Windows ещё не выполнена.

180 тестов прошли. Проверены коэффициенты брони, сохранение здоровья и специальных воздействий, занятых слотов оружия, источника Scorpion и полная связь установки/моделей/боезапаса. Все четыре авторские W3D проходят геометрические проверки. Извлечённый ZIP собирает синтетический BIG и проходит preflight. Сравнение с 0.1.27 подтвердило неизменность китайских юнитов, интерфейса, дыма и Tumbler-текстуры; основные 11 мешей машины побайтно прежние, добавлена точка крепления и отдельная ракетная W3D. Native-выход с завода, поиск целей, стрельба, сохранения, смерть, AI/campaign/FPS требуют проверки в игре.

Требуются Windows, Zero Hour 1.04 и Python 3.10+. Blender для сборки не нужен. Исходные файлы игры не меняются; старые рабочие BIG сохраняются в прежних папках. Коммерческие ресурсы не включены в ZIP. Исправления Цементавра 0.1.26/27 включены.

SHA256 ZIP: `93358d30469c1e906ad8cbe872768642688eab7c300e26a36f2bce9dbfec9022`.

## Предыдущие обновления

# Ultimate Warfare 0.1.27 — убрать лишнее ядерное орудие Цементавра

Пользовательский отчёт подтвердил: материалы и UV исходных моделей сохранены, но транспортное ядерное орудие состоит из дополнительных веток вне `TURRET01`. В сборку попадали `TURRETFRONT`, `TURRETBACK`, `GUNBARREL`, `LIFTERS`, `ELEVATIONBARREL`; они накладывались на установленную башню Повелителя. Исправление удаляет обе дополнительные ветки оружия, сохраняя корпус, ходовую, опоры и башню Повелителя с исходными материалами/UV. Характеристики и остальные юниты не меняются.

[Полный комплект 0.1.27](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.27-source.zip). Для существующей папки 0.1.25 с уже исправленным именем ядерной пушки или 0.1.26 замените только файл сборщика:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/kitbash-0.1.27.py" -OutFile ".\tools\uwmod\kitbash.py" -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-cementaur-0.1.27.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-cementaur-0.1.27.big"
}
```

Новый путь вывода сохраняет предыдущий BIG. Начните новый Skirmish за обычный Китай; проверьте отсутствие старого ствола и кожуха ядерной пушки, положение единственной башни Повелителя, её вращение, вспышки и стрельбу. Кабина, гусеницы и опоры остаются. Результат исправления ещё не проверен в Windows.

174 автоматических теста пройдены; авторские W3D проверены. На извлечённой 0.1.26 воспроизведено попадание транспортного орудия в модель. Замена единственного kitbash.py удаляет эти части и меняет в тестовом BIG только uwcementaur.w3d; все INI, параметры, старые модели, текстуры и эффекты побайтно сохранены. Полный ZIP 0.1.27 собирает тот же исправленный W3D на авторских тестовых ресурсах. Коммерческие модели и пользовательский диагностический отчёт не публикуются.

SHA256 полного ZIP: `4d838c87d3cc5ec966e5c8aef40b36b864a61d0f5a14e006685ad92fd89c0d67`.

## История диагностики

## Диагностика текстур и деталей Цементавра

После игрового фото IMG_2090 проблема внешнего вида ещё не исправлена: нужны исходные привязки и материалы штатных моделей. Скрипт ниже сохраняет метаданные корпуса, башни и уже собранного BIG: имена деталей, кости, число выбранных треугольников, названия текстур, контрольные суммы UV-каналов и материалов. Модели, текстуры и массивы вершин не выгружаются, игра и BIG не меняются. Проверено на извлечённой 0.1.25 с исправленным именем корпуса; 171 автоматический тест прошёл.

Из текущей папки мода:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/inspect_cementaur.py" -OutFile ".\tools\inspect_cementaur.py" -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
py -3 .\tools\inspect_cementaur.py --game-dir $gameDir --archive ".\dist\UltimateWarfare.big" --report ".\dist\cementaur-visual-details.json"
```

Результат: `dist/cementaur-visual-details.json`. Если BIG собирался под другим именем, укажите его в `--archive`. Скрипт отказывается перезаписывать существующий отчёт; повторный запуск требует нового имени `--report`.

# Ultimate Warfare 0.1.26 — исправление имени ядерной пушки

В 0.1.25 было ошибочно указано `ChinaVehicleNukeCannon`. Правильное имя — `ChinaVehicleNukeLauncher`; прежний пользовательский отчёт меню содержит соответствующую заводскую команду. Переустанавливать игру не нужно. Параметры и сборка модели не менялись.

[Полный исправленный комплект 0.1.26](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.26-source.zip).

Для существующей папки 0.1.25 достаточно выполнить из её корня:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/cementaur-0.1.26.json" -OutFile ".\content\units\cementaur.json" -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir
}
```

169 тестов и проверка авторских W3D пройдены. На извлечённой 0.1.25 воспроизведена ошибка отсутствующего объекта, затем замена единственного JSON позволила собрать и проверить синтетический BIG. Исходный ZIP не содержит ресурсов EA. Native-сборка на установке пользователя после исправления ещё не проверена.

SHA256 полного ZIP 0.1.26: `f4bda3f022e9548ec46147fef614071daaab7e364256b5bbfce5bbe6de39fc52`.

## Предыдущая версия и подробности модели

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
