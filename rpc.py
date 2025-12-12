from pypresence import Presence
import time, os, configparser, tempfile, shutil, psutil
import tomllib
from deobfuscator import deobfuscate_name

CLIENT_ID = "1436051986616287232"
CHECK_INTERVAL = 5
TEMP_DIR = os.path.join(tempfile.gettempdir(), "melonds_rpc")
CONFIG_FILE = os.path.join(os.getcwd(), "melonds_path.txt")

print("[INFO] Connecting to Discord...")
RPC = Presence(CLIENT_ID)
try:
    RPC.connect()
    print("[SUCCESS] Connected to Discord RPC!")
except Exception as e:
    print(f"[ERROR] Failed to connect to Discord: {e}")
    print("[INFO] Make sure Discord is running and try again.")
    exit(1)

# --- process checking ---
def is_melonds_running(self):
    """Check if any melonDS related exe is currently running."""
    for proc in psutil.process_iter(['name']):
        try:
            if 'melonds' in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
            continue
    return False

def get_melonds_window_title():
    """Get the window title of melonDS process."""
    try:
        import win32gui
        import win32process
        
        def callback(hwnd, titles):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['pid'] == pid and proc.info['name'].lower() == 'melonds.exe':
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            titles.append(title)
            return True
        
        titles = []
        win32gui.EnumWindows(callback, titles)
        return titles[0] if titles else None
    except ImportError:
        print("[WARN] pywin32 not installed. Install with: pip install pywin32")
        return None
    except Exception as e:
        return None

# --- helper functions for temp dir ---
def prepare_temp_dir():
    """Ensure temp directory exists and is empty."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

def clean_temp_dir():
    """Delete temp directory completely."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

# --- config / path detection ---
def ask_for_config_path():
    """Prompt user for path to melonDS.ini or melonDS.toml or folder containing them."""
    while True:
        path = input("Enter full path to your melonDS.ini or melonDS.toml file (or melonDS folder): ").strip('"').strip()
        if not path:
            continue

        if os.path.isdir(path):
            ini_path = os.path.join(path, "melonDS.ini")
            toml_path = os.path.join(path, "melonDS.toml")
            if os.path.exists(toml_path):
                path = toml_path
            elif os.path.exists(ini_path):
                path = ini_path
            else:
                print("[WARN] No melonDS.ini or melonDS.toml found in that folder.")
                continue

        if os.path.exists(path) and (path.endswith(".ini") or path.endswith(".toml")):
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(path)
            print(f"[INFO] Saved config path to {CONFIG_FILE}")
            return path
        else:
            print("[WARN] Invalid path or unsupported file type. Please try again.")

def load_config_path():
    """Load stored melonDS.ini/.toml path or ask user if not available."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            saved = f.read().strip()
            if os.path.exists(saved):
                return saved
            print("[WARN] Saved path no longer exists — re-entering...")
    return ask_for_config_path()

# --- searching ---
def _find_recentrom_in_obj(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = str(k).lower()
            if 'recent' in lk and 'rom' in lk:
                if isinstance(v, list) and v:
                    return v[0]
                if isinstance(v, str) and v.strip():
                    return v
            res = _find_recentrom_in_obj(v)
            if res:
                return res
    elif isinstance(obj, list):
        for item in obj:
            res = _find_recentrom_in_obj(item)
            if res:
                return res
    return None

def read_rom_from_toml(path):
    """Read TOML and try to find the recent ROM entry (robustly)."""
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
        
        for key in ("RecentROM", "recentRoms", "recentROM", "RecentRoms", "recentrom"):
            if key in data:
                val = data[key]
                if isinstance(val, list) and val:
                    return val[0]
                if isinstance(val, str) and val.strip():
                    return val
        result = _find_recentrom_in_obj(data)
        return result
    except Exception as e:
        print(f"[WARN] Failed to parse TOML: {e}")
        return None

def read_rom_from_ini(path):
    """Read old INI style melonDS config for recent ROM."""
    try:
        parser = configparser.ConfigParser(strict=False)
        parser.read(path, encoding="utf-8")
        for section in parser.sections():
            for key, value in parser.items(section):
                if "recentrom" in key.lower() and value.strip():
                    return value.strip().strip('"')
    except Exception as e:
        print(f"[WARN] Failed to parse INI: {e}")
    return None

def read_rom_from_config(config_path):
    """Read ROM path from the configured melonDS config file (toml or ini)."""
    if not config_path or not os.path.exists(config_path):
        return None
    rom_path = None
    if config_path.endswith(".toml"):
        rom_path = read_rom_from_toml(config_path)
    else:
        rom_path = read_rom_from_ini(config_path)

    if rom_path:
        rom_path = rom_path.strip().strip('"')
        rom_path = os.path.normpath(rom_path)
        if os.path.exists(rom_path):
            return rom_path
        toml_dir = os.path.dirname(config_path)
        rel_try = os.path.join(toml_dir, rom_path)
        if os.path.exists(rel_try):
            return rel_try
    return None

# --- main loop ---
config_path = load_config_path()
print(f"[INFO] Using config: {config_path}")
print("[INFO] Monitoring melonDS process...")

current_display_name = None
current_window_title = None
previous_extracted_name = None
start_time = None
rpc_active = False
idle_shown = False

prepare_temp_dir()

print("[INFO] Showing idle state on Discord...")
try:
    RPC.update(
        details="No ROM loaded",
        state="Idle",
        start=int(time.time()),
        large_image="nds_icon",
        large_text="Nintendo DS Emulator"
    )
    print("[SUCCESS] Initial Discord presence set!")
except Exception as e:
    print(f"[ERROR] Failed to update Discord presence: {e}")

try:
    while True:
        if not is_melonds_running():
            print("[INFO] melonDS.exe not detected — shutting down RPC.")
            RPC.clear()
            clean_temp_dir()
            break

        window_title = get_melonds_window_title()
        
        if window_title != current_window_title:
            print(f"[DEBUG] Window title changed: {window_title}")
            current_window_title = window_title
        
        rom_is_loaded = window_title and " - " in window_title and "melonDS" in window_title
        
        if rom_is_loaded:
            parts = window_title.split(" - ")
            extracted_name = parts[0].strip() if len(parts) >= 2 else None
            
            if extracted_name and extracted_name != previous_extracted_name:
                print(f"[INFO] ROM changed detected from window title: {extracted_name}")
                
                rom_name_clean = deobfuscate_name(extracted_name)
                rom_name_display = rom_name_clean.upper()
                
                print(f"[INFO] Now playing: {rom_name_display}")
                
                clean_temp_dir()
                prepare_temp_dir()
                
                previous_extracted_name = extracted_name
                current_display_name = rom_name_display
                start_time = int(time.time())
                
                try:
                    RPC.update(
                        details=current_display_name,
                        state="Playing on melonDS",
                        start=start_time,
                        large_image="nds_icon",
                        large_text=current_display_name
                    )
                    print(f"[SUCCESS] Discord updated: {current_display_name}")
                    rpc_active = True
                    idle_shown = False
                except Exception as e:
                    print(f"[ERROR] Failed to update Discord: {e}")
        else:
            if rpc_active and not idle_shown:
                print("[INFO] No ROM loaded — showing idle state.")
                try:
                    RPC.update(
                        details="No ROM loaded",
                        state="Idle",
                        large_image="nds_icon",
                        large_text="Nintendo DS Emulator"
                    )
                    print("[SUCCESS] Idle state shown on Discord!")
                except Exception as e:
                    print(f"[ERROR] Failed to update Discord: {e}")
                
                previous_extracted_name = None
                current_display_name = None
                start_time = None
                rpc_active = False
                idle_shown = True
                clean_temp_dir()

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n[INFO] Shutting down gracefully...")
finally:
    RPC.clear()
    RPC.close()
    clean_temp_dir()
    print("[INFO] Cleanup complete. Goodbye!")
