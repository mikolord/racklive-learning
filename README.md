# racklive-learning

Каталог учебных модулей для [Rack Live](https://github.com/mikolord/racklive): интерактивные уроки, игры и тренажёры о сетях.
В Rack Live: **Инструменты → Обучение** — там виден список из этого каталога, нужное скачивается одним нажатием.

- Модули публикует только владелец проекта. Загрузки со стороны не принимаются.
- Модуль — папка `modules/<id>/` с `index.html`, `module.json` и своими файлами (html, css, js, json, картинки).
- Rack Live запускает модуль в изолированном окне без сети и без доступа к самому приложению; модуль может только сохранить свой прогресс (`RLLearn.load()` / `RLLearn.save()` из `/api/learn/bridge.js`).
- Каждый файл при скачивании сверяется с размером и SHA-256 из `index.json`.

## Выложить новый модуль
1. Создать `modules/<id>/` (`index.html`, `module.json`: `id`, `title`, `description`, `version`, `author`, `tag` = course/game/manual/trainer, `icon`).
2. `python tools/build_index.py`
3. commit + push. Обновить модуль — поднять `version` в `module.json` и снова пересобрать индекс.

Лицензия: MIT.
