# Waste Management API Routes
from flask import jsonify, request, session
from datetime import datetime, timedelta

# WASTE MANAGEMENT API ROUTES
def register_waste_routes(app, db, CropResidue, CompostBatch, calculate_crop_residue, calculate_residue_management_options, calculate_compost_recipe, calculate_vermicompost_requirements):
    
    @app.route('/api/waste/residue/calculate', methods=['POST'])
    def calculate_residue():
        """Calculate crop residue from harvest data"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        crop_name = data.get('crop_name')
        yield_kg = data.get('yield_kg')
        
        if not crop_name or not yield_kg:
            return jsonify({'error': 'crop_name and yield_kg required'}), 400
        
        # Calculate residue
        residue_data = calculate_crop_residue(crop_name, float(yield_kg))
        
        # Calculate management options
        management_options = calculate_residue_management_options(
            residue_data['residue_quantity'], 
            crop_name
        )
        
        # Save to database
        residue = CropResidue(
            user_id=session['user_id'],
            crop_name=crop_name,
            harvest_yield=float(yield_kg),
            residue_quantity=residue_data['residue_quantity'],
            residue_type='straw'
        )
        db.session.add(residue)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'residue_quantity': residue_data['residue_quantity'],
            'ratio': residue_data['ratio'],
            'management_options': management_options
        })

    @app.route('/api/waste/residue/history', methods=['GET'])
    def get_residue_history():
        """Get crop residue history"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        residues = CropResidue.query.filter_by(user_id=session['user_id']).order_by(CropResidue.created_at.desc()).limit(10).all()
        
        return jsonify([{
            'id': r.id,
            'crop_name': r.crop_name,
            'harvest_yield': r.harvest_yield,
            'residue_quantity': r.residue_quantity,
            'management_method': r.management_method,
            'date': r.created_at.strftime('%Y-%m-%d')
        } for r in residues])

    @app.route('/api/waste/compost/recipe', methods=['POST'])
    def get_compost_recipe():
        """Calculate optimal compost recipe"""
        data = request.get_json()
        
        green_waste = float(data.get('green_waste', 0))
        brown_waste = float(data.get('brown_waste', 0))
        manure = float(data.get('manure', 0))
        
        recipe = calculate_compost_recipe(green_waste, brown_waste, manure)
        
        return jsonify({
            'success': True,
            'recipe': recipe
        })

    @app.route('/api/waste/compost/create', methods=['POST'])
    def create_compost_batch():
        """Create new compost batch"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        # Calculate completion date based on method
        method = data.get('method', 'hot')
        days_map = {'hot': 45, 'cold': 90, 'vermi': 60}
        days = days_map.get(method, 60)
        
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        completion_date = start_date + timedelta(days=days)
        
        batch = CompostBatch(
            user_id=session['user_id'],
            batch_name=data.get('batch_name'),
            start_date=start_date,
            expected_completion=completion_date,
            composting_method=method,
            total_input_weight=float(data.get('total_weight')),
            green_waste=float(data.get('green_waste', 0)),
            brown_waste=float(data.get('brown_waste', 0)),
            manure=float(data.get('manure', 0))
        )
        
        db.session.add(batch)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'batch_id': batch.id,
            'expected_completion': completion_date.strftime('%Y-%m-%d'),
            'message': 'Compost batch created successfully'
        })

    @app.route('/api/waste/compost/batches', methods=['GET'])
    def get_compost_batches():
        """Get all compost batches"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        batches = CompostBatch.query.filter_by(user_id=session['user_id']).order_by(CompostBatch.created_at.desc()).all()
        
        result = []
        for batch in batches:
            days_remaining = (batch.expected_completion - datetime.now().date()).days
            progress = max(0, min(100, 100 - (days_remaining / 60 * 100)))
            
            result.append({
                'id': batch.id,
                'batch_name': batch.batch_name,
                'method': batch.composting_method,
                'start_date': batch.start_date.strftime('%Y-%m-%d'),
                'expected_completion': batch.expected_completion.strftime('%Y-%m-%d'),
                'days_remaining': max(0, days_remaining),
                'progress': round(progress, 1),
                'input_weight': batch.total_input_weight,
                'expected_output': round(batch.total_input_weight * 0.4, 2),
                'status': batch.status,
                'temperature': batch.current_temperature,
                'moisture': batch.moisture_level
            })
        
        return jsonify(result)

    @app.route('/api/waste/compost/update/<int:batch_id>', methods=['PUT'])
    def update_compost_batch(batch_id):
        """Update compost batch progress"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        batch = CompostBatch.query.filter_by(id=batch_id, user_id=session['user_id']).first()
        if not batch:
            return jsonify({'error': 'Batch not found'}), 404
        
        data = request.get_json()
        
        if 'temperature' in data:
            batch.current_temperature = float(data['temperature'])
        if 'moisture' in data:
            batch.moisture_level = float(data['moisture'])
        if 'turning' in data and data['turning']:
            batch.turning_count += 1
        if 'status' in data:
            batch.status = data['status']
        if 'output_weight' in data:
            batch.output_weight = float(data['output_weight'])
        
        batch.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Batch updated successfully'
        })

    @app.route('/api/waste/vermicompost/calculate', methods=['POST'])
    def calculate_vermicompost():
        """Calculate vermicomposting requirements"""
        data = request.get_json()
        waste_per_day = float(data.get('waste_per_day', 0))
        
        requirements = calculate_vermicompost_requirements(waste_per_day)
        
        return jsonify({
            'success': True,
            'requirements': requirements
        })

    @app.route('/api/waste/dashboard', methods=['GET'])
    def waste_dashboard():
        """Get waste management dashboard data"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        user_id = session['user_id']
        
        # Get residue data
        residues = CropResidue.query.filter_by(user_id=user_id).all()
        total_residue = sum(r.residue_quantity for r in residues)
        
        # Get compost batches
        batches = CompostBatch.query.filter_by(user_id=user_id).all()
        active_batches = [b for b in batches if b.status == 'active']
        completed_batches = [b for b in batches if b.status == 'ready' or b.status == 'harvested']
        
        total_compost_produced = sum(b.output_weight or (b.total_input_weight * 0.4) for b in completed_batches)
        
        # Calculate potential revenue
        potential_revenue = 0
        for residue in residues:
            options = calculate_residue_management_options(residue.residue_quantity, residue.crop_name)
            potential_revenue += options['burning_comparison']['best_alternative_revenue']
        
        # Carbon savings
        total_carbon_saved = total_residue * 0.0015  # tons
        
        return jsonify({
            'total_residue_kg': round(total_residue, 2),
            'active_compost_batches': len(active_batches),
            'total_compost_produced_kg': round(total_compost_produced, 2),
            'potential_revenue': round(potential_revenue, 2),
            'carbon_saved_tons': round(total_carbon_saved, 3),
            'carbon_credit_value': round(total_carbon_saved * 1500, 2),
            'waste_diverted_from_burning': round(total_residue, 2)
        })
