import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter(
    "Pythia8GeneratorFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(7.010e-01),
    crossSection = cms.untracked.double(540000000.),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            #user_decay_file = cms.vstring('GeneratorInterface/EvtGenInterface/data/Bs_JpsiKK_mumuKK.dec'),
            list_forced_decays = cms.vstring('MyB_s0', 'Myanti-B_s0'),
            operates_on_particles = cms.vint32(531),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded = cms.vstring(
"""
#
# This is the decay file for the decay BS0 -> PSI(-> MU+ MU-) K+ K-
#
# Descriptor: [B_s0 -> (J/psi(1S) -> mu+ mu-) ( K+ K-)]
#
# NickName: Bs_Jpsi2K
#
# Physics: Currently using phase space for Bs decays
#
# Tested:
# By: Niladribihari Sahoo
# Date: 24 Dec 2018
#
Alias      MyB_s0   B_s0
Alias      Myanti-B_s0   anti-B_s0
ChargeConj Myanti-B_s0   MyB_s0
Alias      MyPsi  psi(2S)
ChargeConj MyPsi  MyPsi
#
Decay MyB_s0
  1.000         MyPsi     K+  K-      PHSP;
Enddecay
#
CDecay Myanti-B_s0
#
Decay MyPsi
  1.000         mu+         mu-           PHOTOS VLL;
Enddecay
#
End
"""
            ),
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            "SoftQCD:nonDiffractive = on",
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 1.0'),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)

bfilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(531)
)

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(3),
    ParticleID      = cms.untracked.int32(531),
    DaughterIDs     = cms.untracked.vint32(-321, 321, 100443),  ## K-, K+, PSI(2S)
    MinPt           = cms.untracked.vdouble(0.4, 0.4, 6.0),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5, -9999.),
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5,  9999.)
    )

psi2sfilter = cms.EDFilter(
    "PythiaDauVFilter",
    MotherID = cms.untracked.int32(531),
    ParticleID = cms.untracked.int32(100443),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(13, -13),
    MinPt = cms.untracked.vdouble(3.5, 3.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    verbose = cms.untracked.int32(1)
)


ProductionFilterSequence = cms.Sequence(generator*bfilter*decayfilter*psi2sfilter)
