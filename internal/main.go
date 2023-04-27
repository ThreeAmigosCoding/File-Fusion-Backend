package main

import (
	"file-fusion-backend/internal/handler"
	"file-fusion-backend/shared"
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/gin-gonic/gin"
)

func main() {
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("eu-central-1"),
		Credentials: credentials.NewStaticCredentials(
			shared.AccessKey,
			shared.SecretAccessKey,
			"",
		),
	})
	if err != nil {
		fmt.Println(err)
		return
	}

	router := gin.Default()

	handler.Handle(router, sess)

	err = router.Run(":8080")
	if err != nil {
		return
	}

}
