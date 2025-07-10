from fastapi import APIRouter, Request, HTTPException, status, Depends
from app.core.settings import settings
from ..core.security import get_current_user_private
from .network import forward_request

router = APIRouter()

@router.api_route(
    path="/{path_route:path}", 
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], 
    operation_id="catch_all_dynamic_route"
)
async def catch_all(request: Request, path_route: str):
    # Check if the path route matches any of the configured predicates
    path_route = "/" + path_route
    config_route = None
    user_id = None

    print(f"Checking if path [{path_route}] matches any predicate")

    for r in settings.ROUTES:
        if str.startswith(path_route, r.predicate):
            print(f"Found matching predicate: {r.predicate}")
            config_route = r
            # If a match is found, we can break out of the loop
            # This assumes that predicates are unique and ordered by specificity
            break
            
    if not config_route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No matching route found for the given path",
            # headers={"X-Error": "RouteNotFound"}
        )

    # Here you would typically determine which service to call based on the predicate
    
    suffix = path_route[len(config_route.predicate):]
    print(f"Suffix after predicate match: {suffix}")
    
    # Get the service URI from the routes configuration
    service_uri = config_route.uri
    
    if not service_uri:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service URI not configured for the matched predicate",
            # headers={"X-Error": "ServiceURINotConfigured"}
        )
    
    print(f"Service URI for matched predicate: {service_uri}")
    
    # Check if the route requires authentication
    if config_route.auth_required:
        # Here you would typically check for authentication
        # For example, you might check for a valid token in the headers
        try:
            # user_id = await get_current_user_private(token=Depends())
            print("Authentication required for this route")
        except HTTPException as e:
            raise e
        # if not username:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Authentication required for this route",
        #         # headers={"X-Error": "AuthenticationRequired"}
        #     )
        # You would also validate the token here
        
    
    
    # If the path matches then redirect the request to the appropriate service
    
    # Here you would typically make an asynchronous HTTP request to the service
    
    return await forward_request(request, f"{service_uri}/{suffix}", user_id)
    
    ## This should wait for the service to respond and return the response (not locking other possible requests)
    
    # Return the response to the client