package template

import "go.mongodb.org/mongo-driver/mongo"

type DBTemplate struct {
	client *mongo.Client
}

func NewDBTemplate(client *mongo.Client) *DBTemplate {
	return &DBTemplate{
		client: client,
	}
}
