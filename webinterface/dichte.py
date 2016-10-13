from gasrechnungwi import *
import sys                

spfad = "/var/www/gasjet_neu/"
lpfad = "/var/www/gasjet-data/"
ldatei = "gasjet_neu.dat"
sdatei = "dichtetemp.dat" 

gasart = sys.argv[1]

dateianlegen = open(spfad+sdatei, 'w')
dateianlegen.close

if gasart == 'Helium':
            gas = Helium()

elif gasart == 'Neon':
            gas = Neon()

elif gasart == 'Argon':
            gas = Argon()

elif gasart == 'Krypton':
            gas = Krypton()

elif gasart == 'Xenon':
            gas = Xenon()

elif gasart == 'Wasserstoff':
            gas = Wasserstoff()

elif gasart == 'Deuterium':
            gas = Deuterium()

elif gasart == 'Stickstoff':
            gas = Stickstoff()


lese = open(lpfad+ldatei, 'r')
for line in lese: 
    laenge = len(line.rstrip().split(' '))
    if laenge == 17:
       zeit=str((line.rstrip().split(' '))[0])
       dichte = str(gas.rechne_dichte_aus(line))
       dichte = dichte.replace(",", " ")
       dichte = dichte.replace("(", "")
       dichte = dichte.replace(")", "")
       dichte = dichte.replace("'", "")
       dichte = dichte.replace("  ", " ")
       with open(spfad+sdatei, 'a') as schreib:
          schreib.write(zeit + ' ' + dichte + '\n')
schreib.close
