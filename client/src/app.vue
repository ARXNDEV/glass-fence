<template>
  <div id="glass-fence">
    <template v-if="!$client.supported">
      <gf-unsupported />
    </template>
    <template v-else>
      <div class="layout-grid">
        <TopNav class="grid-topnav" @admin="toggleAbout" />
        
        <div class="grid-content">
          <div class="grid-video">
            <gf-video
              ref="video"
              :hideControls="hideControls"
              :extraControls="isEmbedMode"
              @control-attempt="controlAttempt"
            />
          </div>
          
          <div class="grid-sidebar">
            <Sidebar />
          </div>
        </div>

        <BottomBar class="grid-bottom" />
      </div>

      <gf-connect v-if="!connected" />
      <gf-about v-if="about" />
        <ThreatPanel :isOpen="threatPanelOpen" @close="threatPanelOpen = false" />
        <LoadingOverlay v-if="connected && webrtcState !== 'connected'" :state="webrtcState" @retry="() => { window.location.reload() }" />

      
      <notifications
        group="glass-fence"
        position="top left"
        style="top: 60px; pointer-events: none"
        :ignoreDuplicates="true"
      />
    </template>
  </div>
</template>

<style lang="scss">
  @import '~/assets/styles/_variables.scss';

  #glass-fence {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    background: var(--bg-primary);
    overflow: hidden;

    .layout-grid {
      display: flex;
      flex-direction: column;
      height: 100%;
      width: 100%;

      .grid-topnav {
        flex-shrink: 0;
      }

      .grid-content {
        flex-grow: 1;
        display: flex;
        overflow: hidden;

        .grid-video {
          flex: 0 0 70%;
          border-right: 1px solid var(--border-default);
          background: #000;
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .grid-sidebar {
          flex: 0 0 30%;
          background: var(--bg-card);
        }
      }

      .grid-bottom {
        flex-shrink: 0;
      }
    }
  }

  // Scrollbar customization for Brutalist feel
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  ::-webkit-scrollbar-track {
    background: var(--bg-primary);
  }
  ::-webkit-scrollbar-thumb {
    background: var(--border-strong);
    border-radius: 0;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
  }
</style>

<script lang="ts">
  import { Vue, Component, Ref, Watch } from 'vue-property-decorator'

  import Connect from '~/components/connect.vue'
  import Video from '~/components/video.vue'
  import About from '~/components/about.vue'
  import Unsupported from '~/components/unsupported.vue'
  
  import TopNav from '~/components/TopNav.vue'
  import Sidebar from '~/components/Sidebar.vue'
  import BottomBar from '~/components/BottomBar.vue'

  import ThreatPanel from '~/components/ThreatPanel.vue'
  import LoadingOverlay from '~/components/LoadingOverlay.vue'

  @Component({
    name: 'glass-fence',
    components: {
      'gf-connect': Connect,
      'gf-video': Video,
      'gf-about': About,
      'gf-unsupported': Unsupported,
      TopNav,
      Sidebar,
      BottomBar,
      ThreatPanel,
      LoadingOverlay
    },
  })
  export default class extends Vue {
    @Ref('video') video!: Video

    shakeKbd = false

    get isEmbedMode() {
      return !!new URL(location.href).searchParams.get('embed')
    }

    get hideControls() {
      return false
    }

    toggleAbout() {
      this.$accessor.client.toggleAbout()
    }

    controlAttempt() {
      if (this.shakeKbd || this.$accessor.remote.hosted) return

      this.shakeKbd = true
      window.setTimeout(() => (this.shakeKbd = false), 5000)
    }

    get about() {
      return this.$accessor.client.about
    }

    
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

    get connected() {
      return this.$accessor.connected
    }
  }
</script>
