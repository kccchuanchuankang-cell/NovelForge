import jwt
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core import settings
import time

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. 白名单检查
        path = request.url.path
        # 允许访问根路径、文档、登录接口、以及健康检查
        whitelist = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            f"{settings.app.api_prefix}/auth/login",
        ]
        
        # 静态资源放行 (如果是生产环境 Nginx 处理静态资源，这里主要处理静态路由)
        if any(path == p for p in whitelist) or path.startswith("/static"):
            return await call_next(request)

        # 2. Token 校验
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Authentication required"}
            )
        
        token = auth_header.split(" ")[1]
        try:
            # 校验 JWT
            payload = jwt.decode(
                token, 
                settings.admin.secret_key, 
                algorithms=["HS256"]
            )
            # 可以在这里把用户信息存入 request.state
            request.state.user = payload.get("sub")
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Token has expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Invalid token"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": f"Authentication failed: {str(e)}"}
            )

        return await call_next(request)
