#!/bin/bash

nowPath=$(pwd)

cd /tmp

randDirName=$(head -c 64 /dev/urandom | tr -dc A-Za-z0-9)

git clone https://github.com/stsaria/P4PSignaling.git $randDirName
cd $randDirName

pip install P4PCore@git+https://github.com/stsaria/P4PCore.git@main
pip install P4PNodeGossiper@git+https://github.com/stsaria/P4PNodeGossiper.git@main

pip install .

cd $nowPath
