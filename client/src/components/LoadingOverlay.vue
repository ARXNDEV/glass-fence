<template>
  <div class="loading-overlay" v-if="state !== 'connected'" :class="{ 'fade-out': state === 'connected' }">
    <div class="content">
      <div v-if="state === 'connecting'" class="pulse-line"></div>
      <div v-if="state === 'negotiating'" class="pulse-line negotiating"></div>
      
      <p class="message" :class="{'error': state === 'error'}">
        {{ message }}
      </p>

      <button v-if="state === 'error'" class="retry-btn" @click="$emit('retry')">
        RETRY CONNECTION
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'LoadingOverlay',
  props: {
    state: {
      type: String, // 'connecting', 'negotiating', 'connected', 'error'
      required: true,
      default: 'connecting'
    }
  },
  computed: {
    message(): string {
      switch (this.state) {
        case 'connecting': return 'Establishing secure channel…'
        case 'negotiating': return 'Negotiating stream…'
        case 'error': return 'Connection failed. Check firewall or VPN settings.'
        default: return ''
      }
    }
  }
})
</script>

<style lang="scss" scoped>
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: opacity 0.5s ease-in-out;
  
  &.fade-out {
    opacity: 0;
    pointer-events: none;
  }

  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 20px;
  }

  .pulse-line {
    width: 150px;
    height: 2px;
    background: var(--text-primary);
    animation: pulse-white 1.5s infinite;
    
    &.negotiating {
      width: 200px;
      animation-duration: 0.8s;
    }
  }

  .message {
    font-family: var(--font-mono);
    font-size: 14px;
    color: var(--text-secondary);
    letter-spacing: 1px;
    text-transform: uppercase;
    
    &.error {
      color: var(--status-danger-text);
      background: var(--status-danger-bg);
      padding: 4px 8px;
    }
  }

  .retry-btn {
    background: transparent;
    border: 1px solid var(--text-primary);
    color: var(--text-primary);
    padding: 8px 16px;
    font-family: var(--font-main);
    font-size: 12px;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.2s;

    &:hover {
      background: var(--text-primary);
      color: var(--bg-primary);
    }
  }
}
</style>
