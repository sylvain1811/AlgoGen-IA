# AlgoGen-IA

TP Projet algorithmes génétiques du cours d'IA @HE-Arc

## WP1 : Aquisition de données

- GUI
- Fichier

## WP2 : Algo génétique: Généralités

### Fonction de fitness

Calcul de la distance du parcours. 
On enregistre le résultat du calcul de la distance entre deux villes (a et b) dans un dictionnaire de dictionnaires. La clé du premier est est le nom de la ville a, la clé du deuxième est le nom de la ville b. Cela permet de ne pas calculer deux fois la même distance. On regarde d'abord dans le tableau si la distance a été calculée et sinon on la calcul et on la stock.

### Conditions d'arrêts

- Temps : si `current_time - start_time > maxtime`
- Stagnation : si la distance totale (fitness) du meilleur parcours ne s'améliore pas après 25 itérations, on applique l'algorithme _2-opt_. Si le résultat est bon (un meilleur parcours a été trouvé, on continue, sinon on arrête.

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

### Décroisement

dans le cas ou les mutations et les croisements ne trouvent pas de meilleures solutions après plusieurs itérations nous utilisons l'algorithme 2opt également détaillé dans le PDF `arob98.pdf`.
cet algorithme va s'occuper de localiser les chemins qui se croisent et ca réarranger les villes pour décroiser un maximum.

## WP4 : Tests et validation

### Tests

Pour tester le bon fonctionnement de notre algorithme nous nous sommes principalement basé sur le chemin que nous affichons à l'utilisateur. 
En voyant le parcours il est très simple de savoir si nous nous approchons du solution cohérante ou non.
Nous nous sommes également basé sur la distance totale du parcours en fonction du nombre d'itérations pour nous assurer que notre algorithme était efficace.

### Validation

Lorsque nous sommes arrivé à ce que nous pensions être la fin du projet nous avons réalisé que notre solution arrivait trop souvent sur des minimums locaux.
Cela était du au fait que nous avions une approche trop élitiste et que nous ne laissions que très peu de chance aux mauvaises solutions qui aurait pu amener une meilleure solution finale. Nous avons donc adapté notre algorithme pour laisser plus de place à l'aléatoire.

