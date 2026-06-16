import os

def replace_in_file(filepath, old_str, new_str):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_str in content:
            content = content.replace(old_str, new_str)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Skipping {filepath}: {e}")

def main():
    replacements = [
        ("github.com/ARXNDEV/glass-fence", "github.com/ARXNDEV/glass-fence"),
        ("arxndevv/glass-fence", "arxndevv/glass-fence"),
        ("Glass Fence", "Glass Fence"),
    ]
    
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if 'dist' in dirs:
            dirs.remove('dist')
            
        for file in files:
            # Skip images and binary files
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webmanifest', '.xbm', '.woff', '.woff2', '.ttf')):
                continue
            
            filepath = os.path.join(root, file)
            for old_str, new_str in replacements:
                replace_in_file(filepath, old_str, new_str)

if __name__ == "__main__":
    main()
