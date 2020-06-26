package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	// Get environment variables from .env file
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}

	// Get port from environment variable if exists
	// Default port is 8080
	port := ""
	if port = os.Getenv("PORT"); port == "" {
		port = "8080"
	}

	// Endpoint route
	http.HandleFunc("/", Handler)

	// Print and run the server
	fmt.Println(fmt.Sprintf("Server is running on PORT:%s", port))
	if err := http.ListenAndServe(fmt.Sprintf(":%s", port), nil); err != nil {
		log.Fatal(err.Error())
	}
}

// JSON response struct
type Configuration struct {
	UserPersistenceServicePostgresURI string `json:"USER_PERSISTENCE_SERVICE_POSTGRES_URI"`
	UserPersistenceServiceRedisURI    string `json:"USER_PERSISTENCE_SERVICE_REDIS_URI"`
}

// Endpoint handler
func Handler(w http.ResponseWriter, r *http.Request) {
	// Set json content type
	w.Header().Set("Content-Type", "application/json")

	// Get configurations from .env file
	configuration := Configuration{
		UserPersistenceServicePostgresURI: os.Getenv("USER_PERSISTENCE_SERVICE_POSTGRES_URI"),
		UserPersistenceServiceRedisURI:    os.Getenv("USER_PERSISTENCE_SERVICE_REDIS_URI"),
	}

	// Return json response
	json.NewEncoder(w).Encode(configuration)
}
