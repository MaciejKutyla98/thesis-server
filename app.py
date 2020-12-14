import os
 
from flask import Flask
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
def information_about_organization():
    data = {"news": []}
    for record in NEO4J.query("MATCH (d:News) RETURN d"):
        data['news'].append({
            "date": record[0]['date'],
            "descriptionOfNews": record[0]['descriptionOfNews'],
        })
    return data
 
if __name__ == '__main__':
    app.run()