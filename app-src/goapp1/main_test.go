package main

import (
	"net/http"
	"net/http/httptest"
	"regexp"
	"strings"
	"testing"
)

var statusCodeResponse = "handler returned wrong status code: got %v want %v"

// TestGenerateUUIDHandler tests the / endpoint which generates a random UUID.
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
		t.Errorf(statusCodeResponse,
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

// TestHealthzHandler tests the /healthz endpoint which checks the liveness of the service.
func TestHealthzHandler(t *testing.T) {
	// Create a request to pass to our handler
	req, err := http.NewRequest("GET", "/healthz", nil)
	if err != nil {
		t.Fatal(err)
	}

	// Create a ResponseRecorder to record the response
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(healthzHandler)

	// Call the handler function directly and pass in our Request and ResponseRecorder
	handler.ServeHTTP(rr, req)

	// Check the status code is what we expect
	if status := rr.Code; status != http.StatusOK {
		t.Errorf(statusCodeResponse,
			status, http.StatusOK)
	}

	// Check the response body is what we expect
	expected := "OK"
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v",
			rr.Body.String(), expected)
	}
}

// TestReadyHandler tests the /ready endpoint which checks the readiness of the service.
func TestReadyHandler(t *testing.T) {
	// Create a request to pass to our handler
	req, err := http.NewRequest("GET", "/ready", nil)
	if err != nil {
		t.Fatal(err)
	}

	// Create a ResponseRecorder to record the response
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(readyHandler)

	// Call the handler function directly and pass in our Request and ResponseRecorder
	handler.ServeHTTP(rr, req)

	// Check the status code is what we expect
	if status := rr.Code; status != http.StatusOK {
		t.Errorf(statusCodeResponse,
			status, http.StatusOK)
	}

	// Check the response body is what we expect
	expected := "Ready"
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v",
			rr.Body.String(), expected)
	}
}
