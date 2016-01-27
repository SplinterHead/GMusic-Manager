<?php

$pdo = new PDO('sqlite::memory:');

def collect_all_songs() {
    $results = $db->query('SELECT * FROM songs');
    while ($row = $results->fetchArray()) {
        var_dump($row);
    }
}

collect_all_songs();
