#!/bin/bash

# Set the API URL (change the port if necessary)
BASE_URL="http://localhost:8000"

# Sample news URL to test
NEWS_URL="https://techcrunch.com/2024/09/04/boeing-and-nasa-prepare-to-bring-starliner-home-without-its-crew-on-friday/"

# Specific article ID to test
SPECIFIC_ARTICLE_ID="a830d26d-969c-4295-ad5a-9f379137fef6"

# Function to make a request and log the response
make_request() {
    local endpoint=$1
    local method=$2
    local data=$3
    local start_time=$(date +%s.%N)
    
    echo "Testing $method $endpoint"
    response=$(curl -s -X $method "$BASE_URL$endpoint" \
        -H "Content-Type: application/json" \
        -d "$data" \
        -w "\nStatus code: %{http_code}\nTime: %{time_total}s\n")
    
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc)
    
    echo "$response"
    echo "Total script time for this request: ${duration}s"
    echo "----------------------------------------"
}

# Test POST /news/submit (first submission)
echo "1. Submitting a news article"
submit_response=$(make_request "/news/submit" "POST" "{\"url\": \"$NEWS_URL\"}")
article_id=$(echo "$submit_response" | grep -o '"id": "[^"]*' | cut -d'"' -f4)

# Test POST /news/submit (second submission of the same article)
echo "2. Submitting the same news article again"
make_request "/news/submit" "POST" "{\"url\": \"$NEWS_URL\"}"

# Test GET /news (list articles)
echo "3. Listing news articles"
make_request "/news?skip=0&limit=10" "GET"

# Test GET /news/{article_id} (get specific article from submission)
if [ ! -z "$article_id" ]; then
    echo "4. Getting specific news article from submission"
    make_request "/news/$article_id" "GET"
else
    echo "Skipping specific article test as no article ID was returned from submission."
fi

# Test GET /news/{article_id} (get specific article with predefined UUID)
echo "5. Getting specific news article with predefined UUID"
make_request "/news/$SPECIFIC_ARTICLE_ID" "GET"

echo "Test script completed."