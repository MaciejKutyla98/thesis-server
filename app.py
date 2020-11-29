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
 
 
@app.route("/list_all_eestecers")
def list_all_eestecers():
    data = {"eestecers": []}
    for record in NEO4J.query("MATCH (p:Person) RETURN p limit 3"):
        data['eestecers'].append({
            "name": record[0]['name'],
            "born": record[0]['born'],
        })
    return data
 
 
if __name__ == '__main__':
    app.run()