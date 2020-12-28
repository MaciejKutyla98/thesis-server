import os
 
from flask import Flask, request
from neo4j import GraphDatabase
 
app = Flask(__name__)
 
 
class Neo4jConnection:
 
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(
                self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
 
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
 
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(
                database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
 
 
NEO4J = Neo4jConnection(os.environ.get('NEO4J_BOLT_URL'),
                        os.environ.get('NEO4J_USER'),
                        os.environ.get('NEO4J_PASSWORD'))
 
 
@app.route("/information_about_organization")
def information_about_organization():
    data = {"organization": []}
    for record in NEO4J.query("MATCH (o:Organization) RETURN o limit 1"):
        data['organization'].append({
            "organization_name": record[0]['organization_name'],
            "organization_description": record[0]['organization_description'],
            "supervisor_room": record[0]['supervisor_room'],
            "creation_date": record[0]['creation_date'],
            "number_of_members": record[0]['number_of_members'],
            "organization_supervasior": record[0]['organization_supervasior'],
            "number_of_active_projects": record[0]['number_of_active_projects'],
        })
    return data

@app.route("/news")
def news():
    data = {"news": []}
    for record in NEO4J.query("MATCH (d:News) RETURN d"):
        data['news'].append({
            "date": record[0]['date'],
            "descriptionOfNews": record[0]['descriptionOfNews'],
            "tittleOfNews": record[0]['tittleOfNews'],
        })
    return data

@app.route("/projects")
def projects():
    data = {"projects": []}
    for record in NEO4J.query("MATCH (n:Project) RETURN n"):
        data['projects'].append({
            "date": record[0]['date'],
            "description": record[0]['description'],
            "projectName": record[0]['projectName'],
            "coordinators": record[0]['coordinators'],
        })
    return data

@app.route("/activitySheet")
def activitySheet():
    data = {"activitySheet": []}
    for record in NEO4J.query("MATCH (n:Person) RETURN n"):
        data['activitySheet'].append({
            "name": record[0]['name'],
            "fieldOfStudy": record[0]['fieldOfStudy'],
            "faculty": record[0]['faculty'],
            "yearOfStudy": record[0]['yearOfStudy'],
            "position": record[0]['position'],
            "internationalActivity": record[0]['internationalActivity'],
            "currentStatus": record[0]['currentStatus'],
        })
    return data

@app.route("/login")
def login():
    data = {"login": []}
    for record in NEO4J.query("MATCH (n:Person) RETURN n"):
        data['login'].append({
            "name": record[0]['name'],
            "login": record[0]['login'],
            "pass": record[0]['pass'],
        })
    return data

@app.route("/contacts")
def contacts():
    data = {"contacts": []}
    for record in NEO4J.query("MATCH (n:Person) RETURN n"):
        data['contacts'].append({
            "name": record[0]['name'],
            "telephoneNumber": record[0]['telephoneNumber'],
            "mail": record[0]['mail'],
        })
    return data

@app.route("/teams")
def teams():
    data = {"teams": []}
    for record in NEO4J.query("MATCH (n:Team) RETURN n"):
        data['teams'].append({
            "teamName": record[0]['teamName'],
            "teamDescription": record[0]['teamDescription'],
            "teamCoordinators": record[0]['teamCoordinators'],
            "numberOfMembers": record[0]['numberOfMembers'],
        })
    return data

@app.route("/createNewUser", methods=['GET', 'POST'])
def createNewUser():
    request.method == 'POST'
    login = request.args.get('login')
    password = request.args.get('pass')
    name = request.args.get('name')
    my_query = "CREATE(p:Person {login:'"+ str(login) + "', pass:'"+ str(password) + "', name:'"+ str(name) + "'}) Return p"
    NEO4J.query(my_query)
    return request.args



if __name__ == '__main__':
    app.run()