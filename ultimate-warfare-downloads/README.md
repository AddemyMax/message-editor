# Ultimate Warfare — Longma 0.1.16

[Скачать комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.16-source.zip) · [Рендер новой модели](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/uwlongma-classic-preview.png).

Переработка под стиль китайской техники Generals: широкая ходовая часть, высокая гранёная башня, крупные панели, толстые круглые стволы и оливково-песочная окраска. Модель создана из авторской геометрии; игровые модели/текстуры не распространяются. Предпросмотр — Blender, не игровой снимок; красные полосы показывают цвет игрока.

Урон ×2 относительно 0.1.15. Эффективная броня ×2: коэффициенты входящего урона уменьшены с 0.85 до 0.425, здоровье 950. Три выстрела с интервалом 180 мс, затем 6300 мс перезарядки. Цена 2200, строительство 24 с.

Базовый размер ещё на 31.25% больше относительно 0.1.15. Сборщик сравнивает габариты игровой геометрии с локальным ChinaTankOverlord и обеспечивает минимум +20% по трём осям; модель и тень при необходимости масштабируются вместе. Визуальное сравнение в игре требуется.

Распакуйте отдельно, откройте папку UltimateWarfare-0.1.16 и выполните:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
```

Новый Skirmish за обычный Китай, военный завод + центр пропаганды. Постройте Longma и Overlord рядом. Проверьте размер, внешний вид, выезд и проходы между зданиями, движение/бой и три выстрела. При вылете — свежий ReleaseCrashInfo.txt.

129 тестов прошли, W3D проверен, 7 выходных файлов воспроизводятся побайтно. 5692 треугольника, 12616 вершин, 5 мешей, один LOD. Сохраняется декаль вместо объёмной тени. Нативная работа 0.1.14 подтверждена пользователем; эта версия, кампании/AI/сохранения/FPS требуют проверки.

Оригинальные файлы установки не изменяются и не входят в ZIP. Частный BIG строится локально вне игры. Python 3.10+. Код/документация MIT, авторские ресурсы CC0-1.0; подробнее LICENSE и docs/assets.md.

SHA256: `bb071b7b0749f2417c2bc414a6953f51955172be63fbae995028ceb70fd49e48`

Старые ZIP и рендеры оставлены для воспроизводимости.
