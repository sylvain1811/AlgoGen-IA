# AlgoGen-IA

TP Projet algorithmes génétiques du cours d'IA @HE-Arc

## WP1 : Aquisition de données

- GUI : done.
- File : done.

## WP2 : Algo génétique: Généralités

### Fonction de fitness

Calcul de la distance du parcours.
Idée : stockage des distance entre deux points pour calculer qu'une seule fois. Si pas encore calculer -> calcul et stockage.

### Conditions d'arrêts

- Temps : currentTime - start time
- Bouclage : si la distance (fitness) du meilleur parcours ne s'améliore pas après x itérations, on arrête.

### Séléction

- Ordonner la liste de parcours selon fonction de fitness (distance totale).
- Garder que les meilleurs (moitié de la liste).

## WP3 : Algo génétique: opérations génétiques

### Croisements

Croiser les meilleurs (moitié de la liste de départ).
Effectuer assez de croisement pour obtenir une liste de même taille qu'au départ.

### Mutations

Idées: 
- Swaper 10% des villes de chaque parcours.
- Echange de 2 villes contiguës 

## WP4 : Validation - Tests - Livraison
