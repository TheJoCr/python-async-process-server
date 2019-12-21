from starlette.applications import Starlette

# Create and configure the starlette app
def make_app( routes ):
    app = Starlette( debug=True, routes=routes )
    return app
