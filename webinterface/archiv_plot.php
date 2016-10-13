<?php
$datei= $_GET["datei"];
$temp=fopen("/tmp/gasjet_archiv","w");
fwrite($temp, $datei);
fclose($temp);
$shellscript= "/var/www/gasjet/archiv_plot";
shell_exec($shellscript);
//sleep (5);
?>
<html>
<img src="archiv_druck.png">
<img src="archiv_tempdichte.png">
<br><p><br>
<a href="archiv.php">Zur&uuml;ck</a>
</html>
