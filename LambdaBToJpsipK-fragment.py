import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        maxEventsToPrint = cms.untracked.int32(0),
        pythiaPylistVerbosity = cms.untracked.int32(0),
        comEnergy = cms.double(13000.0),

        ExternalDecays = cms.PSet(
            EvtGen130 = cms.untracked.PSet(
                operates_on_particles = cms.vint32(), # 0 (zero) means default list (hardcoded)
                decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evtLbJpsipK_2014.pdl'),
                #user_decay_file =  cms.vstring('GeneratorInterface/EvtGenInterface/data/LambdaB_JPsipK.dec'),
		user_decay_embedded = cms.vstring('#',
'# This is the decay file for LambdaB to Jpsi pK',
'#',
'#',
'Alias    MyLambda_b0    Lambda_b0',
'Alias    Myanti-Lambda_b0    anti-Lambda_b0',
'ChargeConj    MyLambda_b0    Myanti-Lambda_b0',
'Alias    MyJpsi    J/psi',
'ChargeConj    MyJpsi    MyJpsi',
'#',
'Decay MyLambda_b0',
'1.000    p+    K-    MyJpsi    PHSP;',
'Enddecay',
'CDecay Myanti-Lambda_b0',
'#',
'Decay MyJpsi',
'1.000    mu+    mu-    PHOTOS VLL;',
'Enddecay',
'#',
'End'),
                convertPythiaCodes = cms.untracked.bool(False),
                list_forced_decays = cms.vstring('MyLambda_b0',
                    'Myanti-Lambda_b0'),
                ),
            parameterSets = cms.vstring('EvtGen130')
            ),

        PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
            pythia8CP5SettingsBlock,
            processParameters = cms.vstring(
                                            '443:onMode = off',
                                            '443:onIfAny = -13 13',
                                            'SoftQCD:nonDiffractive = on',
                                            'PTFilter:filter = on', # this turn on the filter
                                            'PTFilter:quarkToFilter = 5', # PDG id of q quark (can be any other)
                                            'PTFilter:scaleToFilter = 1.0'),
            parameterSets = cms.vstring('pythia8CommonSettings',
                'pythia8CP5Settings',
                'processParameters',
                )

            )
         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

configurationMetadata = cms.untracked.PSet(
        version = cms.untracked.string('$Revision: 1.1 $'),
        name = cms.untracked.string('$Source: Configuration/Generator/python/PYTHIA8_LambdaB2PK_EtaPtFilter_CUEP8M1_13TeV_cff.py $'),
        annotation = cms.untracked.string('Spring 2016: Pythia8+EvtGen130 generation of Lb --> JPsi P K-, 13TeV, Tune CUETP8M1')
        )

# Filters

bfilter = cms.EDFilter(
        "PythiaFilter",
        MaxEta = cms.untracked.double(9999.),
        MinEta = cms.untracked.double(-9999.),
        ParticleID = cms.untracked.int32(5122)
        )

lbfilter = cms.EDFilter(
        "PythiaDauVFilter",
        verbose         = cms.untracked.int32(1),
        NumberDaughters = cms.untracked.int32(3),
        DaughterIDs = cms.untracked.vint32(443,2212,-321),
        ParticleID      = cms.untracked.int32(5122),
        MinPt           = cms.untracked.vdouble(3.,-1.,-1.),
        MaxEta          = cms.untracked.vdouble(2.5, 2.5, 2.5),
        MinEta          = cms.untracked.vdouble(-2.5, -2.5, -2.5)
        )

Mufilter = cms.EDFilter(
        "PythiaDauVFilter",
        NumberDaughters = cms.untracked.int32(2),
        DaughterIDs = cms.untracked.vint32(13,-13),
        ParticleID      = cms.untracked.int32(443),
        MinPt           = cms.untracked.vdouble(3.,3.),
        MaxEta          = cms.untracked.vdouble(2.5, 2.5, 2.5),
        MinEta          = cms.untracked.vdouble(-2.5, -2.5, -2.5)
        )

ProductionFilterSequence = cms.Sequence(generator*bfilter*lbfilter*Mufilter)
