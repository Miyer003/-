package client

import (
	"context"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// MongoDB 初始化函数
func InitMongoDB(uri string) (*mongo.Client, error) {
	// 设置 MongoDB 的客户端连接选项
	clientOptions := options.Client().ApplyURI(uri)

	// 创建 MongoDB 客户端
	client, err := mongo.NewClient(clientOptions)
	if err != nil {
		return nil, err
	}

	// 创建一个带超时的上下文
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// 连接到 MongoDB
	err = client.Connect(ctx)
	if err != nil {
		return nil, err
	}

	// 验证连接
	err = client.Ping(ctx, nil)
	if err != nil {
		return nil, err
	}

	return client, nil
}
