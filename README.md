
# yt-discord-bot Discord

yt-discord-bot est un bot Discord qui permet de jouer de la musique depuis YouTube, de gérer des playlists, et d'effectuer diverses actions liées à la musique dans un serveur Discord.

## Prérequis

- Python 3.9 ou version supérieure.
- Un environnement virtuel (recommandé mais non obligatoire).

## Installation

### 1. **Cloner le repository**

Clonez ce repository sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/yt-discord-bot.git
```

### 2. **Créer un environnement virtuel (facultatif mais recommandé)**

Dans le dossier du projet, créez un environnement virtuel :

```bash
python3 -m venv venv
```

Activez l'environnement virtuel :

- Sur **Windows** :

```bash
.\venv\Scripts\activate
```

- Sur **macOS/Linux** :

```bash
source venv/bin/activate
```

### 3. **Installer les dépendances**

Une fois l'environnement virtuel activé (ou si vous avez choisi de ne pas utiliser d'environnement virtuel), installez les dépendances requises en exécutant :

```bash
pip install -r requirements.txt
```

Cela installera toutes les bibliothèques nécessaires à l'exécution du bot, telles que `discord.py`, `yt-dlp`, et `python-dotenv`.

### 4. **Configurer le fichier `.env`**

Dans le dossier racine du projet, créez un fichier `.env` contenant votre token Discord. Ce fichier ne doit pas être versionné (ajoutez-le à `.gitignore`).

Le fichier `.env` doit contenir la ligne suivante :

```env
DISCORD_TOKEN= "Votre_Token_Discord_Ici"
```

### 5. **Lancer le bot**

Une fois les dépendances installées et la configuration effectuée, vous pouvez démarrer le bot en exécutant :

```bash
python client.py
```

### 6. **Commandes disponibles**

Voici quelques commandes de base que le bot supporte actuellement avec des **slash commands** :

- `/play <lien ou titre>` : Joue une chanson depuis YouTube.
- `/pause` : Met en pause la chanson en cours.
- `/resume` : Reprend la lecture de la chanson.
- `/stop` : Arrête la lecture et vide la file.
- `/next` : Passe à la chanson suivante.

## Contribuer

1. Forkez le repository.
2. Créez une nouvelle branche (`git checkout -b feature-nom`).
3. Effectuez vos modifications.
4. Soumettez une Pull Request.

## Licence

Ce projet est sous licence MIT
