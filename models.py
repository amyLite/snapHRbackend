# models.py

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://amarinderhoney11:oNnsBi9kuGTMkWg5@snaphrcluster.utb7494.mongodb.net/?retryWrites=true&w=majority&appName=snaphrCluster"
client = AsyncIOMotorClient(MONGO_URI)

# Database and Collection
db = client["snaphr"]
snaphrCollection = db["snaphrCollection"]
questionCollection = db["questionCollection"]

async def check_connection():
    try:
        # Check server status
        server_info =  await db.command("ping")
        print("Connected to MongoDB:", server_info)
    except Exception as e:
        print("Error connecting to MongoDB:", e)

async def push_resume_report(repo):
    """Insert a new user into the database."""
    result = await snaphrCollection.insert_one(repo)
    return str(result.inserted_id)

async def push_questions(questions):
    """Insert a new user into the database."""
    result = await questionCollection.insert_one(questions)
    return str(result.inserted_id)

async def get_questions(questions_id):
    """Retrieve the question document with the specified ID."""
    question_doc = await questionCollection.find_one({"ID": questions_id})
    if question_doc:
        return question_doc.get("questions", [])
    return []

async def get_report(repo_name):
    """Retrieve all reports with the specified report_name."""
    report_cursor = snaphrCollection.find({"report_name": repo_name})
    reports = []
    
    async for document in report_cursor:
        # Convert ObjectId to string
        document["_id"] = str(document["_id"])
        reports.append(document)
    
    return reports

async def get_uuid():
    # Fetch only 'name' fields from all documents
    names_cursor = questionCollection.find({}, {"_id": 0, "ID": 1})

    IDs = []

    async for doc in names_cursor:
        if "ID" in doc:
            IDs.append(doc["ID"])

    return IDs


