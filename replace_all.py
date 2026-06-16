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
        ("name: 'glass-fence-chat'", "name: 'gf-chat'"),
        ("name: 'glass-fence-video'", "name: 'gf-video'"),
        ("name: 'glass-fence-files'", "name: 'gf-files'"),
        ("name: 'glass-fence-menu'", "name: 'gf-menu'"),
        ("name: 'glass-fence-avatar'", "name: 'gf-avatar'"),
        ("name: 'glass-fence-emote'", "name: 'gf-emote'"),
        ("name: 'glass-fence-emotes'", "name: 'gf-emotes'"),
        ("name: 'glass-fence-context'", "name: 'gf-context'"),
        ("name: 'glass-fence-unsupported'", "name: 'gf-unsupported'"),
        ("name: 'glass-fence-connect'", "name: 'gf-connect'"),
        ("name: 'glass-fence-resolution'", "name: 'gf-resolution'"),
        ("name: 'glass-fence-settings'", "name: 'gf-settings'"),
        ("name: 'glass-fence-about'", "name: 'gf-about'"),
        ("name: 'glass-fence-clipboard'", "name: 'gf-clipboard'"),
        ("name: 'glass-fence-emoji'", "name: 'gf-emoji'"),
        ("name: 'glass-fence-markdown'", "name: 'gf-markdown'"),
        ("<glass-fence-", "<gf-"),
        ("</glass-fence-", "</gf-"),
        ("id=\"glass-fence\"", "id=\"glass-fence\""),
        ("#glass-fence", "#glass-fence"),
        ("group=\"glass-fence\"", "group=\"glass-fence\""),
        (".glass-fence-menu", ".gf-menu"),
        ("'~/glass-fence/", "'~/glassfence/"),
        ("\"~/glass-fence/", "\"~/glassfence/"),
        ("module github.com/ARXNDEV/glass-fence", "module github.com/arxndev/glass-fence"),
        ("net.ARXNDEV.glass-fence", "net.arxndev.glass-fence"),
        ("ARXNDEV/glass-fence", "arxndev/glass-fence"),
        ("ARXNDEV", "arxndev"),
        ("/home/glass-fence", "/home/glassfence"),
        ("/usr/bin/glass-fence", "/usr/bin/glass-fence"),
        ("glass-fence.yaml", "glass-fence.yaml"),
        ("glass-fence-rooms", "glass-fence"),
        ("Built on n.eko", ""),
        ("n.eko", "Glass Fence"),
        ("Glass Fence", "Glass Fence"),
        ("glass-fence", "glass-fence")
    ]
    
    directories_to_walk = ['./client', './server', './runtime', './apps', './utils', './webpage', './ai-engine']
    
    for d in directories_to_walk:
        for root, dirs, files in os.walk(d):
            if '.git' in dirs:
                dirs.remove('.git')
            if 'node_modules' in dirs:
                dirs.remove('node_modules')
            if 'dist' in dirs:
                dirs.remove('dist')
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
                
            for file in files:
                # Skip images and binary files
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webmanifest', '.xbm', '.woff', '.woff2', '.ttf', '.bin', '.so', '.a', '.pyc')):
                    continue
                
                filepath = os.path.join(root, file)
                for old_str, new_str in replacements:
                    replace_in_file(filepath, old_str, new_str)

if __name__ == "__main__":
    main()
