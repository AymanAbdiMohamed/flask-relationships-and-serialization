# Flask Relationships and Serialization

Small example app demonstrating SQLAlchemy relationships and serialization using `sqlalchemy-serializer`.

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize or run migrations (a `migrations/` folder already exists in this repo):

```bash
export FLASK_APP=app.py
flask db upgrade
```

4. Run the app:

```bash
python app.py
```

The app listens on `http://127.0.0.1:5000` by default.

## API Endpoints

- `GET /users` — list users
- `POST /users` — create user: JSON `{ "name": "Alice" }`
- `GET /posts` — list posts
- `POST /posts` — create post: JSON `{ "title": "T", "content": "C", "user_id": 1 }`

Example requests:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice"}' http://127.0.0.1:5000/users

curl -X POST -H "Content-Type: application/json" -d '{"title":"Hello","content":"World","user_id":1}' http://127.0.0.1:5000/posts
```

## Notes

- The `User` and `Post` models include `serialize_rules` to avoid circular serialization when converting to dictionaries.
- Uses SQLite by default (`app.db` in project root) for simplicity.

