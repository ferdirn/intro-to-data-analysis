"""Enrollments."""

import unicodecsv
from datetime import datetime


def read_csv(filename):
    """Read CSV function."""
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)


def get_unique_students(data):
    """Get unique students function."""
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students


def remove_udacity_accounts(data):
    """Remove udacity accounts."""
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_account:
            non_udacity_data.append(data_point)
    return non_udacity_data


def remove_free_trial_cancels(data):
    """Remove free trial cancels."""
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data


def within_one_week(join_date, engagement_date):
    """Within one week."""
    time_delta = engagement_date - join_date
    return time_delta.days < 7


enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

for enrollment in enrollments:
    enrollment['join_date'] = datetime.strptime(enrollment['join_date'], '%Y-%m-%d')
    enrollment['cancel_date'] = None if enrollment['cancel_date'] == '' else datetime.strptime(enrollment['cancel_date'], '%Y-%m-%d')
    enrollment['days_to_cancel'] = None if enrollment['days_to_cancel'] == '' else int(enrollment['days_to_cancel'])
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'

for engagement in daily_engagement:
    engagement['utc_date'] = datetime.strptime(engagement['utc_date'], '%Y-%m-%d')
    engagement['num_courses_visited'] = float(engagement['num_courses_visited'])
    engagement['total_minutes_visited'] = float(engagement['total_minutes_visited'])
    engagement['lessons_completed'] = float(engagement['lessons_completed'])
    engagement['projects_completed'] = float(engagement['projects_completed'])

print 'length of data enrollments is', len(enrollments)
print 'length of data daily engagement is', len(daily_engagement)
print 'length of data project submissions is', len(project_submissions)

unique_enrolled_students = get_unique_students(enrollments)
unique_engaged_students = get_unique_students(daily_engagement)
unique_project_submitters = get_unique_students(project_submissions)

print 'total unique enrolled students is', len(unique_enrolled_students)
print 'total unique engaged students is', len(unique_engaged_students)
print 'total unique project submitters is', len(unique_project_submitters)

print daily_engagement[0]['account_key']

suprising = 0
for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in unique_engaged_students and enrollment['join_date'] != enrollment['cancel_date']:
        print enrollment
        suprising = suprising + 1

print 'suprising', suprising

udacity_test_account = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_account.add(enrollment['account_key'])

non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print 'total non_udacity_enrollments', len(non_udacity_enrollments)
print 'total non_udacity_engagement', len(non_udacity_engagement)
print 'total non_udacity_submissions', len(non_udacity_submissions)

paid_students = dict()
for enrollment in non_udacity_enrollments:
    if not enrollment['is_canceled'] or enrollment['days_to_cancel'] > 7:
        key = enrollment['account_key']
        val = enrollment['join_date']
        if key not in paid_students or paid_students[key] < val:
            paid_students[key] = val

print 'total paid_students', len(paid_students)

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)

print 'total paid_enrollments', len(paid_enrollments)
print 'total paid_engagement', len(paid_engagement)
print 'total paid_submissions', len(paid_submissions)

paid_engagement_in_first_week = []
for engagement in paid_engagement:
    account_key = engagement['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement['utc_date']

    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement)

print 'total paid_engagement_in_first_week', len(paid_engagement_in_first_week)
