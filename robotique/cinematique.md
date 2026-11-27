# Cinématique inverse — modèle plan à deux segments

Variables : `L1`, `L2` longueurs des segments ; `x,y` coordonnées de la cible ; `theta1,theta2` angles articulaires. Garder la même unité pour toutes les longueurs.

```text
cos(theta2) = (x² + y² - L1² - L2²) / (2 L1 L2)
theta2 = arccos(cos(theta2))
theta1 = atan2(y,x) - atan2(L2 sin(theta2), L1 + L2 cos(theta2))
```

Condition de portée :
```text
abs(L1-L2) <= sqrt(x²+y²) <= L1+L2
```

Interpolation linéaire :
```text
a(t) = a0 + t(a1-a0), avec 0 <= t <= 1
```

Ce modèle est simplifié : l'équipe doit l'adapter à la géométrie réelle, aux offsets, aux limites mécaniques et à l'axe de base. Vérifier que `cos(theta2)` reste dans [-1,1].
