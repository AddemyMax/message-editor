# Ultimate Warfare 0.1.24 — плотный дым Tumbler

[Полный комплект](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/UltimateWarfare-0.1.24-source.zip). [Один файл дыма для работающей версии](https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-smoke-0.1.24.ini).

По игровому отзыву увеличена плотность облака: 10–14 частиц каждые 2–3 кадра вместо 3–4 каждые 4–6 (средний выброс примерно в 6.9 раза чаще), клубы крупнее, выше непрозрачность, дольше живут отдельные частицы, выше вертикальный объём. Облако появляется сразу. Срок действия 8 с, радиус подавления 60, перезарядка 30 с, все параметры машины, оружие и модели сохранены.

Для уже работающей 0.1.23, включая исправленную папку 0.1.21, откройте PowerShell в корне мода и выполните:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/AddemyMax/message-editor/uw-mod-download/ultimate-warfare-downloads/tumbler-smoke-0.1.24.ini" -OutFile ".\content\effects\tumbler.ini" -ErrorAction Stop
$gameDir = "C:\Program Files (x86)\R.G. Mechanics\Command and Conquer - Generals\Command and Conquer Generals Zero Hour"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Mod.ps1 -GameDir $gameDir -Output ".\dist\UltimateWarfare-smoke-0.1.24.big"
if ($LASTEXITCODE -eq 0) {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Launch-Mod.ps1 -GameDir $gameDir -Archive ".\dist\UltimateWarfare-smoke-0.1.24.big"
}
```

Для полного комплекта распакуйте отдельно и откройте UltimateWarfare-0.1.24; команда загрузки файла ему не нужна. Вывод под новым именем сохраняет прежний рабочий BIG. Повторная сборка в существующий выходной файл запрещена: выбирайте новое имя для -Output и соответствующее -Archive.

161 тест прошёл. Извлечённый ZIP собирает и проверяет синтетический BIG; сравнение с 0.1.23 подтвердило неизменность части INI до ParticleSystem и всех 21 авторских выходных ресурсов. Пользователь подтвердил работу 0.1.23 и наличие дыма; новая плотность ещё не проверена в игре. Проверьте одну гранату, затем несколько облаков одновременно и плавность игры.

Сохраняются миниган, маскировка и отдельная дымовая спецспособность 0.1.23. Генералы/автоматическое строительство AI не расширены. Нужны Windows, установленная Zero Hour 1.04, Python 3.10+. Blender для сборки не нужен. Оригинальные файлы игры не меняются, частный BIG и коммерческие игровые ресурсы не публикуются. Лицензии исходного комплекта указаны в LICENSE/docs/assets.md. Старые версии сохранены.

SHA256 ZIP: `09a9aaa6497069c2fe51c897586e5a7c5680803542509336a913ead80e5c2eb6`
