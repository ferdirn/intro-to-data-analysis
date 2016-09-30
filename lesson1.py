"""Enrollments."""

import unicodecsv


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


enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

print 'length of data enrollments is', len(enrollments)
print 'length of data daily engagement is', len(daily_engagement)
print 'length of data project submissions is', len(project_submissions)

unique_enrolled_students = get_unique_students(enrollments)
unique_engaged_students = get_unique_students(daily_engagement)
unique_project_submitters = get_unique_students(project_submissions)

print 'total unique enrolled students is', len(unique_enrolled_students)
print 'total unique engaged students is', len(unique_engaged_students)
print 'total unique project submitters is', len(unique_project_submitters)
