def calc_maximum_payload(algorithm_instance):
    payload = Payload()
    payload += algorithm_instance.payload
    for condition_instance in algorithm_instance.condition_instances:
        payload += condition_instance.payload
        for object_bx_instance in condition_instance.object_bx_instances:
            payload += object_bx_instance.payload
        for correlation_bx_instance in condition_instance.correlation_bx_instances:
            payload += correlation_bx_instance.payload
    return payload


def distribute(algorithms: list, modules: int, floor, ceiling) -> 'ModuleCollection':
    module_collection = ModuleCollection(modules, floor, ceiling)
    algorithms.sort(key=lambda algorithm: calc_maximum_payload(algorithm), reverse=True)
    for algorithm in algorithms:
        module = module_collection.find_best_match(algorithm)
        module.add_algorithm(algorithm)
    return module_collection


def make_payload(node):
    return Payload(
        slice_luts=node.get('slice_luts', 0),
        processors=node.get('processors', 0),
        brams=node.get('brams', 0),
    )


class ResourceConfig:

    def __init__(self, config: dict) -> None:
        self.config = config
        self.config_resources = self.config.get('resources')
        self.config_mapping = self.config_resources.get('mapping')

    def map_cut(self, key):
        return self.config_mapping.get('cuts')[key]

    def map_object(self, key):
        return self.config_mapping.get('objects')[key]

    def map_condition(self, key):
        return self.config_mapping.get('conditions')[key]

    def get_floor_payload(self):
        return make_payload(self.config_resources.get('floor'))

    def get_ceiling_payload(self):
        return make_payload(self.config_resources.get('ceiling'))

    def get_algorithm_payload(self):
        return make_payload(self.config_resources.get('algorithm'))

    def get_condition_payload(self, condition_type, object_type, cut_type):
        mapped_condition_type = self.map_condition(condition_type)
        if not mapped_condition_type:
            return Payload()
        mapped_object_type = [self.map_object(t) for t in object_type]
        mapped_object_type.sort()
        mapped_cut_type = [self.map_cut(t) for t in cut_type]
        payload = Payload()
        for condition in self.config_resources.get('condition'):
            if condition.get('type') == mapped_condition_type:
                payload += make_payload(condition)
                for object in condition.get('objects', []):
                    if sorted(object.get('type')) == mapped_object_type:
                        payload += make_payload(object)
                        for cut in object.get('cuts', []):
                            if cut.get('type') in mapped_cut_type:
                                payload += make_payload(cut)
        return payload
        #raise KeyError((condition_type, object_type, cut_type))

    def get_object_bx_payload(self, object_type):
        mapped_type = self.map_object(object_type)
        for object_bx in self.config_resources.get('object_bx'):
            if object_bx.get('type') == mapped_type:
                return make_payload(object_bx)
        raise KeyError(object_type)

    def get_correlation_bx_payload(self, object_types):
        mapped_type = [self.map_object(object_type) for object_type in object_types]
        mapped_type.sort()
        for correlation_bx in self.config_resources.get('correlation_bx'):
            if sorted(correlation_bx.get('type')) == mapped_type:
                return make_payload(correlation_bx)
        raise KeyError(object_types)


class Payload:

    def __init__(self, *, slice_luts: int = 0, processors: int = 0, brams: int = 0) -> None:
        self.slice_luts: int = slice_luts
        self.processors: int = processors
        self.brams: int = brams

    def _astuple(self) -> tuple:
        return self.slice_luts, self.processors, self.brams

    def __add__(self, rhs: 'Payload') -> 'Payload':
        slice_luts = self.slice_luts + rhs.slice_luts
        processors = self.processors + rhs.processors
        brams = self.brams + rhs.brams
        return type(self)(slice_luts=slice_luts, processors=processors, brams=brams)

    def __eq__(self, rhs: object) -> bool:
        if isinstance(rhs, type(self)):
            return self._astuple() == rhs._astuple()
        return super().__eq__(rhs)

    def __lt__(self, rhs: object) -> bool:
        if isinstance(rhs, type(self)):
            return self._astuple() < rhs._astuple()
        return super().__eq__(rhs)

    def __str__(self) -> str:
        name = type(self).__name__
        slice_luts = self.slice_luts
        processors = self.processors
        brams = self.brams
        return f"{name}(slice_luts={slice_luts}, processors={processors}, brams={brams})"


class Module:

    def __init__(self, id: int, floor, ceiling) -> None:
        self.id: int = id
        self.floor_payload = floor
        self.ceiling_payload = ceiling
        self.algorithm_instances: set = set()
        self.condition_instances: set = set()
        self.object_bx_instances: set = set()
        self.correlation_bx_instances: set = set()

    def add_algorithm(self, algorithm) -> None:
        self.algorithm_instances.add(algorithm)
        self.condition_instances.update(algorithm.condition_instances)
        for condition in algorithm.condition_instances:
            self.object_bx_instances.update(condition.object_bx_instances)
            self.correlation_bx_instances.update(condition.correlation_bx_instances)

    def calculate_payload(self):
        payload = Payload()
        payload += self.floor_payload
        for algorithm_instance in self.algorithm_instances:
            payload += algorithm_instance.payload
        for condition_instance in self.condition_instances:
            payload += condition_instance.payload
        for object_bx_instance in self.object_bx_instances:
            payload += object_bx_instance.payload
        for correlation_bx_instance in self.correlation_bx_instances:
            payload += correlation_bx_instance.payload
        if payload > self.ceiling_payload:
            raise RuntimeError("resource overflow")
        return payload


class ModuleCollection:

    def __init__(self, size: int, floor, ceiling) -> None:
        self.modules: list = [Module(i, floor, ceiling) for i in range(size)]

    def find_best_match(self, algorithm) -> Module:

        def calc_score(module, algorithm):
            score = 0
            for condition_instance in algorithm.condition_instances:
                if condition_instance in module.condition_instances:
                    score += 10
                for object_bx_instance in condition_instance.object_bx_instances:
                    if object_bx_instance in module.object_bx_instances:
                        score += 10
                for correlation_bx_instance in condition_instance.correlation_bx_instances:
                    if correlation_bx_instance in module.correlation_bx_instances:
                        score += 10
            return score

        def key(module):
            payload = module.calculate_payload()
            score = calc_score(module, algorithm)
            return score, payload

        return sorted(self.modules, key=key)[0]
