from http import HTTPStatus

from aiohttp import web


@web.middleware
async def middleware(request: web.Request, handler):
    logger = request.app["logger"]
    logger.debug({"log_message": "request received", "endpoint": request.path})

    try:
        response = await handler(request)

        logger.debug({
            "method": request.method,
            "endpoint": request.path,
            "status": str(response.status),
        })

        return response
    except web.HTTPException as e:
        if e.status == HTTPStatus.INTERNAL_SERVER_ERROR:
            logger.exception({
                "method": request.method,
                "endpoint": request.path,
                "log_message": e.text,
                "status": str(e.status),
            })
            return web.json_response(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                data={"message": "500: Internal Server Error"},
            )

        if e.status in (HTTPStatus.NOT_FOUND, HTTPStatus.UNAUTHORIZED, HTTPStatus.UNPROCESSABLE_ENTITY):
            logger.warning({
                "method": request.method,
                "endpoint": request.path,
                "log_message": e.text,
                "status": str(e.status),
            })
            return web.json_response(
                status=e.status, data={"message": e.text}
            )

        raise e
    except:
        logger.exception({"log_message": "unexpected error"})

        return web.json_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            data={"message": "500: Internal Server Error"},
        )
