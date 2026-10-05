import os
import json

import redis


class RedisService:
    # Connect to the local Redis server for fast live updates.
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', '6379'))
        self.username = os.getenv('REDIS_USERNAME')
        self.password = os.getenv('REDIS_PASSWORD')
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            decode_responses=True,
        )

    # Check if Redis is responding to requests.
    def connected(self):
        try:
            self.client.ping()
            return True
        except Exception:
            return False

    # Copy the current MongoDB lamp data into Redis so it can be accessed quickly.
    def sync_from_mongo(self, lamps):
        if not self.connected() or not lamps:
            return

        for lamp in lamps:
            payload = {
                'lamp_id': lamp['lamp_id'],
                'zone': lamp['zone'],
                'status': lamp['status'],
                'brightness': str(lamp['brightness']),
                'power_usage': str(lamp['power_usage']),
                'fault': str(bool(lamp.get('fault', False))),
                'last_updated': lamp['last_updated'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(lamp['last_updated'], 'strftime') else str(lamp['last_updated'])
            }
            key = f"lamp:{lamp['lamp_id']}"
            for field, value in payload.items():
                self.client.hset(key, field, value)
            self.client.sadd('streetlight:all_lamps', lamp['lamp_id'])
            self.client.sadd(f"status:{lamp['status']}:lamps", lamp['lamp_id'])
            self.client.sadd(f"zone:{lamp['zone']}:lamps", lamp['lamp_id'])

    # Store a quick summary in Redis for the dashboard widgets.
    def save_summary(self, summary):
        if not self.connected():
            return

        payload = {
            'total_lamps': str(summary.get('total_lamps', 0)),
            'on_count': str(summary.get('on_count', 0)),
            'dim_count': str(summary.get('dim_count', 0)),
            'fault_count': str(summary.get('fault_count', 0)),
            'total_energy': str(summary.get('total_energy', 0)),
        }
        for field, value in payload.items():
            self.client.hset('streetlight:summary', field, value)

        lamp_ids = list(self.client.smembers('streetlight:all_lamps'))
        self.client.delete('streetlight:faulty')
        faulty_ids = []
        for lamp_id in lamp_ids:
            lamp_data = self.client.hgetall(f'lamp:{lamp_id}')
            if lamp_data.get('fault') == 'True':
                faulty_ids.append(lamp_id)

        if faulty_ids:
            self.client.sadd('streetlight:faulty', *faulty_ids)

    # Read the current live lamp status stored in Redis.
    def get_live_state(self):
        if not self.connected():
            return {}

        lamp_ids = self.client.smembers('streetlight:all_lamps')
        state = {}
        for lamp_id in lamp_ids:
            data = self.client.hgetall(f'lamp:{lamp_id}')
            if data:
                state[lamp_id] = data
        return state

    # Get lamp IDs currently marked as faulty in Redis.
    def get_faulty_lamps(self):
        if not self.connected():
            return []
        return list(self.client.smembers('streetlight:faulty'))

    # Add an alert for a fault or important event.
    def add_alert(self, message):
        if not self.connected():
            return

        self.client.lpush('streetlight:alerts', json.dumps({
            'message': message,
            'type': 'fault'
        }))
        self.client.ltrim('streetlight:alerts', 0, 49)

    # Read the latest fault alerts stored in Redis.
    def get_recent_alerts(self):
        if not self.connected():
            return []

        raw = self.client.lrange('streetlight:alerts', 0, 9)
        alerts = []
        for item in raw:
            try:
                alerts.append(json.loads(item))
            except Exception:
                alerts.append({'message': item})
        return alerts
