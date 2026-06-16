package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	ActiveSessions = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "gf_active_sessions",
		Help: "Current WebRTC sessions",
	})

	SessionDuration = promauto.NewHistogram(prometheus.HistogramOpts{
		Name:    "gf_session_duration_sec",
		Help:    "Session length in seconds",
		Buckets: prometheus.ExponentialBuckets(10, 2, 10),
	})

	WebRTCErrors = promauto.NewCounterVec(prometheus.CounterOpts{
		Name: "gf_webrtc_errors_total",
		Help: "WebRTC errors by type",
	}, []string{"type"})

	StreamBitrate = promauto.NewHistogramVec(prometheus.HistogramOpts{
		Name:    "gf_stream_bitrate_kbps",
		Help:    "Stream bitrate by browser type",
		Buckets: prometheus.LinearBuckets(100, 500, 10),
	}, []string{"browser"})

	AIScreenings = promauto.NewCounter(prometheus.CounterOpts{
		Name: "gf_ai_screenings_total",
		Help: "URL screenings sent to AI engine",
	})
)
