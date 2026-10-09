import os
import re

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            if 'venv' in filepath or 'site-packages' in filepath:
                continue
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all <img ...>
            imgs = re.findall(r'<img\s+[^>]*>', content, re.IGNORECASE)
            changed = False
            for img in imgs:
                if 'alt=' not in img:
                    # Add alt=""
                    new_img = img.replace('<img ', '<img alt="" ')
                    content = content.replace(img, new_img)
                    changed = True
            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Added alt="" to images in {filepath}')
