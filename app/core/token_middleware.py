
from fastapi import Request, Response

async def token_middleware(request: Request, call_next) -> Response:
    print("****************************************")
    print(request.client)
    print(request.headers)
    print(request.url)
    print(request.method)
    print(request.query_params)
    # print(await request.body())
    response = await call_next(request)

    
    return response
    
    
