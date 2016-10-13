 <?php
// Mit den folgenden Zeilen lassen sich
// alle Dateien in einem Verzeichnis auslesen
$handle=opendir ("archiv");
echo "Verzeichnisinhalt:<br>";
while ($datei = readdir ($handle)) {
echo '<a href="archiv_plot.php?datei=',$datei,'">',$datei,'</a><br>';
}
closedir($handle);
?> 
