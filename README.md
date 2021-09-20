Pour commencer, assurez vous d'avoir Python v.3.9.4.

Téléchargez le contenu du github dans un dossier et entrez dedans : https://github.com/Pierre12412/LITReview

Ouvrez le terminal de commande avec WIN+R, tapez 'cmd' et Entrée.

Pour vous rendre dans le fichier du projet, tapez cd puis le chemin d'accès, ou aidez vous de la touche TABULATION
Exemple:
C:\Users\Pierre\> cd Desktop (Vous fera parvenir au bureau)

Une fois dans le fichier du projet que vous avez téléchargé, créez un environnement virtuel avec la commande: python -m venv virtualenv

Activez le ensuite avec la commande : virtualenv\Scripts\activate.bat

Puis récupérez les packages Python de requirements.txt avec la commande suivante : pip install -r requirements.txt

Enfin allumez le serveur en entrant dans le dossier src avec la commande : cd src
et en effectuant la commande : python manage.py runserver

Vous pouvez maintenant vous rendre sur le site dans un navigateur avec l'adresse http://127.0.0.1:8000/

Pour arrêter le serveur, appuyez sur CTRL + C dans le terminal