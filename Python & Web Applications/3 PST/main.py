#!/usr/bin/env python3

import argparse
import validators
import requests
import yaml

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4 import Comment

def scan_forms(parsed_html):
    forms = parsed_html.find_all('form')
    for form in forms:
        if(form.get('action') and (form.get('action').find('https') < 0) and (urlparse(url).scheme != 'https')):
            return 'Form Issue: Insecure form action ' + form.get('action') + ' found in document\n'

def scan_comments(parsed_html):
    comments  = parsed_html.find_all(string=lambda text:isinstance(text,Comment))
    for comment in comments:
      if(comment.find('key: ') > -1):
        return 'Comment Issue: Key is found in the HTML comments, please remove\n'

def scan_inputs(parsed_html):
    password_inputs = parsed_html.find_all('input', { 'name' : 'password'})
    for password_input in password_inputs:
      if(password_input.get('type') != 'password'):
        return 'Input Issue: Plaintext password input found. Please change to password type input\n'

config = {'forms': True, 'comments': True, 'passwords': True}

parser = argparse.ArgumentParser(description='The Achilles HTML Vulnerability Analyzer Version 1.0')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument('url', type=str, help="The URL of the HTML to analyze")
parser.add_argument('--config', help='Path to configuration file')
parser.add_argument('-o', '--output', help='Report file output path')

args = parser.parse_args()

if(args.config):
    print('Using config file: ' + args.config)
    config_file = open(args.config, 'r')
    config_from_file = yaml.load(config_file)
    if(config_from_file):
        config = { **config, **config_from_file}

if(args.config):
  print('Using config file: ' + args.config)
  config_file = open(args.config, 'r')

url = args.url

report = ''
    
if(validators.url(url)):
    result_html = requests.get(url).text
    parsed_html = BeautifulSoup(result_html, 'html.parser')
    if(config['forms'] and scan_forms(parsed_html)):
        report += scan_forms(parsed_html)
    if(config['comments'] and scan_comments(parsed_html)):
        report += scan_comments(parsed_html)
    if(config['comments'] and scan_inputs(parsed_html)):
        report += scan_inputs(parsed_html)
else:
    print('Invalud URL. Please include full URL including scheme.')

if(report == ''):
    report += 'Nice job! Your HTML document is secure!\n'
else:
    header =  'Vulnerability Report is as follows:\n'
    header += '==================================\n\n'
    
    report = header + report
    
print(report)
    
if(args.output):
    f = open(args.output, 'w')
    f.write(report)
    f.close
    print('Report saved to: ' + args.output)