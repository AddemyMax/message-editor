# Ultimate Warfare0.1.36 — только исправление масштаба Maus

Пользователь сообщил, что0.1.35 огромен и не похож на Maus Blitzkrieg II. Автоматическое увеличение по Overlord отключено. Установлен фиксированный Scale2 авторского W3D, примерно42.33×20.8 по горизонтальным габаритам до общих настроек движка. Collision/decal shadow согласованы с ним. Это не2×Overlord, а абсолютный коэффициент собственной модели. Боевые параметры Crusader, старые юниты и текущий арт0.1.35 сохранены. Native-масштаб ещё не проверен.

**Новый дизайн Blitzkrieg II не перенесён.** Предоставленная страница https://www.moddb.com/mods/blitzkrieg-ii/images/maus/ возвращает из среды proxy tunnel403. Изображение и лицензия не просмотрены. Для воссоздания нужен доступный скриншот; для буквального переноса — W3D/текстуры и совместимые условия/разрешение. Чужие файлы не добавлялись.

[Небольшое исправление для0.1.35](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.36-scale-fix.zip) · [Полный комплект0.1.36 с прежним артом](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.36-source.zip).

Закройте игру. Из текущей папки мода в PowerShell:

```powershell
$patch = Join-Path $env:TEMP "Maus-0.1.36-scale-fix.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.36-scale-fix.zip" -OutFile $patch -ErrorAction Stop
Expand-Archive -LiteralPath $patch -DestinationPath "." -Force -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.36.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.36.big"
}
```

Начните новый Skirmish и проверьте размер, выезд из завода, движение/стрельбу.202 теста и W3D-проверки прошли. Регрессия проверяет, что Overlord Scale100 не изменяет размер Maus. Извлечённая0.1.35 + fix и полный0.1.36 строят одинаковый BIG; CLI build/check-launch проходят на синтетических данных. Windows-игра не запускалась. Исправление содержит11 авторских файлов, без EA-ресурсов/частных BIG/отчётов.

SHA256 fix: `bf40758df013c68af3e985aadebfb5fde0ce47b84abc83597a0110e76cfbd798`.
SHA256 source: `a5b98beab8e5c47d1c0745e15391a7c7f217d70fc50143ff227936f0815adc3d`.

## Предыдущие версии

# Ultimate Warfare0.1.35 — серый Maus по новому образцу, масштаб от Overlord

По пользовательскому скриншоту прежняя модель0.1.34 оказалась слишком маленькой и не соответствовала образцу. Перестроены широкий сплошной корпус, низкая вытянутая башня с округлым лбом, длинный гладкий ствол, широкие гусеницы и16 мелких катков +2 концевых колеса на каждом борту. Новая тёмно-серая авторская окраска; модель8246 треугольников/20170 вершин,6 мешей/5 костей. Обновлены иконка, редактируемые исходники и превью. Чужая сетка/текстура не импортируются.

**Размер рассчитывается по фактической normal-модели локального ChinaTankOverlord.** Учтены INI Scale, quaternion bind-позы и костные влияния. Собственный Maus также измеряется по W3D; единый Scale даёт минимум1.9× по видимой длине/ширине, сохраняя пропорции. Из-за разного отношения длины к ширине точные осевые коэффициенты могут различаться. Collision BOX и тень увеличены под корпус; пушка/точка выстрела/откат масштабируются вместе с ним. HP/броня/оружие/скорость/экономика/AI/опыт/улучшения остаются Crusader, ячейка и имя Maus прежние. Другие юниты без изменений.

[Новый вид спереди](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.35-front.png) · [Сзади](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.35-rear.png). Это собственная модель в Blender до зависящего от установки Scale, не сравнительный native-скриншот.

[Обновление текущей0.1.34](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.35-update.zip) · [Полный комплект0.1.35](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.35-source.zip).

Закройте игру. Из текущей папки мода в PowerShell:

```powershell
$patch = Join-Path $env:TEMP "Maus-0.1.35-update.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.35-update.zip" -OutFile $patch -ErrorAction Stop
Expand-Archive -LiteralPath $patch -DestinationPath "." -Force -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.35.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.35.big"
}
```

Новый Skirmish: серый Maus с рядом мелких катков должен быть заметно крупнее. Сравните на ровной площадке с обычным Overlord при одинаковом увеличении камеры. Проверьте выход из завода, разворот у зданий/мосты/узкие проходы, выбор группы, стрельбу/откат/наведение, смерть, апгрейды/сохранения/AI/FPS. Native0.1.35 здесь не запускался.201 тест пройден, W3D-проверки пройдены; геометрия, Scale2 у reference, сохранение боевых полей/модулей и прежних юнитов, объединение/верификация модельных зависимостей проверены. Извлечённая0.1.34 + update и полный0.1.35 строят идентичный BIG; CLI build/validate/check-launch проходят на синтетических данных. Windows игра не запускалась.

Update содержит23 авторских файла; исходные EA-ресурсы, private BIG и пользовательские отчёты не публикуются. Установка игры не меняется.

SHA256 update: `78281c89aa2c7fd66b866bf2381910d56b4bcef92e7a86fb6b916f2919fa67fc`.
SHA256 source: `bca68a950a28e92b7ab94051413e4e2b36bde0cc1f927b855867cfb19254fa0f`.

## Предыдущие версии

# Ultimate Warfare0.1.34 — Maus за США

Новый **Maus**: авторская интерпретация Panzer VIII с длинным корпусом/закрытой ходовой, высокой башней, широкой маской и двумя стволами. Малый ствол визуальный: игровой урон не добавляется. Модель/атласы/иконка/редактируемые исходники созданы здесь, чужих ресурсов нет.

**Все не-визуальные параметры взяты из локального AmericaTankCrusader.** Body/здоровье, ArmorSet/WeaponSet/опыт, AI/скорость/поворот/геометрия, цена/время, prerequisites, CommandSet и улучшения сохранены. Новый stock_reskin меняет идентификатор, Draw, название/портрет и decal-тень. Maus доступен в обычном AmericaWarFactory с исходными требованиями Crusader; дополнительный StrategyCenter не добавлен. Кнопка занимает свободный1–12 либо15/16. При полном заводе Tumbler15/Maus16, все оригинальные команды сохранены. Старый Tumbler по-прежнему A33 [4000 HP], китайские юниты прежние.

[Превью спереди](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.34-front.png) · [Сзади](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.34-rear.png). Это фактическая модель в Blender, не игровой кадр.

[Обновление для текущей0.1.33](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.34-update.zip) · [Полный комплект0.1.34](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.34-source.zip).

Полностью закройте игру. В PowerShell из текущей папки мода:

```powershell
$patch = Join-Path $env:TEMP "Maus-0.1.34-update.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Maus-0.1.34-update.zip" -OutFile $patch -ErrorAction Stop
Expand-Archive -LiteralPath $patch -DestinationPath "." -Force -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.34.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.34.big"
}
```

В новом Skirmish за обычные США выпустите Maus и Crusader, сравните их характеристики/улучшения. Проверьте выпуск, движение/поворот/гусеницы, наведение/откат/попадание, смерть, дроны/апгрейды, сохранение/загрузку, AI/кампании и FPS. Native-проверки не выполнялись в облаке.200 автоматических тестов пройдены; проверены точное сохранение не-визуальных полей/модулей, варианты исходных параметров, полные ячейки15/16/отказ при переполнении, прежние юниты и зависимости модели. W3D/геометрия/UV/mapper проверены;4108 треугольников,6 мешей,5 костей. Сборка извлечённой0.1.33 + update и полного0.1.34 даёт одинаковый BIG на авторских фикстурах. Игра не перезаписывается; ресурсы EA и частные BIG не публикуются.

SHA256 update: `d06e6a26d02d5b0f65bea36c16bb5a6ed67c6b0cd533bd5ece3b9cda4e062234`.
SHA256 source: `1734e33a24aa2a37c2b5f3ef14b1a59ddefae7f79e38c2c35cadc771bb04d02e`.

## Предыдущие версии

# Ultimate Warfare 0.1.33 — визуальный обвес Бэтмобиля

Новые скошенные плечи и крылья, ступенчатые бронепластины, клиновидный передний обвес, боковые воздухозаборники/юбки, гидравлика и многослойное реактивное сопло. Обновлены иконка, редактируемые исходники и два Blender-превью. Это авторская модель, не импорт киношной/чужой сетки.

**4000 HP и исходная броня «Повелителя» сохранены.** Сравнение с0.1.32 подтверждает побайтно прежние игровые INI и статистики; в тестовом BIG изменены только модель, иконка и подписи A33. Точные границы, все14 костей, шесть вращающихся колёс и миниган прежние. 11884 треугольника (+15%),11 мешей. 194 теста и W3D-проверка пройдены. Нативный внешний вид/пересечения при движении/вращении, смерть, сохранения и FPS не проверены в облаке.

[Спереди](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.33-front.png) · [Сзади](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.33-rear.png). Это рендеры экспортированной модели в Blender, не скриншоты SAGE.

[Визуальное обновление для текущей0.1.32](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.33-design-update.zip) · [Полный комплект0.1.33](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.33-source.zip).

Полностью закройте игру. В PowerShell из текущей папки мода:

```powershell
$patch = Join-Path $env:TEMP "Tumbler-0.1.33-design-update.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.33-design-update.zip" -OutFile $patch -ErrorAction Stop
Expand-Archive -LiteralPath $patch -DestinationPath "." -Force -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.33.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.33.big"
}
```

Новый Skirmish/новая машина: метка **Batmobile A33 [4000 HP]**. Сравните новую геометрию в движении с двух сторон. Update содержит15 авторских файлов (модель/иконка/редактируемые источники/превью, генератор, конфигурация и документация); установочные файлы игры не меняются. Старый BIG не перезаписывается. Проверены CLI build/preflight извлечённой0.1.32 с update и полного0.1.33: одинаковый BIG на авторских фикстурах.

SHA256 update: `bcbd9d01aae36a70aea75657946fe79c06e25796244f27ee8ea1be9313c2f94b`.
SHA256 source: `e8f5f74ee14559e1c2337f89b3d3ecf84336c28d7f8c6887d8b7bd5941ba3c79`.

## Предыдущие версии

# Ultimate Warfare 0.1.32 — 4000 HP и броня «Повелителя»

По просьбе пользователя Бэтмобиль получает MaxHealth/InitialHealth=4000 и исходные коэффициенты брони всех ArmorSet локального ChinaTankOverlord. Множитель брони=1, единые5% отключены. Относительные subdual-параметры сохранены. Оружие, скорость, цена, модель, маскировка, дым и четыре ракеты не менялись. Метка: **Batmobile A32 [4000 HP]**.

[Обновление текущей папки 0.1.28–31](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.32-update.zip).
[Полный комплект 0.1.32](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.32-source.zip).

Полностью закройте игру. В PowerShell из текущей папки мода:

```powershell
$patch = Join-Path $env:TEMP "Tumbler-0.1.32-update.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.32-update.zip" -OutFile $patch -ErrorAction Stop
Expand-Archive -LiteralPath $patch -DestinationPath "." -Force -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.32.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.32.big"
}
```

Начните новый Skirmish, постройте новую машину и проверьте метку A32 [4000 HP]. Установочные файлы игры не меняются. 194 теста и W3D-проверка прошли; сравнение всех38 эффективных коэффициентов включает обычную/дополнительную ArmorSet и исходные DEFAULT/повторы. Извлечённая0.1.28 + update и полный0.1.32 собирают одинаковый тестовый BIG. Нативная игра/PowerShell здесь не запускались.

SHA256 update: `9672455c99162451631e9df4ee7d46ca8d2697340a4af13146d71fc8997bb7bd`.
SHA256 source: `23c37e792e1d4330af8440e9cfe7bd916c392a99f3a6a0782a104c0b232b0f3f`.

## Предыдущие версии

# Ultimate Warfare 0.1.31 — исправленная броня, 5000 HP и метка загрузки

В частной таблице брони найдено неверное имя KILLPILOT; native DamageTypeFlags принимает KILL_PILOT. Ошибка генератора исправлена, все 38 типов сверены с опубликованным кодом SAGE; build/preflight отклоняют неизвестные имена. Предыдущий отчёт подтверждал проценты в BIG, но не валидность имён или загруженный Windows-процесс. Связь найденной ошибки с конкретной игровой быстрой гибелью ещё требует native-проверки.

Бэтмобиль получает MaxHealth/InitialHealth=5000, единую броню 5% обычного боевого урона и имя **Batmobile A31 [5000 HP]**. Остальные характеристики, оружие, ракеты, дым и модель прежние. Subdual cap и recovery amount масштабируются вместе с HP, чтобы исходный лимит не делал EMP недостижимым. Launcher не запускает новую игру поверх уже открытого Generals/game.dat и не завершает процессы сам. Для проверки нужна новая схватка/новая машина, без старого сохранения.

[Небольшой ZIP обновления для 0.1.28–30](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.31-update.zip). [Полный комплект 0.1.31](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.31-source.zip).

Полностью закройте игру. Из текущей папки мода выполните:

```powershell
$patch = Join-Path $env:TEMP "Tumbler-0.1.31-update.zip"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/Tumbler-0.1.31-update.zip" -OutFile $patch -ErrorAction Stop
Expand-Archive -LiteralPath $patch -DestinationPath "." -Force -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-0.1.31.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-0.1.31.big"
}
```

Обновление заменяет шесть авторских файлов мода: catalog, манифест Tumbler, rocket/armor модуль, reference_vehicle, launcher и диагностический скрипт. Файлы установки игры не меняются, старые BIG сохраняются. Полный комплект уже включает исправления; ему загрузка update.zip не нужна.

В новом Skirmish выпустите машину за обычные США. На выделенной машине должно быть **Batmobile A31 [5000 HP]**. Если надписи нет, сначала проверьте запуск нового BIG/сохранение. При наличии метки сравните попадания одного Humvee/Gattling и танковой пушки. Это поможет проверить реальную загруженную версию, а не только содержимое файла на диске.

193 автоматических теста прошли. Проверены канонические типы, отказ от KILLPILOT при build/preflight, HP/initialHP/report=5000, коэффициенты5%, относительные subdual-параметры и сохранение старого оружия/моделей. Извлечённая 0.1.28 + update.zip собирает тот же тестовый BIG, что полный 0.1.31. Native-стрельба/смерть и новый PowerShell guard здесь не выполнялись: Windows/pwsh недоступны. Пользовательские отчёты и ресурсы EA не публикуются.

SHA256 update ZIP: `e49d1f62d1b9ced849d819c0f009345a1a5c16206dd4db8198200b816a13a31e`.

SHA256 полного ZIP: `50da1dd4bf6224e157144e3ac904f3b67f0f05bc03afa8f3fb93fa36aa886236`.

## Предыдущие обновления

## Проверка фактической брони Бэтмобиля

После отзыва об отсутствии ощутимого усиления доступен read-only инструмент для проверки уже собранного BIG. Он показывает фактическое здоровье, все ArmorSet/эффективные проценты, checksum архива и сборочного manifest, оружие машины и исходных Humvee/Gattling/танков, базовую оценку урона за попадание. Он не подтверждает, какой архив уже загружен в Windows-процесс, и не учитывает бонусы/несколько атакующих в оценках. Сами игровые INI/модели не выгружаются, игра и BIG не меняются.

Из папки мода:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/inspect_tumbler_armor.py" -OutFile ".\tools\inspect_tumbler_armor.py" -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
py -3 .\tools\inspect_tumbler_armor.py --game-dir $gameDir --archive ".\dist\UltimateWarfare-0.1.30.big" --report ".\dist\tumbler-armor-details.json"
```

Если игра запускалась с другим BIG, укажите его в --archive. Результат — dist/tumbler-armor-details.json. Отчёт содержит только метаданные, не оригинальные файлы игры. 189 автоматических тестов прошли, включая отличение реального содержимого архива от устаревшего manifest, вычисление пулемётного урона и запрет записи в игру/перезаписи отчёта. Инструмент проверен на извлечённом 0.1.30 с авторскими входными данными. Причина пользовательской игровой слабой брони пока не установлена: необходим реальный отчёт из его BIG. Параметры мода этим диагностическим обновлением не меняются.

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
