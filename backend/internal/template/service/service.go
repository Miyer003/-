package service

import (
	"context"

	"yunyiwang/pkg/base"
	"yunyiwang/pkg/db"
)

type TemplateService struct {
	ctx context.Context
	db  *db.Database
}

func NewTemplateService(ctx context.Context, clientset *base.ClientSet) *TemplateService {
	return &TemplateService{
		ctx: ctx,
		db:  clientset.DBClient,
	}
}
