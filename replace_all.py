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
        ("name: 'neko-chat'", "name: 'gf-chat'"),
        ("name: 'neko-video'", "name: 'gf-video'"),
        ("name: 'neko-files'", "name: 'gf-files'"),
        ("name: 'neko-menu'", "name: 'gf-menu'"),
        ("name: 'neko-avatar'", "name: 'gf-avatar'"),
        ("name: 'neko-emote'", "name: 'gf-emote'"),
        ("name: 'neko-emotes'", "name: 'gf-emotes'"),
        ("name: 'neko-context'", "name: 'gf-context'"),
        ("name: 'neko-unsupported'", "name: 'gf-unsupported'"),
        ("name: 'neko-connect'", "name: 'gf-connect'"),
        ("name: 'neko-resolution'", "name: 'gf-resolution'"),
        ("name: 'neko-settings'", "name: 'gf-settings'"),
        ("name: 'neko-about'", "name: 'gf-about'"),
        ("name: 'neko-clipboard'", "name: 'gf-clipboard'"),
        ("name: 'neko-emoji'", "name: 'gf-emoji'"),
        ("name: 'neko-markdown'", "name: 'gf-markdown'"),
        ("<neko-", "<gf-"),
        ("</neko-", "</gf-"),
        ("id=\"neko\"", "id=\"glass-fence\""),
        ("#neko", "#glass-fence"),
        ("group=\"neko\"", "group=\"glass-fence\""),
        (".neko-menu", ".gf-menu"),
        ("'~/neko/", "'~/glassfence/"),
        ("\"~/neko/", "\"~/glassfence/")
    ]
    
    for root, dirs, files in os.walk('./client'):
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
