
"""
Helper function
"""
def helpfunction(shell, *args):
    # generate a string seperated by new lines.
    output = "Commands\n"
    for k in shell.builtins.keys():
        output += f"{k}\n"
    return output

"""
"""
def greet(shell, *args):
    return "Hello world!"


"""
"""
def goodbye(shell, *args):
    exit(0)