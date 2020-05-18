from secure import SecureHeaders

secure_headers = SecureHeaders()


def setup_middlewares(app, tracer):
    @app.middleware('response')
    async def set_secure_headers(request, response):
        with tracer.start_span(str(response)) as span:
            span.set_tag("body", response.body)

        secure_headers.sanic(response)
