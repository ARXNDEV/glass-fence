import os
import re

directories = ['client/src/components', 'client/src/assets/styles']

color_mapping = {
    r'#fff(fff)?': 'var(--gf-bg)',
    r'#000(000)?': 'var(--gf-text)',
    r'#f5f5f5': 'var(--gf-surface)',
    r'#ebebeb': 'var(--gf-surface2)',
    r'#111(111)?': 'var(--gf-text)',
    r'#666(666)?': 'var(--gf-muted)',
    r'#0051a8': 'var(--gf-accent)',
    r'#16a34a': 'var(--gf-success)',
    r'#d97706': 'var(--gf-warning)',
    r'#dc2626': 'var(--gf-danger)',
    r'#f04747': 'var(--gf-danger)',
    r'#a62626': 'var(--gf-danger)',
    r'rgba\(\$color:\s*#fff(?:fff)?,\s*\$alpha:\s*0\.05\)': 'var(--gf-surface)',
    r'rgba\(\$color:\s*#fff(?:fff)?,\s*\$alpha:\s*0\.1\)': 'var(--gf-surface2)',
    r'rgba\(\$color:\s*#fff(?:fff)?,\s*\$alpha:\s*0\.2\)': 'var(--gf-border)',
    r'rgba\(\$color:\s*#000(?:000)?,\s*\$alpha:\s*0\.2\)': 'var(--gf-border)',
}

def replace_hex_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    for pattern, replacement in color_mapping.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

for directory in directories:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.vue') or file.endswith('.scss'):
                replace_hex_in_file(os.path.join(root, file))
