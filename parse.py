from bs4 import BeautifulSoup
import os
from pathlib import Path
import pickle
import json
import pprint
import re

pp = pprint.PrettyPrinter(indent=2)

def record_selection(sel, record):
    """Take a selection of key value list and add them to a dict
    
    Arguments:
        sel {List[Key, Value]} 
        record {dict} - dict to store passed key value into
    """
    if len(sel) < 2:
        raise ValueError

    record[sel[0].text.strip()] = sel[1].text.strip()

def parse_experiences(soup):
    experiences = []
    for content in soup.select('#experience-section .pv-profile-section__card-item-v2'):
        multi_role_company = content.select_one('.pv-entity__company-details')
        if multi_role_company:
            template = {}
            record_selection(multi_role_company.select('h3 span'), template)
            
            for item in content.select('li.pv-entity__position-group-role-item'):
                exp = template.copy()
                record_selection(item.select('.pv-entity__summary-info-v2 h3 span'), exp)
                for detail in item.select('h4'):
                    record_selection(detail.select('span'), exp)
                experiences.append(exp)
        else:
            experience = {}
            context = content.select_one('.pv-entity__summary-info')
            experience['role'] = context.select_one('h3').text.strip()
            experience['company'] = content.select_one('.pv-entity__secondary-title').text.strip()
            for item in context.select('h4'):
                record_selection(item.select('span'), experience)
            experiences.append(experience)
            
    return experiences

def parse_educations(soup):
    educations = []
    for item in soup.select('#education-section li'):
        education = {}
        education['school'] = item.select_one('.pv-entity__school-name').text.strip()
        for p in item.select('.pv-entity__summary-info p'):
            print(p)
            record_selection(p.select('span'), education)
        educations.append(education)
    return educations

def parse_linkedin_profile(html):
    result = {}
    selector_mapping = {
        'name': 'h1.pv-top-card-section__name',
        'role': 'h2.pv-top-card-section__headline',
        'summary': 'p.pv-top-card-section__summary-text'
    }

    soup = BeautifulSoup(html, 'html.parser')
    for key, value in selector_mapping.items():
        try:
            result[key] = soup.select_one(value).text.strip()
        except AttributeError:
            result[key] = None

    result['experiences'] = parse_experiences(soup)
    result['educations'] = parse_educations(soup)
    return result

if __name__ == '__main__':
    folder = Path('./pages')
    results = []
    i = 0
    for fname in os.listdir(folder):
        if not re.match('.+.html$', fname):
            continue
        i+=1
        if i > 3:
            break
        print('parsing', fname)
        with open(folder/fname, 'r') as f:
            html = f.read()
            result = parse_linkedin_profile(html)
            if result['name'] != None:
                results.append(result)
        
    pp.pprint(results)

    # with open('./profiles.p', 'wb') as f:
    #     pickle.dump(results, f) 
        
    # with open('./profiles2.json', 'w') as f:
    #     json.dump(results, f)