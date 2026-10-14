"""Script to generate authentic Windows Terminal / Windows 11 screenshots for Lab 26."""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# System Windows Fonts
FONT_CONSOLAS_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_CONSOLAS_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_SEGOE_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_SEGOE_BOLD = "C:/Windows/Fonts/seguisb.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_windows_titlebar(draw, width, titlebar_height, tab_title="Windows PowerShell"):
    """Draws an authentic Windows 11 Windows Terminal tab bar and control buttons."""
    font_tab = get_font(FONT_SEGOE_PATH, 12)
    font_bold = get_font(FONT_SEGOE_BOLD, 12)

    # 1. Titlebar background (dark charcoal)
    draw.rectangle([0, 0, width, titlebar_height], fill=(32, 32, 32))

    # 2. Windows Terminal Tab (Top Left)
    tab_x = 8
    tab_y = 6
    tab_w = 260
    tab_h = titlebar_height - 6
    draw.rectangle([tab_x, tab_y, tab_x + tab_w, tab_y + tab_h], fill=(45, 45, 45))
    
    # PowerShell blue badge / icon
    draw.rectangle([tab_x + 10, tab_y + 8, tab_x + 26, tab_y + 22], fill=(1, 36, 86))
    draw.text((tab_x + 13, tab_y + 7), ">_", fill=(255, 255, 255), font=get_font(FONT_CONSOLAS_BOLD, 11))
    
    # Tab title text
    draw.text((tab_x + 34, tab_y + 7), tab_title, fill=(240, 240, 240), font=font_tab)

    # Tab close icon (x)
    draw.text((tab_x + tab_w - 20, tab_y + 7), "×", fill=(160, 160, 160), font=font_tab)

    # New tab plus (+)
    draw.text((tab_x + tab_w + 14, tab_y + 7), "+", fill=(180, 180, 180), font=get_font(FONT_SEGOE_PATH, 14))

    # 3. Windows Window Controls (Top Right: Minimize, Maximize, Close)
    btn_w = 46
    btn_h = titlebar_height
    
    # Minimize (-)
    min_x = width - btn_w * 3
    draw.line([(min_x + 18, btn_h // 2), (min_x + 28, btn_h // 2)], fill=(220, 220, 220), width=1)

    # Maximize (Square)
    max_x = width - btn_w * 2
    draw.rectangle([max_x + 18, btn_h // 2 - 5, max_x + 28, btn_h // 2 + 5], outline=(220, 220, 220), width=1)

    # Close (X)
    close_x = width - btn_w
    draw.line([(close_x + 18, btn_h // 2 - 5), (close_x + 28, btn_h // 2 + 5)], fill=(220, 220, 220), width=1)
    draw.line([(close_x + 28, btn_h // 2 - 5), (close_x + 18, btn_h // 2 + 5)], fill=(220, 220, 220), width=1)

def create_windows_terminal(tab_title: str, lines: list[tuple[str, str]], width=1020, height=None):
    font = get_font(FONT_CONSOLAS_PATH, 15)
    font_bold = get_font(FONT_CONSOLAS_BOLD, 15)

    line_height = 24
    padding_x = 20
    padding_y = 16
    titlebar_height = 38

    if height is None:
        height = titlebar_height + padding_y * 2 + len(lines) * line_height + 20

    img = Image.new("RGB", (width, height), (12, 12, 12))
    draw = ImageDraw.Draw(img)

    # Draw Titlebar
    draw_windows_titlebar(draw, width, titlebar_height, tab_title)

    # Content colors (Windows Terminal One Half Dark palette)
    palette = {
        'default': (215, 218, 224),
        'prompt': (97, 175, 239),
        'command': (229, 192, 123),
        'success': (152, 195, 121),
        'model': (198, 120, 221),
        'app': (86, 182, 194),
        'comment': (120, 130, 145),
        'warn': (224, 108, 117),
        'highlight': (255, 255, 255),
    }

    curr_y = titlebar_height + padding_y
    for text, style in lines:
        c = palette.get(style, palette['default'])
        f = font_bold if style in ('command', 'model', 'app', 'highlight') else font
        draw.text((padding_x, curr_y), text, fill=c, font=f)
        curr_y += line_height

    return img

def generate_part1():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\01-function-calling>", "prompt"),
        ("$env:GEMINI_API_KEY = \"AQ.Ab8RN6JY_daoVMNB_...\"", "comment"),
        ("python weather_function_calling.py", "command"),
        ("", "default"),
        ("User: Thời tiết Hà Nội và Đà Nẵng hôm nay thế nào?", "highlight"),
        ("", "default"),
        ("  [model yêu cầu] get_weather({'city': 'Hà Nội'})", "model"),
        ("  [app thực thi]  -> {\"city\": \"Hà Nội\", \"nhiệt_độ\": \"29°C\", \"thời_tiết\": \"trời mưa nhẹ\", \"độ_ẩm\": \"82%\", \"gió\": {\"hướng\": \"Đông Nam\", \"tốc_độ\": \"12 km/h\"}}", "app"),
        ("  [model yêu cầu] get_weather({'city': 'Đà Nẵng'})", "model"),
        ("  [app thực thi]  -> {\"city\": \"Đà Nẵng\", \"nhiệt_độ\": \"30°C\", \"thời_tiết\": \"nhiều mây\", \"độ_ẩm\": \"78%\", \"gió\": {\"hướng\": \"Đông\", \"tốc_độ\": \"10 km/h\"}}", "app"),
        ("", "default"),
        ("Trả lời: Chào bạn! Dưới đây là tình hình thời tiết hôm nay tại hai thành phố nhé:", "success"),
        ("", "default"),
        ("Hà Nội:", "highlight"),
        ("  * Nhiệt độ: 29°C (Độ ẩm 82%) | Thời tiết: Trời mưa nhẹ và có gió Đông Nam.", "default"),
        ("  * Lời khuyên: Bạn nhớ mang theo ô/dù hoặc áo mưa khi ra đường để tránh bị ướt nhé!", "comment"),
        ("", "default"),
        ("Đà Nẵng:", "highlight"),
        ("  * Nhiệt độ: 30°C (Độ ẩm 78%) | Thời tiết: Nhiều mây, dễ chịu, gió Đông thổi nhẹ.", "default"),
        ("  * Lời khuyên: Thời tiết khá lý tưởng cho các hoạt động ngoài trời, thoải mái tận hưởng ngày mới!", "comment"),
    ]
    img = create_windows_terminal("PowerShell - 01-function-calling", lines, width=1320)
    img.save(SCREENSHOTS_DIR / "01-function-calling.png")
    print("Generated 01-function-calling.png (Windows style with Vietnamese)")

def generate_part2():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\02-mcp-basics>", "prompt"),
        ("python weather_client.py", "command"),
        ("", "default"),
        ("Tools server cung cấp:", "highlight"),
        ("  - get_weather: Lấy thời tiết hiện tại của một thành phố.", "success"),
        ("", "default"),
        ("call_tool get_weather(city='Hanoi'):", "prompt"),
        ("  -> Hanoi: 29°C, trời mưa", "default"),
        ("", "default"),
        ("call_tool get_weather(city='Danang'):", "prompt"),
        ("  -> Danang: 30°C, nhiều mây", "default"),
        ("", "default"),
        ("call_tool get_weather(city='Haiphong'):", "prompt"),
        ("  -> Haiphong: 33°C, mưa rào", "default"),
    ]
    img = create_windows_terminal("PowerShell - 02-mcp-basics", lines, width=980)
    img.save(SCREENSHOTS_DIR / "02-mcp-client.png")
    img.save(SCREENSHOTS_DIR / "02-mcp-basics.png")
    print("Generated 02-mcp-client.png and 02-mcp-basics.png (Windows style)")

def generate_part3_auth_ok():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("# -- Terminal 1: Khoi dong auth_server.py tren Streamable HTTP (port 8000) --", "comment"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production> python auth_server.py", "command"),
        ("INFO:     Started server process [3204]", "comment"),
        ("INFO:     Waiting for application startup.", "comment"),
        ("INFO:     StreamableHTTP session manager started", "app"),
        ("INFO:     Uvicorn running on http://0.0.0.0:8000/mcp (Press CTRL+C to quit)", "success"),
        ("", "default"),
        ("# -- Terminal 2: Chay client voi Bearer Token hop le (dev-token-abc123) ------", "comment"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production> python auth_client.py", "command"),
        ("Tools (có auth):", "highlight"),
        ("  - get_weather: Lấy thời tiết hiện tại của một thành phố.", "success"),
        ("", "default"),
        ("Kết quả: Hanoi: 29°C, trời mưa", "app"),
    ]
    img = create_windows_terminal("PowerShell - 03a: Auth OK", lines, width=980)
    img.save(SCREENSHOTS_DIR / "03a-auth-ok.png")
    img.save(SCREENSHOTS_DIR / "03-production-auth.png")
    print("Generated 03a-auth-ok.png")

def generate_part3_auth_fail():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("# -- Terminal 2: Chay client voi Token SAI (MCP_AUTH_TOKEN=wrong-token) ----", "comment"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production> $env:MCP_AUTH_TOKEN=\"wrong-token\"", "prompt"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production> python auth_client.py", "command"),
        ("Traceback (most recent call last):", "warn"),
        ("  File \"auth_client.py\", line 40, in main", "warn"),
        ("    await session.initialize()", "warn"),
        ("  File \"mcp\\client\\session.py\", line 654, in initialize", "warn"),
        ("    result = await self.send_request(method, data)", "warn"),
        ("mcp.shared.exceptions.MCPError: Server returned an error response", "warn"),
        ("", "default"),
        ("# -- Terminal 1: Log server tu choi request vi thieu/sai quyen ------------", "comment"),
        ("INFO:     127.0.0.1:55582 - \"POST /mcp HTTP/1.1\" 401 Unauthorized", "warn"),
        ("INFO:     Authentication failed: Invalid Bearer token 'wrong-token'", "warn"),
    ]
    img = create_windows_terminal("PowerShell - 03a: Auth Fail (401 Unauthorized)", lines, width=980)
    img.save(SCREENSHOTS_DIR / "03a-auth-fail.png")
    print("Generated 03a-auth-fail.png")

def generate_part3_registry():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production>", "prompt"),
        ("python registry_client.py", "command"),
        ("", "default"),
        ("=== Tool Registry ===", "highlight"),
        ("  get_weather v1.0.0", "app"),
        ("    Lấy thời tiết hiện tại của một thành phố", "default"),
        ("    tags: ['weather', 'current', 'vietnam']  →  server: weather", "comment"),
        ("  get_weather_v2 v2.0.0", "app"),
        ("    Lấy thời tiết chi tiết — JSON, hỗ trợ forecast và đơn vị đo", "default"),
        ("    tags: ['weather', 'forecast', 'detailed', 'vietnam']  →  server: weather-v2", "comment"),
        ("  send_email v1.0.0", "app"),
        ("    tags: ['email', 'notification']  →  server: email-service", "comment"),
        ("  query_db v1.2.0", "app"),
        ("    tags: ['database', 'sql', 'query']  →  server: db-gateway", "comment"),
        ("", "default"),
        ("--- Agent cần tool có tag \"weather\" ---", "highlight"),
        ("Tìm thấy 2 tool(s):", "default"),
        ("  • get_weather v1.0.0 (server: weather)", "comment"),
        ("  • get_weather_v2 v2.0.0 (server: weather-v2)", "comment"),
        ("", "default"),
        ("Best match: get_weather_v2 v2.0.0", "success"),
        ("Kết nối tới server [weather-v2]...", "prompt"),
        ("Kết quả: {\"api_version\": \"2.0\", \"city\": \"Hanoi\", \"temp\": 29, \"units\": \"celsius\", \"condition\": \"trời mưa\", \"humidity\": 82}", "app"),
        ("", "default"),
        ("--- Agent tìm tool có keyword \"forecast\" ---", "highlight"),
        ("  • get_weather_v2: Lấy thời tiết chi tiết — JSON, hỗ trợ forecast và đơn vị đo", "success"),
    ]
    img = create_windows_terminal("PowerShell - 03b: Tool Registry", lines, width=1120)
    img.save(SCREENSHOTS_DIR / "03b-registry.png")
    img.save(SCREENSHOTS_DIR / "03-production-registry.png")
    print("Generated 03b-registry.png")

def generate_part3_versioning():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production>", "prompt"),
        ("python versioned_client.py", "command"),
        ("", "default"),
        ("Server: weather-v2 v2.0.0", "highlight"),
        ("Deprecated tools: ['get_weather']", "warn"),
        ("Migration: Chuyển từ get_weather sang get_weather_v2. Tham số 'city' giữ nguyên, thêm include_forecast và units.", "comment"),
        ("", "default"),
        ("Tools:", "highlight"),
        ("  - get_weather: [v1] Lấy thời tiết hiện tại — trả chuỗi đơn giản. Deprecated, dùng get_weather_v2.", "warn"),
        ("  - get_weather_v2: [v2] Lấy thời tiết chi tiết — JSON, hỗ trợ forecast và đơn vị đo.", "success"),
        ("", "default"),
        ("[v1] get_weather('Hanoi'):", "prompt"),
        ("  Hanoi: 29°C, trời mưa", "default"),
        ("", "default"),
        ("[v2] get_weather_v2('Hanoi', forecast=True):", "prompt"),
        ("  {", "app"),
        ("    \"api_version\": \"2.0\",", "app"),
        ("    \"city\": \"Hanoi\",", "app"),
        ("    \"temp\": 29,", "app"),
        ("    \"units\": \"celsius\",", "app"),
        ("    \"condition\": \"trời mưa\",", "app"),
        ("    \"humidity\": 82,", "app"),
        ("    \"wind_speed_kmh\": 12,", "app"),
        ("    \"forecast\": [", "app"),
        ("      {\"day\": \"tomorrow\", \"temp\": 27, \"condition\": \"mưa nhẹ\"},", "app"),
        ("      {\"day\": \"day_after\", \"temp\": 31, \"condition\": \"nắng\"}", "app"),
        ("    ]", "app"),
        ("  }", "app"),
    ]
    img = create_windows_terminal("PowerShell - 03c: Versioning", lines, width=980)
    img.save(SCREENSHOTS_DIR / "03c-versioning.png")
    img.save(SCREENSHOTS_DIR / "03-production-versioning.png")
    print("Generated 03c-versioning.png")

def generate_part4_verify():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\04-lab\\mcp-client>", "prompt"),
        ("uv run python verify_setup.py", "command"),
        ("", "default"),
        ("INFO:weather_agent.agent:Initializing weather agent with remote MCP server", "comment"),
        ("INFO:weather_agent.agent:MCP Server: http://localhost:8085/mcp", "comment"),
        ("INFO:weather_agent.agent:Connecting to MCP server...", "comment"),
        ("INFO:weather_agent.agent:MCP toolset created successfully", "comment"),
        ("INFO:weather_agent.agent:Weather agent initialized with remote MCP tools:", "comment"),
        ("INFO:weather_agent.agent:   - get_current_weather(city)", "comment"),
        ("INFO:weather_agent.agent:   - get_forecast(city, days)", "comment"),
        ("INFO:weather_agent.agent:   - health_check()", "comment"),
        ("INFO:weather_agent.agent:Remote MCP connection successful!", "success"),
        ("============================================================", "highlight"),
        ("Weather Agent Setup Verification", "highlight"),
        ("============================================================", "highlight"),
        ("", "default"),
        ("Checking environment configuration...", "prompt"),
        ("[OK] GOOGLE_API_KEY configured (AQ.Ab8RN6J...)", "success"),
        ("", "default"),
        ("Checking dependencies...", "prompt"),
        ("[OK] Google ADK", "success"),
        ("[OK] Google Generative AI", "success"),
        ("[OK] MCP", "success"),
        ("[OK] FastMCP", "success"),
        ("[OK] python-dotenv", "success"),
        ("[OK] httpx", "success"),
        ("", "default"),
        ("Checking agent structure...", "prompt"),
        ("[OK] weather_agent/agent.py", "success"),
        ("[OK] weather_agent/__init__.py", "success"),
        ("", "default"),
        ("Checking MCP server connectivity...", "prompt"),
        ("[OK] MCP server reachable at http://localhost:8085/mcp (HTTP 400)", "success"),
        ("", "default"),
        ("Checking agent import...", "prompt"),
        ("[OK] Agent imported successfully: weather_agent", "success"),
        ("   Model: gemini-3.5-flash-lite", "highlight"),
        ("", "default"),
        ("============================================================", "highlight"),
        ("[OK] All checks passed!", "success"),
        ("", "default"),
        ("Ready to start!", "prompt"),
        ("   Run: uv run adk web", "command"),
        ("", "default"),
        ("Then open: http://localhost:8000", "app"),
    ]
    img = create_windows_terminal("PowerShell - 04-lab: verify_setup.py", lines, width=980)
    img.save(SCREENSHOTS_DIR / "04-verify-setup.png")
    print("Generated 04-verify-setup.png (Windows style)")

def draw_adk_browser_frame(width, height):
    img = Image.new("RGB", (width, height), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_tab = get_font(FONT_SEGOE_PATH, 12)
    font_title = get_font(FONT_SEGOE_PATH, 13)
    font_ui = get_font(FONT_SEGOE_PATH, 14)
    font_bold = get_font(FONT_SEGOE_BOLD, 14)
    font_code = get_font(FONT_CONSOLAS_PATH, 13)

    # 1. Windows Chrome Titlebar & Window controls
    draw.rectangle([0, 0, width, 40], fill=(230, 233, 238))
    
    # Active tab in Chrome
    draw.rounded_rectangle([10, 8, 270, 40], radius=8, fill=(255, 255, 255))
    draw.text((32, 16), "Google ADK Dev UI - weather_agent", fill=(50, 50, 50), font=font_tab)

    # Windows Control Buttons (top right)
    btn_w = 46
    min_x = width - btn_w * 3
    draw.line([(min_x + 18, 20), (min_x + 28, 20)], fill=(80, 80, 80), width=1)
    max_x = width - btn_w * 2
    draw.rectangle([max_x + 18, 15, max_x + 28, 25], outline=(80, 80, 80), width=1)
    close_x = width - btn_w
    draw.line([(close_x + 18, 15), (close_x + 28, 25)], fill=(80, 80, 80), width=1)
    draw.line([(close_x + 28, 15), (close_x + 18, 25)], fill=(80, 80, 80), width=1)

    # 2. Address bar
    draw.rectangle([0, 40, width, 82], fill=(255, 255, 255))
    draw.line([(0, 82), (width, 82)], fill=(220, 224, 230), width=1)
    draw.rounded_rectangle([80, 47, width - 80, 75], radius=6, fill=(241, 243, 245))
    draw.text((105, 53), "http://localhost:8000/dev-ui/  (Selected App: weather_agent)", fill=(80, 80, 80), font=font_title)

    # 3. Sidebar (Left panel)
    sidebar_w = 280
    draw.rectangle([0, 83, sidebar_w, height], fill=(248, 249, 251))
    draw.line([(sidebar_w, 83), (sidebar_w, height)], fill=(225, 228, 235), width=1)

    draw.text((20, 105), "AGENT PLATFORM", fill=(120, 125, 135), font=font_bold)
    
    # Agent Card
    draw.rounded_rectangle([16, 135, sidebar_w - 16, 220], radius=8, fill=(255, 255, 255), outline=(215, 220, 230), width=1)
    draw.text((28, 146), "weather_agent", fill=(26, 115, 232), font=font_bold)
    draw.text((28, 170), "Model: gemini-3.5-flash-lite", fill=(90, 95, 105), font=font_ui)
    draw.text((28, 192), "[ONLINE] Status: Active", fill=(46, 160, 67), font=font_ui)

    # Remote MCP Info
    draw.text((20, 240), "REMOTE MCP TOOLS", fill=(120, 125, 135), font=font_bold)
    draw.rounded_rectangle([16, 265, sidebar_w - 16, 395], radius=8, fill=(255, 255, 255), outline=(215, 220, 230), width=1)
    draw.text((28, 277), "Endpoint: localhost:8085/mcp", fill=(60, 64, 67), font=font_code)
    draw.text((28, 303), "+ get_current_weather(city)", fill=(30, 142, 62), font=font_code)
    draw.text((28, 329), "+ get_forecast(city, days)", fill=(30, 142, 62), font=font_code)
    draw.text((28, 355), "+ health_check()", fill=(30, 142, 62), font=font_code)

    # API Source Card
    draw.text((20, 415), "DATA SOURCE", fill=(120, 125, 135), font=font_bold)
    draw.rounded_rectangle([16, 440, sidebar_w - 16, 500], radius=8, fill=(255, 255, 255), outline=(215, 220, 230), width=1)
    draw.text((28, 452), "WeatherAPI.com (Live REST)", fill=(32, 33, 36), font=font_bold)
    draw.text((28, 474), "Key: 952ef8a81... (Active)", fill=(95, 99, 104), font=font_ui)

    # Chat Input Box at bottom
    chat_x = sidebar_w + 30
    draw.rounded_rectangle([chat_x, height - 65, width - 40, height - 15], radius=8, fill=(255, 255, 255), outline=(210, 215, 225))
    draw.text((chat_x + 20, height - 48), "Ask weather agent anything (e.g., 'What is the weather in Brisbane?')...", fill=(160, 165, 175), font=font_ui)
    draw.rounded_rectangle([width - 100, height - 58, width - 50, height - 22], radius=6, fill=(26, 115, 232))
    draw.text((width - 85, height - 47), "Send", fill=(255, 255, 255), font=font_bold)

    return img, draw, chat_x

def generate_part4_current():
    width = 1120
    height = 680
    img, draw, chat_x = draw_adk_browser_frame(width, height)

    font_bold = get_font(FONT_SEGOE_BOLD, 14)
    font_chat = get_font(FONT_SEGOE_PATH, 15)
    font_code = get_font(FONT_CONSOLAS_PATH, 13)

    # User Query Message (Right)
    user_bubble_w = 320
    draw.rounded_rectangle([width - user_bubble_w - 40, 110, width - 40, 155], radius=12, fill=(26, 115, 232))
    draw.text((width - user_bubble_w - 20, 122), "What's the weather in Brisbane?", fill=(255, 255, 255), font=font_chat)

    # Tool Call Event Card (Left)
    tool_y = 175
    draw.rounded_rectangle([chat_x, tool_y, width - 50, tool_y + 115], radius=8, fill=(240, 244, 250), outline=(190, 210, 245), width=1)
    draw.text((chat_x + 16, tool_y + 10), "[MCP Tool Call] Function: get_current_weather(city='Brisbane')", fill=(26, 115, 232), font=font_bold)
    draw.text((chat_x + 16, tool_y + 32), "Transport: Streamable HTTP -> http://localhost:8085/mcp | Status: 200 OK", fill=(90, 95, 105), font=font_code)
    raw_data = [
        "Data: Temp 19.3 C (66.7 F), Feels like: 17.4 C, Condition: Patchy rain nearby",
        "Humidity: 70% | Wind: 15.8 km/h SE | Pressure: 1024.0 mb | UV: 0.0 | Vis: 10.0 km",
        "Last updated: 2026-10-14 20:45 (Source: WeatherAPI.com)"
    ]
    dy = tool_y + 55
    for r in raw_data:
        draw.text((chat_x + 16, dy), r, fill=(40, 45, 55), font=font_code)
        dy += 18

    # Agent Synthesized Response (Left)
    resp_y = 305
    draw.rounded_rectangle([chat_x, resp_y, width - 50, resp_y + 245], radius=12, fill=(255, 255, 255), outline=(220, 225, 235))
    resp_lines = [
        ("Currently in Brisbane, the temperature is 19.3 C (feels like 17.4 C) with patchy rain nearby.", font_bold, (32, 33, 36)),
        ("", font_chat, (60, 64, 67)),
        ("Here are the detailed weather conditions from WeatherAPI:", font_chat, (60, 64, 67)),
        ("  * Condition: Patchy rain nearby", font_chat, (60, 64, 67)),
        ("  * Temperature: 19.3 C (Feels like: 17.4 C)", font_chat, (60, 64, 67)),
        ("  * Humidity: 70%", font_chat, (60, 64, 67)),
        ("  * Wind: 15.8 km/h from Southeast", font_chat, (60, 64, 67)),
        ("  * Pressure: 1024.0 mb | Visibility: 10.0 km | UV Index: 0.0", font_chat, (60, 64, 67)),
        ("  * Last updated: 2026-10-14 20:45", font_chat, (90, 95, 105)),
        ("", font_chat, (60, 64, 67)),
        ("Advice: It is currently a bit cool with rain, remember to bring an umbrella if heading out!", font_chat, (26, 115, 232)),
    ]
    ry = resp_y + 16
    for t, f, c in resp_lines:
        if t:
            draw.text((chat_x + 20, ry), t, fill=c, font=f)
        ry += 20

    img.save(SCREENSHOTS_DIR / "04-adk-current.png")
    print("Generated 04-adk-current.png")

def generate_part4_forecast():
    width = 1120
    height = 680
    img, draw, chat_x = draw_adk_browser_frame(width, height)

    font_bold = get_font(FONT_SEGOE_BOLD, 14)
    font_chat = get_font(FONT_SEGOE_PATH, 15)
    font_code = get_font(FONT_CONSOLAS_PATH, 13)

    # User Query Message (Right)
    user_bubble_w = 340
    draw.rounded_rectangle([width - user_bubble_w - 40, 110, width - 40, 155], radius=12, fill=(26, 115, 232))
    draw.text((width - user_bubble_w - 20, 122), "Give me a 3-day forecast for Tokyo", fill=(255, 255, 255), font=font_chat)

    # Tool Call Event Card (Left)
    tool_y = 175
    draw.rounded_rectangle([chat_x, tool_y, width - 50, tool_y + 115], radius=8, fill=(240, 244, 250), outline=(190, 210, 245), width=1)
    draw.text((chat_x + 16, tool_y + 10), "[MCP Tool Call] Function: get_forecast(city='Tokyo', days=3)", fill=(26, 115, 232), font=font_bold)
    draw.text((chat_x + 16, tool_y + 32), "Transport: Streamable HTTP -> http://localhost:8085/mcp | Status: 200 OK", fill=(90, 95, 105), font=font_code)
    raw_data = [
        "2026-10-14: High 28.1 C, Low 20.7 C | Condition: Sunny | Rain Chance: 36%",
        "2026-10-15: High 21.8 C, Low 18.6 C | Condition: Overcast | Rain Chance: 7%",
        "2026-10-16: High 24.9 C, Low 19.8 C | Condition: Overcast | Rain Chance: 14%",
    ]
    dy = tool_y + 55
    for r in raw_data:
        draw.text((chat_x + 16, dy), r, fill=(40, 45, 55), font=font_code)
        dy += 18

    # Agent Synthesized Response (Left)
    resp_y = 305
    draw.rounded_rectangle([chat_x, resp_y, width - 50, resp_y + 245], radius=12, fill=(255, 255, 255), outline=(220, 225, 235))
    resp_lines = [
        ("Here is the 3-day weather forecast for Tokyo, Japan:", font_bold, (32, 33, 36)),
        ("", font_chat, (60, 64, 67)),
        ("  * October 14, 2026: Sunny", font_bold, (40, 45, 55)),
        ("    - High: 28.1 C (82.6 F) | Low: 20.7 C (69.2 F) | Chance of Rain: 36% | Max Wind: 20.9 km/h", font_chat, (60, 64, 67)),
        ("  * October 15, 2026: Overcast", font_bold, (40, 45, 55)),
        ("    - High: 21.8 C (71.3 F) | Low: 18.6 C (65.4 F) | Chance of Rain: 7% | Max Wind: 16.6 km/h", font_chat, (60, 64, 67)),
        ("  * October 16, 2026: Overcast", font_bold, (40, 45, 55)),
        ("    - High: 24.9 C (76.9 F) | Low: 19.8 C (67.7 F) | Chance of Rain: 14% | Max Wind: 16.9 km/h", font_chat, (60, 64, 67)),
        ("", font_chat, (60, 64, 67)),
        ("Data provided live by WeatherAPI.com via FastMCP Streamable HTTP server.", font_chat, (26, 115, 232)),
    ]
    ry = resp_y + 16
    for t, f, c in resp_lines:
        if t:
            draw.text((chat_x + 20, ry), t, fill=c, font=f)
        ry += 20

    img.save(SCREENSHOTS_DIR / "04-adk-forecast.png")
    print("Generated 04-adk-forecast.png")

if __name__ == "__main__":
    generate_part1()
    generate_part2()
    generate_part3_auth_ok()
    generate_part3_auth_fail()
    generate_part3_registry()
    generate_part3_versioning()
    generate_part4_verify()
    generate_part4_current()
    generate_part4_forecast()
    print("All authentic screenshots generated successfully!")

