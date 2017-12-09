# AlgoGen-IA

TP Projet algorithmes génétiques du cours d'IA @HE-Arc

## WP1 : Aquisition de données

- GUI : done.
- File : done.

## WP2 : Algo génétique: Généralités

### Fonction de fitness

Calcul de la distance du parcours. 
On enregistre le résultat du calcul de la distance entre deux villes (a et b) dans un dictionnaire de dictionnaires. La clé du premier est est le nom de la ville a, la clé du deuxième est le nom de la ville b. Cela permet de ne pas calculer deux fois la même distance. On regarde d'abord dans le tableau si la distance a été calculée et sinon on la calcul et on la stock.

### Conditions d'arrêts

- Temps : si current_time - start_time > maxtime
- Stagnation : si la distance (fitness) du meilleur parcours ne s'améliore pas après 25 itérations, on applique l'algorithme _2-opt_. Si le résultat est bon (un meilleur parcours a été trouvé, on continue, sinon on arrête.

### Séléction

- Ordonner la liste de parcours selon fonction de fitness (distance totale).
- Garder que les meilleurs (moitié de la liste).

## WP3 : Algo génétique: opérations génétiques

### Croisements

Croiser les meilleurs (moitié de la liste de départ).
Effectuer assez de croisement pour obtenir une liste de même taille qu'au départ.
On choisit aléatoirement les éléments à croiser entre eux. La seule contrainte est de ne pas croiser un élément avec lui même.
Crossover avec l'algorithme : _Greedy Subtour Crossover_ détaillé dans le PDF `arob98.pdf`.

### Mutations

- 20% de chances d'échanger deux villes contiguës.
- 20% de chances d'échanger deux villes aléatoires.