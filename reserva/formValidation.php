<?php

$name = $_POST['name'] ?? '';
$email = $_POST['email'] ?? '';
$phone = $_POST['phone'] ?? '';
$date = $_POST['date'] ?? '';
$time = $_POST['time'] ?? '';
$room = $_POST['room'] ?? '';
$assistants = $_POST['assistants'] ?? 0;
$usercode = $_POST['usercode'] ?? '';
$promo = $_POST['promo'] ?? '';
$policy = isset($_POST['policy']);
$resources = isset($_POST['resources']) ? $_POST['resources'] : [];

if (preg_match('/^[a-zA-Z ]+$/', $name)) {
    echo "Name: $name (Correct)<br>";
} else {
    echo "Name: $name (Invalid)<br>";
}

if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Email: $email (Correct)<br>";
} else {
    echo "Email: $email (Invalid)<br>";
}

if (preg_match('/^[6789][0-9]{8}$/', $phone)) {
    echo "Phone: $phone (Correct)<br>";
} else {
    echo "Phone: $phone (Invalid)<br>";
}

$today = date('Y-m-d');
$tomorrow = date('Y-m-d', strtotime('+1 day'));

if ($date > $today && $date >= $tomorrow) {
    echo "Date: $date (Correct)<br>";
} else {
    echo "Date: $date (Invalid)<br>";
}

if (!empty($time)) {
    echo "Time: $time (Correct)<br>";
} else {
    echo 'Time: Invalid<br>';
}

if ($assistants >= 1 && $assistants <= 6) {
    if ($room === 'silence' && $assistants <= 3) {
        echo 'Room: Silence (Correct)<br>';
    } elseif ($room === 'group' && $assistants <= 6) {
        echo 'Room: Group (Correct)<br>';
    } else {
        echo 'Room: Capacity exceeded (Invalid)<br>';
    }

    echo "Assistants: $assistants (Correct)<br>";
} else {
    echo "Assistants: $assistants (Invalid)<br>";
}

if (empty($resources)) {
    echo 'Resources: None (Correct)<br>';
} else {
    echo 'Resources: ' . implode(', ', $resources) . ' (Correct)<br>';
}

if (preg_match('/^[A-Z]{2}[0-9]{6}$/', $usercode)) {
    echo "User code: $usercode (Correct)<br>";
} else {
    echo "User code: $usercode (Invalid)<br>";
}

if (empty($promo)) {
    echo 'Promo code: None (Correct)<br>';
} else {
    echo "Promo code: $promo (Applied)<br>";
}

if ($policy) {
    echo 'Policy: Accepted (Correct)<br>';
} else {
    echo 'Policy: Not accepted (Invalid)<br>';
}
