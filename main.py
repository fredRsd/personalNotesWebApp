from website import makeApp #imports makeApp function from __init__.py (necessary) in website directory

app = makeApp() #assigns makeApp(), which runs a flask object to app

if __name__ == '__main__':  #if current module is run as main script(not imported)
    app.run(debug=True) #flask development server starts. debug mode is set true in developer mode

