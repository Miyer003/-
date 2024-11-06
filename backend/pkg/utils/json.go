package utils

import (
	"encoding/json"
)

func JSONEncode(v interface{}) (string, error) {
	data, err := json.Marshal(v)
	if err != nil {
		return "", err
	}
	return string(data), nil
}
