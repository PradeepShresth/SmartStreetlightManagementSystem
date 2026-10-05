from flask import Flask, jsonify, render_template, request

# Import database service classes for MongoDB and Redis.
from database.mongo_service import MongoService
from database.redis_service import RedisService

# Create the Flask app.
app = Flask(__name__)

# Create service objects to handle storage and live data.
mongo_service = MongoService()
redis_service = RedisService()


# Homepage: show the dashboard view.
@app.route('/')
def home():
    summary = mongo_service.get_summary()
    lamps = mongo_service.get_all_lamps()
    return render_template('dashboard.html', summary=summary, lamps=lamps)


# Alias route for the dashboard page.
@app.route('/dashboard')
def dashboard():
    summary = mongo_service.get_summary()
    lamps = mongo_service.get_all_lamps()
    return render_template('dashboard.html', summary=summary, lamps=lamps)


# Return summary information for the dashboard and API users.
@app.route('/api/summary')
def summary():
    summary_data = mongo_service.get_summary()
    return jsonify({
        'summary': summary_data,
        'faulty_lamps': mongo_service.get_faulty_lamps(),
        'alerts': redis_service.get_recent_alerts(),
        'mongo_connected': mongo_service.connected(),
        'redis_connected': redis_service.connected(),
    })


# Get all lamps or add a new lamp.
@app.route('/api/lights', methods=['GET', 'POST'])
def lights():
    if request.method == 'POST':
        payload = request.get_json(silent=True) or {}
        lamp_id = payload.get('lamp_id')
        zone = payload.get('zone')
        if not lamp_id or not zone:
            return jsonify({'error': 'lamp_id and zone are required'}), 400

        lamp = mongo_service.add_lamp(
            lamp_id=lamp_id,
            zone=zone,
            lamp_type=payload.get('lamp_type', 'LED'),
            location=payload.get('location', 'Unknown'),
            power_rating=payload.get('power_rating', 80),
            brightness=payload.get('brightness', 100),
            status=payload.get('status', 'on'),
            fault=payload.get('fault', False)
        )
        redis_service.sync_from_mongo(mongo_service.get_all_lamps())
        return jsonify({'message': 'Lamp added', 'lamp': lamp}), 201

    lamps = mongo_service.get_all_lamps()
    summary_data = mongo_service.get_summary()
    live_state = redis_service.get_live_state()

    return jsonify({
        'lamps': lamps,
        'summary': summary_data,
        'live_state': live_state,
        'faulty_lamps': mongo_service.get_faulty_lamps(),
        'alerts': redis_service.get_recent_alerts(),
        'mongo_connected': mongo_service.connected(),
        'redis_connected': redis_service.connected(),
    })


# Update or delete one streetlight by lamp ID.
@app.route('/api/lights/<lamp_id>', methods=['PUT', 'DELETE'])
def lamp_detail(lamp_id):
    if request.method == 'PUT':
        payload = request.get_json(silent=True) or {}
        updated = mongo_service.update_lamp(lamp_id, **payload)
        redis_service.sync_from_mongo(mongo_service.get_all_lamps())
        return jsonify({'message': 'Lamp updated', 'lamp': updated})

    mongo_service.delete_lamp(lamp_id)
    redis_service.sync_from_mongo(mongo_service.get_all_lamps())
    return jsonify({'message': f'Lamp {lamp_id} removed'})


# Record when a technician performs maintenance on a lamp.
@app.route('/api/maintenance', methods=['POST'])
def maintenance_record():
    payload = request.get_json(silent=True) or {}
    lamp_id = payload.get('lamp_id')
    action = payload.get('action')
    description = payload.get('description')
    technician = payload.get('technician', 'System')

    if not lamp_id or not action or not description:
        return jsonify({'error': 'lamp_id, action and description are required'}), 400

    record = mongo_service.add_maintenance_record(lamp_id, action, description, technician)
    return jsonify({'message': 'Maintenance recorded', 'record': record})


# Simulate a live refresh of lamp state and update Redis summary.
@app.route('/api/refresh')
def refresh_lights():
    lamps = mongo_service.update_random_states()
    if lamps:
        redis_service.sync_from_mongo(lamps)
        redis_service.save_summary(mongo_service.get_summary())
        for lamp in lamps:
            if lamp.get('fault'):
                redis_service.add_alert(f"{lamp['lamp_id']} reported a fault in {lamp['zone']}")

    return jsonify({
        'message': 'Streetlight data refreshed successfully.',
        'summary': mongo_service.get_summary(),
        'faulty_lamps': mongo_service.get_faulty_lamps(),
        'alerts': redis_service.get_recent_alerts(),
        'lamps': lamps,
    })


# Alternative update route for the dashboard refresh action.
@app.route('/api/update')
def update_lights():
    lamps = mongo_service.update_random_states()
    if lamps:
        redis_service.sync_from_mongo(lamps)
        redis_service.save_summary(mongo_service.get_summary())
        for lamp in lamps:
            if lamp.get('fault'):
                redis_service.add_alert(f"{lamp['lamp_id']} reported a fault in {lamp['zone']}")

    return jsonify({
        'message': 'Streetlight records updated successfully.',
        'summary': mongo_service.get_summary(),
        'faulty_lamps': mongo_service.get_faulty_lamps(),
        'alerts': redis_service.get_recent_alerts(),
    })


if __name__ == '__main__':
    # Seed initial lamp records if MongoDB is empty.
    mongo_service.seed_data()
    lamps = mongo_service.get_all_lamps()

    # Copy MongoDB data into Redis for fast live access.
    redis_service.sync_from_mongo(lamps)
    redis_service.save_summary(mongo_service.get_summary())

    # Start the local web application.
    app.run(debug=True, host='0.0.0.0', port=5000)
