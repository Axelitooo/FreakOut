# FreakOut
Studies - Terminal card game

FEATURES :

Freak Out ! est un jeu de cartes pour 2 joueurs qui s'éxécute dans le terminal. Le jeu comporte 20 cartes, portant une couleur
et un numéro de 0 à 9. Le but du jeu est de se débarasser de toutes ses cartes, le plus vite possible. Une carte est posée au 
milieu au début du jeu, et on peut jouer une carte de la même couleur avec une valeur juste en dessous ou juste au dessus, ou 
bien la carte de couleur opposée et de même numéro. En cas d'erreur ou d'indécision de la part du joueur, il tire une carte.

=> Tester la défaite : lancer FreakOut.py et spammer les touches du clavier, ou attendre la fin du timer 5 fois.

=> Tester la victoire : lancer FreakOutEasyWin.py et jouer la bonne carte.

-----------------------------------------------------------------------------------------------------------------------------------

PRECISIONS :

Python 3.6. Utilisation de la bibliothèque sysv_ipc.

Le main crée la message queue, la shared memory contenant la pioche, et les process Display, Board, et les Players.
Les entrées clavier sont gérées par le main, qui les transmet via la message queue.
Deux mutex, pour la pioche et l'action, permettent d'éviter les conflits lorsque les joueurs piochent ou soumettent une carte.

Comme l'affiche le terminal, les deux joueurs jouent sur le clavier à l'aide des touches qui leur sont respectivement attribuées. 
Le temps imparti pour jouer est de 10 secondes.

Si on interrompt le programme, la message queue ne sera pas nettoyée et cela conduira la prochaine exécution à se terminer
prématurément. Il suffit de laisser le programme se terminer pour pouvoir le relancer sans problème.

Les messages de shutdown qui permettent d'arrêter l'exécution sont passés de process en process.
Cela prend plusieurs secondes, en raison des timers des jouers, et de quelques time.sleep().
Nous avons mis en évidence l'arrêt différé des process par des messages affichés en majuscule.

Comme il est assez difficile de gagner avec les règles proposées, nous avons créé une variante du programme qui permet de gagner
en 1 coup. Cela permet de vérifier que notre code s'exécute correctement dans le cas d'une victoire.

-----------------------------------------------------------------------------------------------------------------------------------
