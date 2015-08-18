TOP = ../../../extensions/master
include $(TOP)/configure/CONFIG

DIRS = lakeshore336

DIRS := $(wildcard $(DIRS))

include $(TOP)/configure/RULES_DIRS_INT
