package template

import (
	"context"

	"yunyiwang/kitex_gen/template"
	"yunyiwang/pkg/base"
)

// TemplateServiceImpl implements the last service interface defined in the IDL.
type TemplateServiceImpl struct {
	ClientSet *base.ClientSet
}

func NewTemplateService(clientSet *base.ClientSet) *TemplateServiceImpl {
	return &TemplateServiceImpl{
		ClientSet: clientSet,
	}
}

// Ping implements the TemplateServiceImpl interface.
func (s *TemplateServiceImpl) Ping(ctx context.Context, req *template.PingRequest) (resp *template.PingResponse, err error) {
	// TODO: Your code here...

	return
}
