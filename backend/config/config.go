package config

import (
	"os"

	"yunyiwang/pkg/logger"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"

	_ "github.com/spf13/viper/remote"
)

var (
	Server        *server
	Service       *service
	Etcd          *etcd
	MoggoDB       *mongoDB
	runtime_viper = viper.New()
)

func Init(service string) {
	// 从环境变量中获取 etcd 地址
	etcdAddr := os.Getenv("ETCD_ADDR")
	if etcdAddr == "" {
		logger.Fatalf("config.Init: etcd addr is empty")
	}
	logger.Infof("config.Init: etcd addr: %v", etcdAddr)
	Etcd = &etcd{Addr: etcdAddr}

	// use etcd for config save
	err := runtime_viper.AddRemoteProvider("etcd3", Etcd.Addr, "/config")
	if err != nil {
		logger.Fatalf("config.Init: add remote provider error: %v", err)
	}
	runtime_viper.SetConfigName("config")
	runtime_viper.SetConfigType("yaml")
	if err := runtime_viper.ReadRemoteConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			logger.Fatal("config.Init: could not find config files")
		} else {
			logger.Fatal("config.Init: read config error: %v", err)
		}
		logger.Fatal("config.Init: read config error: %v", err)
	}
	configMapping(service)
	// 持续监听配置
	runtime_viper.OnConfigChange(func(e fsnotify.Event) {
		logger.Infof("config: config file changed: %v\n", e.String())
	})
	runtime_viper.WatchConfig()
}

func configMapping(srv string) {
	c := new(config)
	if err := runtime_viper.Unmarshal(&c); err != nil {
		logger.Fatalf("config.configMapping: config: unmarshal error: %v", err)
	}

	Server = &c.Server
	Server.Secret = []byte(runtime_viper.GetString("server.jwt-secret"))
	MoggoDB = &c.MongoDB
	Service = GetService(srv)
}

func GetService(srvname string) *service {
	logger.Debugf("get service name: %v", srvname)
	addrlist := runtime_viper.GetStringSlice("services." + srvname + ".addr")
	logger.Debugf("get addrlist: %v", addrlist)

	return &service{
		Name:     runtime_viper.GetString("services." + srvname + ".name"),
		AddrList: addrlist,
		LB:       runtime_viper.GetBool("services." + srvname + ".load-balance"),
	}
}
