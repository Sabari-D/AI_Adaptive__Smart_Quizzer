
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import os 
import random 
from hashlib import sha256 
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_mail import Mail, Message

from services.user_service import UserService 
from services.ai_service import AIService 
from services.adaptive_service import AdaptiveService 


load_dotenv()

app = Flask(__name__)
CORS(app) 

app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your_email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your_app_password')

SECRET_KEY = os.getenv("SECRET_KEY_FOR_TOKENS", "YOUR_SUPER_SECRET_KEY_FOR_TOKENS")
FRONTEND_URL = os.getenv("FRONTEND_RESET_URL", 'http://localhost:5173/reset-password')
s = URLSafeTimedSerializer(SECRET_KEY)

mail = Mail(app)

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    users_collection = db["users"]
    contents_collection = db["contents"] 
    quiz_history_collection = db["quiz_history"]
    
    # NEW: Initialize the feedback collection
    user_feedback_collection = db["user_feedback"]
    # NEW: Initialize the moderation collection (used by /api/feedback/flag)
    moderation_queue_collection = db["moderation_queue"]
    
    user_service = UserService(users_collection, contents_collection, bcrypt) 
    ai_service = AIService() 
    adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) 
    
    users_collection.create_index("email", unique=True)
    
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user_email = get_jwt_identity()
        user = user_service.find_user_by_email(current_user_email)

        if not user or not user.get('is_admin', False):
            return jsonify({"msg": "Access Denied: Admin privileges required."}), 403 

        return func(*args, **kwargs)
    return wrapper


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

## 1. User Registration (Signup) - UPDATED
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    mobile_number = data.get('mobile_number')

    if not email or not password or not username or not mobile_number:
        return jsonify({"msg": "Missing required fields (email, password, username, mobile number)."}), 400

    # MOBILE NUMBER VALIDATION (10 Digits)
    if len(mobile_number) != 10 or not mobile_number.isdigit():
        return jsonify({"msg": "Enter a valid mobile number (must be 10 digits)."}), 400
    
    new_user_email = user_service.register_user(email, password, username, mobile_number)

    if new_user_email:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token, is_admin=False), 201 
    else:
        return jsonify({"msg": "User with this email already exists"}), 409

## 2. User Login
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_data = user_service.check_password(email, password)

    if user_data:
        
        today = datetime.now().date()
        last_login = user_data.get('last_login_date')
        
        current_streak = user_data.get('login_streak', 0)
        
        if last_login:
            last_login_date = last_login.date()

            if last_login_date == today - timedelta(days=1):
                current_streak += 1
            
            elif last_login_date == today:
                pass 
            
            else:
                current_streak = 1 
        else:
            current_streak = 1 

        
        user_service.users_collection.update_one(
            {"_id": user_data['_id']},
            {"$set": {
                "login_streak": current_streak,
                "last_login_date": datetime.now()
            }}
        )
        
        access_token = create_access_token(identity=email)
        
        is_admin_status = user_data.get('is_admin', False) 

        return jsonify(
            access_token=access_token, 
            is_admin=is_admin_status 
        ), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_email = get_jwt_identity() 
    user = user_service.find_user_by_email(current_user_email)
    
    if user:
        user['is_admin'] = user.get('is_admin', False)
        return jsonify(user), 200
    
    return jsonify({"msg": "User not found"}), 404


@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_email = get_jwt_identity()
    data = request.get_json()

    was_modified = user_service.update_profile(current_user_email, data)

    if was_modified:
        return jsonify({"msg": "Profile updated successfully"}), 200
    else:
        if user_service.find_user_by_email(current_user_email):
            return jsonify({"msg": "User found but no valid changes applied"}), 200
        else:
            return jsonify({"msg": "User not found"}), 404


@app.route('/api/auth/request-password-reset', methods=['POST'])
def request_password_reset():
    
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"msg": "Email is required."}), 400

    user = users_collection.find_one({'email': email}) 

    
    if not user:
        return jsonify({"message": "If an account exists, a reset link has been sent to your email."}), 200

    
    try:
        token = s.dumps(email, salt='password-reset-salt')
        reset_link = f"{FRONTEND_URL}/{token}"
        
        
        msg = Message(
            'SmartQuizzer Password Reset Request',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = (
            f"Hello,\n\n"
            f"You requested a password reset for your SmartQuizzer account.\n"
            f"Click the following link to reset your password:\n\n"
            f"{reset_link}\n\n"
            f"This link will expire in a few hours.\n\n"
            f"If you did not request this, please ignore this email."
        )
        mail.send(msg) 
        
        return jsonify({"message": "If an account exists, a reset link has been sent to your email."}), 200
    
    except Exception as e:
        print(f"Error sending reset email: {e}")
        return jsonify({"message": "An error occurred. Please try again later."}), 500


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    if not all([token, new_password]):
        return jsonify({"msg": "Token and new password are required."}), 400

    email = None
    try:
        
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        return jsonify({"msg": "Token expired. Please request a new reset link."}), 400
    except BadTimeSignature:
        return jsonify({"msg": "Invalid reset token."}), 400

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"msg": "User associated with token not found."}), 404

    
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    users_collection.update_one(
        {"_id": user['_id']},
        {"$set": {"password": hashed_password}}
    )

    return jsonify({"msg": "Password reset successfully. Please log in with your new password."}), 200


@app.route('/api/content/upload', methods=['POST'])
@jwt_required()
def upload_content():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    
    title = request.form.get('title', 'General Knowledge') 
    method = request.form.get('method')
    
    raw_text = ""
    
    
    if method == 'paste':
        raw_text = request.form.get('raw_text', '')
        source_type = "Pasted Text"
        
    elif method == 'url':
        content_url = request.form.get('content_url', '')
        if not content_url:
            return jsonify({"msg": "URL not provided."}), 400
        
        raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
        source_type = "Analyzed URL"
        if not raw_text:
             return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

    elif method == 'file':
        if 'file' not in request.files:
            return jsonify({"msg": "No file part in the request."}), 400
            
        uploaded_file = request.files['file']
        
        if uploaded_file.filename == '':
            return jsonify({"msg": "No selected file."}), 400
        
        if not allowed_file(uploaded_file.filename):
            return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

        
        raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
        source_type = f"Uploaded File ({uploaded_file.filename})"
        
        if not raw_text:
            return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
    else:
        return jsonify({"msg": "Invalid ingestion method."}), 400

    
    knowledge_chunks = ai_service.process_content(raw_text)

    if not knowledge_chunks:
        return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
    content_data = {
        "user_id": user['_id'],
        "title": title,
        "source_type": source_type,
        "chunks": knowledge_chunks,
        "chunk_count": len(knowledge_chunks),
        "created_at": datetime.now()
    }
    

    content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
    return jsonify({
        "msg": "Content processed and saved successfully.",
        "content_id": str(content_id),
        "chunk_count": len(knowledge_chunks)
    }), 201


@app.route('/api/content/list', methods=['GET'])
@jwt_required()
def list_user_content():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    
    content_list = list(user_service.contents_collection.find(
        {"user_id": user['_id']},
        {"title": 1, "chunk_count": 1, "created_at": 1} 
    ).sort("created_at", -1))

    
    for content in content_list:
        content['_id'] = str(content['_id'])
        content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

    return jsonify(content_list), 200


@app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
@jwt_required()
def generate_question(content_id):
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404

    
    
    data = request.get_json()
    requested_question_type = data.get('question_type')
    
    if not requested_question_type:
        return jsonify({"msg": "Question type is missing from request body."}), 400

    
    try:
        content_document = user_service.contents_collection.find_one(
            {"_id": ObjectId(content_id), "user_id": user['_id']}
        )
    except Exception:
        return jsonify({"msg": "Invalid content ID format."}), 400

    if not content_document:
        return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
    knowledge_chunks = content_document.get('chunks', [])
    if not knowledge_chunks:
        return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
    
    
    selected_chunk_text = None
    
    
    weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

    if weak_chunk_result:
        
        selected_chunk_text = weak_chunk_result['chunk_text'] 
        print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
        
        worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
        if worst_type and random.random() < 0.5: 
            final_question_type = worst_type
            print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
        else:
            final_question_type = requested_question_type
    else:
        
        selected_chunk_text = random.choice(knowledge_chunks)
        final_question_type = requested_question_type
        print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
    
    subject = content_document.get('title', 'General Knowledge Topic') 
    difficulty = user.get('difficulty_level', 'Intermediate') 
    
    
    question_data = ai_service.generate_quiz_question(
        content_chunk=selected_chunk_text, 
        question_type=final_question_type, 
        subject=subject, 
        difficulty=difficulty
    )
    
    if question_data:
        question_data['content_chunk'] = selected_chunk_text 
        question_data['content_id'] = content_id
        
        return jsonify(question_data), 200
    else:
        return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500


@app.route('/api/quiz/log-answer', methods=['POST'])
@jwt_required()
def log_user_answer():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    

    data = request.get_json()
    
    
    content_id = data.get('content_id')
    chunk_text = data.get('content_chunk')
    is_correct = data.get('is_correct')
    question_type = data.get('question_type')
    time_taken_ms = data.get('time_taken_ms') 
    
    if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
        return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

    
    log_data = {
        "user_id": user['_id'],
        "content_id": content_id,
        "chunk_hash": sha256(chunk_text.encode()).hexdigest(), 
        "is_correct": bool(is_correct),
        "question_type": question_type,
        "difficulty_level": user.get('difficulty_level', 'Intermediate'),
        "time_taken_ms": time_taken_ms, 
        "timestamp": datetime.now()
    }
    
    
    db["quiz_history"].insert_one(log_data)
    
    return jsonify({"msg": "Performance logged successfully."}), 201


@app.route('/api/analytics/performance', methods=['GET'])
@jwt_required()
def get_performance_analytics():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    
    performance_data = list(db["quiz_history"].find(
        {"user_id": user['_id']},
        
    ).sort("timestamp", -1).limit(20))

    
    processed_data = []
    
    for log in reversed(performance_data):
        processed_data.append({
            "is_correct": log['is_correct'],
            "question_type": log['question_type'],
            "time_taken_ms": log.get('time_taken_ms', 0),
            "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(processed_data), 200


@app.route('/api/coaching/suggest', methods=['POST'])
@jwt_required()
def generate_coaching_suggestion():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404

    

    data = request.get_json()
    quiz_results = data.get('quiz_results') 
    total_correct = data.get('total_correct')
    total_answered = data.get('total_answered')

    if not quiz_results or total_answered == 0:
        return jsonify({"msg": "No quiz data provided for analysis."}), 400

    
    failure_data = []
    for q in quiz_results:
        
        if 'isCorrect' in q and q['isCorrect'] == False: 
            failure_data.append({
                'type': q['type'],
                'chunk_preview': q['content_chunk'][:40] + '...',
                'question': q['question']
            })

    
    prompt = (
        f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
        f"Overall Score: {total_correct}/{total_answered}. "
        f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
        f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
        f"Your response must include:\n"
        f"1. A motivational opening.\n"
        f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
        f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
        f"FAILURE DATA: {failure_data}"
    )

    
    try:
        response_text = ai_service.generate_coaching_text(prompt)
    except Exception as e:
        print(f"Coaching AI call failed: {e}")
        return jsonify({"msg": "AI coaching generation failed."}), 500

    return jsonify({"suggestion_text": response_text}), 200


@app.route('/api/gamification/stats', methods=['GET'])
@jwt_required()
def get_gamification_stats():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    
    total_answered = db["quiz_history"].count_documents({"user_id": user['_id']})
    
    
    if total_answered >= 100 and "Q100_MASTER" not in user.get('badges', []):
        user_service.users_collection.update_one(
            {"_id": user['_id']},
            {"$addToSet": {"badges": "Q100_MASTER"}} 
        )
        
        user = user_service.find_user_by_email(current_user_email)

    
    return jsonify({
        "login_streak": user.get('login_streak', 0),
        "badges": user.get('badges', []),
        "total_answered": total_answered,
        "last_login_date": user.get('last_login_date').strftime("%Y-%m-%d") if user.get('last_login_date') else None
    }), 200


@app.route('/api/analytics/blindspot', methods=['GET'])
@jwt_required()
def get_cognitive_blindspot():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    user_id = user['_id']
    
    if not user:
        return jsonify({"msg": "User not found."}), 404

    try:
        
        accuracy_by_type = list(db["quiz_history"].aggregate([
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$question_type",
                "avg_accuracy": {"$avg": {"$cond": ["$is_correct", 1, 0]}},
                "avg_time": {"$avg": "$time_taken_ms"}
            }}
        ]))
        
        
        overall_stats = next(db["quiz_history"].aggregate([
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": None,
                "overall_accuracy": {"$avg": {"$cond": ["$is_correct", 1, 0]}},
                "overall_avg_time": {"$avg": "$time_taken_ms"}
            }}
        ]), None)

        if not overall_stats or overall_stats['overall_avg_time'] == 0:
             return jsonify({"type": "Initial State", "suggestion": "Answer more questions to generate diagnostic data."}), 200

        
        mcq_stats = next((item for item in accuracy_by_type if item['_id'] in ['MCQ', 'True/False']), None)
        short_answer_stats = next((item for item in accuracy_by_type if item['_id'] in ['Short Answer', 'Fill-in-the-Blank']), None)
        
        if mcq_stats and short_answer_stats:
            
            if mcq_stats['avg_accuracy'] > 0.8 and short_answer_stats['avg_accuracy'] < 0.6:
                return jsonify({
                    "type": "Application Blind Spot", 
                    "suggestion": "You have a **Knowledge Application Gap**. You can recall facts (MCQ accuracy is high), but struggle with synthesis and problem-solving (Short Answer is low). Focus on quizzes requiring step-by-step thinking.",
                    "severity": "High"
                }), 200

        
        if overall_stats['overall_accuracy'] > 0.8:
            slow_types = [item for item in accuracy_by_type if item['avg_time'] > (overall_stats['overall_avg_time'] * 1.5)]
            if slow_types:
                slow_type_name = slow_types[0]['_id']
                return jsonify({
                    "type": "Fluency Blind Spot",
                    "suggestion": f"Your knowledge is correct, but your **Fluency is low** on **{slow_type_name}** questions. You require extra time to retrieve information. Focus on rapid-fire review sessions to increase speed and automaticity.",
                    "severity": "Medium"
                }), 200

        
        weakest_chunk = adaptive_service.get_weakest_chunk(user_id, content_id=None, threshold=0.7) 
        
        if weakest_chunk and weakest_chunk['correct_rate'] < 0.5:
            
            strongest_chunk = adaptive_service.get_strongest_chunk(user_id, content_id=None, threshold=0.85)

            if strongest_chunk and weakest_chunk['content_id'] == strongest_chunk['content_id']:
                return jsonify({
                    "type": "Topic Drift Blind Spot",
                    "suggestion": f"You have **Inconsistent Mastery** within the same topic. You are mastering some areas but ignoring key chunks. Focus on the single topic you are weak in until you reach mastery before moving on.",
                    "severity": "Low"
                }), 200

        
        return jsonify({"type": "Clear Cognitive State", "suggestion": "Great job! Your recent performance shows consistent mastery and fluency across all topics."}), 200

    except Exception as e:
        print(f"Blindspot detection error: {e}")
        return jsonify({"msg": "Diagnostic analysis failed."}), 500


@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
@admin_required 
def get_admin_stats():
    
    try:
      
        total_users = db["users"].count_documents({})

        
        total_interactions = db["quiz_history"].count_documents({})
        
        
        total_content = user_service.contents_collection.count_documents({})

        
        accuracy_pipeline = [
            {"$group": {
                "_id": None,
                "total_answered": {"$sum": 1},
                "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
            }}
        ]
        accuracy_result = list(db["quiz_history"].aggregate(accuracy_pipeline))

        overall_accuracy = 0
        if accuracy_result and accuracy_result[0]['total_answered'] > 0:
            overall_accuracy = round(
                (accuracy_result[0]['total_correct'] / accuracy_result[0]['total_answered']) * 100
            )

        return jsonify({
            "total_users": total_users,
            "total_interactions": total_interactions,
            "total_content_items": total_content,
            "overall_accuracy_percent": overall_accuracy
        }), 200

    except Exception as e:
        print(f"Admin stats error: {e}")
        return jsonify({"msg": "Failed to fetch admin stats."}), 500


## 13. User Feedback Submission (Missing Route)
@app.route('/api/feedback/submit', methods=['POST'])
@jwt_required()
def submit_feedback():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    data = request.get_json()
    
    rating = data.get('rating') # 1-5 star rating
    suggestions = data.get('suggestions', '')
    experience_rating = data.get('experience_rating') # e.g., "Very Good", "Poor"
    
    if rating is None or experience_rating is None:
        return jsonify({"msg": "Rating and experience selection are required."}), 400

    # Prepare feedback data
    feedback_data = {
        "user_id": user['_id'],
        "experience_rating": experience_rating,
        "star_rating": int(rating),
        "suggestions": suggestions,
        "timestamp": datetime.now()
    }
    
    try:
        # Insert into the dedicated feedback collection
        user_feedback_collection.insert_one(feedback_data)
        return jsonify({"message": "Feedback submitted successfully"}), 201
    except Exception as e:
        print(f"Feedback database insertion error: {e}")
        return jsonify({"msg": "Internal server error during feedback submission."}), 500


@app.route('/api/feedback/flag', methods=['POST'])
@jwt_required()
def log_question_flag():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    

    data = request.get_json()
    
    
    question_id = data.get('question_id') 
    reason = data.get('reason', 'Inappropriate/Broken Content')
    
    if not question_id:
        return jsonify({"msg": "Missing question ID."}), 400

    
    flag_data = {
        "user_id": user['_id'],
        "question_content_id": question_id,
        "reason": reason,
        "status": "Pending Review",
        "timestamp": datetime.now()
    }
    
    
    db["moderation_queue"].insert_one(flag_data)
    
    return jsonify({"msg": "Question flagged for review. Thank you for your feedback."}), 201


@app.route('/api/admin/moderation/queue', methods=['GET'])
@jwt_required()
@admin_required 
def get_moderation_queue():
    
    try:
        
        queue_data = list(db["moderation_queue"].find(
            {"status": "Pending Review"} 
        ).sort("timestamp", -1)) 

        
        for item in queue_data:
            item['_id'] = str(item['_id'])
            item['user_id'] = str(item.get('user_id', 'N/A')) 
            item['timestamp'] = item['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(queue_data), 200

    except Exception as e:
        print(f"Moderation queue fetch error: {e}")
        return jsonify({"msg": "Failed to fetch moderation queue."}), 500


@app.route('/api/admin/moderation/resolve/<flag_id>', methods=['PATCH'])
@jwt_required()
@admin_required 
def resolve_flag(flag_id):
    
    try:
      
        result = db["moderation_queue"].update_one(
            {"_id": ObjectId(flag_id)},
            {"$set": {"status": "Resolved", "reviewed_at": datetime.now()}}
        )
        if result.modified_count == 1:
            return jsonify({"msg": f"Flag {flag_id} resolved successfully."}), 200
        return jsonify({"msg": "Flag not found."}), 404
    except Exception as e:
        return jsonify({"msg": f"Error resolving flag: {e}"}), 500


@app.route('/api/admin/moderation/delete/<flag_id>', methods=['DELETE'])
@jwt_required()
@admin_required 
def delete_flag(flag_id):
    
    try:
        
        result = db["moderation_queue"].delete_one({"_id": ObjectId(flag_id)})
        
        if result.deleted_count == 1:
            return jsonify({"msg": f"Flag {flag_id} deleted successfully."}), 200
        return jsonify({"msg": "Flag not found."}), 404
    except Exception as e:
        return jsonify({"msg": "Error deleting flag: Server Error."}), 500


@app.route('/api/admin/leaderboard', methods=['GET'])
@jwt_required()
@admin_required 
def get_live_leaderboard():
    
    try:
        
        leaderboard_pipeline = [
            
            {"$group": {
                "_id": "$user_id",
                "total_answered": {"$sum": 1},
                "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
            }},
            
            {"$project": {
                "user_id": "$_id",
                "accuracy": {"$divide": ["$total_correct", "$total_answered"]},
                "total_attempts": "$total_answered",
            }},
            
            {"$sort": {"accuracy": -1, "total_attempts": -1}},
            {"$limit": 5} 
        ]
        
        top_users_data = list(db["quiz_history"].aggregate(leaderboard_pipeline))
        
        
        leaderboard = []
        for rank, item in enumerate(top_users_data):
            
            user_object_id = item['user_id']
            
            
            user_doc = db["users"].find_one({"_id": ObjectId(user_object_id)}) 
            
            leaderboard.append({
                "rank": rank + 1,
                "email": user_doc.get('email', 'Unknown User'),
                "accuracy": round(item['accuracy'] * 100, 1),
                "total_attempts": item['total_attempts']
            })

        return jsonify(leaderboard), 200

    except Exception as e:
        print(f"Leaderboard fetch error: {e}")
        return jsonify({"msg": "Failed to fetch leaderboard: Server Error."}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

