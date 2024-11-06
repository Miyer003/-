package logger

import (
	"github.com/cloudwego/kitex/pkg/klog"
	kitexzap "github.com/kitex-contrib/obs-opentelemetry/logging/zap"
)

var loggerObj *kitexzap.Logger

type Logger struct {
	*kitexzap.Logger
}

func init() {
	loggerObj = DefaultLogger()
	klog.SetLogger(loggerObj)
}

func (l *Logger) Printf(template string, args ...interface{}) {
	l.Infof(template, args...)
}

func GetLogger() *Logger {
	return &Logger{loggerObj}
}
