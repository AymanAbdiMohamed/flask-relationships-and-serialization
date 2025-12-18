# 
# Imports
# 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin

# 
# Application Configuration
# 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 
# Extensions
# 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 
# Models
# 
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # One-to-many: User → Posts
    posts = db.relationship(
        'Post',
        backref='user',
        cascade='all, delete-orphan'
    )

    # Prevent circular serialization
    serialize_rules = ('-posts.user',)

    def __repr__(self):
        return f"<User id={self.id} name={self.name!r}>"


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Prevent circular serialization when a Post serializes its User
    serialize_rules = ('-user.posts',)

    def __repr__(self):
        return f"<Post id={self.id} title={self.title!r} user_id={self.user_id}>"

# 
# Routes
# 

#  USERS 
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


#  POSTS 
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    required_fields = ['title', 'content', 'user_id']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'title, content, and user_id are required'
        }), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    post = Post(
        title=data['title'],
        content=data['content'],
        user=user
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201

# 
# Application Entry Point
# 
if __name__ == '__main__':
    app.run(debug=True)
