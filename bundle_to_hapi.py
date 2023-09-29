import requests
import argparse

parser = argparse.ArgumentParser(description='Upload a FHIR bundle from a json file to a fhir server.')
parser.add_argument('filename', metavar='F', type=str, nargs='+',
                    help='Name of the bundle json file')
parser.add_argument('endpoint', matavar='E', type='str', nargs='+',
                    help='FHIR server base endpoint')

args = parser.parse_args()

bundle_file = open(args.filename[0], 'r')
bundle = bundle_file.read()

# url = 'https://fhir.agg-data.connectathon.dev.cirg.uw.edu/fhir/'
# url = 'https://fhir.ips-demo.dev.cirg.uw.edu/fhir/'
url = 'https://localhost:8080/'
hed = {'Content-Type': 'application/json+fhir'}
data = bundle

response = requests.post(url=url, data=data, headers=hed)
print(response.text)
print(response.status_code)