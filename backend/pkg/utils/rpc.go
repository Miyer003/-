package utils

import (
	"yunyiwang/kitex_gen/model"
	"yunyiwang/pkg/errno"
)

// IsSuccess 通用的rpc结果处理
func IsSuccess(baseResp *model.BaseResp) bool {
	return baseResp.Code == errno.SuccessCode
}
