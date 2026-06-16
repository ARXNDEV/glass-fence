<template>
  <div id="neko">
    <template v-if="!$client.supported">
      <neko-unsupported />
    </template>
    <template v-else>
      <div class="layout-grid">
        <TopNav class="grid-topnav" @admin="toggleAbout" />
        
        <div class="grid-content">
          <div class="grid-video">
            <neko-video
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

      <neko-connect v-if="!connected" />
      <neko-about v-if="about" />
      
      <notifications
        group="neko"
        position="top left"
        style="top: 60px; pointer-events: none"
        :ignoreDuplicates="true"
      />
    </template>
  </div>
</template>

<style lang="scss">
  @import '~/assets/styles/_variables.scss';

  #neko {
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

  @Component({
    name: 'neko',
    components: {
      'neko-connect': Connect,
      'neko-video': Video,
      'neko-about': About,
      'neko-unsupported': Unsupported,
      TopNav,
      Sidebar,
      BottomBar
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

    get connected() {
      return this.$accessor.connected
    }
  }
</script>
