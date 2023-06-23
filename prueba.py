try:
    if '1' != 1:
        raise "algun error"
    else:
        print("no se producido error")
except "algun errro":
    print("se ha producido algun error")