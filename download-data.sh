#!/bin/bash

mkdir data
pushd data
wget "https://adsdb.mikel.xyz/Population-EstimatesData.csv"
wget "https://adsdb.mikel.xyz/Population-EstimatesData-1.csv"
wget "https://adsdb.mikel.xyz/Population-EstimatesData-2.csv"
wget "https://adsdb.mikel.xyz/Population-EstimatesData-3.csv"
popd
