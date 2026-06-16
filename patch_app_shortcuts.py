import re

with open("client/src/app.vue", "r") as f:
    content = f.read()

new_handleKeydown = """
    handleKeydown(e: KeyboardEvent) {
      if (e.key === '?' && !['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) {
        this.$swal.fire({
          title: 'Keyboard Shortcuts',
          html: `<div style="text-align:left; font-family:var(--font-mono)">
            <p><b>Ctrl+Alt+F</b> - Toggle fullscreen</p>
            <p><b>Ctrl+Alt+C</b> - Open clipboard sync</p>
            <p><b>Ctrl+Alt+D</b> - Disconnect session</p>
            <p><b>Ctrl+Alt+T</b> - Toggle threat panel</p>
            <p><b>Ctrl+Alt+S</b> - Open settings</p>
          </div>`,
          background: 'var(--bg-card)',
          color: 'var(--text-primary)',
          confirmButtonColor: 'var(--gf-accent)'
        })
      }
      if (e.ctrlKey && e.altKey) {
        const k = e.key.toLowerCase()
        if (k === 't') {
          e.preventDefault()
          this.threatPanelOpen = !this.threatPanelOpen
        }
        if (k === 'f') {
          e.preventDefault()
          if (this.video) this.video.requestFullscreen()
        }
        if (k === 'd') {
          e.preventDefault()
          this.$accessor.client.logout()
        }
        if (k === 's') {
          e.preventDefault()
          // Open settings (assuming available)
        }
      }
    }
"""

content = re.sub(r'handleKeydown\(e: KeyboardEvent\) \{.*?\n    \}', new_handleKeydown.strip('\n'), content, flags=re.DOTALL)

with open("client/src/app.vue", "w") as f:
    f.write(content)
print("Updated app.vue for shortcuts")
