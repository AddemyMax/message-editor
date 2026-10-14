# Ultimate Warfare — прототип 0.1.14

[Скачать комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.14-source.zip).

Распакуйте отдельно, откройте папку UltimateWarfare-0.1.14 и выполните:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
```

В 0.1.13 пользователь успешно собрал BIG и запустил игру, но производство «Лунмы» завершилось вылетом. Журнал согласуется с переполнением старого буфера объёмных теней. В 0.1.14 только у нового танка объёмная тень заменена декалью; модель и остальные юниты сохраняются. Проверка исправления в игре ещё нужна.

127 автоматических тестов прошли, бинарная структура модели проверена. Испытание: новый Skirmish за обычный Китай, военный завод и центр пропаганды, производство Longma за 2200. Затем движение, башня, стрельба. При вылете сохраните свежий ReleaseCrashInfo.txt.

Меню завода сохраняет исходные команды и получает 15-ю кнопку с частным оверлеем стандартной панели. Кнопки производства немного уже. Новые CSF-метки добавляются с сохранением исходных записей. Оригинальные архивы и исполняемые файлы не изменяются и не входят в ZIP. Частный BIG собирается локально вне установки. Нужен Python 3.10+.

SHA256 ZIP: `17208547ebd724b9a08a6a105486516e44a32423254eeec12796a0b84b82ff0d`

Старые ZIP сохранены для воспроизводимости. uwlongma-preview.png — рендер авторской модели в Blender, не игровой снимок. Код/документация — MIT, авторские ресурсы — CC0-1.0; подробности в LICENSE и docs/assets.md.
