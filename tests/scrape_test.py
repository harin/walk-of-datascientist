import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from scrape import is_datascience_role_name, parse_linkedin_profile


def test_is_datascience_role_name():
    valid_roles = [
        'Data Scientist @ Instagram',
        'Data Scientist at Google',
        'Data Scientist @ Airbnb',
    ]

    invalid_roles = [
        'Head of Payments Data Science at Facebook',
        'Product at Instagram',
        'Database Reporting and Programming',
        'Data Scientist at Apple'
    ]

    roles = ['data scientist']
    companies = ['facebook', 'instagram', 'google', 'airbnb']
    
    for role in valid_roles:
        assert is_datascience_role_name(role, roles, companies) == True

    for role in invalid_roles:
        assert is_datascience_role_name(role, roles, companies) == False


def test_parse_linkedin_profile():
    with open('./tests/data/adamstopek__.html', 'r') as f:
        html = f.read()
        result = parse_linkedin_profile(html)
        assert result['name'] == 'Adam Stopek'
        assert result['role'] == 'Data Scientist @ Google'