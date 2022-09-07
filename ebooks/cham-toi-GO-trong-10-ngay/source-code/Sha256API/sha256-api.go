package main

import (
	"mks.com.vn/checksha256/v/controller"

	"github.com/gin-gonic/gin"
)

func setupRouter() *gin.Engine {
	router := gin.Default()
	router.Static("/public", "./public")

	client := router.Group("/check")
	{
		client.POST("/sha256", controller.Sha256)

	}

	return router
}
func main() {
	r := setupRouter()
	r.Run(":8080")
}
