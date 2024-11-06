package logger

import (
	"github.com/cloudwego/kitex/pkg/klog"
)

func Debug(args ...interface{}) {
	klog.Debug(args)
}

func Debugf(template string, args ...interface{}) {
	klog.Debugf(template, args...)
}

func Info(args ...interface{}) {
	klog.Info(args)
}

func Infof(template string, args ...interface{}) {
	klog.Infof(template, args...)
}

func Warn(args ...interface{}) {
	klog.Warn(args)
}

func Warnf(template string, args ...interface{}) {
	klog.Warnf(template, args)
}

func Error(args ...interface{}) {
	klog.Error(args)
}

func Errorf(template string, args ...interface{}) {
	klog.Errorf(template, args...)
}

func Fatal(args ...interface{}) {
	klog.Fatal(args)
}

func Fatalf(template string, args ...interface{}) {
	klog.Fatalf(template, args...)
}
