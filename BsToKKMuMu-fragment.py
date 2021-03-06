import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
                         EvtGen130 = cms.untracked.PSet(
                           decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                           particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
                           user_decay_embedded= cms.vstring('#',
'# This is the decay file for the decay BS0 -> MU+ MU- -> K+ K-',
'#',
'Alias      MyB_s0   B_s0',
'Alias      Myanti-B_s0   anti-B_s0',
'ChargeConj Myanti-B_s0   MyB_s0 ',
'#',
'Decay MyB_s0',
'1.000 K+  K-  mu+  mu-                        PHSP;',
'Enddecay',
'CDecay Myanti-B_s0',
'#',
'End'),
                           list_forced_decays = cms.vstring('MyB_s0','Myanti-B_s0'),
                           operates_on_particles = cms.vint32(),
                           convertPythiaCodes = cms.untracked.bool(False)
                           ),
                         parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CP5SettingsBlock,
                                                     processParameters = cms.vstring('SoftQCD:nonDiffractive = on',
                                                                                     'PTFilter:filter = on',
                                                                                     'PTFilter:quarkToFilter = 5',
                                                                                     'PTFilter:scaleToFilter = 1.0',
                                                                                     ),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CP5Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

###########
# Filters #
###########

bfilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(531)  ## Bs
    )

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(4),
    ParticleID      = cms.untracked.int32(531),
    DaughterIDs     = cms.untracked.vint32(-13, 13, -321, 321),  ## mu+, mu-, K+, K-
    MinPt           = cms.untracked.vdouble(3.5, 3.5, 0.4, 0.4),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5, -2.5, -2.5),
    MaxEta          = cms.untracked.vdouble(2.5, 2.5, 2.5, 2.5)
    )



ProductionFilterSequence = cms.Sequence(generator*bfilter*decayfilter)
