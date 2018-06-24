SMART HOME-ino
===============
F�r die Veranstaltung Grundlagen der Informatik II haben wir uns vorgenommen als Projekt ein Smart-Home zu konstruieren. Durch die vielen unterschiedlichen Bauelemente in einem Arduino Kit haben wir uns erhofft ein sehr umfangreiches Smart-Home mit vielen Funktionen zu erstellen. Desweiteren sollte das Smart-Home f�r die Nutzer eine einfache Benutzeroberfl�che zur Verf�gung stellen, die wir �ber Python programmieren.

Die Funktionen des Smart Homes belaufen sich auf folgendes:

1.	RGB Lichter steuerung, mittels Farbauswahl an einem farbrad (color chooser)

2.	Alarmanlagen steuerung und benachrichtigung mittels email bei ausschlag

Lichtsteuerung
---------
Die Funktion erm�glicht die Steuerung einer RGB-LED �ber die Python programmierte Benutzeroberfl�che. Der Nutzer hat die M�glichkeit die RGB-LED ein- und auszuschalten. Zus�tzlich kann man sie in jeder m�glichen Farbe aufleuchten lassen. Bei der Auswahl einer Farbe werden die dazugeh�rigen Grundfarben Rot, Gr�n und Blau mit Werten von 0 bis 255 von Python an das Arduino weitergeleitet. Anschlie�end wird der von den Werten abh�ngige Strom �ber die jeweiligen Pins an die RGB-LED gesendet und bilden die ausgew�hlte Farbe. �ber den �Off-Button� l�sst sich die Lampe ausschalten, indem die Werte der Grundfarben an den Pins auf 0 gesetzt werden und kein Strom an der RGB-LED ankommt.


Alarmanlage
---------
Das Alarmsystem besteht in unserem Smart-Home aus einem Bewegungsmelder, der RGB-LED, und einem Piezo (Buzzer). �ber die Benutzeroberfl�che kann das Alarmsystem an- und ausgeschalten werden. Wenn das Alarmsystem angeschalten ist und der Bewegungsmelder ausschl�gt, sendet der Arduino an Python ein Signal, dass der Alarm ausgel�st wurde. Infolge dessen setzt der Arduino die RGB-LED auf die Farbe Rot, die als Alarmsignal dienen soll und aktiviert den Piezo, welcher Alarmt�ne von sich gibt. Der Alarm kann �ber die Benutzeroberfl�che wieder ausgeschaltet werden und die RGB-LED nimmt die vorherige Farbe wieder an. Als Addition des Ganzen wird der Benutzer des Systems per E-Mail benachrichtigt, sobald der Alarm ausgel�st wird.


Erweiterungsm�glichkeiten
---------
	Bei der Erweiterung des Programmes sind einem eigentlich keine Grenzen gesetzt.
	Hier sind einige Ideen, welche wir leider nicht mehr realisieren konnten:
	*	Funktion zur erkennung von offenen Fenstern und/oder T�ren
	*	Steuerung der Stromzufuhr von einigen Elektrischen Gegenst�nden im Haus
	*	Eine benutzung �ber ein Smart Phone, mittels einer Python App

Entwickler
---------
 *	Okan Dogtas (4450377)
 *	Sercan Eyig�n (4444473)
 *	Manuel Schendel (4446837)


