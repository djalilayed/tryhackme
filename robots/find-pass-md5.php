<?php
// script used on tryhackme room Robots https://tryhackme.com/room/robots
// script to find the correct password based on givem double md5 hash for password of form username+dd+mm
// Youtube walk through: https://youtu.be/ZAylF3vSzzQ

$target_hash = "dfb35334bf2a1338fa40e5fbb4ae4753";
$username = "rgiskard";
for ($month = 1; $month <= 12; $month++) {
    for ($day = 1; $day <= 31; $day++) {
        $ddmm = sprintf("%02d%02d", $day, $month);
        $inner_hash = md5($username . $ddmm);
        $test_hash = md5($inner_hash);
        if ($test_hash === $target_hash) {
            echo "Found: $ddmm (Inner: $inner_hash, Double: $test_hash)\n";
            exit;
        }
    }
}
echo "No match found\n";
?>
