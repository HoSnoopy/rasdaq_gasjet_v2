#!/usr/bin/python
#coding: utf-8

# Einfaches Pythonscript zum Auslesen von 2 MCP3208-ADC-Wandlern (insgesamt 16 Kanaele) per SPI-Interface (NICHT GPIO!)
# Ich habe als Referenzspannung 3,3V, die per Spannungsteiler von max. 10V heruntergebrochen werden.

import spidev
import time
import datetime
import math
import sys
import zmq
import os

# Temperatursensor 
#TC        = 2.000 # max 20K bei 10V
#TC        = 10.00 # max 100K bei 10V
#TC        = 15.00 # max 150K bei 10V
TC         = 30.0 # max 300K bei 10V

# Einlaßdrucksensor
PE         = 10.0 #max. 100Bar bei 10V

spi = spidev.SpiDev()

# Frequenz des SPI-Busses. Maximal 5000000, geht man drueber, kommen unsinnige Werte heraus.

datei = '/opt/data/gasjet_neu.dat'
archiv = '/opt/data/archive/'
herz = 1000
warte = 0.9

dat = open(datei, 'w')
dat.close

#ZMQ-Socket zum Senden der Werte an andere Programme

host = "192.168.10.4"
port = 10000
thema = '10001'
context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://{}:{}".format(host, port))


# umrechnen der werte in ein schoeneres Format und in einen String
def eformat(f, prec, exp_digits):
    s = "%.*e" % (prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d" % (mantissa, exp_digits + 1, int(exp))

# umrechnen der Spannung in einen Druckwert
def ionivac(wert):
    u = float(wert)
    p = 10 ** (u - 12)
    p = eformat(p, 2, 2)
    return (p)


# umrechnen der Spannung in einen Druckwert
def widerange(wert):
    u = float(wert)
    p = 10 ** ((u - 7.75) / (0.75))
    p = eformat(p, 2, 2)
    return (p)


# umrechnen der Spannung in einen Temperaturwert
def temperatur(wert):
    u = float(wert)
    t = TC * u
    if t < 3:   #wenn Temperatur unter 3K liegt, ist vmtl. die Kühlung ausgeschaltet => Düse hat Raumtemperatur
       t = 300
    t = str(t)
    return (t)

#umrechnen der Spannung in einen Druckwert/Einlassdruck
def edruck(wert):
    u = float(wert)
    p = PE * u
    p = str(p)
    return (p)

while True:
   ts = time.time()
   uhrzeit = str(datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S'))
   if uhrzeit <> '23:59:59':  #schreibe in aktuelle datei bis der Tag vorbei ist
    try:
        zeile = []
        for s in range(2):
            spi.open(0, s)  # oeffnen des einen oder anderen MCP3208
#            spi.max_speed_hz = (herz)
            for c in range(8):
                # Bestimmung des Kommandos zum Empfangen der einzelnen Kanaele. Siehe dazu auch https://github.com/xaratustrah/rasdaq
                if c < 4:
                    com1 = 0x06
                    com2 = c * 0x40
                else:
                    com1 = 0x07
                    com2 = (c - 4) * 0x40

                antwort = spi.xfer([com1, com2, 0])

                val = ((antwort[1] << 8) + antwort[2])  # Interpretieren der Antwort
                val = int(val)
                u = val * 0.002441406
                zeile.append(str(u))
            spi.close()
        # herausschreiben und Umrechnung der Spannungswerte am Ende der 16 eingelesenen Kanaele
        ts = time.time()
        ausgang = (str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')) + ' ')  # Zeitskala
        ausgang = (ausgang + (widerange(zeile[0])) + ' ') #E1 an Kanal1 von ADC1
        ausgang = (ausgang + (widerange(zeile[1])) + ' ') #E2 an Kanal2 von ADC1
        ausgang = (ausgang + (widerange(zeile[2])) + ' ') #E3 an Kanal3 von ADC1
        ausgang = (ausgang + (ionivac(zeile[3])) + ' ')   #E4 an Kanal4 von ADC1
        ausgang = (ausgang + (widerange(zeile[4])) + ' ') #S1 an Kanal5 von ADC1
        ausgang = (ausgang + (widerange(zeile[5])) + ' ') #S2 an Kanal6 von ADC1
        ausgang = (ausgang + (ionivac(zeile[6])) + ' ')   #S3 an Kanal7 von ADC1
        ausgang = (ausgang + (ionivac(zeile[7])) + ' ')   #S4 an Kanal8 von ADC1
        ausgang = (ausgang + (ionivac(zeile[8])) + ' ') #WWK an Kanal1 von ADC2
        ausgang = (ausgang + (temperatur(zeile[9])) + ' ') #Düsentemp an Kanal2 von ADC2
        ausgang = (ausgang + (edruck(zeile[10])) + ' ') #Einlassdruck
        ausgang = (ausgang + (zeile[11]) + ' ')   #Eingang noch nicht belegt
        ausgang = (ausgang + (zeile[12]) + ' ')   #Eingang noch nicht belegt
        ausgang = (ausgang + (zeile[13]) + ' ')   #Eingang noch nicht belegt
        ausgang = (ausgang + (zeile[14]) + ' ')   #Eingang noch nicht belegt
        ausgang = (ausgang + (zeile[15]) + ' ')   #Eingang noch nicht belegt
        ausgang = ausgang[:-1]

#Den zu sendenden ZMQ-Block vorbereiten
        socketblock = ausgang[20:] 
        socketblock = socketblock.replace(" ", ",")
        ausgang = (ausgang + '\n')
        with open(datei, 'a') as d:
            d.write(ausgang)
        sock.send_string("{} {}".format(thema, (str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S'))+" "+ socketblock)))
        time.sleep(warte)

    except (KeyboardInterrupt, SystemExit):
        # except:
        break
   else:  #lege am Ende des Tages neue Datei und verschiebe die "alte" ins Archiv
    ts = time.time()
    dateizeit = str(datetime.datetime.fromtimestamp(ts).strftime('%Y_%m-%d-%H_%M_%S'))
    archivname = (archiv + 'gasjet-' + dateizeit + '.dat')
    os.rename(datei, archivname)
    dat = open(datei, 'w')
    dat.close
