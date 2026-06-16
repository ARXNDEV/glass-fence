import re

# Hook into session/manager.go
with open("server/internal/session/manager.go", "r") as f:
    content = f.read()

content = re.sub(
    r'(import \()',
    r'\1\n\t"time"\n\t"github.com/ARXNDEV/glass-fence/server/internal/metrics"\n',
    content
)

# Connect event
content = re.sub(
    r'(func \(manager \*SessionManagerCtx\) Create.*?\{)',
    r'\1\n\tmetrics.ActiveSessions.Inc()\n\tsession.Set("connectedAt", time.Now())\n',
    content
)

# Disconnect event
content = re.sub(
    r'(func \(manager \*SessionManagerCtx\) Destroy.*?\{)',
    r'\1\n\tmetrics.ActiveSessions.Dec()\n\tif val, ok := session.Get("connectedAt"); ok {\n\t\tmetrics.SessionDuration.Observe(time.Since(val.(time.Time)).Seconds())\n\t}\n',
    content
)

with open("server/internal/session/manager.go", "w") as f:
    f.write(content)


# Hook into webrtc/manager.go for WebRTCErrors
with open("server/internal/webrtc/manager.go", "r") as f:
    webrtc_content = f.read()

webrtc_content = re.sub(
    r'(import \()',
    r'\1\n\t"github.com/ARXNDEV/glass-fence/server/internal/metrics"\n',
    webrtc_content
)

webrtc_content = re.sub(
    r'(webrtc.PeerConnectionStateFailed:\s*\n\s*logger.Warn\(\).Msg\("webrtc failed"\))',
    r'\1\n\t\t\tmetrics.WebRTCErrors.WithLabelValues("failed").Inc()',
    webrtc_content
)

with open("server/internal/webrtc/manager.go", "w") as f:
    f.write(webrtc_content)

print("Updated manager.go for metrics")
