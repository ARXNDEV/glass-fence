<template>
  <div class="sidebar">
    <div class="sidebar-header">
      THREAT INTELLIGENCE
    </div>

    <div class="sidebar-section">
      <div class="section-title">URL Analysis</div>
      <div class="url-info">
        <span class="mono">> stream.isolated</span>
        <div class="status-clean">STATUS: CLEAN</div>
      </div>
    </div>

    <div class="sidebar-section log-section">
      <div class="section-title">SESSION LOG</div>
      <div class="log-feed">
        <div class="log-entry" v-for="(log, i) in logs" :key="i" :class="log.level">
          <span class="time">{{ log.time }}</span> {{ log.msg }}
        </div>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="section-title">ACTIVE SESSIONS</div>
      <div class="session-list">
        <div class="session-item" v-for="session in activeSessions" :key="session.id">
          <span>{{ session.displayname || 'Anonymous' }}</span>
          <div class="dot active"></div>
        </div>
        <div class="session-item" v-if="activeSessions.length === 0">
          <span>NO ACTIVE SESSIONS</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '~/assets/styles/_variables.scss';

.sidebar {
  width: 100%;
  height: 100%;
  background: var(--bg-card);
  border-left: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  overflow-y: auto;

  .sidebar-header {
    padding: 15px 20px;
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1px;
    border-bottom: 1px solid var(--border-default);
    color: var(--text-primary);
  }

  .sidebar-section {
    border-bottom: 1px solid var(--border-default);
    padding: 20px;

    .section-title {
      font-size: 10px;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 15px;
    }

    .url-info {
      display: flex;
      flex-direction: column;
      gap: 10px;

      .mono {
        font-family: var(--text-mono);
        font-size: 12px;
        color: var(--text-primary);
      }

      .status-clean {
        font-size: 12px;
        font-weight: bold;
        color: var(--text-primary);
        padding: 4px 8px;
        border: 1px solid var(--border-default);
        display: inline-block;
        width: fit-content;
      }
    }

    &.log-section {
      flex: 1;
      display: flex;
      flex-direction: column;

      .log-feed {
        flex: 1;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 8px;

        .log-entry {
          font-family: var(--text-mono);
          font-size: 11px;
          color: var(--text-secondary);
          animation: log-entry 0.3s ease forwards;

          .time {
            color: var(--text-primary);
            margin-right: 8px;
          }
        }
      }
    }

    .session-list {
      display: flex;
      flex-direction: column;
      gap: 10px;

      .session-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: var(--text-mono);
        font-size: 12px;
        padding: 8px 12px;
        border: 1px solid var(--border-subtle);
        background: rgba(255, 255, 255, 0.02);

        .dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: var(--text-primary);
          animation: pulse-white 2s infinite;
        }
      }
    }
  }
}
</style>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator'

interface LogEntry {
  time: string
  msg: string
  level: 'info' | 'warn' | 'error'
}

@Component({ name: 'gf-sidebar' })
export default class extends Vue {
  private logs: LogEntry[] = []
  private maxLogs = 50

  @Watch('$accessor.connected', { immediate: true })
  onConnectionChange(connected: boolean) {
    this.addLog(`Connection: ${connected ? 'connected' : 'disconnected'}`, connected ? 'info' : 'warn')
  }

  @Watch('memberCount')
  onMemberCountChange(newCount: number, oldCount: number) {
    if (newCount > oldCount) this.addLog('Member joined session', 'info')
    else if (newCount < oldCount) this.addLog('Member left session', 'warn')
  }

  @Watch('$accessor.remote.hosting')
  onHostingChange(hosting: boolean) {
    if (hosting) this.addLog('Control requested', 'info')
    else this.addLog('Control released', 'info')
  }

  mounted() {
    // Add initial log on mount
    this.addLog('Glass Fence session initialized', 'info')
  }

  addLog(msg: string, level: LogEntry['level'] = 'info') {
    const now = new Date()
    const time = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`
    this.logs.unshift({ time, msg, level })
    if (this.logs.length > this.maxLogs) this.logs.pop()
  }

  get activeSessions() {
    return Object.values(this.$accessor.user.members || {})
  }

  get memberCount() {
    return this.activeSessions.length
  }
}
</script>
