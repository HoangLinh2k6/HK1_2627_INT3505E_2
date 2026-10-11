import uuid
import yaml
from flask import Flask, jsonify, send_file, request

app = Flask(__name__)

def load_spec():
    with open('openapi.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@app.route('/openapi.json', methods=['GET'])
def get_openapi_json():
    return jsonify(load_spec())

@app.route('/docs', methods=['GET'])
def render_swagger_ui():
    return send_file('index.html')

TASKS_DB = {}

@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    status = request.args.get('status')
    limit = request.args.get('limit', default=10, type=int)
    tasks = list(TASKS_DB.values())
    if status:
        tasks = [t for t in tasks if t.get('status') == status]
    return jsonify({"data": tasks[:limit], "total": len(tasks), "page": 1}), 200

@app.route('/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    if "title" not in data:
        return jsonify({"description": "thiếu title"}), 400
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": data["title"],
        "status": "open",
        "priority": data.get("priority", "normal"),
        "dueDate": data.get("dueDate"),
        "assigneeId": data.get("assigneeId")
    }
    TASKS_DB[task_id] = task
    return jsonify(task), 201

@app.route('/v1/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    if task_id not in TASKS_DB:
        return jsonify({"description": "task không tồn tại"}), 404
    return jsonify(TASKS_DB[task_id]), 200

@app.route('/v1/tasks/<task_id>', methods=['PATCH'])
def update_task(task_id):
    if task_id not in TASKS_DB:
        return jsonify({"description": "task không tồn tại"}), 404
    data = request.get_json() or {}
    TASKS_DB[task_id].update({k: v for k, v in data.items() if v is not None})
    return jsonify(TASKS_DB[task_id]), 200

@app.route('/v1/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id not in TASKS_DB:
        return jsonify({"description": "task không tồn tại"}), 404
    del TASKS_DB[task_id]
    return '', 204