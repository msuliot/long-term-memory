from pymongo import MongoClient
from env_config import envs
from datetime import datetime, timezone
from bson import ObjectId

env = envs()

class MongoHelper:
    def __init__(self):
        self.client = MongoClient(env.mongo_uri) # mongo cluster uri
        self.db = self.client['ltm'] # ltm is the database name

    def generate_timestamp(self):
        current_time_utc = datetime.now(timezone.utc)
        formatted_time_utc = current_time_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        return formatted_time_utc
    
    def generate_date(self):
        current_time_utc = datetime.now(timezone.utc)
        formatted_time_utc = current_time_utc.strftime('%Y-%m-%d')
        return formatted_time_utc
    
    
    # CONVERSATION
    def conversation_delete(self, conversation_id):
        collection = self.db['conversations']
        response = collection.delete_one({"_id": ObjectId(conversation_id)})
        return response


    def conversation_create(self, profile_id):
        collection = self.db['conversations']
        new_conversation = {
            "profile_id": profile_id,
            "start_time": self.generate_timestamp(),
            "end_time": "",
            "messages": []
        }
        response = collection.insert_one(
            new_conversation
        )
        return str(response.inserted_id)


    def conversation_update(self, conversation_id, message):
        collection = self.db['conversations']
        timestamp = datetime.now(timezone.utc).isoformat()
        result = collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$push": {"messages": message},
                "$set": {"end_time": timestamp}
            }
        )
        return result
    
    # PROFILE
    def profile_upsert(self, user_id, name, email, phone):
        collection = self.db['profiles']
        profile = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "phone": phone
        }
        response = collection.update_one(
            {"user_id": user_id},  # Search query to find the user by user_id
            {"$set": profile},     # Update the fields with new values
            upsert=True            # Insert if the user_id does not exist
        )
        if response.upserted_id:
            print(f"Profile created with ID: {response.upserted_id}")
        else:
            print(f"Profile updated for user_id: {user_id}")
        

    def profile_find(self, user_id):
        collection = self.db['profiles']
        profile = collection.find_one({"user_id": user_id})
        return profile
    
    # SUMMARY
    def summary_update(self, conversation_id, profile_id, conversation_summary):
        collection = self.db['summary']  

        ltm_summary = {
            "conversation_id": conversation_id,
            "date": self.generate_date(),
            "summary": conversation_summary
        }

        response = collection.update_one(
            {"_id": ObjectId(profile_id)},
            {
                "$push": {"conversations": ltm_summary}
            },
            upsert=True
        )

        if response.upserted_id:
            print(f"LTM summary created with ID: {response.upserted_id}")
        else:
            print(f"LTM summary updated for id: {profile_id}")

        return response
    
    def summary_find(self, pid):
        collection = self.db['summary']
        summaries = collection.find_one({"_id": ObjectId(pid)})
        return summaries