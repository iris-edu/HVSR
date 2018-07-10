#
# DESCRIPTION
#   a collection of functions to print messages
#
# HISTORY
#   2018-07-10 IRIS DMC Product Team (Manoch): prerelease R.2018191
#   2015-05-19 IRIS DMC Product Team (Manoch): created (R.2015139)
#
# NOTES
# 
#


def message(thisMessage):
    """print a run message"""
    bar = "*" * 12
    prin ("%s %s %s"%(bar,thisMessage,bar))


def error(message,code):
    """print an error message"""
    print("\n[ERROR] %s\n"%(message))
    return(code)


def warning(sender,message):
    """print a warning message"""
    print("[WARNING from %s] %s"%(sender,message))


def info(message):
    """print an informative message"""
    print("[INFO] %s"%(message))
    return


def param(params,var):
    """get a variable from the parameter file by name"""
    if var in dir(params):
      return params
    code = error("'".join(["variable ",var," not in the parameter file"]),code=2)
    import sys
    sys.exit(code)
