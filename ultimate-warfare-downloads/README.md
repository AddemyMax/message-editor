# Ultimate Warfare — Longma 0.1.18: оригинальные игровые текстуры

[Скачать исходный комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.18-source.zip).

По предоставленным пользователем атласам подготовлена первая раскладка деталей оригинальной техники: броня и крыша Повелителя, механические панели и катки Battlemaster, гусеничная текстура NVTreads. Цвет игрока и авторская оптика сохраняются. Размер, три ствола, урон и защита прежние.

Игровые изображения берутся из установленной игры при сборке и собираются в частный uwlongma.tga. У пользователя они найдены в Textures.big соседней папки Command and Conquer Generals. ZIP содержит только код, координаты участков и авторские ресурсы-заглушки; оригинальные DDS/TGA/PNG не распространяются. Старые Blender-превью не показывают эту поверхность. Новый результат нужно оценить в SAGE.

Распакуйте отдельно, откройте папку UltimateWarfare-0.1.18 и выполните:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
```

Новый Skirmish за обычный Китай, военный завод и центр пропаганды. Поставьте Longma рядом с Повелителем при одинаковом освещении. Проверьте крышу, борта, стволы, катки и цвет игрока. Раскладка исходных деталей — первый вариант; новый игровой снимок требуется для оценки соответствия.

142 теста прошли на авторской синтетике; W3D проверен; 7 авторских исходных выходных файлов воспроизводятся побайтно. Отслеживаются текстуры в общей папке Generals, изменения их контрольных сумм и новые loose-файлы. BIG запрещено записывать внутрь обеих установок. Оригиналы не изменяются.

Частный BIG содержит игровые данные и не распространяется как авторский MIT/CC0-контент. Условия исходного комплекта — LICENSE/docs/assets.md. Нужен Python 3.10+, Blender для сборки не нужен.

SHA256 ZIP: `27a24524399fd64cad5bcf1d2b5283426156e820d46e54da6e2a8252a890917e`

Старые архивы/авторские превью сохранены. Нативная сборка 0.1.18 и внешний вид ещё не подтверждены.
