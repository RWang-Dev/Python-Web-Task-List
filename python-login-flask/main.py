# When __init__ is put inside a folder, the folder becomes a package
from website import create_app

app = create_app()



# Only if this main file is run does this function run
if __name__ == '__main__':
    app.run(debug=True)