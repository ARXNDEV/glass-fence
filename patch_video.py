import re

with open("client/src/components/video.vue", "r") as f:
    content = f.read()

# Add properties
prop_injection = """
    private aiStatus = 'checking'
    private connQuality = { latency: 0, packetLoss: 0, level: 'green' }
    private statsInterval = 0
    private aiInterval = 0
"""
content = re.sub(r'(private focused = false)', r'\1' + prop_injection, content)

# Add logic in created/mounted/beforeDestroy
lifecycle_injection = """
    async checkAI() {
      try {
        const r = await fetch((process.env.VUE_APP_AI_ENGINE_URL || 'http://localhost:8000') + '/health', {
          signal: AbortSignal.timeout ? AbortSignal.timeout(3000) : undefined
        })
        const data = await r.json()
        this.aiStatus = data.models_loaded ? 'online' : 'loading'
      } catch {
        this.aiStatus = 'offline'
      }
    }

    async updateStats() {
      if (!this.$client.peerConnection) return
      try {
        const stats = await this.$client.peerConnection.getStats()
        stats.forEach(report => {
          if (report.type === 'inbound-rtp' && report.kind === 'video') {
            const jitter = report.jitter || 0
            const packetsLost = report.packetsLost || 0
            const packetsReceived = report.packetsReceived || 1
            const latency = Math.round(jitter * 1000)
            const packetLoss = Math.round((packetsLost / (packetsReceived + packetsLost)) * 100) || 0
            let level = 'green'
            if (latency > 150) level = 'red'
            else if (latency >= 50) level = 'amber'
            
            this.connQuality = { latency, packetLoss, level }
          }
        })
      } catch(e) {}
    }
"""

content = re.sub(r'(@Watch\(' "['\"]" r'fullscreen' "['\"]" r'\))', lifecycle_injection + r'\n    \1', content)

# Modify mounted / beforeDestroy
if 'mounted()' in content:
    content = re.sub(r'(mounted\(\)\s*\{)', r'\1\n      this.checkAI()\n      this.aiInterval = window.setInterval(this.checkAI.bind(this), 15000)\n      this.statsInterval = window.setInterval(this.updateStats.bind(this), 2000)\n', content)
else:
    # find where to insert
    pass

if 'beforeDestroy()' in content:
    content = re.sub(r'(beforeDestroy\(\)\s*\{)', r'\1\n      window.clearInterval(this.aiInterval)\n      window.clearInterval(this.statsInterval)\n', content)

# Template injection
template_injection = """
      <div class="badges">
        <div class="quality-badge" :class="connQuality.level" :title="'Latency: ' + connQuality.latency + 'ms | Loss: ' + connQuality.packetLoss + '%'">
          QoS: {{ connQuality.latency }}ms
        </div>
        <div class="ai-badge" :class="aiStatus">
          AI Engine: {{ aiStatus.toUpperCase() }}
        </div>
      </div>
"""
content = re.sub(r'(<div class="isolated-badge">ISOLATED</div>)', r'\1' + template_injection, content)

style_injection = """
    .video-top-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 15px;
      .badges {
        display: flex;
        gap: 10px;
        align-items: center;
        
        .quality-badge, .ai-badge {
          font-family: var(--font-mono);
          font-size: 10px;
          padding: 2px 6px;
          border-radius: 12px;
          color: #000;
          font-weight: 700;
        }
        
        .quality-badge.green { background: var(--gf-success); }
        .quality-badge.amber { background: var(--gf-warning); }
        .quality-badge.red { background: var(--gf-danger); color: #fff; }
        
        .ai-badge.online { background: var(--gf-success); }
        .ai-badge.loading { background: var(--gf-warning); }
        .ai-badge.offline { background: var(--gf-danger); color: #fff; }
        .ai-badge.checking { background: var(--gf-muted); color: #fff; }
      }
    }
"""

content = re.sub(r'(\.video-top-bar \{[^\}]*padding: 0 15px;)', r'\1' + style_injection, content)

with open("client/src/components/video.vue", "w") as f:
    f.write(content)
print("Updated video.vue")
