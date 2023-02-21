from website import create_app

app = create_app()

#this condition is met if we run this file
if __name__ == "__main__":
    #runs flask application, stratup a web server 
    app.run(debug=True)


#C:\Users\luker\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages\flask_sqlalchemy\__init__.py:872: 
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.