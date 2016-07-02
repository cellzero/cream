@echo off
set OLD_PATH=%PATH%
set PATH=lib;%PATH%

%1

set PATH=%OLD_PATH%
set OLD_PATH=