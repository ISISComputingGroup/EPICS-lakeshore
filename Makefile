TOP = ../../extensions
include $(TOP)/configure/CONFIG

ACTIONS += uninstall kit zip

DIRS = lakeshore336

DIRS := $(wildcard $(DIRS))

include $(TOP)/configure/RULES_DIRS
