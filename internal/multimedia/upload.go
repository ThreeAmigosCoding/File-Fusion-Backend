package multimedia

import (
	"file-fusion-backend/internal/model"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/gin-gonic/gin"
	"mime/multipart"
	"net/http"
	"path/filepath"
	"time"
)

func UploadFile(context *gin.Context, session *session.Session) {
	username := context.Param("username")

	file, err := context.FormFile("file")
	if err != nil {
		context.JSON(http.StatusBadRequest, err)
		return
	}
	extension := filepath.Ext(file.Filename)

	multimedia := model.NewMultimediaMetadata(username+"-"+file.Filename, file.Filename, extension,
		float32(file.Size/1024), time.Now(), time.Now(), username)

	//region DynamoDB
	db := dynamodb.New(session)
	item, err := dynamodbattribute.MarshalMap(multimedia)
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	input := &dynamodb.PutItemInput{
		Item:      item,
		TableName: aws.String("multimedia_metadata"),
	}

	if _, err := db.PutItem(input); err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	//endregion

	//region S3 Bucket
	fileData, err := file.Open()
	if err != nil {
		context.JSON(http.StatusInternalServerError, err)
		return
	}
	defer func(fileData multipart.File) {
		err := fileData.Close()
		if err != nil {

		}
	}(fileData)

	svc := s3.New(session)

	// Create a new S3 object
	_, err = svc.PutObject(&s3.PutObjectInput{
		Body:   fileData,
		Bucket: aws.String("multimedia-cloud-storage"), // replace with your bucket name
		Key:    aws.String(username + "/" + file.Filename),
	})
	if err != nil {
		context.JSON(http.StatusInternalServerError, err)
		return
	}
	//endregion

	context.JSON(http.StatusOK, gin.H{
		"message": "File uploaded successfully",
	})

}
