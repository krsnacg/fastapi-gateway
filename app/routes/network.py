import httpx
from fastapi import Response, Request, HTTPException, status
from ..core.settings import settings

async def forward_request(request: Request, target_url: str, user_id: str | None) -> Response:
    try:
        forward_headers = dict(request.headers)
        
        if "authorization" in request.headers:
            del forward_headers["authorization"]
        
        if user_id:
            forward_headers["X-User-ID"] = str(user_id)
            ## Can add roles or other user info if needed
            
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=forward_headers,
                content=await request.body(),
                params=request.query_params,
                timeout=10
            )
            # Filtra headers que no deberían pasarse de vuelta al cliente
            excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
            response_headers = {
                name: value for name, value in response.headers.items()
                if name.lower() not in excluded_headers
            }

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers,#dict(response.headers),
                media_type=response.headers.get("content-type", "application/json")
            )

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error forwarding request to backend: {exc}"
        )
        