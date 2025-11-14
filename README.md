



Configuration (.env)
- Copier `.env.example` en `.env` à la racine du projet.
- Adapter les variables selon votre environnement.
  - `PROJECT_NAME` définit le titre de l’API.
  - `CORS_ORIGINS` est une liste JSON des origines autorisées (ex: `"http://localhost:5173"`).
  - `API_PREFIX` applique un préfixe à toutes les routes (ex: `/api/v1`). Par défaut vide pour ne pas casser les URLs existantes.
- Le chargement du fichier `.env` est géré par `pydantic-settings` (`model_config.env_file`), il suffit de redémarrer le serveur pour prendre en compte les changements.

Exemple de `.env` minimal
```
PROJECT_NAME="Hopitalia Assurance API"
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]
```

Démarrage
- Installer les dépendances: `./.venv/Scripts/pip.exe install -r requirements.txt`
- Lancer en dev: `./.venv/Scripts/uvicorn.exe app.main:app --reload`
- Ouvrir: `http://127.0.0.1:8000/` et `http://127.0.0.1:8000/docs`


Tests
- Les tests utilisent `pytest` + `httpx` avec `ASGITransport` (pas de serveur externe requis).
- Support async via `pytest-asyncio` et `httpx.AsyncClient`.
- Lancer les tests: `./.venv/Scripts/python.exe -m pytest -q`.
- Couverture: `/`, `/health` (réponse typée Pydantic), `/hello/{name}`.
- Notes: avertissements de dépréciation liés à `@app.on_event` bénins; migration vers lifespan à prévoir.
- Sous Windows/OneDrive, `PytestCacheWarning` peut apparaître sans impact.

Base de données (Postgres) & Alembic
- Configurer `.env`:
  - `DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/hopitalia"`
  - `DB_ECHO=false` (mettre à `true` pour log SQL)
- Module SQLAlchemy: `app/core/database.py` expose `Base`, `engine`, `SessionLocal`, `get_db()`.
- Migrations Alembic:
  - Fichier `alembic.ini` et dossier `alembic/` déjà fournis
  - URL override via `.env` dans `alembic/env.py` (utilise `settings.DATABASE_URL`)
- Commandes Alembic courantes:
  - Créer une migration: `./.venv/Scripts/alembic.exe revision --autogenerate -m "init"`
  - Appliquer: `./.venv/Scripts/alembic.exe upgrade head`
  - Voir l’état: `./.venv/Scripts/alembic.exe current`
- Autogénération:
  - Déclarez les modèles SQLAlchemy en important `Base` de `app.core.database` (ex: `class User(Base): ...`).
  - Assurez-vous que les modèles sont importés quelque part dans votre package (ex: `app/models/__init__.py`) pour que Alembic les découvre.



<!-- ./.venv/Scripts/pip.exe install -r requirements.txt  -->

<!-- ./.venv/Scripts/uvicorn.exe app.main:app --reload  -->