<?php
header('Content-Type: application/json');

// Get the raw POST data
$json = file_get_contents('php://input');
$data = json_decode($json, true);

if ($data === null) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON data']);
    exit;
}

// Save to file
file_put_contents('./wallet-data.json', json_encode($data, JSON_PRETTY_PRINT));

echo json_encode(['success' => true]);
?>