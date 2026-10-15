# Ultimate Warfare 0.1.22 — Tumbler: миниган, маскировка и дым

Исправлена остановка сборки на DeliveryDecal внутри DeliverPayload исходного ObjectCreationList.ini. Движок наследует здесь таблицу DeliverPayloadData; парсер теперь учитывает её вложенный блок. Исходные записи сохраняются, модели и игровые параметры прежние. Старый комплект 0.1.21 воспроизвёл ошибку на авторском источнике; замена только ini.py позволила построить и проверить синтетический BIG. Сборку на настоящей установке нужно повторить.

Если уже распакована 0.1.21, вместо нового ZIP можно заменить только парсер. Из её корня в прежнем PowerShell с заданным $gameDir:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/ini-parser-0.1.22.py" -OutFile ".\tools\uwmod\ini.py" -ErrorAction Stop
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir
}
```


[Скачать комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.22-source.zip) · [Спереди](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-0.1.21-preview.png) · [Сзади](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-0.1.21-rear-preview.png).

Сохранены здоровье, броня, основные пушки, скорость, цена, время производства и масштаб 0.1.20. Longma не менялась. По игровому снимку снижена кабина, добавлены клиновидные щитки передних колёс и кожухи сдвоенных задних, возвращены графитовая окраска и тёмные диски. Геометрия реконструирована по референсам Tumbler; точное совпадение с фильмом не заявляется. PNG — реальные Blender-рендеры экспортируемой модели, не игровые снимки.

Новые системы:

- Верхний шестистовольный миниган с независимым наведением. Дополнительный SECONDARY наследует пулемёт обычного Humvee вашей установки; основные PRIMARY сохранены для всех исходных ветеранских наборов. Движок выбирает оружие; одновременную стрельбу обоих типов не обещаем.
- Врождённая маскировка через 3 с без стрельбы/урона; движение не раскрывает. Стрельба любым оружием и урон раскрывают, штатные детекторы работают. Владелец видит полупрозрачную машину.
- Smoke grenade: отдельная кнопка, затем точка на земле. Дальность 180, одна граната, перезарядка 30 с с таймером. Облако на 8 с радиусом 60 продлевает короткий NO_ATTACK только врагам: они временно не стреляют, но могут двигаться. Союзники не затрагиваются; HP-урона нет. Это STATUS-длительность с учётом штатной брони; возможен краткий остаточный эффект после выхода. Дым не создаёт физическую преграду обзору движка.

Распакуйте отдельно, откройте PowerShell в UltimateWarfare-0.1.22:

```powershell
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir
```

Новый Skirmish за обычные США, военный завод и Центр стратегии. Проверьте миниган на пехоте и сохранённые пушки на технике, маскировку без детектора и возле него, бросок/перезарядку дыма, подавление и восстановление огня врагов. Нужны проверка выезда, колёс/поворотов, сохранение/загрузка и FPS на группе машин с дымом. Генералы и автоматическое строительство AI не расширены.

157 тестов прошли на авторских данных, три W3D проверены. Сравнение синтетических BIG 0.1.20/0.1.21 подтвердило сохранение базовых параметров и Longma. Новые способности и модель 0.1.21 ещё не проверены в нативной Zero Hour. Нужны Windows, локальная Zero Hour 1.04 и Python 3.10+; Blender для сборки не нужен.

SHA256 ZIP: `77338b187f9cf4fb7fcb2b20a92f22fc059ee3ebe3a91cc1f2b7d3072fb5bd15`

Исходные файлы игры не изменяются; ObjectCreationList.ini и другие полные таблицы читаются из установки и дополняются только в частном BIG. В ZIP нет оригинальной игры/текстур, чужих моделей, исходного игрового снимка пользователя или частного BIG. Код/документация MIT; авторская геометрия/пиксели CC0-1.0 в пределах прав автора. Права на фильм и названия остаются у правообладателей. Старые версии сохранены.
