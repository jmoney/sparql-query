import argparse
import os
import rdflib
import re

from pathlib import Path
from rdflib import Namespace, XSD


binding_re = re.compile(r'^SPARQL_BIND_(?P<type>.+)_(?P<name>.+)$')
NOTES_NS = Namespace('https://www.jmoney.dev/notes#')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='sparql-query',
                    description='Queries a TTL file via SPARQL',
                    epilog='Peronsal project by @jmoney')

    parser.add_argument('--query-file', action='store', dest='query_file')
    parser.add_argument('--local-ttl', action='store', dest='local_ttl')
    parser.add_argument('--format', action='store', dest='format', default='json')

    args = parser.parse_args()

    g = rdflib.Graph()
    location = Path(args.local_ttl)
    if location.is_dir():
        for file in location.iterdir():
            if file.suffix == '.ttl':
                g.parse(location=file, format="text/turtle")
    else:
        g.parse(location=location, format="text/turtle")

    query = Path(args.query_file).read_text()
    bindings = {}
    for name, value in os.environ.items():
        if match := binding_re.match(name):
            bindings = {**bindings, match.group('name'): rdflib.Literal(value, datatype=XSD[match.group('type')])}

    qres = g.query(query, initBindings=bindings)
    if qres.type == 'CONSTRUCT':
        qres.graph.bind('notes', NOTES_NS)
    print(qres.serialize(format=args.format).decode('utf-8'))
