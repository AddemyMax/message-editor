# Ultimate Warfare — крупная трёхствольная «Лунма» 0.1.15

[Скачать комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.15-source.zip).

[Рендер авторской модели](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/uwlongma-triple-preview.png) — Blender, не игровой снимок.

Модель увеличена в 1,6 раза по каждой оси, башня расширена и усилена панелями, добавлены три отдельных ствола, обновлена окраска. Здоровье и броня прежние. Три выстрела с интервалом 180 мс, затем 6300 мс перезарядки. Сохраняется тень-декаль: пользователь подтвердил работу 0.1.14 после отказа от объёмной тени. Новая трёхствольная версия ещё требует проверки в игре.

Распакуйте отдельно, откройте папку UltimateWarfare-0.1.15 и выполните:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
```

Новый Skirmish за обычный Китай, военный завод + центр пропаганды, Longma за 2200. Проверьте размер, выезд, проходы между зданиями и выстрелы из всех трёх стволов. При вылете сохраните свежий ReleaseCrashInfo.txt. Старые сохранения для теста не используйте.

128 автоматических тестов прошли. W3D проверен, 7 генерируемых файлов воспроизводятся побайтно; Blender-сцена и рендер обновлены. 8220 треугольников, 17988 вершин, один LOD. Кампании/AI/сохранения/FPS новой версии не проверены.

Оригинальные файлы игры не изменяются и не входят в ZIP. Частный BIG строится локально, вне установки. Нужен Python 3.10+. Код/документация MIT, авторские ресурсы CC0-1.0; подробности в LICENSE и docs/assets.md.

SHA256 ZIP: `c10db6d0ba016c12078993e6b405217730248126bb713f9ea047de2283aa3e07`

Старые ZIP и однопушечный рендер uwlongma-preview.png сохранены для воспроизводимости.
