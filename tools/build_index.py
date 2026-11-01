"""Собирает index.json каталога из папок modules/<id>/ (описание берётся из module.json, размеры и SHA-256 считаются тут).
Запуск из корня репозитория: python tools/build_index.py   — затем commit + push. Rack Live сверяет каждый файл с этими суммами при скачивании."""
import hashlib, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXTS = ('.html', '.css', '.js', '.json', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.txt', '.md', '.woff2')
ID_RE = re.compile(r'^[a-z][a-z0-9-]{2,40}$')
out, bad = [], 0
base = os.path.join(ROOT, 'modules')
for mid in sorted(os.listdir(base)):
    folder = os.path.join(base, mid)
    if not os.path.isdir(folder):
        continue
    try:
        meta = json.load(open(os.path.join(folder, 'module.json'), encoding='utf-8'))
        assert meta['id'] == mid and ID_RE.match(mid) and meta['title'], 'module.json: id/название'
        assert os.path.isfile(os.path.join(folder, 'index.html')), 'нет index.html'
        files = []
        for dp, dn, fn in os.walk(folder):
            dn[:] = sorted(d for d in dn if not d.startswith('.'))
            for n in sorted(fn):
                if n.startswith('.'):
                    continue
                full = os.path.join(dp, n)
                rel = os.path.relpath(full, folder).replace('\\', '/')
                assert rel.lower().endswith(EXTS), 'недопустимый тип файла: ' + rel
                blob = open(full, 'rb').read()
                assert len(blob) <= 3_000_000, 'файл больше 3 МБ: ' + rel
                files.append({'name': rel, 'size': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()})
        assert len(files) <= 80, 'слишком много файлов'
        out.append({**{k: meta.get(k, '') for k in ('id', 'title', 'description', 'version', 'author', 'tag', 'icon')}, 'new': bool(meta.get('new')), 'files': files})
    except Exception as e:
        print(f'ОШИБКА {mid}: {e}')
        bad += 1
if bad:
    sys.exit(1)
with open(os.path.join(ROOT, 'index.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump({'format': 'racklive-learning', 'version': 1, 'modules': out}, f, ensure_ascii=False, indent=1)
print(f'index.json: модулей {len(out)}')
