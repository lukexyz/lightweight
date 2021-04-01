from fastcore.script import *

@call_parse
def main(msg:Param("The message", str),
         upper:Param("Convert to uppercase?", store_true)):
    "Print `msg`, optionally converting to uppercase"
    print(msg.upper() if upper else msg)


