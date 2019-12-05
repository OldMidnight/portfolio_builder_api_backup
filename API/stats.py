from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import WebsiteStats, User
from datetime import datetime, timedelta

bp = Blueprint('stats', __name__, url_prefix='/stats')

@bp.route('/add_record', methods=('POST',))
def add_record():
    data = request.get_json()
    domain = data['domain']
    date_time = data['date_time']
    print(data)
    stats = WebsiteStats(domain=domain, visit_date_time=date_time)
    stats.add()
    return jsonify(error=False), 200


@bp.route('/fetch_weekly', methods=('GET',))
@jwt_required
def fetch_weekly():
    ''' Fetch weekly stats '''
    current_time = datetime.utcnow()
    day = current_time.weekday()
    labels = []
    values = []
    value_labels = []

    user_id = get_jwt_identity()
    user_domain = User.query.filter_by(u_id=user_id).first().domain
    stats = WebsiteStats.query.filter(WebsiteStats.domain == user_domain, WebsiteStats.visit_date_time > (current_time - timedelta(days=6))).all()
    data = {
        '0': [],
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
    }

    data_labels = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    # append visits for specific days in data
    for stat in stats:
        if stat.visit_date_time.weekday() == 0:
            data['0'].append(stat.visit_date_time)
        elif stat.visit_date_time.weekday() == 1:
            data['1'].append(stat.visit_date_time)
        elif stat.visit_date_time.weekday() == 2:
            data['2'].append(stat.visit_date_time)
        elif stat.visit_date_time.weekday() == 3:
            data['3'].append(stat.visit_date_time)
        elif stat.visit_date_time.weekday() == 4:
            data['4'].append(stat.visit_date_time)
        elif stat.visit_date_time.weekday() == 5:
            data['5'].append(stat.visit_date_time)
        elif stat.visit_date_time.weekday() == 6:
            data['6'].append(stat.visit_date_time)

    temp_day = day
    if len(data[str(temp_day)]) == 0:
        temp_day -= 1
        while not data[str(temp_day)] and temp_day != day:
            if temp_day == 0:
                temp_day = 6
            else:
                temp_day -= 1
    if len(data[str(temp_day)]) == 0:
        last_visitor_time = 'No Visitors This Week.'
    else:
        last_visitor_time = data[str(temp_day)][-1]

        time_difference = str(current_time - last_visitor_time)
        time_difference = time_difference.split(':')
        time_difference[0] = time_difference[0] + ' hours,'
        time_difference[1] = time_difference[1] + ' minutes and'
        time_difference[2] = str(int(float(time_difference[2]))) + ' seconds ago'
        last_visitor_time = ' '.join(time_difference)

    i = day
    labels.append(i)

    i = day
    while i > 0:
        i -= 1
        labels.append(i)

    i = 6
    while i > day:
        labels.append(i)
        i -= 1

    labels.reverse()
    
    for day in labels:
        values.append(len(data[str(day)]))

    for label in labels:
        value_labels.append(data_labels[label])

    avg = 0
    for value in values:
        avg = avg + value

    avg = avg // 7

    highest_val = '0'
    for val in data:
        if len(data[val]) >= len(data[highest_val]):
            highest_val = val

    highest = str(len(data[highest_val])) + ' visitors - ' + data[highest_val][-1].strftime('%A')

    return jsonify(values=values, labels=value_labels, last_visitor_time=last_visitor_time, avg=avg, highest=highest), 200

@bp.route('/fetch_hourly', methods=('GET',))
@jwt_required
def fetch_hourly():
    current_time = datetime.utcnow()
    labels = []
    value_labels = []
    values = []
    user_id = get_jwt_identity()
    user_domain = User.query.filter_by(u_id=user_id).first().domain
    stats = WebsiteStats.query.filter(WebsiteStats.domain == user_domain, WebsiteStats.visit_date_time > (current_time - timedelta(hours=23))).all()

    data = {
        '0': [],
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '7': [],
        '8': [],
        '9': [],
        '10': [],
        '11': [],
        '12': [],
        '13': [],
        '14': [],
        '15': [],
        '16': [],
        '17': [],
        '18': [],
        '19': [],
        '20': [],
        '21': [],
        '22': [],
        '23': []
    }

    data_labels = {
        '0': '12 AM',
        '3': '3 AM',
        '6': '6 AM',
        '9': '9 AM',
        '12': '12 PM',
        '15': '3 PM',
        '18': '6 PM',
        '21': '9 PM'
    }

    for stat in stats:
        hour = stat.visit_date_time.hour
        data[str(hour)].append(stat.visit_date_time)


    i = current_time.hour
    labels.append(i)


    first_label = labels[0]
    i = first_label
    while i != 0:
        i -= 1
        labels.append(i)

    i = 23
    while i != first_label:
        labels.append(i)
        i -= 1

    labels.reverse()

    for hour in labels:
        values.append(len(data[str(hour)]))

    for label in labels:
        if label % 3 == 0:
            value_labels.append(data_labels[str(label)])
        else:
            value_labels.append(' ')

    avg = 0
    for value in values:
        avg = avg + value

    avg = avg // 8

    highest_val = '0'
    for val in data:
        if len(data[val]) >= len(data[highest_val]):
            highest_val = val

    if not data[highest_val]:
        highest = 'No visitors yet'
    else:
        highest = str(len(data[highest_val])) + ' visitors - ' + str(data[highest_val][-1].strftime('%I %p'))

    return jsonify(values=values, labels=value_labels, avg=avg, highest=highest), 200

@bp.route('/fetch_monthly', methods=('GET',))
@jwt_required
def fetch_monthly():
    current_time = datetime.utcnow()
    labels = []
    value_labels = []
    values = []
    user_id = get_jwt_identity()
    user_domain = User.query.filter_by(u_id=user_id).first().domain
    stats = WebsiteStats.query.filter(WebsiteStats.domain == user_domain, WebsiteStats.visit_date_time > (current_time - timedelta(days=364))).all()
    data = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '7': [],
        '8': [],
        '9': [],
        '10': [],
        '11': [],
        '12': []
    }

    data_labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    for stat in stats:
        month = stat.visit_date_time.month
        data[str(month)].append(stat.visit_date_time)


    i = current_time.month
    labels.append(i)

    while i != 1:
        i -= 1
        labels.append(i)
    
    i = 12
    while i != current_time.month:
        labels.append(i)
        i -= 1
    labels.reverse()
    
    for month in labels:
        values.append(len(data[str(month)]))

    for label in labels:
        value_labels.append(data_labels[label - 1])

    avg = 0
    for value in values:
        avg = avg + value

    avg = avg // 12

    highest_val = '1'
    for val in data:
        if len(data[val]) >= len(data[highest_val]):
            highest_val = val

    if not data[highest_val]:
        highest = 'No visitors yet'
    else:
        highest = str(len(data[highest_val])) + ' visitors - ' + str(data[highest_val][-1].strftime('%B'))

    return jsonify(values=values, labels=value_labels, avg=avg, highest=highest), 200