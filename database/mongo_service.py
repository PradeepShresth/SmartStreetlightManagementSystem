import os
from datetime import datetime

from pymongo import MongoClient


# This helper converts MongoDB objects into plain Python data so Flask can safely return JSON.
def _serialize_document(doc):
    if not isinstance(doc, dict):
        return doc

    clean = dict(doc)
    if '_id' in clean:
        clean['_id'] = str(clean['_id'])
    if 'last_updated' in clean and hasattr(clean['last_updated'], 'strftime'):
        clean['last_updated'] = clean['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
    if 'date' in clean and hasattr(clean['date'], 'strftime'):
        clean['date'] = clean['date'].strftime('%Y-%m-%d %H:%M:%S')
    return clean


class MongoService:
    # Connect to MongoDB using the default local database address.
    def __init__(self):
        self.mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
        self.db = self.client['smart_streetlight']
        self.collection = self.db['streetlights']

    # Check if MongoDB is available before running database operations.
    def connected(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False

    # Basic sample records used when MongoDB is not available.
    def sample_lamps(self):
        return [
            {
                'lamp_id': 'SL-101',
                'zone': 'Downtown',
                'status': 'on',
                'brightness': 82,
                'power_usage': 130,
                'fault': False,
                'energy_today_kwh': 18.2,
                'last_updated': datetime.utcnow()
            },
            {
                'lamp_id': 'SL-102',
                'zone': 'Downtown',
                'status': 'dim',
                'brightness': 46,
                'power_usage': 70,
                'fault': False,
                'energy_today_kwh': 14.8,
                'last_updated': datetime.utcnow()
            },
            {
                'lamp_id': 'SL-203',
                'zone': 'North Ave',
                'status': 'on',
                'brightness': 90,
                'power_usage': 145,
                'fault': False,
                'energy_today_kwh': 21.5,
                'last_updated': datetime.utcnow()
            },
            {
                'lamp_id': 'SL-304',
                'zone': 'Industrial',
                'status': 'fault',
                'brightness': 0,
                'power_usage': 0,
                'fault': True,
                'energy_today_kwh': 9.7,
                'last_updated': datetime.utcnow()
            },
            {
                'lamp_id': 'SL-405',
                'zone': 'Park Road',
                'status': 'dim',
                'brightness': 52,
                'power_usage': 75,
                'fault': False,
                'energy_today_kwh': 12.9,
                'last_updated': datetime.utcnow()
            }
        ]

    # Insert a small initial dataset so the dashboard has visible data.
    def seed_data(self):
        if not self.connected():
            return False
        if self.collection.count_documents({}) == 0:
            self.collection.insert_many(self.sample_lamps())
        return True

    # Return all streetlights from MongoDB or fallback sample data.
    def get_all_lamps(self):
        if self.connected():
            return [_serialize_document(doc) for doc in self.collection.find().sort('lamp_id', 1)]
        return [_serialize_document(doc) for doc in self.sample_lamps()]

    # Build the summary used by the dashboard cards.
    def get_summary(self):
        if self.connected():
            total_lamps = self.collection.count_documents({})
            on_count = self.collection.count_documents({'status': 'on'})
            dim_count = self.collection.count_documents({'status': 'dim'})
            fault_count = self.collection.count_documents({'fault': True})
            total_energy = round(sum(doc['energy_today_kwh'] for doc in self.collection.find()), 2)
            return {
                'total_lamps': total_lamps,
                'on_count': on_count,
                'dim_count': dim_count,
                'fault_count': fault_count,
                'total_energy': total_energy,
                'mongo_connected': True,
            }

        return {
            'total_lamps': len(self.sample_lamps()),
            'on_count': 2,
            'dim_count': 2,
            'fault_count': 1,
            'total_energy': 76.1,
            'mongo_connected': False,
        }

    # Add a new lamp record to MongoDB and return a JSON-safe version.
    def add_lamp(self, lamp_id, zone, lamp_type='LED', location='Unknown', power_rating=80, brightness=100, status='on', fault=False):
        record = {
            'lamp_id': lamp_id,
            'zone': zone,
            'lamp_type': lamp_type,
            'location': location,
            'power_rating': power_rating,
            'status': status,
            'brightness': brightness,
            'power_usage': max(20, int(power_rating * 1.3)),
            'fault': fault,
            'energy_today_kwh': 0.0,
            'last_updated': datetime.utcnow(),
            'maintenance_history': []
        }

        if self.connected():
            self.collection.update_one({'lamp_id': lamp_id}, {'$set': record}, upsert=True)
            return _serialize_document(record)

        return _serialize_document(record)

    # Update the selected lamp with new details.
    def update_lamp(self, lamp_id, **values):
        if self.connected():
            self.collection.update_one({'lamp_id': lamp_id}, {'$set': values})
        return self.get_lamp_by_id(lamp_id)

    # Remove a decommissioned streetlight from the database.
    def delete_lamp(self, lamp_id):
        if self.connected():
            self.collection.delete_one({'lamp_id': lamp_id})
        return True

    # Fetch one lamp using its unique ID.
    def get_lamp_by_id(self, lamp_id):
        if self.connected():
            doc = self.collection.find_one({'lamp_id': lamp_id})
            return _serialize_document(doc)
        for lamp in self.sample_lamps():
            if lamp['lamp_id'] == lamp_id:
                return _serialize_document(lamp)
        return None

    # Save maintenance action details for a lamp.
    def add_maintenance_record(self, lamp_id, action, description, technician='System'):
        record = {
            'lamp_id': lamp_id,
            'action': action,
            'description': description,
            'technician': technician,
            'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }

        if self.connected():
            self.collection.update_one({'lamp_id': lamp_id}, {'$push': {'maintenance_history': record}})
            self.collection.update_one({'lamp_id': lamp_id}, {'$set': {'last_updated': datetime.utcnow()}})

        return record

    # Return all lamps marked as faulty.
    def get_faulty_lamps(self):
        if self.connected():
            return [_serialize_document(doc) for doc in self.collection.find({'fault': True}).sort('zone', 1)]
        return [_serialize_document(lamp) for lamp in self.sample_lamps() if lamp.get('fault')]

    # Simulate live lamp state changes for the demo dashboard.
    def update_random_states(self):
        if not self.connected():
            return []

        for lamp in self.collection.find():
            new_brightness = lamp['brightness'] + __import__('random').choice([-8, -5, 5, 8, 10])
            lamp['brightness'] = max(0, min(100, new_brightness))
            lamp['power_usage'] = max(20, min(190, lamp['power_usage'] + __import__('random').choice([-15, 10, 15])))
            lamp['status'] = 'on' if lamp['brightness'] >= 60 else 'dim'

            if __import__('random').random() < 0.12:
                lamp['fault'] = True
                lamp['status'] = 'fault'
                lamp['brightness'] = 0
                lamp['power_usage'] = 0
            elif lamp['fault'] and __import__('random').random() < 0.35:
                lamp['fault'] = False
                lamp['status'] = 'on'

            lamp['last_updated'] = datetime.utcnow()
            self.collection.update_one({'_id': lamp['_id']}, {'$set': lamp})

        return [_serialize_document(doc) for doc in self.collection.find().sort('lamp_id', 1)]
