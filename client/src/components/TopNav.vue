<template>
  <div class="top-nav">
    <div class="brand">
      <img src="/logo.svg" alt="Glass Fence Shield" class="logo-img" />
      <span class="brand-text">GLASS FENCE</span>
    </div>

    <div class="status-indicators">
      <div class="pill session-pill">
        <span>SESSION: {{ isConnected ? 'ACTIVE' : 'OFFLINE' }}</span>
        <div class="dot" :class="{ active: isConnected }"></div>
      </div>
      
      <div class="pill threat-pill" :class="threatClass">
        <span>THREAT: {{ threatLevel }}</span>
      </div>

      <div class="pill sessions-count">
        <span>SESSIONS: {{ sessionCount }}</span>
      </div>
    </div>

    <div class="actions">
      <button class="action-btn" :class="{ active: hosting }" @click="toggleControl">
        {{ hosting ? 'RELEASE CONTROL' : 'TAKE CONTROL' }}
      </button>
      <button class="action-btn" @click="$emit('admin')">ADMIN ↗</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '~/assets/styles/_variables.scss';

.top-nav {
  height: 50px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  font-family: var(--font-display);

  .brand {
    display: flex;
    align-items: center;
    gap: 12px;

    .logo-img {
      height: 24px;
      width: 24px;
      object-fit: contain;
    }

    .brand-text {
      font-weight: 700;
      font-size: 16px;
      letter-spacing: 2px;
      color: var(--text-primary);
    }
  }

  .status-indicators {
    display: flex;
    align-items: center;
    gap: 20px;

    .pill {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      letter-spacing: 1px;
      font-weight: 500;
      color: var(--text-secondary);

      .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--text-secondary);

        &.active {
          background: var(--text-primary);
          animation: pulse-white 2s infinite;
        }
      }

      &.threat-pill {
        &.safe span {
          color: var(--status-safe);
        }
        &.warning span {
          color: var(--status-warn);
        }
        &.critical span {
          background: var(--status-danger-bg);
          color: var(--status-danger-text);
          padding: 2px 6px;
          animation: threat-flash 1s infinite;
        }
      }
    }
  }

  .actions {
    display: flex;
    gap: 10px;

    .action-btn {
      background: transparent;
      border: 1px solid var(--border-default);
      color: var(--text-primary);
      font-family: var(--font-display);
      font-size: 12px;
      letter-spacing: 1px;
      padding: 6px 12px;
      cursor: pointer;
      transition: all var(--transition);

      &:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: var(--border-strong);
      }

      &.active {
        background: var(--text-primary);
        color: var(--bg-primary);
      }
    }
  }
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({ name: 'gf-topnav' })
export default class extends Vue {
  get sessionCount() {
    return Object.keys(this.$accessor.user.members || {}).length
  }

  get threatLevel(): string {
    // Default CLEAR; will upgrade once AI engine is integrated
    return this.$accessor.connected ? 'CLEAR' : 'OFFLINE'
  }

  get threatClass() {
    return {
      safe: this.threatLevel === 'CLEAR',
      warning: this.threatLevel === 'CAUTION',
      critical: this.threatLevel === 'CRITICAL',
      offline: this.threatLevel === 'OFFLINE',
    }
  }

  get isConnected() {
    return this.$accessor.connected
  }
  get hosting() {
    return this.$accessor.remote.hosting
  }

  get hosted() {
    return this.$accessor.remote.hosted
  }

  toggleControl() {
    if (this.hosting) {
      this.$accessor.remote.release()
    } else {
      this.$accessor.remote.request()
    }
  }
}
</script>
