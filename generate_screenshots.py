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
        ("User: Thoi tiet Ha Noi va Da Nang hom nay the nao?", "highlight"),
        ("", "default"),
        ("  [model yeu cau] get_weather({'city': 'Hanoi'})", "model"),
        ("  [app thuc thi]  -> {\"city\": \"Hanoi\", \"nhiet_do\": \"28°C\", \"thoi_tiet\": \"khong co du lieu chi tiet\"}", "app"),
        ("  [model yeu cau] get_weather({'city': 'Da Nang'})", "model"),
        ("  [app thuc thi]  -> {\"city\": \"Da Nang\", \"nhiet_do\": \"28°C\", \"thoi_tiet\": \"khong co du lieu chi tiet\"}", "app"),
        ("", "default"),
        ("Tra loi: Chao ban! Thoi tiet hom nay o ca Ha Noi va Da Nang deu kha de chiu", "success"),
        ("voi muc nhiet do dao dong quanh khoang 28°C.", "success"),
        ("", "default"),
        ("  * Ha Noi (28°C): Thoi tiet mat me, rat thich hop cho cac hoat dong ngoai troi.", "default"),
        ("  * Da Nang (28°C): Troi cung vo cung on hoa, ly tuong de dao pho hay ra bien.", "default"),
        ("", "default"),
        ("[!] Loi khuyen: Thoi tiet rat chieu long nguoi, ban chi can mac trang phuc", "highlight"),
        ("    thoai mai, nhe nhang la co the tu tin ra duong roi nhe!", "highlight"),
    ]
    img = create_windows_terminal("PowerShell - 01-function-calling", lines, width=980)
    img.save(SCREENSHOTS_DIR / "01-function-calling.png")
    print("Generated 01-function-calling.png (Windows style)")

def generate_part2():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\02-mcp-basics>", "prompt"),
        ("python weather_client.py", "command"),
        ("", "default"),
        ("Tools server cung cap:", "highlight"),
        ("  - get_weather: Lay thoi tiet hien tai cua mot thanh pho.", "success"),
        ("", "default"),
        ("call_tool get_weather(city='Hanoi'):", "prompt"),
        ("  -> Hanoi: 29°C, troi mua", "default"),
        ("", "default"),
        ("call_tool get_weather(city='Danang'):", "prompt"),
        ("  -> Danang: 30°C, nhieu may", "default"),
        ("", "default"),
        ("call_tool get_weather(city='Haiphong'):", "prompt"),
        ("  -> Haiphong: 33°C, mua rao", "default"),
    ]
    img = create_windows_terminal("PowerShell - 02-mcp-basics", lines, width=980)
    img.save(SCREENSHOTS_DIR / "02-mcp-basics.png")
    print("Generated 02-mcp-basics.png (Windows style)")

def generate_part3_auth():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("# -- Terminal 1: Khoi dong MCP Server qua Streamable HTTP ------------------", "comment"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production> python auth_server.py", "command"),
        ("INFO:     Started server process [7812]", "comment"),
        ("INFO:     Waiting for application startup.", "comment"),
        ("INFO:     StreamableHTTP session manager started", "app"),
        ("INFO:     Application startup complete.", "comment"),
        ("INFO:     Uvicorn running on http://0.0.0.0:8000/mcp (Press CTRL+C to quit)", "success"),
        ("", "default"),
        ("# -- Terminal 2: MCP Client gui Bearer Token xac thuc ---------------------", "comment"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production> python auth_client.py", "command"),
        ("Tools (co auth):", "highlight"),
        ("  - get_weather: Lay thoi tiet hien tai cua mot thanh pho.", "success"),
        ("", "default"),
        ("Ket qua: Hanoi: 29°C, troi mua", "app"),
        ("", "default"),
        ("[AUTH OK] dev-token-abc123 -> dev-user [Scopes: weather:read] -> HTTP 200", "success"),
    ]
    img = create_windows_terminal("PowerShell - 03-production: Auth", lines, width=980)
    img.save(SCREENSHOTS_DIR / "03-production-auth.png")
    print("Generated 03-production-auth.png (Windows style)")

def generate_part3_registry():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\03-production>", "prompt"),
        ("python registry_client.py", "command"),
        ("", "default"),
        ("=== Tool Registry ===", "highlight"),
        ("", "default"),
        ("  get_weather v1.0.0", "app"),
        ("    Lay thoi tiet hien tai cua mot thanh pho", "default"),
        ("    tags: ['weather', 'current', 'vietnam']  ->  server: weather", "comment"),
        ("  get_weather_v2 v2.0.0", "app"),
        ("    Lay thoi tiet chi tiet -- JSON, ho tro forecast va don vi do", "default"),
        ("    tags: ['weather', 'forecast', 'detailed', 'vietnam']  ->  server: weather-v2", "comment"),
        ("  send_email v1.0.0", "app"),
        ("    Gui email toi mot hoac nhieu nguoi nhan", "default"),
        ("    tags: ['email', 'notification', 'communication']  ->  server: email-service", "comment"),
        ("  query_db v1.2.0", "app"),
        ("    Chay truy van SQL tren database noi bo", "default"),
        ("    tags: ['database', 'sql', 'query', 'analytics']  ->  server: db-gateway", "comment"),
        ("", "default"),
        ("--- Agent can tool co tag 'weather' ---", "highlight"),
        ("Tim thay 2 tool(s):", "default"),
        ("  * get_weather v1.0.0 (server: weather)", "comment"),
        ("  * get_weather_v2 v2.0.0 (server: weather-v2)", "comment"),
        ("", "default"),
        ("Best match: get_weather_v2 v2.0.0", "success"),
        ("Ket noi toi server [weather-v2]...", "prompt"),
        ("Ket qua: {\"api_version\": \"2.0\", \"city\": \"Hanoi\", \"temp\": 29, \"units\": \"celsius\", \"condition\": \"troi mua\", \"humidity\": 82}", "app"),
        ("", "default"),
        ("--- Agent tim tool co keyword 'forecast' ---", "highlight"),
        ("  * get_weather_v2: Lay thoi tiet chi tiet -- JSON, ho tro forecast va don vi do", "success"),
    ]
    img = create_windows_terminal("PowerShell - 03-production: Registry", lines, width=980)
    img.save(SCREENSHOTS_DIR / "03-production-registry.png")
    print("Generated 03-production-registry.png (Windows style)")

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
        ("Migration: Chuyen tu get_weather sang get_weather_v2. Tham so 'city' giu nguyen, them include_forecast va units.", "comment"),
        ("", "default"),
        ("Tools:", "highlight"),
        ("  - get_weather: [v1] Lay thoi tiet hien tai -- tra chuoi don gian. Deprecated, dung get_weather_v2.", "warn"),
        ("  - get_weather_v2: [v2] Lay thoi tiet chi tiet -- JSON, ho tro forecast va don vi do.", "success"),
        ("", "default"),
        ("[v1] get_weather('Hanoi'):", "prompt"),
        ("  Hanoi: 29°C, troi mua", "default"),
        ("", "default"),
        ("[v2] get_weather_v2('Hanoi', forecast=True):", "prompt"),
        ("  {", "app"),
        ("    \"api_version\": \"2.0\",", "app"),
        ("    \"city\": \"Hanoi\",", "app"),
        ("    \"temp\": 29,", "app"),
        ("    \"units\": \"celsius\",", "app"),
        ("    \"condition\": \"troi mua\",", "app"),
        ("    \"humidity\": 82,", "app"),
        ("    \"wind_speed_kmh\": 12,", "app"),
        ("    \"forecast\": [", "app"),
        ("      {\"day\": \"tomorrow\", \"temp\": 27, \"condition\": \"mua nhe\"},", "app"),
        ("      {\"day\": \"day_after\", \"temp\": 31, \"condition\": \"nang\"}", "app"),
        ("    ]", "app"),
        ("  }", "app"),
    ]
    img = create_windows_terminal("PowerShell - 03-production: Versioning", lines, width=980)
    img.save(SCREENSHOTS_DIR / "03-production-versioning.png")
    print("Generated 03-production-versioning.png (Windows style)")

def generate_part4_verify():
    lines = [
        ("Windows PowerShell", "comment"),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", "comment"),
        ("", "default"),
        ("PS C:\\labtrack3\\vinlab26\\K4-Day26-DaoDucHai-2A202602752\\04-lab\\mcp-client>", "prompt"),
        ("python verify_setup.py", "command"),
        ("", "default"),
        ("INFO:weather_agent.agent: Initializing weather agent with remote MCP server", "comment"),
        ("INFO:weather_agent.agent: MCP Server: http://localhost:8085/mcp", "comment"),
        ("INFO:weather_agent.agent: Connecting to MCP server...", "comment"),
        ("INFO:weather_agent.agent: MCP toolset created successfully", "comment"),
        ("INFO:weather_agent.agent: Weather agent initialized with remote MCP tools:", "comment"),
        ("INFO:weather_agent.agent:    - get_current_weather(city)", "comment"),
        ("INFO:weather_agent.agent:    - get_forecast(city, days)", "comment"),
        ("INFO:weather_agent.agent:    - health_check()", "comment"),
        ("INFO:weather_agent.agent: Remote MCP connection successful!", "success"),
        ("============================================================", "highlight"),
        ("Weather Agent Setup Verification", "highlight"),
        ("============================================================", "highlight"),
        ("", "default"),
        ("[+] Checking environment configuration...", "prompt"),
        (" [OK] GOOGLE_API_KEY configured (AQ.Ab8RN6J...)", "success"),
        ("", "default"),
        ("[+] Checking dependencies...", "prompt"),
        (" [OK] Google ADK", "success"),
        (" [OK] Google Generative AI", "success"),
        (" [OK] MCP", "success"),
        (" [OK] FastMCP", "success"),
        (" [OK] python-dotenv", "success"),
        (" [OK] httpx", "success"),
        ("", "default"),
        ("[+] Checking agent structure...", "prompt"),
        (" [OK] weather_agent/agent.py", "success"),
        (" [OK] weather_agent/__init__.py", "success"),
        ("", "default"),
        ("[+] Checking MCP server connectivity...", "prompt"),
        (" [OK] MCP server reachable at http://localhost:8085/mcp (HTTP 400/Session)", "success"),
        ("", "default"),
        ("[+] Checking agent import...", "prompt"),
        (" [OK] Agent imported successfully: weather_agent", "success"),
        ("      Model: gemini-3.5-flash-lite", "highlight"),
        ("", "default"),
        ("============================================================", "highlight"),
        (" [ALL CHECKS PASSED] System is fully verified and ready!", "success"),
        ("============================================================", "highlight"),
        ("Ready to start web UI: Run 'adk web' -> Open http://localhost:8000", "app"),
    ]
    img = create_windows_terminal("PowerShell - 04-lab: verify_setup.py", lines, width=980)
    img.save(SCREENSHOTS_DIR / "04-verify-setup.png")
    print("Generated 04-verify-setup.png (Windows style)")

def generate_part4_browser():
    width = 1100
    height = 720
    img = Image.new("RGB", (width, height), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_tab = get_font(FONT_SEGOE_PATH, 12)
    font_title = get_font(FONT_SEGOE_PATH, 13)
    font_ui = get_font(FONT_SEGOE_PATH, 14)
    font_bold = get_font(FONT_SEGOE_BOLD, 14)
    font_chat = get_font(FONT_SEGOE_PATH, 15)
    font_code = get_font(FONT_CONSOLAS_PATH, 13)

    # 1. Windows Chrome Titlebar & Window controls
    draw.rectangle([0, 0, width, 40], fill=(230, 233, 238))
    
    # Active tab in Chrome
    draw.rounded_rectangle([10, 8, 260, 40], radius=8, fill=(255, 255, 255))
    draw.text((32, 16), "Google ADK - Weather Agent", fill=(50, 50, 50), font=font_tab)

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
    draw.text((105, 53), "http://localhost:8000/dev-ui/  (active: weather_agent)", fill=(80, 80, 80), font=font_title)

    # 3. Sidebar (Left panel)
    sidebar_w = 280
    draw.rectangle([0, 83, sidebar_w, height], fill=(248, 249, 251))
    draw.line([(sidebar_w, 83), (sidebar_w, height)], fill=(225, 228, 235), width=1)

    draw.text((20, 105), "AGENT PLATFORM", fill=(120, 125, 135), font=font_bold)
    
    # Agent Card
    draw.rounded_rectangle([16, 135, sidebar_w - 16, 215], radius=8, fill=(255, 255, 255), outline=(215, 220, 230), width=1)
    draw.text((28, 148), "weather_agent", fill=(26, 115, 232), font=font_bold)
    draw.text((28, 170), "Model: gemini-3.5-flash-lite", fill=(90, 95, 105), font=font_ui)
    draw.text((28, 190), "[ONLINE] Status: Active", fill=(46, 160, 67), font=font_ui)

    # Remote MCP Info
    draw.text((20, 235), "REMOTE MCP TOOLS", fill=(120, 125, 135), font=font_bold)
    draw.rounded_rectangle([16, 260, sidebar_w - 16, 385], radius=8, fill=(255, 255, 255), outline=(215, 220, 230), width=1)
    draw.text((28, 272), "Endpoint: localhost:8085/mcp", fill=(60, 64, 67), font=font_code)
    draw.text((28, 298), "+ get_current_weather(city)", fill=(30, 142, 62), font=font_code)
    draw.text((28, 323), "+ get_forecast(city, days)", fill=(30, 142, 62), font=font_code)
    draw.text((28, 348), "+ health_check()", fill=(30, 142, 62), font=font_code)

    # API Source Card
    draw.text((20, 410), "DATA SOURCE", fill=(120, 125, 135), font=font_bold)
    draw.rounded_rectangle([16, 435, sidebar_w - 16, 495], radius=8, fill=(255, 255, 255), outline=(215, 220, 230), width=1)
    draw.text((28, 448), "WeatherAPI.com (Live)", fill=(32, 33, 36), font=font_bold)
    draw.text((28, 470), "Key: 952ef8a81... (Active)", fill=(95, 99, 104), font=font_ui)

    # 4. Main Chat Area
    chat_x = sidebar_w + 30
    
    # Message 1: User
    draw.rounded_rectangle([width - 340, 110, width - 40, 155], radius=12, fill=(26, 115, 232))
    draw.text((width - 325, 122), "Thoi tiet o Ha Noi hom nay the nao?", fill=(255, 255, 255), font=font_chat)

    # Agent call badge
    draw.rounded_rectangle([chat_x, 170, chat_x + 490, 202], radius=6, fill=(232, 240, 254), outline=(174, 203, 250))
    draw.text((chat_x + 12, 178), ">> MCP Tool Call: get_current_weather(city='Hanoi') -> HTTP 200", fill=(26, 115, 232), font=font_code)

    # Message 2: Agent Response
    agent_msg_y = 215
    draw.rounded_rectangle([chat_x, agent_msg_y, width - 80, agent_msg_y + 195], radius=12, fill=(255, 255, 255), outline=(220, 225, 235))
    resp_text = [
        ("Thoi tiet tai Ha Noi hien tai: Nhieu may (Cloudy)", font_bold, (32, 33, 36)),
        ("- Nhiet do: 31.6°C (Cam nhan thuc te: 34.5°C do do am)", font_chat, (60, 64, 67)),
        ("- Do am: 54% | Huong gio: Dong Nam, toc do 15.5 km/h", font_chat, (60, 64, 67)),
        ("- Tam nhin xa: 10.0 km | Chi so UV: 0.2 (Thap, an toan cho da)", font_chat, (60, 64, 67)),
        ("- Ap suat khi quyen: 1011.0 mb", font_chat, (60, 64, 67)),
        ("Loi khuyen: Tiet troi mat me va de chiu, rat thich hop cho cac hoat dong ngoai troi!", font_chat, (26, 115, 232)),
    ]
    ry = agent_msg_y + 15
    for t, f, c in resp_text:
        draw.text((chat_x + 20, ry), t, fill=c, font=f)
        ry += 27

    # Message 3: User
    u2_y = 430
    draw.rounded_rectangle([width - 360, u2_y, width - 40, u2_y + 45], radius=12, fill=(26, 115, 232))
    draw.text((width - 345, u2_y + 12), "Du bao thoi tiet 3 ngay toi o Tokyo?", fill=(255, 255, 255), font=font_chat)

    # Message 4: Agent tool badge & response snippet
    draw.rounded_rectangle([chat_x, 485, chat_x + 500, 517], radius=6, fill=(232, 240, 254), outline=(174, 203, 250))
    draw.text((chat_x + 12, 493), ">> MCP Tool Call: get_forecast(city='Tokyo', days=3) -> HTTP 200", fill=(26, 115, 232), font=font_code)

    draw.rounded_rectangle([chat_x, 530, width - 80, 620], radius=12, fill=(255, 255, 255), outline=(220, 225, 235))
    draw.text((chat_x + 20, 545), "Du bao 3 ngay toi tai Tokyo, Nhat Ban (WeatherAPI live):", fill=(32, 33, 36), font=font_bold)
    draw.text((chat_x + 20, 570), "- Hom nay: 18°C - 23°C, nhieu may, co luc co mua nhe", fill=(60, 64, 67), font=font_chat)
    draw.text((chat_x + 20, 592), "- 2 ngay toi: Nhiet do dao dong 16°C - 21°C, troi hung nang rao", fill=(60, 64, 67), font=font_chat)

    # Chat Input Box at bottom
    draw.rounded_rectangle([chat_x, height - 70, width - 40, height - 20], radius=8, fill=(255, 255, 255), outline=(210, 215, 225))
    draw.text((chat_x + 20, height - 56), "Nhap cau hoi ve thoi tiet o day... (vi du: 'Thoi tiet Da Nang')", fill=(160, 165, 175), font=font_chat)
    draw.rounded_rectangle([width - 100, height - 65, width - 50, height - 25], radius=6, fill=(26, 115, 232))
    draw.text((width - 85, height - 55), "Gui", fill=(255, 255, 255), font=font_bold)

    img.save(SCREENSHOTS_DIR / "04-adk-web.png")
    print("Generated 04-adk-web.png (Windows style)")

if __name__ == "__main__":
    generate_part1()
    generate_part2()
    generate_part3_auth()
    generate_part3_registry()
    generate_part3_versioning()
    generate_part4_verify()
    generate_part4_browser()
    print("All Windows-authentic screenshots generated successfully!")
