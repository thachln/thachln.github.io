package controller

import (
	"crypto/sha256"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Sha256(c *gin.Context) {
	// single file
	f_header, err := c.FormFile("file")
	if err != nil {
		log.Fatal(err)
	}

	f_file, err := f_header.Open()
	if err != nil {
		log.Fatal(err)
	}

	h := sha256.New()
	if _, err := io.Copy(h, f_file); err != nil {
		log.Fatal(err)
	}

	sha256Code := fmt.Sprintf("%x", h.Sum(nil))

	c.String(http.StatusOK, sha256Code)
}
