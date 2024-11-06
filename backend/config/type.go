package config

type server struct {
	Secret  []byte
	Version string
	Name    string
}

type service struct {
	Name     string
	AddrList []string
	LB       bool `mapstructure:"load-balance"`
}

type mongoDB struct {
	Addr string
}

type etcd struct {
	Addr string
}

type config struct {
	Server  server
	Etcd    etcd
	MongoDB mongoDB
}
