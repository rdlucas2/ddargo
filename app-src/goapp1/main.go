package main

import (
	"fmt"
	"net/http"

	"github.com/google/uuid"
)

func generateUUIDHandler(w http.ResponseWriter, r *http.Request) {
	randomUUID := uuid.New().String()
	fmt.Fprintf(w, "Random UUID: %s", randomUUID)
}

func main() {
	http.HandleFunc("/", generateUUIDHandler)

	fmt.Println("Server starting on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}
}