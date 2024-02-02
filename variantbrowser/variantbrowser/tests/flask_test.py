#import flask
#import unittest
#import flask_test
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



def test_request_example(client):
    
    response = client.get("/")
    print(dir(client.application.url_map))
    for f in client.application.url_map.iter_rules():
        print(f)
    assert response.status_code == 200


#if __name__ == '__main__':
#    unittest.main()
