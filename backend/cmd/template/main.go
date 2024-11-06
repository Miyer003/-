package main

import (
	"net"

	"yunyiwang/config"
	"yunyiwang/internal/template"
	"yunyiwang/pkg/base"
	"yunyiwang/pkg/constants"
	"yunyiwang/pkg/logger"
	"yunyiwang/pkg/utils"

	etcd "github.com/kitex-contrib/registry-etcd"

	"github.com/cloudwego/kitex/pkg/limit"
	"github.com/cloudwego/kitex/pkg/rpcinfo"
	"github.com/cloudwego/kitex/server"

	"yunyiwang/kitex_gen/template/templateservice"
)

var (
	serviceName = constants.TemplateServiceTableName
	clientSet   *base.ClientSet
)

func init() {
	config.Init(serviceName)
	// eshook.InitLoggerWithHook(serviceName)
	clientSet = base.NewClientSet(base.WithDBClient(config.MoggoDB.Addr))
}

func main() {
	r, err := etcd.NewEtcdRegistry([]string{config.Etcd.Addr})
	if err != nil {
		logger.Fatalf("Classroom: etcd registry failed, error: %v", err)
	}
	listenAddr, err := utils.GetAvailablePort()
	if err != nil {
		logger.Fatalf("Classroom: get available port failed: %v", err)
	}
	logger.Infof("Classroom: listen addr: %v", listenAddr)
	addr, err := net.ResolveTCPAddr("tcp", listenAddr)
	if err != nil {
		logger.Fatalf("Classroom: listen addr failed %v", err)
	}

	svr := templateservice.NewServer(
		template.NewTemplateService(clientSet),
		server.WithServerBasicInfo(&rpcinfo.EndpointBasicInfo{
			ServiceName: serviceName,
		}),
		server.WithMuxTransport(),
		server.WithServiceAddr(addr),
		server.WithRegistry(r),
		server.WithLimit(&limit.Option{
			MaxConnections: constants.MaxConnections,
			MaxQPS:         constants.MaxQPS,
		}),
	)
	server.RegisterShutdownHook(clientSet.Close)

	if err = svr.Run(); err != nil {
		logger.Fatalf("Template: server run failed: %v", err)
	}
}
