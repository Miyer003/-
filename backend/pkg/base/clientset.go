package base

import (
	"sync"

	"yunyiwang/pkg/db"
)

var (
	instance *ClientSet
	once     sync.Once
)

// ClientSet storage various client objects
// Notice: some or all of them maybe nil, we should check obj when use
type ClientSet struct {
	DBClient *db.Database // Database
	cleanups []func()     // Functions to clean resources
}

type Option func(clientSet *ClientSet)

// NewClientSet will be protected by sync.Once for ensure only 1 instance could be created in 1 lifecycle
func NewClientSet(opt ...Option) *ClientSet {
	once.Do(func() {
		var options []Option
		instance = &ClientSet{}
		options = append(options, opt...)
		for _, opt := range options {
			opt(instance)
		}
	})
	return instance
}

// Close iterates over all cleanup functions and calls them.
func (cs *ClientSet) Close() {
	for _, cleanup := range cs.cleanups {
		cleanup()
	}
}
