<?php
/**
 * Mad Dogs Germany — einfache Kontaktformular-Verarbeitung.
 * ---------------------------------------------------------------
 * Voraussetzung: PHP-fähiges Webhosting (z. B. IONOS Webhosting).
 * Wird die Seite stattdessen auf einem reinen Static-Host betrieben
 * (Netlify, Vercel, GitHub Pages ...), funktioniert dieses Skript
 * NICHT — siehe README.md für Alternativen (Netlify Forms,
 * Formspree, Web3Forms). Das Frontend-Formular selbst benötigt in
 * jedem Fall nur eine erreichbare `action`-URL, die JSON im Format
 * { ok: true|false, message?, errors? } zurückgibt.
 *
 * Sicherheitsmaßnahmen:
 *   - Honeypot-Feld "website" (für Menschen unsichtbar/versteckt)
 *   - Server-seitige Validierung (nie nur aufs Frontend verlassen)
 *   - Keine Ausgabe von Nutzereingaben als HTML (kein XSS-Risiko)
 *   - Header-Injection verhindert (Zeilenumbrüche entfernt)
 *
 * TODO vor Live-Schaltung:
 *   - Empfänger-Adresse prüfen/bestätigen
 *   - Absender-Domain per SPF/DKIM autorisieren, damit mail()
 *     nicht im Spam landet (beim Hoster nachfragen)
 *   - Optional: Rate-Limiting / einfache Session-Prüfung ergänzen
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');

$recipient = 'info@mad-dogs-germany.de'; // TODO: Empfänger bei Bedarf anpassen

function respond(int $status, array $data): void
{
    http_response_code($status);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(405, ['ok' => false, 'message' => 'Methode nicht erlaubt.']);
}

// Honeypot: Bots füllen verstecktes Feld aus. Menschlichen Absendern
// wird ein stiller "Erfolg" vorgetäuscht, um Bots nicht zu verraten,
// dass sie erkannt wurden.
if (!empty($_POST['website'])) {
    respond(200, ['ok' => true, 'message' => 'Danke für deine Nachricht!']);
}

$name = trim((string) ($_POST['name'] ?? ''));
$email = trim((string) ($_POST['email'] ?? ''));
$message = trim((string) ($_POST['message'] ?? ''));
$consent = isset($_POST['consent']);

$errors = [];
if ($name === '') {
    $errors['name'] = 'Bitte Namen angeben.';
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Bitte eine gültige E-Mail-Adresse angeben.';
}
if ($message === '') {
    $errors['message'] = 'Bitte eine Nachricht eingeben.';
}
if (!$consent) {
    $errors['consent'] = 'Bitte der Datenverarbeitung zustimmen.';
}

if (!empty($errors)) {
    respond(422, ['ok' => false, 'errors' => $errors]);
}

// Header-Injection verhindern
$safeName = str_replace(["\r", "\n"], '', $name);
$safeEmail = str_replace(["\r", "\n"], '', $email);

$subject = 'Neue Kontaktanfrage über mad-dogs-germany.de';
$body = "Neue Nachricht über das Kontaktformular:\n\n"
    . "Name: {$safeName}\n"
    . "E-Mail: {$safeEmail}\n\n"
    . "Nachricht:\n{$message}\n";

$headers = "From: website@mad-dogs-germany.de\r\n"
    . "Reply-To: {$safeName} <{$safeEmail}>\r\n"
    . "Content-Type: text/plain; charset=UTF-8\r\n";

$sent = @mail($recipient, $subject, $body, $headers);

if (!$sent) {
    respond(500, [
        'ok' => false,
        'message' => 'Nachricht konnte nicht gesendet werden. Bitte versuche es später erneut oder kontaktiere uns direkt.',
    ]);
}

respond(200, [
    'ok' => true,
    'message' => 'Danke für deine Nachricht! Wir melden uns so schnell wie möglich.',
]);
