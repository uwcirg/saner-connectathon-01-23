import json
import argparse

parser = argparse.ArgumentParser(description='Create a FHIR bundle from a json file array of resources.')
parser.add_argument('filename', metavar='F', type=str, nargs='+',
                    help='the name of the json file')

args = parser.parse_args()

entry_file = open(args.filename[0], 'r')
entries = json.loads(entry_file.read())

outfile = open('bundle.json', 'w')

newEntries = []
for entry in entries:
    if 'resource' not in entry.keys():
        if 'resourceType' in entry.keys():
            newEntry = {'resource': entry}
        else:
            print("entries.json doesn't contain resources")
            exit(1)
    else:
        newEntry = entry
    # entry['request'] = {'method': 'PUT', 'url': entry['resource']['resourceType'] + "/" + entry['resource']['id']}
    newEntry['request'] = {'method': 'POST', 'url': newEntry['resource']['resourceType']}
    newEntries.append(newEntry)

bundle = {
    'resourceType': 'Bundle',
    'id': 'mr-sample-upload',
    'type': 'transaction',
    'entry': newEntries
}

outfile.write(json.dumps(bundle, indent='\t'))