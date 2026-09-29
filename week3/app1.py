from flask import Flask, jsonify, request

app = Flask(__name__)

POSTS = [
    {"id": 1, "title": "A1", "content": "a1", "tags": ["b1", "b2"]},
    {"id": 2, "title": "A2", "content": "a2", "tags": ["b2", "b3"]},
]

@app.route('/blog/posts', methods=['GET'])
def get_posts():
    tag = request.args.get('tag')
    if tag:
        posts = [p for p in POSTS if tag in p.get('tags', [])]
    else:
        posts = POSTS
    if posts is None:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(posts), 200

@app.route('/blog/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post), 200

@app.route('/blog/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_post = {
        "id": len(POSTS) + 1,
        "title": data['title'],
        "content": data['content'],
        "tags": data.get('tags', [])
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201