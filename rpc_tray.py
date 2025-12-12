from pypresence import Presence
import time, os, tempfile, shutil, psutil, threading, sys, winreg, re
from deobfuscator import deobfuscate_name
from PIL import Image, ImageDraw
import pystray    

CLIENT_ID = "1436051986616287232"
CHECK_INTERVAL = 3
TEMP_DIR = os.path.join(tempfile.gettempdir(), "melonds_rpc")

REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "melonDS-RPC"

class MelonDSRPC:
    def __init__(self):
        self.rpc = None
        self.running = False
        self.thread = None
        self.current_display_name = None
        self.current_window_title = None
        self.previous_extracted_name = None
        self.start_time = None
        self.rpc_active = False
        self.icon = None
        self.autostart_enabled = self.check_autostart()
        self.no_rom_counter = 0
        
    def create_image(self):
        """Load system tray icon from ICO file."""
        try:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, "rpc_tray.ico")
            else:
                icon_path = "rpc_tray.ico"
            return Image.open(icon_path)
        except:
            image = Image.new('RGB', (64, 64), color='#008148')
            dc = ImageDraw.Draw(image)
            dc.rectangle([10, 10, 54, 54], fill='white')
            dc.text((20, 22), "DS", fill='#008148')
            return image
    
    def get_exe_path(self):
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            return os.path.abspath(sys.argv[0])
    
    def check_autostart(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except:
            return False
    
    def enable_autostart(self):
        try:
            exe_path = self.get_exe_path()
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
            winreg.CloseKey(key)
            self.autostart_enabled = True
            self.update_menu()
            return True
        except:
            return False
    
    def disable_autostart(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            self.autostart_enabled = False
            self.update_menu()
            return True
        except:
            return False
    
    def toggle_autostart(self, icon, item):
        if self.autostart_enabled:
            self.disable_autostart()
        else:
            self.enable_autostart()
    
    def update_menu(self):
        if self.icon:
            menu = pystray.Menu(
                pystray.MenuItem("melonDS RPC", lambda: None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    "Autostart with Windows",
                    self.toggle_autostart,
                    checked=lambda item: self.autostart_enabled
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit", self.quit_app)
            )
            self.icon.menu = menu
    
    def is_discord_running(self):
        for proc in psutil.process_iter(['name']):
            try:
                if 'discord' in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    def is_melonds_running(self):
        """Check if any melonDS related exe is running."""
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                if 'melonds' in proc_name and 'rpc' not in proc_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                continue
        return False
    
    def get_melonds_window_title(self):
        """Get the window title of melonDS process."""
        try:
            import win32gui
            import win32process
            
            def callback(hwnd, titles):
                if win32gui.IsWindowVisible(hwnd):
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if proc.info['pid'] == pid and 'melonds' in proc.info['name'].lower():
                                title = win32gui.GetWindowText(hwnd)
                                if title:
                                    titles.append(title)
                        except:
                            pass
                return True
            
            titles = []
            win32gui.EnumWindows(callback, titles)
            return titles[0] if titles else None
        except:
            return None
    
    def prepare_temp_dir(self):
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
    
    def clean_temp_dir(self):
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
    
    def connect_rpc(self):
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.update_icon_status("Connected to Discord")
            return True
        except:
            self.update_icon_status("Discord not available")
            return False
    
    def disconnect_rpc(self):
        """Disconnect and clear RPC from Discord."""
        if self.rpc:
            try:
                self.rpc.clear()
                self.rpc.close()
            except:
                pass
            self.rpc = None
            self.rpc_active = False
    
    def update_icon_status(self, status):
        if self.icon:
            self.icon.title = f"melonDS RPC\n{status}"
    
    def run_rpc(self):
        """Main RPC loop - only shows presence when melonDS is running."""
        self.prepare_temp_dir()
        
        while self.running:
            # Check if melonDS is running FIRST
            if not self.is_melonds_running():
                # melonDS not running - clear Discord presence
                if self.rpc_active:
                    self.disconnect_rpc()
                    self.update_icon_status("Waiting for melonDS")
                    self.current_display_name = None
                    self.previous_extracted_name = None
                    self.clean_temp_dir()
                
                time.sleep(CHECK_INTERVAL)
                continue
            
            discord_running = self.is_discord_running()
            
            if not discord_running:
                if self.rpc:
                    self.disconnect_rpc()
                self.update_icon_status("Discord not running")
                time.sleep(5)
                continue
            
            if not self.rpc:
                if not self.connect_rpc():
                    time.sleep(5)
                    continue
            
            window_title = self.get_melonds_window_title()
            
            if window_title != self.current_window_title:
                self.current_window_title = window_title
            
            # Skip if title is EXACTLY "melonDS" (menu click flicker)
            if window_title and window_title.strip() == "melonDS":
                # Menu interaction - skip this check entirely
                time.sleep(CHECK_INTERVAL)
                continue
            
            rom_is_loaded = window_title and " - " in window_title
            extracted_name = None
            
            if rom_is_loaded:
                if "melonDS" in window_title and " - " in window_title:
                    parts = window_title.split(" - ", 1)
                    if len(parts) >= 2:
                        rom_part = parts[1].strip()
                        rom_part = re.sub(r'\s*\[[\d/]+\]\s*$', '', rom_part)
                        extracted_name = rom_part.strip()
            
            # Process extracted name
            if extracted_name:
                if extracted_name != self.previous_extracted_name:
                    rom_name_clean = deobfuscate_name(extracted_name)
                    rom_name_display = rom_name_clean.upper()
                    
                    self.clean_temp_dir()
                    self.prepare_temp_dir()
                    
                    self.previous_extracted_name = extracted_name
                    self.current_display_name = rom_name_display
                    self.start_time = int(time.time())
                    
                    try:
                        self.rpc.update(
                            details=self.current_display_name,
                            state="Playing on melonDS",
                            start=self.start_time,
                            large_image="nds_icon",
                            large_text=self.current_display_name
                        )
                        self.rpc_active = True
                        self.update_icon_status(f"Playing: {rom_name_display[:20]}")
                    except:
                        self.rpc = None
            else:
                # No ROM extracted - clear if we had one
                if self.previous_extracted_name is not None:
                    self.previous_extracted_name = None
                    self.current_display_name = None
                    
                    try:
                        self.rpc.update(
                            details="melonDS",
                            state="No ROM loaded",
                            large_image="nds_icon",
                            large_text="Nintendo DS Emulator"
                        )
                        self.rpc_active = True
                        self.update_icon_status("melonDS idle (no ROM)")
                    except:
                        self.rpc = None
                elif not self.rpc_active:
                    try:
                        self.rpc.update(
                            details="melonDS",
                            state="No ROM loaded",
                            large_image="nds_icon",
                            large_text="Nintendo DS Emulator"
                        )
                        self.rpc_active = True
                        self.update_icon_status("melonDS idle (no ROM)")
                    except:
                        self.rpc = None


            
            time.sleep(CHECK_INTERVAL)
        
        self.disconnect_rpc()
        self.clean_temp_dir()
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_rpc, daemon=True)
            self.thread.start()
            self.update_icon_status("Starting...")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def quit_app(self, icon, item):
        self.stop()
        icon.stop()

def main():
    app = MelonDSRPC()
    
    if not app.autostart_enabled:
        app.enable_autostart()
    
    menu = pystray.Menu(
        pystray.MenuItem("melonDS RPC", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            "Autostart with Windows",
            app.toggle_autostart,
            checked=lambda item: app.autostart_enabled
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", app.quit_app)
    )
    
    app.icon = pystray.Icon("melonds_rpc", app.create_image(), "melonDS RPC", menu)
    app.start()
    app.icon.run()

if __name__ == "__main__":
    main()
