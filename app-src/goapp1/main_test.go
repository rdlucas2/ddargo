package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"strings"
	"regexp"
)

func TestGenerateUUIDHandler(t *testing.T) {
	// Create a request to pass to our handler
	req, err := http.NewRequest("GET", "/", nil)
	if err != nil {
		t.Fatal(err)
	}

	// Create a ResponseRecorder to record the response
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(generateUUIDHandler)

	// Call the handler function directly and pass in our Request and ResponseRecorder
	handler.ServeHTTP(rr, req)

	// Check the status code is what we expect
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Check the response body contains "Random UUID: " followed by a valid UUID
	expectedPrefix := "Random UUID: "
	if !strings.HasPrefix(rr.Body.String(), expectedPrefix) {
		t.Errorf("handler returned unexpected body prefix: got %v want %v",
			rr.Body.String()[:len(expectedPrefix)], expectedPrefix)
	}

	// Extract the UUID part
	uuidPart := strings.TrimPrefix(rr.Body.String(), expectedPrefix)

	// Check if the UUID is valid
	uuidRegex := regexp.MustCompile(`^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[8|9|aA|bB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$`)
	if !uuidRegex.MatchString(uuidPart) {
		t.Errorf("handler returned invalid UUID: %v", uuidPart)
	}
}