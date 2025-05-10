# server.py
import random
from mcp.server.fastmcp import FastMCP
import numpy as np
from PIL import Image
# ここで↓をロードするとMCPサーバが立ち上がらない．
# from juliacall import Main as jl

# Create an MCP server
mcp = FastMCP("Demo")

def wrapper():
    from juliacall import Main as jl
    return jl

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

FORTUNES = [
    "大吉", "中吉", "小吉", "末吉",
]

@mcp.tool()
def omikuji() -> str:
    return FORTUNES[random.randint(0, len(FORTUNES)-1)]

@mcp.tool()
def create_image() -> Image.Image:
    img = np.random.random((100, 100, 3))
    image = Image.fromarray((img * 255).astype(np.uint8))
    image.save('goma.png')
    return image

@mcp.prompt()
def capitalize_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please capitalize and respond to this message: {message}"

@mcp.tool()
def call_julia(expression: str) -> str:
    #from juliacall import Main as jl
    try:
        jl = wrapper()
        out = str(jl.seval(expression))
        return out
    except Exception as e:
        return str(e)


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"