package handler

import (
	"file-fusion-backend/internal/multimedia"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/gin-gonic/gin"
)

func Handle(router *gin.Engine, awsSession *session.Session) {
	router.POST("/upload-file/:username", func(context *gin.Context) {
		multimedia.UploadFile(context, awsSession)
	})
}
