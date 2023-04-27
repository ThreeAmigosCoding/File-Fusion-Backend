package model

type User struct {
	Name        string `json:"name"`
	LastName    string `json:"lastName"`
	Username    string `json:"username"`
	Email       string `json:"email"`
	Password    string `json:"password"`
	DateOfBirth string `json:"dateOfBirth"`
}
