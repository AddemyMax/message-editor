# Ultimate Warfare — комплект первого прототипа

Эта отдельная ветка предназначена для передачи файлов мода; приложение message-editor не изменено.

- `UltimateWarfare-0.1.1-source.zip` — исходный комплект мода для оригинальной Zero Hour 1.04.
- `uwlongma-preview.png` — оригинальный рендер модели «Лунма» в Blender; игровой запуск ещё не проверен.

Откройте нужный файл на GitHub и нажмите **Download raw file** (значок скачивания). Для архива нужен именно ZIP этой папки, а не общий архив React-репозитория.

Распакуйте ZIP и откройте вложенную папку `UltimateWarfare-0.1.1`, где находятся `README.md`, `scripts`, `tools` и `content`. Откройте в ней PowerShell и выполните:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Prepare-Test.ps1 -GameDir "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
```

Для диагностики и сборки нужен Python 3.10+. Оригинальные файлы игры не перезаписываются. Нативные испытания Zero Hour и Windows-скриптов ещё не выполнены; 75 автоматических тестов инструментов проходят на синтетических данных.

SHA256 ZIP: `6e4dacc69d96797a5ccd7a27f71d43a40c28aafa8b9bded96073cd17656c347d`

ZIP не содержит оригинальные игровые архивы, исполняемые файлы или локально собранный BIG. Код и документация — MIT; авторская геометрия и изображения — CC0-1.0. Полные условия находятся в LICENSE и docs/assets.md исходного комплекта.
