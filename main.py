import argparse
import rdflib

from pathlib import Path

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='sparql-query',
                    description='Queries a TTL file via SPARQL',
                    epilog='Peronsal project by @jmoney')

    parser.add_argument('--query-file', action='store', dest='query_file')
    parser.add_argument('--local-ttl', action='store', dest='local_ttl')
    parser.add_argument('--format', action='store', dest='format', default='text/turtle')

    args = parser.parse_args()

    g = rdflib.Graph()
    result = g.parse(location=args.local_ttl, format=args.format)

    query = Path(args.query_file).read_text()
    qres = g.query(query)
    print(qres.serialize(format="json").decode('utf-8'))
