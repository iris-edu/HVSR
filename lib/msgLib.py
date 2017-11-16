#
# DESCRIPTION
#   a collection of functions to print messages
#
# HISTORY
#   2015-05-19 IRIS DMC Product Team (Manoch): created (R.2015139)
#
# NOTES
# 
#

#
# run message
#
def message(thisMessage):
   bar = "**********************"
   prin ("%s %s %s"%(bar,thisMessage,bar))

#
# error
#
def error(message,code):
   print("\n[ERROR] %s\n"%(message))
   return(code)

#
# warning
#
def warning(sender,message):
   print("[WARNING from %s] %s"%(sender,message))

#
# info
#
def info(message):
   print("[INFO] %s"%(message))
   return


#
# get a variable from the parameter file by name
#
def param(params,var):
  if var in dir(params):
    return params
  code = error("variable '"+var+"' not in the parameter file",code=2)
  import sys
  sys.exit(code)
