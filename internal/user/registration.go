package main

//chage package and see what to do with them

import (
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	"github.com/gin-gonic/gin"
	"net/http"
)

type User struct {
	Name     string `json:"name"`
	LastName string `json:"last_name"`
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

func main() {
	r := gin.Default()
	r.POST("/users", func(context *gin.Context) {

		var user User
		if err := context.ShouldBindJSON(&user); err != nil {
			context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		sess, err := session.NewSession(&aws.Config{
			Region: aws.String("eu-central-1"),
			Credentials: credentials.NewStaticCredentials(
				"AKIASBHDTYUR3QIMSNY7",
				"f0Ub63ziRlfMKykcKPy5b3Hw75NGVcLGmTMAmtnJ",
				"", // leave it empty if you don't have one
			),
		})
		if err != nil {
			fmt.Println(err)
			return
		}
		svc := dynamodb.New(sess)

		item, err := dynamodbattribute.MarshalMap(user)
		if err != nil {
			context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		// Construct the PutItem input
		input := &dynamodb.PutItemInput{
			Item:      item,
			TableName: aws.String("user"),
		}

		// Call the PutItem API
		if _, err := svc.PutItem(input); err != nil {
			context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		context.JSON(http.StatusOK, user)
	})

	if err := r.Run(":8080"); err != nil {
		fmt.Println(err)
	}
}
