import FWCore.ParameterSet.Config as cms
import pickle
with open('PSet.pkl', 'rb') as handle:
    process = pickle.load(handle)
