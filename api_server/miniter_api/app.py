from flask import Flask, request, jsonify, current_app
from flask.json  import JSONEncoder
from sqlalchemy import create_engine, text

def get_user(user_id):
    user = current_app.database.execute(text("""
        SELECT
            id,
            name,
            email,
            profile
        FROM
            users
        WHERE id = :user_id
    """),{
        'user_id' : user_id
    }).fetchone()

    return {
        'id' : user['id'],
        'name' : user['name'],
        'email' : user['email'],
        'profile' : user['profile']
    } if user else None

def insert_user(user):
    user_id = current_app.database.execute(text("""
        INSERT INTO users(
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :name,
            :email,
            :profile,
            :password
        )
    """),user).lastrowid

    return user_id

def insert_tweet(user_tweet):
    return current_app.database.execute(text("""
        INSERT INTO tweets(
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet).rowcount

def insert_follow(user_follow):
    return current_app.database.execute(text("""
        INSERT INTO users_follow_list(
            user_id,
            follow_id
        ) VALUES (
            :id,
            :follow
        )
    """),user_follow)

def insert_unfollow(user_unfollow):
    return current_app.database.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id = :id AND follow_id = :unfollow
    """),user_unfollow)

def get_timeline(user_id):
    rows = current_app.database.execute(text("""
        SELECT t.user_id, t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list f ON f.user_id = :user_id
        WHERE t.user_id = :user_id OR t.user_id = f.follow_id
    """),{
        'user_id' : user_id
    }).fetchall()

    return [{
        'user_id' : row['user_id'],
        'tweet' : row['tweet']
    } for row in rows]

def create_app(test_config = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database

    @app.route("/ping",methods=['GET'])
    def ping():
        return "pong"

    @app.route("/sign-up",methods=['POST'])
    def sign_up():
        new_user = request.json
        new_user_id = insert_user(new_user)

        return jsonify(get_user(new_user_id))

    @app.route("/tweet",methods=['POST'])
    def tweet():
        user_tweet = request.json
        tweet = user_tweet['tweet']

        if len(tweet) > 300:
            return '300자를 초과했습니다', 400
        
        insert_tweet(user_tweet)

        return '', 200

    @app.route("/follow",methods=['POST'])
    def follow():
        user_follow = request.json
        insert_follow(user_follow)
        
        return '', 200

    @app.route("/unfollow",methods=['POST'])
    def unfollow():
        user_unfollow = request.json
        insert_unfollow(user_unfollow)
    
        return '', 200

    @app.route("/timeline/<int:user_id>",methods=['GET'])
    def timeline(user_id):
        timeline = get_timeline(user_id)

        return jsonify({
            'user_id' : user_id,
            'timeline' : timeline
        })

    
    return app