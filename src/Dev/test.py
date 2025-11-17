debug = True

for i in range(5):
    debug = not debug
    print(f"Debug mode is {'on' if debug else 'off'}")