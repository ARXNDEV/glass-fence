import re

with open("client/src/app.vue", "r") as f:
    content = f.read()

# Add ThreatPanel and LoadingOverlay imports
import_injection = """
  import ThreatPanel from '~/components/ThreatPanel.vue'
  import LoadingOverlay from '~/components/LoadingOverlay.vue'
"""
content = re.sub(r'(import BottomBar from .*?\n)', r'\1' + import_injection, content)

# Add to components block
content = re.sub(r"(BottomBar\n\s*\}\,)", r"BottomBar,\n      ThreatPanel,\n      LoadingOverlay\n    },", content)

# Add state and logic
logic_injection = """
    threatPanelOpen = false
    webrtcState = 'connecting'

    mounted() {
      window.addEventListener('keydown', this.handleKeydown)
      if (this.$client.peerConnection) {
        this.$client.peerConnection.onconnectionstatechange = () => {
          const state = this.$client.peerConnection.connectionState
          if (state === 'failed' || state === 'disconnected') this.webrtcState = 'error'
          else if (state === 'connected') this.webrtcState = 'connected'
          else this.webrtcState = 'negotiating'
        }
      }
    }
    beforeDestroy() {
      window.removeEventListener('keydown', this.handleKeydown)
    }
    handleKeydown(e: KeyboardEvent) {
      if (e.ctrlKey && e.altKey) {
        if (e.key.toLowerCase() === 't') {
          e.preventDefault()
          this.threatPanelOpen = !this.threatPanelOpen
        }
      }
    }
"""
content = re.sub(r'(get connected\(\) \{)', logic_injection + r'\n    \1', content)

# Add to template
template_injection = """
        <ThreatPanel :isOpen="threatPanelOpen" @close="threatPanelOpen = false" />
        <LoadingOverlay v-if="connected && webrtcState !== 'connected'" :state="webrtcState" @retry="() => { window.location.reload() }" />
"""
content = re.sub(r'(<gf-about v-if="about" />)', r'\1' + template_injection, content)

with open("client/src/app.vue", "w") as f:
    f.write(content)
print("Updated app.vue")
