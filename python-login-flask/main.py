# This file is run when building the website
# When __init__ is put inside a folder, the folder becomes a package when imported

from website import create_app  

app = create_app()

# Only if this main file is run directly does this function run (not import)
if __name__ == '__main__':
    app.run(debug=True) # Debug = True: every time we change code it reloads the website