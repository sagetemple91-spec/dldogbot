<?php
// ===========================================
// 🌐 DL LookUp Bot — NowPayments Webhook Handler
// ===========================================

// Telegram Bot Token
$bot_token = "8345132951:AAEbG31cfstAflhNaBqkieSrF5KF7KU_-eQ";
$telegram_api_url = "https://api.telegram.org/bot$bot_token/sendMessage";

// Log file for debugging
$log_file = __DIR__ . "/payment_log.txt";

// Read raw POST body from NowPayments
$raw_post = file_get_contents("php://input");
$data = json_decode($raw_post, true);

// Log all webhook requests
file_put_contents($log_file, "[" . date("Y-m-d H:i:s") . "] " . $raw_post . PHP_EOL, FILE_APPEND);

// Validate payload
if (!isset($data['payment_status']) || !isset($data['order_id'])) {
    http_response_code(400);
    echo "Invalid payload";
    exit;
}

$status = strtolower($data['payment_status']);
$order_id = $data['order_id'];
$amount = $data['price_amount'] ?? 0;

// Extract Telegram user ID (e.g. "user_123456789")
if (strpos($order_id, "user_") === 0) {
    $user_id = intval(str_replace("user_", "", $order_id));
} else {
    http_response_code(400);
    echo "Invalid order_id format";
    exit;
}

// ✅ If payment confirmed or finished
if ($status === "finished" || $status === "confirmed") {
    $message = "🎉 *Payment Confirmed!*\n\n💰 Amount: \$$amount\n✅ Status: *$status*\n\nYour wallet has been credited successfully. Enjoy your lookup!";
    
    $payload = [
        'chat_id' => $user_id,
        'text' => $message,
        'parse_mode' => 'Markdown'
    ];
    
    $ch = curl_init($telegram_api_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_exec($ch);
    curl_close($ch);
}

http_response_code(200);
echo "OK";
?>
