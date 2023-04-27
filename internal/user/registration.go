package main

//chage package and see what to do with them

var (
	tableName string = "user"
)

//func main() {
//	r := gin.Default()
//	r.POST("/users", func(context *gin.Context) {
//
//		var user model.User
//		if err := context.ShouldBindJSON(&user); err != nil {
//			context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
//			return
//		}
//		encryptedPassword, _ := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
//		user.Password = string(encryptedPassword)
//		//region Session and database
//		sess, err := session.NewSession(&aws.Config{
//			Region: aws.String("eu-central-1"),
//			Credentials: credentials.NewStaticCredentials(
//				shared.AccessKey,
//				shared.SecretAccessKey,
//				"", // leave it empty if you don't have one
//			),
//		})
//		if err != nil {
//			fmt.Println(err)
//			return
//		}
//		db := dynamodb.New(sess)
//		//endregion
//
//		//region Check if user with username exists
//		getInput := &dynamodb.GetItemInput{
//			TableName: aws.String(tableName),
//			Key: map[string]*dynamodb.AttributeValue{
//				"username": {
//					S: aws.String(user.Username),
//				},
//			},
//		}
//
//		getResult, err := db.GetItem(getInput)
//		if err != nil {
//			context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
//			return
//		}
//		if getResult.Item != nil {
//			context.JSON(http.StatusBadRequest, "Username already taken!")
//			return
//		}
//		//endregion
//
//		//region Writing to dynamoDb
//		item, err := dynamodbattribute.MarshalMap(user)
//		if err != nil {
//			context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
//			return
//		}
//
//		// Construct the PutItem input
//		input := &dynamodb.PutItemInput{
//			Item:      item,
//			TableName: aws.String("user"),
//		}
//
//		// Call the PutItem API
//		if _, err := db.PutItem(input); err != nil {
//			context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
//			return
//		}
//		//endregion
//
//		context.JSON(http.StatusOK, user)
//	})
//
//	if err := r.Run(":8080"); err != nil {
//		fmt.Println(err)
//	}
//}
