import os
import re

directories = ['.']
excludes = ['.git', 'node_modules', 'dist', 'final_replace.py', 'replace_hex.py', 'patch_video.py', 'patch_touch.py', 'patch_app.py', 'patch_chat.py', 'patch_compose.py', 'patch_compose_ds.py']

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in excludes]
    for file in files:
        if file in excludes or file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.svg') or file.endswith('.mp4') or file.endswith('.webp'):
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Replacements
            content = content.replace('m1k1o', 'ARXNDEV')
            content = content.replace('M1k1o', 'ARXNDEV')
            content = content.replace('NEKO_', 'GF_')
            content = content.replace('Neko_', 'GF_')
            content = content.replace('neko_', 'gf_')
            content = content.replace('Neko', 'Glass Fence')
            content = content.replace('neko', 'glass-fence')
            content = content.replace('NEKO', 'GLASS_FENCE')
            
            # fix potential typescript space issues that might be reintroduced
            content = re.sub(r'Glass Fence([A-Z][a-zA-Z]+)', r'GlassFence\1', content)
            
            if content != original_content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Updated {filepath}")
        except Exception as e:
            pass

print("Final replacement complete.")
