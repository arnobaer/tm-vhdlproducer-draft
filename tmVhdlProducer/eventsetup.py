"""Module to convert vent setup to dictionary."""

import tmEventSetup
import tmGrammar

__all__ = ['load', 'sorted_objects']

CutTypes = {
    tmEventSetup.Threshold: 'Threshold',
    tmEventSetup.Eta: 'Eta',
    tmEventSetup.Phi: 'Phi',
    tmEventSetup.Charge: 'Charge',
    tmEventSetup.Quality: 'Quality',
    tmEventSetup.Isolation: 'Isolation',
    tmEventSetup.DeltaEta: 'DeltaEta',
    tmEventSetup.DeltaPhi: 'DeltaPhi',
    tmEventSetup.DeltaR: 'DeltaR',
    tmEventSetup.Mass: 'Mass',
    tmEventSetup.ChargeCorrelation: 'ChargeCorrelation',
    tmEventSetup.Count: 'Count',
    tmEventSetup.Slice: 'Slice',
    tmEventSetup.TwoBodyPt: 'TwoBodyPt',
    tmEventSetup.OvRmDeltaEta: 'OvRmDeltaEta',
    tmEventSetup.OvRmDeltaPhi: 'OvRmDeltaPhi',
    tmEventSetup.OvRmDeltaR: 'OvRmDeltaR',
    tmEventSetup.ImpactParameter: 'ImpactParameter',
    tmEventSetup.UnconstrainedPt: 'UnconstrainedPt',
    tmEventSetup.MassDeltaR: 'MassDeltaR',
    tmEventSetup.MassUpt: 'MassUpt'
}

ObjectTypes = {
    tmEventSetup.Muon: 'Muon',
    tmEventSetup.Egamma: 'Egamma',
    tmEventSetup.Tau: 'Tau',
    tmEventSetup.Jet: 'Jet',
    tmEventSetup.ETT: 'ETT',
    tmEventSetup.HTT: 'HTT',
    tmEventSetup.ETM: 'ETM',
    tmEventSetup.HTM: 'HTM',
    tmEventSetup.EXT: 'EXT',
    tmEventSetup.Precision: 'Precision',
    tmEventSetup.MBT0HFP: 'MBT0HFP',
    tmEventSetup.MBT1HFP: 'MBT1HFP',
    tmEventSetup.MBT0HFM: 'MBT0HFM',
    tmEventSetup.MBT1HFM: 'MBT1HFM',
    tmEventSetup.ETTEM: 'ETTEM',
    tmEventSetup.ETMHF: 'ETMHF',
    tmEventSetup.TOWERCOUNT: 'TOWERCOUNT',
    tmEventSetup.ASYMET: 'ASYMET',
    tmEventSetup.ASYMHT: 'ASYMHT',
    tmEventSetup.ASYMETHF: 'ASYMETHF',
    tmEventSetup.ASYMHTHF: 'ASYMHTHF',
    tmEventSetup.CENT0: 'CENT0',
    tmEventSetup.CENT1: 'CENT1',
    tmEventSetup.CENT2: 'CENT2',
    tmEventSetup.CENT3: 'CENT3',
    tmEventSetup.CENT4: 'CENT4',
    tmEventSetup.CENT5: 'CENT5',
    tmEventSetup.CENT6: 'CENT6',
    tmEventSetup.CENT7: 'CENT7',
    tmEventSetup.MUS0: 'MUS0',
    tmEventSetup.MUS1: 'MUS1',
    tmEventSetup.MUSOOT0: 'MUSOOT0',
    tmEventSetup.MUSOOT1: 'MUSOOT1'
}

FunctionTypes = {
    tmEventSetup.CombFunction: 'CombFunction',
    tmEventSetup.DistFunction: 'DistFunction',
    tmEventSetup.MassFunction: 'MassFunction',
    tmEventSetup.InvariantMassFunction: 'InvariantMassFunction',
    tmEventSetup.TransverseMassFunction: 'TransverseMassFunction',
    tmEventSetup.CombOvRmFunction: 'CombOvRmFunction',
    tmEventSetup.DistOvRmFunction: 'DistOvRmFunction',
    tmEventSetup.InvariantMassOvRmFunction: 'InvariantMassOvRmFunction',
    tmEventSetup.TransverseMassOvRmFunction: 'TransverseMassOvRmFunction',
    tmEventSetup.InvariantMassDeltaRFunction: 'InvariantMassDeltaRFunction',
    tmEventSetup.InvariantMassUptFunction: 'InvariantMassUptFunction'
}

ComparisonOperators = {
    tmEventSetup.GE: 'GE',
    tmEventSetup.NE: 'NE',
    tmEventSetup.EQ: 'EQ'
}

CombinationTypes = {
    tmEventSetup.MuonMuonCombination: 'MuonMuonCombination,',
    tmEventSetup.MuonEsumCombination: 'MuonEsumCombination,',
    tmEventSetup.CaloMuonCombination: 'CaloMuonCombination,',
    tmEventSetup.CaloCaloCombination: 'CaloCaloCombination,',
    tmEventSetup.CaloEsumCombination: 'CaloEsumCombination,'
}

ConditionTypes = {
    tmEventSetup.SingleMuon: 'SingleMuon',
    tmEventSetup.DoubleMuon: 'DoubleMuon',
    tmEventSetup.TripleMuon: 'TripleMuon',
    tmEventSetup.QuadMuon: 'QuadMuon',
    tmEventSetup.SingleEgamma: 'SingleEgamma',
    tmEventSetup.DoubleEgamma: 'DoubleEgamma',
    tmEventSetup.TripleEgamma: 'TripleEgamma',
    tmEventSetup.QuadEgamma: 'QuadEgamma',
    tmEventSetup.SingleTau: 'SingleTau',
    tmEventSetup.DoubleTau: 'DoubleTau',
    tmEventSetup.TripleTau: 'TripleTau',
    tmEventSetup.QuadTau: 'QuadTau',
    tmEventSetup.SingleJet: 'SingleJet',
    tmEventSetup.DoubleJet: 'DoubleJet',
    tmEventSetup.TripleJet: 'TripleJet',
    tmEventSetup.QuadJet: 'QuadJet',
    tmEventSetup.TotalEt: 'TotalEt',
    tmEventSetup.TotalHt: 'TotalHt',
    tmEventSetup.MissingEt: 'MissingEt',
    tmEventSetup.MissingHt: 'MissingHt',
    tmEventSetup.Externals: 'Externals',
    tmEventSetup.MuonMuonCorrelation: 'MuonMuonCorrelation',
    tmEventSetup.MuonEsumCorrelation: 'MuonEsumCorrelation',
    tmEventSetup.CaloMuonCorrelation: 'CaloMuonCorrelation',
    tmEventSetup.CaloCaloCorrelation: 'CaloCaloCorrelation',
    tmEventSetup.CaloEsumCorrelation: 'CaloEsumCorrelation',
    tmEventSetup.InvariantMass: 'InvariantMass',
    tmEventSetup.MinBiasHFP0: 'MinBiasHFP0',
    tmEventSetup.MinBiasHFP1: 'MinBiasHFP1',
    tmEventSetup.MinBiasHFM0: 'MinBiasHFM0',
    tmEventSetup.MinBiasHFM1: 'MinBiasHFM1',
    tmEventSetup.TotalEtEM: 'TotalEtEM',
    tmEventSetup.MissingEtHF: 'MissingEtHF',
    tmEventSetup.TowerCount: 'TowerCount',
    tmEventSetup.TransverseMass: 'TransverseMass',
    tmEventSetup.SingleEgammaOvRm: 'SingleEgammaOvRm',
    tmEventSetup.DoubleEgammaOvRm: 'DoubleEgammaOvRm',
    tmEventSetup.TripleEgammaOvRm: 'TripleEgammaOvRm',
    tmEventSetup.QuadEgammaOvRm: 'QuadEgammaOvRm',
    tmEventSetup.SingleTauOvRm: 'SingleTauOvRm',
    tmEventSetup.DoubleTauOvRm: 'DoubleTauOvRm',
    tmEventSetup.TripleTauOvRm: 'TripleTauOvRm',
    tmEventSetup.QuadTauOvRm: 'QuadTauOvRm',
    tmEventSetup.SingleJetOvRm: 'SingleJetOvRm',
    tmEventSetup.DoubleJetOvRm: 'DoubleJetOvRm',
    tmEventSetup.TripleJetOvRm: 'TripleJetOvRm',
    tmEventSetup.QuadJetOvRm: 'QuadJetOvRm',
    tmEventSetup.CaloCaloCorrelationOvRm: 'CaloCaloCorrelationOvRm',
    tmEventSetup.InvariantMassOvRm: 'InvariantMassOvRm',
    tmEventSetup.TransverseMassOvRm: 'TransverseMassOvRm',
    tmEventSetup.AsymmetryEt: 'AsymmetryEt',
    tmEventSetup.AsymmetryHt: 'AsymmetryHt',
    tmEventSetup.AsymmetryEtHF: 'AsymmetryEtHF',
    tmEventSetup.AsymmetryHtHF: 'AsymmetryHtHF',
    tmEventSetup.Centrality0: 'Centrality0',
    tmEventSetup.Centrality1: 'Centrality1',
    tmEventSetup.Centrality2: 'Centrality2',
    tmEventSetup.Centrality3: 'Centrality3',
    tmEventSetup.Centrality4: 'Centrality4',
    tmEventSetup.Centrality5: 'Centrality5',
    tmEventSetup.Centrality6: 'Centrality6',
    tmEventSetup.Centrality7: 'Centrality7',
    tmEventSetup.InvariantMass3: 'InvariantMass3',
    tmEventSetup.InvariantMassDeltaR: 'InvariantMassDeltaR',
    tmEventSetup.InvariantMassUpt: 'InvariantMassUpt',
    tmEventSetup.MuonShower0: 'MuonShower0',
    tmEventSetup.MuonShower1: 'MuonShower1',
    tmEventSetup.MuonShowerOutOfTime0: 'MuonShowerOutOfTime0',
    tmEventSetup.MuonShowerOutOfTime1: 'MuonShowerOutOfTime1'
}

ScaleTypes = {
    tmEventSetup.EtScale: 'EtScale',
    tmEventSetup.EtaScale: 'EtaScale',
    tmEventSetup.PhiScale: 'PhiScale',
    tmEventSetup.DeltaPrecision: 'DeltaPrecision',
    tmEventSetup.MassPrecision: 'MassPrecision',
    tmEventSetup.MassPtPrecision: 'MassPtPrecision',
    tmEventSetup.MathPrecision: 'MathPrecision',
    tmEventSetup.CountScale: 'CountScale',
    tmEventSetup.TwoBodyPtPrecision: 'TwoBodyPtPrecision',
    tmEventSetup.TwoBodyPtMathPrecision: 'TwoBodyPtMathPrecision',
    tmEventSetup.OvRmDeltaPrecision: 'OvRmDeltaPrecision',
    tmEventSetup.UnconstrainedPtScale: 'UnconstrainedPtScale',
    tmEventSetup.InverseDeltaRPrecision: 'InverseDeltaRPrecision'
}


def load(fp) -> dict:
    context = tmEventSetup.getTriggerMenu(fp.name)
    return load_event_setup(context)


def load_event_setup(es):
    return {
        'name': es.getName(),
        'comment': es.getComment(),
        'conditions': load_conditions(es),
        'algorithms': load_algorithms(es),
        'uuid_firmware': es.getFirmwareUuid(),
        'uuid_menu': es.getMenuUuid(),
        'n_modules': es.getNmodules(),
        'scales': load_scales(es),
        'scale_set_name': es.getScaleSetName(),
        'version': es.getVersion()
    }


def load_object_cut(cut):
    return {
        'name': cut.getName(),
        'object_type': ObjectTypes[cut.getObjectType()],
        'cut_type': CutTypes[cut.getCutType()],
        'data': cut.getData(),
        'key': cut.getKey(),
        'minimum': {
            'value': cut.getMinimumValue(),
            'index': cut.getMinimumIndex()
        },
        'maximum': {
            'value': cut.getMaximumValue(),
            'index': cut.getMaximumIndex()
        },
        'precision': cut.getPrecision()
    }


def load_object_cuts(object_):
    return [load_object_cut(cut) for cut in object_.getCuts()]


def load_object(object_):
    return {
        'name': object_.getName(),
        'external_channel_id': object_.getExternalChannelId(),
        'external_signal_name': object_.getExternalSignalName(),
        'threshold': object_.getThreshold(),
        'type': ObjectTypes[object_.getType()],
        'comparison_operator': object_.getComparisonOperator(),
        'bx_offset': object_.getBxOffset(),
        'cuts': load_object_cuts(object_)
    }


def load_objects(condition: tmEventSetup.esCondition) -> list:
    return [load_object(object_) for object_ in condition.getObjects()]


def load_cut(cut):
    return {
        'name': cut.getName(),
        'object_type': FunctionTypes[cut.getObjectType()],
        'cut_type': CutTypes[cut.getCutType()],
        'data': cut.getData(),
        'key': cut.getKey(),
        'minimum': {
            'value': cut.getMinimumValue(),
            'index': cut.getMinimumIndex()
        },
        'maximum': {
            'value': cut.getMaximumValue(),
            'index': cut.getMaximumIndex()
        },
        'precision': cut.getPrecision()
    }


def load_cuts(context) -> list:
    return [load_cut(cut) for cut in context.getCuts()]


def load_conditions(context):
    conditions = []
    for key, value in context.getConditionMapPtr().items():
        conditions.append({
            'name': value.getName(),
            'type': ConditionTypes[value.getType()],
            'objects': load_objects(value),
            'cuts': load_cuts(value)
        })
    return conditions


def load_algorithms(context):
    algorithms = []
    for key, value in context.getAlgorithmMapPtr().items():
        rpn_vector = value.getRpnVector()
        algorithms.append({
            'name': value.getName(),
            'index': value.getIndex(),
            'module_id': value.getModuleId(),
            'module_index': value.getModuleIndex(),
            'expression': value.getExpression(),
            'expression_in_condition': value.getExpressionInCondition(),
            'rpn_vector': rpn_vector,
            'conditions': [token for token in rpn_vector if not tmGrammar.isGate(token)]
        })
    return algorithms


def load_bin(bin_):
    return {
        'hw_index': bin_.hw_index,
        'maximum': bin_.maximum,
        'minimum': bin_.minimum
    }


def load_bins(scale):
    return [load_bin(bin_) for bin_ in scale.getBins()]


def load_scale(scale):
    return {
        'name': scale.getName(),
        'scale_type': ScaleTypes[scale.getScaleType()],
        'object_type': ObjectTypes[scale.getObjectType()],
        'minimum': scale.getMinimum(),
        'maximum': scale.getMaximum(),
        'step': scale.getStep(),
        'n_bits': scale.getNbits(),
        'bins': load_bins(scale)
    }


def load_scales(es):
    return [load_scale(scale) for scale in es.getScaleMapPtr().values()]


def sorted_objects(objects):
    return sorted(objects, key=lambda object_: list(ObjectTypes.values()).index(object_.get('type')))
