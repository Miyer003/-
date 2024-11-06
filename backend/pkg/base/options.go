package base

import (
	"context"

	"yunyiwang/pkg/base/client"
	"yunyiwang/pkg/db"
	"yunyiwang/pkg/logger"
)

// WithDBClient will create database object
func WithDBClient(addr string) Option {
	return func(clientSet *ClientSet) {
		DB, err := client.InitMongoDB(addr)
		if err != nil {
			logger.Fatal("init database failed, err: %v", err)
		}

		clientSet.DBClient = db.NewDatabase(DB)
		clientSet.cleanups = append(clientSet.cleanups, func() {
			err = DB.Disconnect(context.Background())
			if err != nil {
				logger.Errorf("close DB failed, err: %v", err)
			}
		})
	}
}
