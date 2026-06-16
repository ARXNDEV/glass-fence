<template>
  <div class="threat-panel" :class="{ open: isOpen }" @mouseenter="autoScroll = false" @mouseleave="autoScroll = true">
    <div class="header">
      <div class="title">
        <i class="fas fa-shield-alt"></i>
        <span>THREAT INTELLIGENCE</span>
      </div>
      <i class="fas fa-times close-btn" @click="$emit('close')"></i>
    </div>
    <div class="content" ref="scrollContainer">
      <div class="event" v-for="(event, idx) in events" :key="idx" :class="event.category">
        <div class="event-time">{{ formatTime(event.ts) }}</div>
        <div class="event-url" :title="event.url">{{ truncate(event.url, 40) }}</div>
        <div class="event-score">
          <div class="bar-bg">
            <div class="bar-fg" :style="{ width: (event.threat_score * 100) + '%' }"></div>
          </div>
          <span class="val">{{ event.threat_score }}</span>
        </div>
        <div class="event-category">{{ event.category.toUpperCase() }}</div>
        <div class="event-blocked" v-if="event.blocked">BLOCKED</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'ThreatPanel',
  props: {
    isOpen: Boolean
  },
  data() {
    return {
      events: [] as any[],
      ws: null as WebSocket | null,
      autoScroll: true
    }
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.$emit('read')
        this.scrollToBottom()
      }
    }
  },
  mounted() {
    this.connect()
  },
  beforeDestroy() {
    if (this.ws) this.ws.close()
  },
  methods: {
    connect() {
      const url = process.env.VUE_APP_AI_ENGINE_URL || 'http://localhost:8000'
      const wsUrl = url.replace('http://', 'ws://').replace('https://', 'wss://')
      this.ws = new WebSocket(`${wsUrl}/ws/threats`)
      this.ws.onmessage = (e) => {
        const data = JSON.parse(e.data)
        this.events.push(data)
        if (this.events.length > 100) this.events.shift()
        if (!this.isOpen) {
          this.$emit('new-event')
        }
        if (this.autoScroll && this.isOpen) {
          this.$nextTick(() => this.scrollToBottom())
        }
      }
      this.ws.onclose = () => {
        setTimeout(this.connect, 5000)
      }
    },
    formatTime(ts: string) {
      const d = new Date(ts)
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    },
    truncate(str: string, n: number) {
      return str.length > n ? str.substr(0, n - 1) + '...' : str
    },
    scrollToBottom() {
      const container = this.$refs.scrollContainer as HTMLElement
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }
  }
})
</script>

<style lang="scss" scoped>
.threat-panel {
  position: absolute;
  top: 30px;
  right: 0;
  width: 500px;
  height: calc(100% - 30px);
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 100;
  font-family: var(--font-mono);

  &.open {
    transform: translateX(0);
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border-default);

    .title {
      font-weight: 700;
      color: var(--gf-danger);
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .close-btn {
      cursor: pointer;
      color: var(--text-secondary);
      &:hover { color: var(--text-primary); }
    }
  }

  .content {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;

    .event {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px;
      background: var(--bg-card);
      border-left: 3px solid transparent;
      font-size: 11px;

      &.safe { border-color: var(--gf-success); }
      &.suspicious { border-color: var(--gf-warning); }
      &.phishing, &.malware { border-color: var(--gf-danger); }

      .event-time { color: var(--text-secondary); width: 60px; }
      .event-url { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--text-primary); }
      
      .event-score {
        width: 80px;
        display: flex;
        align-items: center;
        gap: 5px;

        .bar-bg {
          flex: 1;
          height: 4px;
          background: var(--border-strong);
          border-radius: 2px;
          overflow: hidden;

          .bar-fg {
            height: 100%;
            background: var(--text-primary);
          }
        }
        .val { width: 25px; text-align: right; }
      }

      .event-category {
        width: 70px;
        text-align: right;
        color: var(--text-secondary);
      }

      .event-blocked {
        background: var(--gf-danger);
        color: #fff;
        padding: 2px 4px;
        border-radius: 2px;
        font-weight: 700;
      }
    }
  }
}
</style>
