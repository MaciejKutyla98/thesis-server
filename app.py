import os

from flask import Flask
from neo4j import GraphDatabase

app = Flask(__name__)


class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def return_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(
                self._create_and_return_greeting, message)
            return greeting

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)",
                        message=message)
        return result.single()[0]


@app.route('/')
def hello_world():
    greeter = HelloWorldExample(os.environ.get('NEO4J_BOLT_URL'),
                                os.environ.get('NEO4J_USER'),
                                os.environ.get('NEO4J_PASSWORD'))
    txt = greeter.return_greeting("hello, world")
    greeter.close()
    return txt
