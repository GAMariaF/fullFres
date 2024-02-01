#import flask
#import unittest
#import flask_test
from variantbrowser.backend.__init__ import create_app
import pytest

#class TestApp(unittest.TestCase):

    #def setUp(self):
    #    app = create_app()
    #    app.testing = True
    #    self.app = app.test_client()
    #    
    #def test_home(self):
#
    #    #result = self.app.get('127.0.0.1/api/import')
#
    #    def has_no_empty_params(rule):
    #        defaults = rule.defaults if rule.defaults is not None else ()
    #        arguments = rule.arguments if rule.arguments is not None else ()
    #        return len(defaults) >= len(arguments)
    #    
    #    links = []
    #    result = self.app.application.url_map.iter_rules()
    #    
    #    for rule in result:
#
    #        if "GET" in rule.methods and has_no_empty_params(rule):
    #            url = url_for(rule.endpoint, **(rule.defaults or {}))
    #            links.append((url, rule.endpoint))
#
    #    print(links)
#
    #    res1 = self.app.post("/login")
#
    #    print(res1)

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_request_example(client):
    response = client.get("/api/samples")
    assert b"<h2>Hello, World!</h2>" in response.data


#if __name__ == '__main__':
#    unittest.main()
