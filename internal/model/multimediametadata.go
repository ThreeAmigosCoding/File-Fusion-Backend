package model

import "time"

type MultimediaMetadata struct {
	Id          string    `json:"id"`
	Name        string    `json:"name"`
	Type        string    `json:"type"`
	SizeInKB    float32   `json:"sizeInKB"`
	CreatedAt   time.Time `json:"createdAt"`
	LastChanged time.Time `json:"lastChanged"`
	Username    string    `json:"username"`
}

func NewMultimediaMetadata(id string, name string, Type string, sizeInKB float32,
	createdAt time.Time, lastChanged time.Time, username string) *MultimediaMetadata {
	return &MultimediaMetadata{
		Id:          id,
		Name:        name,
		Type:        Type,
		SizeInKB:    sizeInKB,
		CreatedAt:   createdAt,
		LastChanged: lastChanged,
		Username:    username}
}
