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

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "OK")
}

func readyHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Ready")
}

func main() {
	http.HandleFunc("/", generateUUIDHandler)
	http.HandleFunc("/healthz", healthzHandler)
	http.HandleFunc("/ready", readyHandler)

	fmt.Println("Server starting on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}
}