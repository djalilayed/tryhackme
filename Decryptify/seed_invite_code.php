<?php
/**
 * script for tryhackme room Decryptify https://tryhackme.com/room/decryptify
 * Script generated with assistance of ChatGPT
 * video walk through: https://youtu.be/g1yGPDJjo9I
 * Calculates the seed value for invite code generation.
 *
 * The algorithm is:
 *    seed = hexdec( (string)( strlen($email) + $constant_value + hexdec(substr($email, 0, 8)) ) )
 *
 * @param string $email
 * @param int    $constant_value
 * @return int
 */
function calculate_seed_value($email, $constant_value) {
    $email_length = strlen($email);
    $email_hex = hexdec(substr($email, 0, 8));
    $sum = $email_length + $constant_value + $email_hex;
    // Convert the numeric sum to string, then interpret it as hex.
    $seed_value = hexdec((string)$sum);
    return $seed_value;
}

/**
 * Given a seed value, initializes mt_rand and returns the generated random number.
 *
 * @param int $seed_value
 * @return int
 */
function generate_mt_rand_output($seed_value) {
    mt_srand($seed_value);
    return mt_rand();
}

// ---------- Step 1: Recover the constant using known invite for alpha@fake.thm ----------

// Known values from the log for alpha@fake.thm:
$alpha_email = "alpha@fake.thm";
$alpha_invite_b64 = "MTM0ODMzNzEyMg=="; // Invite code for alpha@fake.thm from the log
// Decode the invite code to get the mt_rand() output.
$alpha_mt_rand_output = (int) base64_decode($alpha_invite_b64);

// From php_mt_seed, you obtained the seed that produced alpha's mt_rand() output:
$alpha_seed = 1324931; 

// Calculate the email-derived portion (without applying hexdec to the entire sum):
$alpha_email_length = strlen($alpha_email);
$alpha_email_hex = hexdec(substr($alpha_email, 0, 8));
$alpha_email_part = $alpha_email_length + $alpha_email_hex;

// The original seed was generated as:
//    alpha_seed = hexdec( (string)($alpha_email_part + constant_value) )
// To invert hexdec, convert the seed back to its hex string and interpret that as a decimal number:
$A = (int) dechex($alpha_seed);
// Now, recover the constant:
$constant_value = $A - $alpha_email_part;
echo "Recovered constant: $constant_value\n";

// ---------- Step 2: Generate invite code for hello@fake.thm using the recovered constant ----------

$target_email = "hello@fake.thm";
$target_seed = calculate_seed_value($target_email, $constant_value);
$target_mt_rand = generate_mt_rand_output($target_seed);
$target_invite_code = base64_encode($target_mt_rand);

echo "Invite code for $target_email is: $target_invite_code\n";
?>
