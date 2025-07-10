# Gateway Microservice

A FastAPI-based API gateway that routes requests to multiple microservices based on configured predicates.

## Configuration

### Route Configuration

Routes are configured in `configuration/routes.yml`:

```yaml
routes:
  - id: user-service
    uri: http://localhost:8090
    predicate: /api/v1/users/**
    auth-required: true

server:
  port: 8090
```