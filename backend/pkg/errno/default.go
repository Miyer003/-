package errno

var (
	// Success
	Success = NewErrNo(SuccessCode, "Success")

	ParamError         = NewErrNo(ParamErrorCode, "parameter error")
	ParamEmpty         = NewErrNo(ParamEmptyCode, "some params that required are empty")
	ParamMissingHeader = NewErrNo(ParamMissingHeaderCode, "missing request header data (id or cookies)")

	AuthFailedError      = NewErrNo(AuthErrorCode, "authorization failed")
	BizError             = NewErrNo(BizErrorCode, "business error")
	InternalServiceError = NewErrNo(InternalServiceErrorCode, "internal service error")

	UserExistedError      = NewErrNo(InternalDatabaseErrorCode, "user existed")
	UserNonExistError     = NewErrNo(InternalDatabaseErrorCode, "user didn't exist")
	SuffixError           = NewErrNo(ParamErrorCode, "invalid file")
	NoAccessError         = NewErrNo(AuthErrorCode, "user don't have authority to this biz")
	NoRunningPictureError = NewErrNo(BizErrorCode, "no valid picture")

	// internal error
	UpcloudError    = NewErrNo(BizFileUploadErrorCode, "upload to upcloud error")
	SFCreateIDError = NewErrNo(InternalDatabaseErrorCode, "sf create id failed")

	// redis
	RedisError = NewErrNo(InternalRedisErrorCode, "redis error")
)
