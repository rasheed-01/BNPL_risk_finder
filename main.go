package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

type BNPLRequest struct {
	PurchaseAmount   float64 `json:"purchase_amount"`
	PastFraudReports int     `json:"past_fraud_reports"`
	SocialScore      int     `json:"social_score"`
}

type RiskResponse struct {
	Score    int    `json:"score"`
	Grade    string `json:"grade"`
	Decision string `json:"decision"`
}

func main() {
	r := gin.Default()

	r.POST("/bnpl-check", func(c *gin.Context) {
		var req BNPLRequest
		if err := c.BindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input"})
			return
		}

		jsonData, _ := json.Marshal(req)
		resp, err := http.Post("http://localhost:5001/risk", "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to contact ML engine"})
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		var risk RiskResponse
		json.Unmarshal(body, &risk)

		c.JSON(http.StatusOK, risk)
	})

	r.Run(":8080")
}
