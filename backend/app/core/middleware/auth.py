import jwt
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core import settings
import time

from loguru import logger

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method
        
        # 1. 放行 OPTIONS 请求 (CORS 预检)
        if method == "OPTIONS":
            return await call_next(request)

        # 2. 路径标准化处理 (移除末尾斜杠)
        normalized_path = path.rstrip("/") if path != "/" else "/"
        
        # 3. 白名单检查
        # 允许访问根路径、文档、登录接口、以及健康检查
        whitelist = [
            "",
            "/docs",
            "/redoc",
            "/openapi.json",
            f"{settings.app.api_prefix}/auth/login",
            f"{settings.app.api_prefix}",
        ]
        
        # 检查是否在白名单中
        is_whitelisted = any(normalized_path == p for p in whitelist) or path.startswith("/static")
        
        if is_whitelisted:
            return await call_next(request)

        # 4. Token 提取逻辑 (Header -> Query Param)
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            # 兼容 SSE 等无法设置 Header 的场景，支持从 query 参数提取 token
            token = request.query_params.get("token")

        if not token:
            logger.warning(f"Auth failed: No token found for {method} {path}")
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Authentication required"}
            )
        
        try:
            # 校验 JWT
            payload = jwt.decode(
                token, 
                settings.admin.secret_key, 
                algorithms=["HS256"]
            )
            # 可以在这里把用户信息存入 request.state
            request.state.user = payload.get("sub")
            return await call_next(request)
        except jwt.ExpiredSignatureError:
            logger.warning(f"Auth failed: Token expired for {method} {path}")
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Token has expired"}
            )
        except jwt.InvalidTokenError:
            logger.warning(f"Auth failed: Invalid token for {method} {path}")
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Invalid token"}
            )
        except Exception as e:
            logger.error(f"Auth failed: Error {str(e)} for {method} {path}")
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": f"Authentication failed: {str(e)}"}
            )
