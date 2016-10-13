<html>
 <head>
  <title>Gasjet</title>
  <meta http-equiv="refresh" content="1; URL=http://ulpc24.gsi.de/gasjet/current.php">
 </head>
 <body>
<h1>
<center>
<p><br><p>
<a href="current.php">Dichte</a>: 
<?php
$datei = file("/var/www/gasjet-data/dichte.dat");

foreach($datei AS $ausgabe)
   {
	echo $ausgabe;
   }
?>
 Partikel/cm&sup2;
<p><br><p>
D&uumlsentemperatur: 
<?php
$datei = file("/var/www/gasjet-data/temp.dat");

foreach($datei AS $ausgabe)
   {
	echo $ausgabe;
   }
?>
 K
<p><br><p>
Gasgeschwindigkeit: 
<?php
$datei = file("/var/www/gasjet-data/vgas.dat");

foreach($datei AS $ausgabe)
   {
	echo $ausgabe;
   }
?>
 m/s
<p><br><p>
Druck in E1: 
<?php
$datei = file("/var/www/gasjet-data/e1.dat");

foreach($datei AS $ausgabe)
   {
	echo $ausgabe;
   }
?>
 mBar
</center><h5>
<div align="right">
<a href="index.php">zur&uuml;ck</a>
 </body>
</html>
