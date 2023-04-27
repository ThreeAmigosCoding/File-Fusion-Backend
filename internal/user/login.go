package user

import (
	"file-fusion-backend/internal/model"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
	"net/http"
)

func Login(context *gin.Context, session *session.Session) {
	var userLoginDto model.UserLoginDTO
	if err := context.ShouldBindJSON(&userLoginDto); err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	db := dynamodb.New(session)

	getInput := &dynamodb.GetItemInput{
		TableName: aws.String("user"),
		Key: map[string]*dynamodb.AttributeValue{
			"username": {
				S: aws.String(userLoginDto.Username),
			},
		},
	}

	getResult, err := db.GetItem(getInput)
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	if getResult.Item == nil {
		context.JSON(http.StatusNotFound, "Invalid username or password!")
		return
	}

	hashedPassword := getResult.Item["password"].S

	err = bcrypt.CompareHashAndPassword([]byte(*hashedPassword), []byte(userLoginDto.Password))
	if err != nil {
		context.JSON(http.StatusUnauthorized, "Invalid username or password!")
		return
	}

	context.JSON(http.StatusOK, gin.H{"message": "Login successful!"})
}
