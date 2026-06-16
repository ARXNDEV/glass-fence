import re

# Update chat.vue for HH:MM timestamp
with open("client/src/components/chat.vue", "r") as f:
    chat_content = f.read()

chat_content = re.sub(
    r'timestamp\(time: Date\) \{.*?return.*?\n\s+\}',
    """timestamp(time: Date) {
      const str = new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      return str
    }""",
    chat_content,
    flags=re.DOTALL
)

with open("client/src/components/chat.vue", "w") as f:
    f.write(chat_content)

# Update side.vue for unread count
with open("client/src/components/side.vue", "r") as f:
    side_content = f.read()

template_injection = """
        <li :class="{ active: tab === 'chat' }" @click.stop.prevent="change('chat')">
          <i class="fas fa-comment-alt"></i>
          <span>{{ $t('side.chat') }}</span>
          <span class="unread-badge" v-if="unreadCount > 0">{{ unreadCount }}</span>
        </li>
"""
side_content = re.sub(
    r'<li :class="\{ active: tab === \'chat\' \}" @click\.stop\.prevent="change\(\'chat\'\)">.*?<span>\{\{ \$t\(\'side\.chat\'\) \}\}</span>.*?</li>',
    template_injection,
    side_content,
    flags=re.DOTALL
)

script_injection = """
    private lastMsgLength = 0
    get unreadCount() {
      if (this.tab === 'chat') {
        this.lastMsgLength = this.$accessor.chat.messages.length
        return 0
      }
      return Math.max(0, this.$accessor.chat.messages.length - this.lastMsgLength)
    }
"""

side_content = re.sub(r'(get tab\(\) \{)', script_injection + r'\n    \1', side_content)

style_injection = """
    .unread-badge {
      background: var(--gf-danger);
      color: #fff;
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 10px;
      margin-left: 5px;
      font-weight: bold;
    }
"""

side_content = re.sub(r'(\.side \{[^\}]*display: flex;)', r'\1' + style_injection, side_content)

with open("client/src/components/side.vue", "w") as f:
    f.write(side_content)
print("Updated chat.vue and side.vue")
