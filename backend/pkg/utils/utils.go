package utils

import (
	"errors"
	"mime/multipart"
	"net"
	"strings"

	"yunyiwang/config"
	"yunyiwang/pkg/logger"
)

// AddrCheck 会检查当前的监听地址是否已被占用
func AddrCheck(addr string) bool {
	l, err := net.Listen("tcp", addr)
	if err != nil {
		return false
	}
	l.Close()
	return true
}

// GetAvailablePort 会尝试获取可用的监听地址
func GetAvailablePort() (string, error) {
	if config.Service.AddrList == nil {
		return "", errors.New("utils.GetAvailablePort: config.Service.AddrList is nil")
	}
	logger.Debugf("Available AddrList: %v", config.Service.AddrList)
	for _, addr := range config.Service.AddrList {
		if ok := AddrCheck(addr); ok {
			logger.Debugf("Finally Choose to listen: %v", addr)
			return addr, nil
		}
	}
	return "", errors.New("utils.GetAvailablePort: not available port from config")
}

// IsAllowImageFile 检查文件格式是否合规，支持jpg png jpeg格式
func IsAllowImageFile(header *multipart.FileHeader) bool {
	contentType := header.Header.Get("Content-Type")
	// MIME类型判断
	if strings.HasPrefix(contentType, "image/") {
		return true
	}

	filename := header.Filename
	extensions := []string{".jpg", ".png", ".jpeg"} // Add more image extensions if needed
	for _, ext := range extensions {
		if strings.HasSuffix(strings.ToLower(filename), ext) {
			return true
		}
	}

	return false
}
