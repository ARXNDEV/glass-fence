<template>
  <div class="bottom-bar">
    <div class="item">
      <span>GLASS FENCE v1.0.0</span>
    </div>
    <div class="item">
      <span>WebRTC: <span class="highlight">{{ webrtcStatus }}</span></span>
    </div>
    <div class="item">
      <span>ISOLATION: <span class="highlight">{{ isolationStatus }}</span></span>
    </div>
    <div class="item">
      <span>AI ENGINE: <span class="highlight">{{ aiStatus }}</span></span>
    </div>
    <div class="item">
      <span>BLOCKED: <span class="highlight">{{ threatsBlocked }}</span></span>
    </div>
    <div class="item right">
      <span>arxndev © 2025</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '~/assets/styles/_variables.scss';

.bottom-bar {
  height: 30px;
  background: var(--bg-primary);
  border-top: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 30px;

  .item {
    font-family: var(--text-mono);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    text-transform: uppercase;

    .highlight {
      color: var(--text-secondary);
      font-weight: bold;
    }

    &.right {
      margin-left: auto;
    }
  }
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({ name: 'gf-bottombar' })
export default class extends Vue {
  get webrtcStatus() {
    return this.$accessor.connected ? 'CONNECTED' : 'DISCONNECTED'
  }

  get isolationStatus() {
    return this.$accessor.connected ? 'ACTIVE' : 'INACTIVE'
  }

  get aiStatus() {
    return this.$accessor.client.aiConnected ? 'ONLINE' : 'OFFLINE'
  }
  get threatsBlocked() {
    return this.$accessor.client.threatsBlocked
  }
}
</script>
