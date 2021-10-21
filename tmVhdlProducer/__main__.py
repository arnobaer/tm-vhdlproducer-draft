import argparse

from .eventsetup import load, sorted_objects
from .algodist import distribute


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='file')
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.filename) as fp:
        es = load(fp)

    print(es)

    condition_cache = {}
    for condition in es.get('conditions'):
        if condition.get('name') not in condition_cache:
            condition_cache[condition.get('name')] = condition

    for algorithm in es.get('algorithms'):
        for token in algorithm.get('conditions'):
            print(token, condition_cache[token])

    print('object_bxs:')
    for x in calc_object_bx_instances(es):
        print(x)

    print('object_bx_correlations:')
    for x in calc_object_bx_correlation_instances(es):
        print(x)

    for module in distribute(es).modules:
        print(module.id, len(module.algorithms), len(module.conditions), len(module.object_bxs), len(module.object_bx_correlations))


def calc_object_bx_instances(es):
    object_bx = set()
    for condition in es.get('conditions'):
        for object_ in condition.get('objects'):
            key = object_.get('type'), object_.get('bx_offset')
            object_bx.add(key)
    return object_bx


def calc_object_bx_correlation_instances(es):
    object_bx_correlations = set()
    def create_key(a, b):
        return a.get('type'), a.get('bx_offset'), b.get('type'), b.get('bx_offset')
    for c in es.get('conditions'):
        objects = sorted_objects(c.get('objects'))
        if len(objects) == 2:
            a, b = objects
            key = create_key(a, b)
            object_bx_correlations.add(key)
        elif len(objects) == 3:
            a, b, c = objects
            key = create_key(a, b)
            object_bx_correlations.add(key)
            key = create_key(a, c)
            object_bx_correlations.add(key)
            key = create_key(b, c)
            object_bx_correlations.add(key)
    return object_bx_correlations


if __name__ == '__main__':
    main()
