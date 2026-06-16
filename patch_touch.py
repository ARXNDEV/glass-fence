import re

with open("client/src/components/video.vue", "r") as f:
    content = f.read()

new_touch = """
    private lastTouchDistance = 0
    onTouchHandler(e: TouchEvent) {
      if (e.touches.length === 2 && e.type === 'touchmove') {
        const t1 = e.touches[0]
        const t2 = e.touches[1]
        const dist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY)
        if (this.lastTouchDistance > 0) {
          const delta = this.lastTouchDistance - dist
          const wheelEvent = new WheelEvent('wheel', {
            bubbles: true, cancelable: true, view: window,
            deltaY: delta * 2, clientX: (t1.clientX + t2.clientX) / 2, clientY: (t1.clientY + t2.clientY) / 2
          })
          if (e.target) e.target.dispatchEvent(wheelEvent)
        }
        this.lastTouchDistance = dist
        return
      }
      if (e.type === 'touchend') {
        this.lastTouchDistance = 0
      }

      let first = e.changedTouches[0]
      let type = ''
      switch (e.type) {
        case 'touchstart': type = 'mousedown'; break
        case 'touchmove': type = 'mousemove'; break
        case 'touchend': type = 'mouseup'; break
        default: return
      }

      const simulatedEvent = new MouseEvent(type, {
        bubbles: true,
        cancelable: true,
        view: window,
        screenX: first.screenX,
        screenY: first.screenY,
        clientX: first.clientX,
        clientY: first.clientY,
        button: 0,
        buttons: 1
      })
      if (first.target) first.target.dispatchEvent(simulatedEvent)
    }
"""

content = re.sub(r'onTouchHandler\(e: TouchEvent\) \{.*?(?=\n\s+onCompositionStartHandler|\n\s+private)', new_touch, content, flags=re.DOTALL)

with open("client/src/components/video.vue", "w") as f:
    f.write(content)
print("Updated touch handler")
