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
        <div class="log-entry" v-for="(log, i) in simulatedLogs" :key="i">
          <span class="time">{{ log.time }}</span> {{ log.msg }}
        </div>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="section-title">ACTIVE SESSIONS</div>
      <div class="session-list">
        <div class="session-item">
          <span>SESSION #001</span>
          <div class="dot active"></div>
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
import { Component, Vue } from 'vue-property-decorator'

@Component({ name: 'Sidebar' })
export default class extends Vue {
  // Simulated logs for the mockup
  get simulatedLogs() {
    return [
      { time: '14:32:01', msg: 'System initialized.' },
      { time: '14:32:02', msg: 'WebRTC proxy connected.' },
      { time: '14:32:05', msg: 'Container spun up.' },
      { time: '14:32:09', msg: 'URL loaded securely.' },
      { time: '14:33:12', msg: 'Heartbeat OK.' },
    ]
  }
}
</script>
