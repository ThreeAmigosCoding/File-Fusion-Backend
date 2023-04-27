package model

import "time"

type User struct {
	Name        string    `json:"name"`
	LastName    string    `json:"lastName"`
	Username    string    `json:"username"`
	Email       string    `json:"email"`
	Password    string    `json:"password"`
	DateOfBirth time.Time `json:"dateOfBirth"`
}

type UserLoginDTO struct {
	Username string `json:"username"`
	Password string `json:"password"`
}
