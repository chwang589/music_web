package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/truemail-rb/truemail-go"
)

type ValidateRequest struct {
	Email string `json:"email"`
}

type ValidateResponse struct {
	Valid   bool   `json:"valid"`
	Email   string `json:"email"`
	Message string `json:"message"`
}

func main() {
	// Configure truemail
	configuration, err := truemail.NewConfiguration(
		truemail.ConfigurationAttr{
			// Verifier email address (should be your domain)
			VerifierEmail: "noreply@musicweb.com",
			// Optional: Add your email servers for better validation
			// SmtpSafeCheck: true,
		},
	)
	if err != nil {
		log.Fatal("Failed to create truemail configuration:", err)
	}

	http.HandleFunc("/validate", func(w http.ResponseWriter, r *http.Request) {
		// Enable CORS
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		if r.Method != "POST" {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req ValidateRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid JSON", http.StatusBadRequest)
			return
		}

		// Validate email using truemail
		result := truemail.IsValid(req.Email, configuration)

		response := ValidateResponse{
			Valid:   result,
			Email:   req.Email,
			Message: "Email validation completed",
		}

		if !result {
			response.Message = "Email is not valid or deliverable"
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"status": "healthy",
			"service": "email-validator",
		})
	})

	fmt.Println("Email validator service starting on :8001")
	log.Fatal(http.ListenAndServe(":8001", nil))
}