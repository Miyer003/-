package client

import (
	"errors"
	"fmt"

	"yunyiwang/kitex_gen/template/templateservice"

	"yunyiwang/config"
	"yunyiwang/pkg/constants"

	etcd "github.com/kitex-contrib/registry-etcd"

	"github.com/cloudwego/kitex/client"
)

// 通用的RPC客户端初始化函数
func initRPCClient[T any](serviceName string, newClientFunc func(string, ...client.Option) (T, error)) (*T, error) {
	if config.Etcd == nil || config.Etcd.Addr == "" {
		return nil, errors.New("config.Etcd.Addr is nil")
	}
	// 初始化Etcd Resolver
	r, err := etcd.NewEtcdResolver([]string{config.Etcd.Addr})
	if err != nil {
		return nil, fmt.Errorf("initRPCClient etcd.NewEtcdResolver failed: %w", err)
	}
	// 初始化具体的RPC客户端
	client, err := newClientFunc(serviceName, client.WithResolver(r), client.WithMuxConnection(constants.MuxConnection))
	if err != nil {
		return nil, fmt.Errorf("initRPCClient NewClient failed: %w", err)
	}
	return &client, nil
}

func InitTemplateRPCClient() (*templateservice.Client, error) {
	return initRPCClient(constants.TemplateServiceName, templateservice.NewClient)
}
