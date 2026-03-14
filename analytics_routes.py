"""
Analytics Dashboard Routes
Add these routes to app.py
"""

@app.route('/analytics')
def analytics():
    """Analytics dashboard with historical data"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        user = db.session.get(User, session['user_id'])
        
        # Get historical expense data (last 12 months)
        twelve_months_ago = datetime.now() - timedelta(days=365)
        expenses = Expense.query.filter(
            Expense.user_id == user.id,
            Expense.date >= twelve_months_ago
        ).order_by(Expense.date).all()
        
        # Group by month
        monthly_income = {}
        monthly_expense = {}
        
        for exp in expenses:
            month_key = exp.date.strftime('%Y-%m')
            if exp.type == 'income':
                monthly_income[month_key] = monthly_income.get(month_key, 0) + exp.amount
            else:
                monthly_expense[month_key] = monthly_expense.get(month_key, 0) + exp.amount
        
        # Prepare chart data
        months = sorted(set(list(monthly_income.keys()) + list(monthly_expense.keys())))
        income_data = [monthly_income.get(m, 0) for m in months]
        expense_data = [monthly_expense.get(m, 0) for m in months]
        profit_data = [monthly_income.get(m, 0) - monthly_expense.get(m, 0) for m in months]
        
        # Format month labels
        month_labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in months]
        
        # Category-wise expense breakdown
        category_expenses = {}
        for exp in expenses:
            if exp.type == 'expense':
                category_expenses[exp.category] = category_expenses.get(exp.category, 0) + exp.amount
        
        # Disease history trends
        disease_history = DiseaseDetection.query.filter_by(user_id=user.id).order_by(DiseaseDetection.detected_at).all()
        disease_by_month = {}
        for disease in disease_history:
            month_key = disease.detected_at.strftime('%Y-%m')
            disease_by_month[month_key] = disease_by_month.get(month_key, 0) + 1
        
        # Crop yield history (if available)
        crop_data_history = CropData.query.filter_by(user_id=user.id).all()
        
        # Calculate key metrics
        total_income = sum(income_data)
        total_expenses = sum(expense_data)
        net_profit = total_income - total_expenses
        avg_monthly_profit = net_profit / len(months) if months else 0
        
        # ROI calculation
        roi = (net_profit / total_expenses * 100) if total_expenses > 0 else 0
        
        # Growth rate (comparing last 3 months vs previous 3 months)
        if len(profit_data) >= 6:
            recent_profit = sum(profit_data[-3:])
            previous_profit = sum(profit_data[-6:-3])
            growth_rate = ((recent_profit - previous_profit) / previous_profit * 100) if previous_profit != 0 else 0
        else:
            growth_rate = 0
        
        analytics_data = {
            'user': user,
            'months': month_labels,
            'income_data': income_data,
            'expense_data': expense_data,
            'profit_data': profit_data,
            'category_expenses': category_expenses,
            'disease_trends': disease_by_month,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'avg_monthly_profit': round(avg_monthly_profit, 2),
            'roi': round(roi, 2),
            'growth_rate': round(growth_rate, 2),
            'total_diseases_detected': len(disease_history),
            'crops_planted': len(crop_data_history)
        }
        
        return render_template('analytics.html', **analytics_data)
    
    except Exception as e:
        logger.error(f"Analytics dashboard error: {e}")
        flash('Error loading analytics dashboard', 'error')
        return redirect(url_for('dashboard'))

@app.route('/api/analytics/export', methods=['GET'])
def export_analytics():
    """Export analytics data as CSV"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user = db.session.get(User, session['user_id'])
        
        # Get all expenses
        expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()
        
        # Create CSV
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Date', 'Type', 'Category', 'Description', 'Amount'])
        
        # Write data
        for exp in expenses:
            writer.writerow([
                exp.date.strftime('%Y-%m-%d'),
                exp.type,
                exp.category,
                exp.description,
                exp.amount
            ])
        
        # Create response
        output.seek(0)
        return send_file(
            BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'analytics_{user.username}_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    
    except Exception as e:
        logger.error(f"Export analytics error: {e}")
        return jsonify({'error': str(e)}), 500
