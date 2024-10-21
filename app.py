from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store (for simplicity)
users = {}
workouts = {}
goals = {}
current_user_id = 1
current_workout_id = 1
current_goal_id = 1

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/")
def home():
    return "Welcome to the Fitness Tracker!"

# User Management
@app.route("/api/register", methods=["POST"])
def register():
    global current_user_id
    data = request.get_json()
    user_id = current_user_id
    users[user_id] = {
        "id": user_id,
        "username": data.get("username"),
        "password": data.get("password"),  # Simplified, no real hashing for now
        "workouts": [],
        "goals": []
    }
    current_user_id += 1
    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    for user in users.values():
        if user["username"] == username and user["password"] == password:
            return jsonify({"message": "Login successful", "user_id": user["id"]}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/profile", methods=["GET"])
def profile():
    user_id = request.args.get("user_id")
    if user_id and int(user_id) in users:
        return jsonify(users[int(user_id)]), 200
    return jsonify({"error": "User not found"}), 404

# Workout Management
@app.route("/api/workouts", methods=["POST"])
def log_workout():
    global current_workout_id
    user_id = request.json.get("user_id")
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    workout = {
        "id": current_workout_id,
        "type": request.json.get("type"),
        "duration": request.json.get("duration"),
        "distance": request.json.get("distance", None),
        "calories": request.json.get("calories"),
    }
    current_workout_id += 1
    users[int(user_id)]["workouts"].append(workout)
    return jsonify({"message": "Workout logged", "workout_id": workout["id"]}), 201

@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    user_id = request.args.get("user_id")
    if user_id and int(user_id) in users:
        return jsonify(users[int(user_id)]["workouts"]), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/api/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    user_id = request.args.get("user_id")
    if user_id and int(user_id) in users:
        for workout in users[int(user_id)]["workouts"]:
            if workout["id"] == workout_id:
                return jsonify(workout), 200
    return jsonify({"error": "Workout not found"}), 404

@app.route("/api/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    user_id = request.json.get("user_id")
    if user_id and int(user_id) in users:
        for workout in users[int(user_id)]["workouts"]:
            if workout["id"] == workout_id:
                workout.update(request.get_json())
                return jsonify({"message": "Workout updated", "workout": workout}), 200
    return jsonify({"error": "Workout not found"}), 404

@app.route("/api/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    user_id = request.json.get("user_id")
    if user_id and int(user_id) in users:
        user_workouts = users[int(user_id)]["workouts"]
        users[int(user_id)]["workouts"] = [w for w in user_workouts if w["id"] != workout_id]
        return jsonify({"message": "Workout deleted"}), 200
    return jsonify({"error": "Workout not found"}), 404

# Goal Management
@app.route("/api/goals", methods=["POST"])
def create_goal():
    global current_goal_id
    user_id = request.json.get("user_id")
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    goal = {
        "id": current_goal_id,
        "goal": request.json.get("goal"),
        "progress": request.json.get("progress", 0)
    }
    current_goal_id += 1
    users[int(user_id)]["goals"].append(goal)
    return jsonify({"message": "Goal created", "goal_id": goal["id"]}), 201

@app.route("/api/goals", methods=["GET"])
def get_goals():
    user_id = request.args.get("user_id")
    if user_id and int(user_id) in users:
        return jsonify(users[int(user_id)]["goals"]), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/api/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    user_id = request.json.get("user_id")
    if user_id and int(user_id) in users:
        for goal in users[int(user_id)]["goals"]:
            if goal["id"] == goal_id:
                goal.update(request.get_json())
                return jsonify({"message": "Goal updated", "goal": goal}), 200
    return jsonify({"error": "Goal not found"}), 404

@app.route("/api/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    user_id = request.json.get("user_id")
    if user_id and int(user_id) in users:
        user_goals = users[int(user_id)]["goals"]
        users[int(user_id)]["goals"] = [g for g in user_goals if g["id"] != goal_id]
        return jsonify({"message": "Goal deleted"}), 200
    return jsonify({"error": "Goal not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

