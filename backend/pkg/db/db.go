package db

import "go.mongodb.org/mongo-driver/mongo"

type Database struct {
	client *mongo.Client
}

func NewDatabase(client *mongo.Client) *Database {
	return &Database{
		client: client,
	}
}
