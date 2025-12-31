import os
import zipfile

root = os.path.abspath(os.path.dirname(__file__))
zip_name = os.path.join(root, os.path.basename(root) + '.zip')

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(root):
        # skip common caches and git metadata
        if any(p in dirpath for p in (os.path.join(root, '__pycache__'), os.path.join(root, '.git'))):
            continue
        rel = os.path.relpath(dirpath, root)
        for f in filenames:
            if f.endswith('.pyc'):
                continue
            file_path = os.path.join(dirpath, f)
            if os.path.abspath(file_path) == os.path.abspath(zip_name):
                continue
            arcname = os.path.join(rel, f) if rel != '.' else f
            zf.write(file_path, arcname)

print(zip_name)
