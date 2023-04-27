package handler

import (
	"file-fusion-backend/internal/multimedia"
	"file-fusion-backend/internal/user"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/gin-gonic/gin"
)

func Handle(router *gin.Engine, awsSession *session.Session) {
	router.POST("/register", func(context *gin.Context) {
		user.Register(context, awsSession)
	})

	router.POST("/login", func(context *gin.Context) {
		user.Login(context, awsSession)
	})

	router.POST("/upload-file/:username", func(context *gin.Context) {
		multimedia.UploadFile(context, awsSession)
	})
}
