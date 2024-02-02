from variantbrowser.vb_app import create_app
import pytest

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    #app.register_blueprint(routes)
    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
