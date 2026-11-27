# Calculs électriques — ORION-SORT

## 1. Donnée du sujet
Le sujet indique une alimentation secteur 5 V / 3 A minimum pour le thème B.

## 2. Dimensionnement réel
Le courant maximal doit être déterminé à partir de la fiche technique des servos réellement utilisés.

Formule :
I_total_max = somme des courants maximaux des servos susceptibles de fonctionner simultanément + marge.

Puissance :
P = V × I

Exemple de calcul à compléter après réception des références :
- Servo 1 : Imax = ___ A
- Servo 2 : Imax = ___ A
- Servo 3 : Imax = ___ A
- Servo 4 : Imax = ___ A
- Total = ___ A
- Marge de dimensionnement = ___ %
- Alimentation retenue = 5 V / ___ A

## 3. Protection
La protection doit être dimensionnée en fonction :
- du courant nominal et des pointes ;
- du calibre admissible des fils ;
- de l'alimentation choisie ;
- du comportement réel des servos.

Ne pas choisir un fusible uniquement à partir d'une valeur générique.

## 4. Logique
L'ESP32 et les capteurs ne doivent pas être alimentés par la ligne de puissance des servos sans régulation adaptée.
