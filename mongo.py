from pymongo import MongoClient
import sys

def clean_database(uri):
    try:
        client = MongoClient(uri)
        print("✅ Connected to MongoDB!")

        # List all databases except internal ones
        databases = [db for db in client.list_database_names() if db not in ('admin', 'local', 'config')]
        if not databases:
            print("No user databases found to clean.")
            return

        print("\nFound the following databases:")
        for db in databases:
            print(f" - {db}")

        confirm = input("\n⚠️  Are you sure you want to delete ALL data from these databases? Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Aborted.")
            return

        for db_name in databases:
            db = client[db_name]
            collections = db.list_collection_names()
            for collection_name in collections:
                result = db[collection_name].delete_many({})
                print(f"🧹 Cleared {result.deleted_count} documents from {db_name}.{collection_name}")

        print("\n✅ All user databases have been cleaned.")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    uri = input("Enter your MongoDB URI (e.g., mongodb+srv://user:pass@cluster.mongodb.net/): ").strip()
    clean_database(uri)
