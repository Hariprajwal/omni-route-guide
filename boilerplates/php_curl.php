<?php

// OmniRoute Local Server Endpoint
$api_url = "http://localhost:20128/v1/chat/completions";

// Headers: OmniRoute mimics OpenAI, so we pass a dummy Bearer token
$headers = [
    "Content-Type: application/json",
    "Authorization: Bearer dummy-key"
];

// Payload
$data = [
    "model" => "felo/auto", // Explicitly use the free keyless Felo provider
    "stream" => false,      // Set to true if you want a streaming response
    "messages" => [
        [
            "role" => "user",
            "content" => "Hello! What can you do?"
        ]
    ]
];

// Initialize cURL
$ch = curl_init($api_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

echo "Sending request to OmniRoute...\n";

// Execute the request
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if (curl_errno($ch)) {
    echo "cURL Error: " . curl_error($ch) . "\n";
} else {
    $result = json_decode($response, true);
    
    if ($http_code == 200) {
        echo "\n--- Response ---\n";
        echo $result['choices'][0]['message']['content'] . "\n";
    } else {
        echo "Error HTTP $http_code\n";
        echo "Server replied: $response\n";
    }
}

curl_close($ch);
?>
