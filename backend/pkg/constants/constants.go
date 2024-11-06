package constants

import "time"

const (
	JWTValue = "MTAxNTkwMTg1Mw=="

	MuxConnection    = 1                     // (RPC) 最大连接数
	RPCTimeout       = 3 * time.Second       // (RPC) RPC请求超时时间
	ConnectTimeout   = 50 * time.Millisecond // (RPC) 连接超时时间
	StreamBufferSize = 1024                  // (RPC) 流请求 Buffer 尺寸

	TemplateServiceName      = "template"
	ApiServiceName           = "api"
	TemplateServiceTableName = "template"

	MaxQPS          = 100
	MaxVideoSize    = 300000
	MaxListLength   = 100
	MaxGoroutines   = 10
	MaxOpenConns    = 100
	MaxConnections  = 1000             // (DB) 最大连接数
	MaxIdleConns    = 10               // (DB) 最大空闲连接数
	ConnMaxLifetime = 10 * time.Second // (DB) 最大可复用时间
	ConnMaxIdleTime = 5 * time.Minute  // (DB) 最长保持空闲状态时间
	PageSize        = 10

	NumWorkers = 10 // 最大的并发数量

	FailureRateLimiterBaseDelay = time.Minute
	FailureRateLimiterMaxDelay  = 30 * time.Minute

	B  = 1
	KB = 1024 * B
	MB = 1024 * KB
	GB = 1024 * MB
)
