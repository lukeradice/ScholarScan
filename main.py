from website import create_app

app = create_app()

#this condition is met if we run this file
if __name__ == "__main__":
    #runs flask application, stratup a web server 
    app.run(debug=True)


    