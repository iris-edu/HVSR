#
# DESCRIPTION
#   a collection of functions to print messages
#
# HISTORY
#   2020-06-03 IRIS DMC Product Team (Manoch): style update V.2020.155
#   2018-07-10 IRIS DMC Product Team (Manoch): pre-release V.2018.191
#   2015-05-19 IRIS DMC Product Team (Manoch): created (V.2015.139)
#
# NOTES
# 
#


def message(post_message):
    """print a run message"""
    bar = "*" * 12
    print("%s %s %s" % (bar, post_message, bar))


def error(err_message, code):
    """print an error message"""
    print("\n[ERR] %s\n" % err_message, flush=True)
    return code


def warning(sender, warn_message):
    """print a warning message"""
    print("[WARN] from %s: %s" % (sender, warn_message), flush=True)


def info(info_message):
    """print an informative message"""
    print("[INFO] %s" % info_message, flush=True)
    return


def param(params, var):
    """get a variable from the parameter file by name"""
    if var in dir(params):
        return params
    code = error("'".join(["variable ", var, " not in the parameter file"]), code=2)
    import sys
    sys.exit(code)
