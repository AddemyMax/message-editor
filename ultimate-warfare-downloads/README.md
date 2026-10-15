# Ultimate Warfare — Longma 0.1.17

[Скачать комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.17-source.zip) · [Предпросмотр текстур](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/uwlongma-surface-preview.png).

По игровому снимку пользователя переработаны поверхности: светлая серо-зелёная броня вместо крупных пятен камуфляжа, тёмные стыки, светлые кромки, заклёпки, решётки и лючки. Авторская текстура приближается к стилю исходной техники; оригинальные игровые изображения не включаются. UV крыши теперь непрерывны, цилиндры оборачивают текстуру один раз. Добавлен пропущенный флаг OkToChangeModelColor=Yes для цвета игрока.

Форма, размер относительно Повелителя, три ствола, урон и броня сохранены от 0.1.16. Нативное визуальное сравнение новой версии ещё требуется; рендер Blender не показывает результат в SAGE.

Распакуйте отдельно, откройте папку UltimateWarfare-0.1.17 и выполните:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
```

Новый Skirmish за обычный Китай, военный завод и центр пропаганды. Поставьте Longma рядом с исходным танком при том же освещении. Проверьте палитру, читаемость деталей, полосы цвета игрока и стрельбу. Нужен новый игровой снимок.

131 автоматический тест прошёл; W3D проверен; 7 генерируемых файлов воспроизводятся побайтно. 5692 треугольника, 12616 вершин, 5 мешей, один LOD и тень-декаль. Кампании/AI/сохранения/FPS не проверены.

Исходные игровые файлы не изменяются и не входят в ZIP. Частный BIG строится локально вне установки. Python 3.10+. Код MIT, авторские ресурсы CC0-1.0; условия в LICENSE/docs/assets.md.

SHA256 ZIP: `a9c87ebe4def8a10f96f458cb7e18959a9826d875e8c00d2f1c73f060653ebf0`

Старые архивы и рендеры сохранены.
