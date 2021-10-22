import argparse
import os

import yaml

from .eventsetup import load, sorted_objects
from .algodist import distribute, Payload, ResourceConfig


class AlgorithmInstance:

    def __init__(self, name: str, index: int):
        self.name: str = name
        self.index: int = index
        self.condition_instances = set()

    def add_condition_instance(self, instance):
        self.condition_instances.add(instance)


class ConditionInstance:

    def __init__(self, name, condition_type, objects, cuts):
        self.name = name
        self.condition_type = condition_type
        self.objects = objects
        self.cuts = cuts
        self.object_bx_instances = set()
        self.correlation_bx_instances = set()

    def add_object_bx_instance(self, instance):
        self.object_bx_instances.add(instance)

    def add_correlation_bx_instance(self, instance):
        self.correlation_bx_instances.add(instance)


class ObjectBxInstance:

    def __init__(self, object_bx):
        self.object_bx = object_bx


class CorrelationBxInstance:

    def __init__(self, correlation_bx):
        super().__init__()
        self.correlation_bx = correlation_bx


def calc_object_bx(condition):
    object_bx = set()
    name = condition.get('name')
    for object_ in condition.get('objects'):
        key = object_.get('type'), object_.get('bx_offset')
        object_bx.add(key)
    return object_bx


def calc_correlation_bx(condition):
    object_bx_correlations = set()
    def create_key(a, b):
        return a.get('type'), a.get('bx_offset'), b.get('type'), b.get('bx_offset')
    objects = sorted_objects(condition.get('objects'))
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

    ####

    condition_cache = {}

    for condition in es.get('conditions'):
        condition_cache.setdefault(condition.get('name'), condition)

    algorithm_instances = {}
    condition_instances = {}
    object_bx_instances = {}
    correlation_bx_instances = {}

    for condition_key, condition in condition_cache.items():
        if condition_key not in condition_instances:
            condition_instance = ConditionInstance(
                condition['name'],
                condition['type'],
                condition['objects'],
                condition['cuts'],
            )

            for object_bx in calc_object_bx(condition):
                if object_bx not in object_bx_instances:
                    object_bx_instance = ObjectBxInstance(object_bx)
                    object_bx_instances[object_bx] = object_bx_instance
                object_bx_instance = object_bx_instances[object_bx]
                condition_instance.add_object_bx_instance(object_bx_instance)

            for correlation_bx in calc_correlation_bx(condition):
                if correlation_bx not in correlation_bx_instances:
                    correlation_bx_instance = CorrelationBxInstance(correlation_bx)
                    correlation_bx_instances[correlation_bx] = correlation_bx_instance
                correlation_bx_instance = correlation_bx_instances[correlation_bx]
                condition_instance.add_correlation_bx_instance(correlation_bx_instance)

            condition_instances[condition_instance.name] = condition_instance

    for algorithm in es['algorithms']:
        algorithm_instance = AlgorithmInstance(algorithm['name'], algorithm['index'])
        for condition_name in algorithm['conditions']:
            condition_instance = condition_instances[condition_name]
            algorithm_instance.add_condition_instance(condition_instance)
        algorithm_instances[algorithm_instance.name] = algorithm_instance

    ###

    filename = os.path.join(os.path.dirname(__file__), 'config', 'default.yaml')
    with open(filename) as fp:
        config = ResourceConfig(yaml.safe_load(fp))

    for algorithm_instance in algorithm_instances.values():
        algorithm_instance.payload = config.get_algorithm_payload()

    for condition_instance in condition_instances.values():
        object_type = [obj.get('type') for obj in condition_instance.objects]
        cut_type = [cut['cut_type'] for cut in condition_instance.cuts]
        condition_instance.payload = config.get_condition_payload(
            condition_instance.condition_type,
            object_type,
            cut_type
        )

    for object_bx_instance in object_bx_instances.values():
        object_bx_instance.payload = config.get_object_bx_payload(object_bx_instance.object_bx[0])

    for correlation_bx_instance in correlation_bx_instances.values():
        correlation_bx_instance.payload = config.get_correlation_bx_payload([
            correlation_bx_instance.correlation_bx[0],
            correlation_bx_instance.correlation_bx[2]
        ])

    ###

    for a in algorithm_instances.values():
        print(a.name)
        for c in a.condition_instances:
            print('-', c.name)
            for o in c.object_bx_instances:
                print('--', o.object_bx)
            for x in c.correlation_bx_instances:
                print('--', x.correlation_bx)

    ###

    for module in distribute(list(algorithm_instances.values()), 6, floor=config.get_floor_payload(), ceiling=config.get_ceiling_payload()).modules:
        print(
            module.id,
            len(module.algorithm_instances),
            len(module.condition_instances),
            len(module.object_bx_instances),
            len(module.correlation_bx_instances),
            module.calculate_payload()
        )


if __name__ == '__main__':
    main()
