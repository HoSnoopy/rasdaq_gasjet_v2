<?php

exec ("/var/www/gasjet_neu/plot"); ?>
<center>
<img src="druck_e.png">

<?php
$path="/var/www/gasjet-data/";
$datei="gasjet_neu.dat";
$datei= $path . $datei;
$daten = file($datei);
$zeile = $daten[count($daten)-1];
$zerlegen = explode(" ", $zeile);
$e1 = $zerlegen[1];
$wwk = $zerlegen[9];
echo '<br>';
echo 'Druck in E1: ';
echo $e1;
echo ' mBar, Druck in WWK: ';
echo $wwk;
echo ' mBar </br>' ."\n";
?>

<img src="druck_s.png">

<?php
$path="/var/www/gasjet_neu/";

$gasart=$_GET["gasart"];
  if ($gasart == "Wasserstoff" || $gasart == "Helium" || $gasart == "Argon" || $gasart == "Neon" || $gasart == "Krypton" || $gasart == "Xenon" || $gasart == "Stickstoff")  {
    exec ("$path/plot_dichte $gasart");
    $datei="dichtetemp.dat";
    $datei= $path . $datei;
    $daten = file($datei);
    $zeile = $daten[count($daten)-1];
    $zerlegen = explode(" ", $zeile);
    $dichte = $zerlegen[1];
    $temperatur = $zerlegen[2];
    echo '<br>';
    echo 'Dichte: ';
    echo $dichte;
    echo ' Partikel/cm², D&uuml;sentemperatur: ';
    echo $temperatur;
    echo 'K </br>' ."\n";
  }  else {
    echo "<br><p><br>";
    echo "Es wurde keine Gasart gew&auml;hlt. Das Anzeigen der Dichte ist nicht m&ouml;glich."; 
    exec ("rm $path/tempdichte.png"); 
  }
?>
<img src="tempdichte.png">
<p><br><p>
<form action="gasjet.php">
<label>Gasart:
<select name="gasart">
<option>Wasserstoff</option>
<option>Helium</option>
<option>Neon</option>
<option>Argon</option>
<option>Krypton</option>
<option>Xenon</option>
<option>Stickstoff</option>
<input type="submit" value="Seite neu laden">
</select>
</label>
</form>
<?php
header("Refresh: 2; url=http://ulpc24.gsi.de/gasjet_neu/gasjet.php?gasart=$gasart");
?>
