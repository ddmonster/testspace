    # swagger-ui

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi import FastAPI
def setup_swagger_ui(app:FastAPI):
    """set up static point mount first"""
    @app.get("/localdocs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,  # type: ignore
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            # swagger_js_url=BASE_DIR/'static'/'swagger-ui'/'swagger-ui-bundle.js',
            # swagger_css_url=BASE_DIR/'static'/'swagger-ui'/'swagger-ui.css',
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @app.get("/localredoc", include_in_schema=False)
    async def custom_redoc_swagger_ui_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,  # type: ignore
            title=app.title + " - Swagger UI",
            # swagger_js_url=BASE_DIR/'static'/'swagger-ui'/'swagger-ui-bundle.js',
            # swagger_css_url=BASE_DIR/'static'/'swagger-ui'/'swagger-ui.css',
            redoc_js_url="/static/redoc.standalone.js",
            redoc_favicon_url="/static/favicon.png",
        )
    # app.add_route(cast(str,app.docs_url), custom_swagger_ui_html, include_in_schema=False)
    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)  # type: ignore
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()