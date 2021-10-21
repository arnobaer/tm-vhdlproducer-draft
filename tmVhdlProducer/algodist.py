class ModuleCollection:

    def __init__(self, size: int):
        self.modules: list = [Module(i) for i in range(size)]


class Module:

    def __init__(self, id: int) -> None:
        self.id: int = id
        self.algorithms: set = set()
        self.conditions: set = set()
        self.object_bxs: set = set()
        self.object_bx_correlations: set = set()

    def add_algorithm(self, algorithm):
        self.algorithms.add(algorithm)
        self.conditions.update(algorithm.conditions)
        self.object_bxs.update(algorithm.object_bxs)
        self.object_bx_correlations.update(algorithm.object_bx_correlations)


class Algorithm:

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.conditions: set = set()
        self.object_bxs: set = set()
        self.object_bx_correlations: set = set()


def find_best_match(module_collection, algorithm) -> Module:
    return sorted(module_collection.modules, key=lambda module: len(module.algorithms))[0]


def distribute(es) -> ModuleCollection:
    module_collection = ModuleCollection(6)
    for algorithm in es.get('algorithms'):
        module = find_best_match(module_collection, algorithm)
        module.add_algorithm(Algorithm(algorithm.get('name')))
    return module_collection
