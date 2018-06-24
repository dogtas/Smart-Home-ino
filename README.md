SMART HOME-ino
===============
Für die Veranstaltung Grundlagen der Informatik II haben wir uns vorgenommen als Projekt ein Smart-Home zu konstruieren. Durch die vielen unterschiedlichen Bauelemente in einem Arduino Kit haben wir uns erhofft ein sehr umfangreiches Smart-Home mit vielen Funktionen zu erstellen. Desweiteren sollte das Smart-Home für die Nutzer eine einfache Benutzeroberfläche zur Verfügung stellen, die wir über Python programmieren.

Die Funktionen des Smart Homes belaufen sich auf folgendes:

1.	RGB Lichter steuerung, mittels Farbauswahl an einem farbrad (color chooser)

2.	Alarmanlagen steuerung und benachrichtigung mittels email bei ausschlag

Lichtsteuerung
---------
Die Funktion ermöglicht die Steuerung einer RGB-LED über die Python programmierte Benutzeroberfläche. Der Nutzer hat die Möglichkeit die RGB-LED ein- und auszuschalten. Zusätzlich kann man sie in jeder möglichen Farbe aufleuchten lassen. Bei der Auswahl einer Farbe werden die dazugehörigen Grundfarben Rot, Grün und Blau mit Werten von 0 bis 255 von Python an das Arduino weitergeleitet. Anschließend wird der von den Werten abhängige Strom über die jeweiligen Pins an die RGB-LED gesendet und bilden die ausgewählte Farbe. Über den “Off-Button” lässt sich die Lampe ausschalten, indem die Werte der Grundfarben an den Pins auf 0 gesetzt werden und kein Strom an der RGB-LED ankommt.


Alarmanlage
---------
Das Alarmsystem besteht in unserem Smart-Home aus einem Bewegungsmelder, der RGB-LED, und einem Piezo (Buzzer). Über die Benutzeroberfläche kann das Alarmsystem an- und ausgeschalten werden. Wenn das Alarmsystem angeschalten ist und der Bewegungsmelder ausschlägt, sendet der Arduino an Python ein Signal, dass der Alarm ausgelöst wurde. Infolge dessen setzt der Arduino die RGB-LED auf die Farbe Rot, die als Alarmsignal dienen soll und aktiviert den Piezo, welcher Alarmtöne von sich gibt. Der Alarm kann über die Benutzeroberfläche wieder ausgeschaltet werden und die RGB-LED nimmt die vorherige Farbe wieder an. Als Addition des Ganzen wird der Benutzer des Systems per E-Mail benachrichtigt, sobald der Alarm ausgelöst wird.


Erweiterungsmöglichkeiten
---------
	Bei der Erweiterung des Programmes sind einem eigentlich keine Grenzen gesetzt.
	Hier sind einige Ideen, welche wir leider nicht mehr realisieren konnten:
	*	Funktion zur erkennung von offenen Fenstern und/oder Türen
	*	Steuerung der Stromzufuhr von einigen Elektrischen Gegenständen im Haus
	*	Eine benutzung über ein Smart Phone, mittels einer Python App

Entwickler
---------
 *	Okan Dogtas (4450377)
 *	Sercan Eyigün (4444473)
 *	Manuel Schendel (4446837)


