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

enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

for enrollment in enrollments:
    enrollment['join_date'] = datetime.strptime(enrollment['join_date'], '%Y-%m-%d')
    enrollment['cancel_date'] = None if enrollment['cancel_date'] == '' else datetime.strptime(enrollment['cancel_date'], '%Y-%m-%d')
    enrollment['days_to_cancel'] = None if enrollment['days_to_cancel'] == '' else int(enrollment['days_to_cancel'])
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'

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
    if not enrollment['days_to_cancel'] or enrollment['days_to_cancel'] > 7:
        key = enrollment['account_key']
        val = enrollment['join_date']
        if key not in paid_students or paid_students[key] < val:
            paid_students[key] = val

print 'total paid_students', len(paid_students)
