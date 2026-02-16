try:
    from . import cautogui_core
except ImportError:
    import cautogui_core
from PIL import Image
import ctypes
import time
import math

class Tweens:
    """Mathematical easing functions for smooth mouse movement."""
    @staticmethod
    def linear(n):
        return n

    @staticmethod
    def easeInQuad(n): return n**2
    
    @staticmethod
    def easeOutQuad(n): return -n * (n - 2)
    
    @staticmethod
    def easeInOutQuad(n):
        n *= 2
        if n < 1: return 0.5 * n**2
        return -0.5 * ((n - 1) * (n - 3) - 1)

    @staticmethod
    def easeInCubic(n): return n**3
    
    @staticmethod
    def easeOutCubic(n): return (n - 1)**3 + 1
    
    @staticmethod
    def easeInOutCubic(n):
        n *= 2
        if n < 1: return 0.5 * n**3
        return 0.5 * ((n - 2)**3 + 2)

    @staticmethod
    def easeInSine(n): return -1 * math.cos(n * (math.pi / 2)) + 1
    
    @staticmethod
    def easeOutSine(n): return math.sin(n * (math.pi / 2))
    
    @staticmethod
    def easeInOutSine(n): return -0.5 * (math.cos(math.pi * n) - 1)

    @staticmethod
    def easeInExpo(n): return 0 if n == 0 else 2**(10 * (n - 1))
    
    @staticmethod
    def easeOutExpo(n): return 1 if n == 1 else 1 - 2**(-10 * n)

    @staticmethod
    def easeInElastic(n, period=0.3):
        if n == 0 or n == 1: return n
        p = period
        s = p / 4
        return -(2**(10 * (n - 1)) * math.sin((n - 1 - s) * (2 * math.pi) / p))

    @staticmethod
    def easeOutElastic(n, period=0.3):
        if n == 0 or n == 1: return n
        p = period
        s = p / 4
        return (2**(-10 * n) * math.sin((n - s) * (2 * math.pi) / p) + 1)

    @staticmethod
    def easeInBack(n, s=1.70158): return n**2 * ((s + 1) * n - s)
    
    @staticmethod
    def easeOutBack(n, s=1.70158): return (n - 1)**2 * ((s + 1) * (n - 1) + s) + 1
    @staticmethod
    def easeOutBounce(n):
        if n < 1 / 2.75:
            return 7.5625 * n**2
        elif n < 2 / 2.75:
            n -= 1.5 / 2.75
            return 7.5625 * n**2 + 0.75
        elif n < 2.5 / 2.75:
            n -= 2.25 / 2.75
            return 7.5625 * n**2 + 0.9375
        else:
            n -= 2.625 / 2.75
            return 7.5625 * n**2 + 0.984375

    @staticmethod
    def easeInBounce(n): return 1 - Tweens.easeOutBounce(1 - n)

    @staticmethod
    def easeInOutBounce(n):
        if n < 0.5: return Tweens.easeInBounce(n * 2) * 0.5
        return Tweens.easeOutBounce(n * 2 - 1) * 0.5 + 0.5

class CAutoGUI:
    FAILSAFE = True
    FAILSAFE_POINTS = [(0, 0)]
    _TWEEN_MAP = {name: func for name, func in Tweens.__dict__.items() 
                  if isinstance(func, staticmethod)}
    KEY_MAP = {
        'enter': 0x0D,
        'esc': 0x1B,
        'tab': 0x09,
        'space': 0x20,
        'backspace': 0x08,
        'shift': 0x10,
        'ctrl': 0x11,
        'alt': 0x12,
        'f5': 0x74,
    }


    def position(self):
        """
        return the current xy coordinates of the mouse cursor as a two-integer tuple. multimonitor
        """
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)




    def __init__(self):
        self.user32 = ctypes.windll.user32
    
    def _check_failsafe(self):
        if self.FAILSAFE:
            pos = self.position() 
            if pos in self.FAILSAFE_POINTS:
                raise Exception("Failsafe activated: Mouse moved to a corner.")

    def moveTo(self, x, y, duration=0.0 , tween=None):
        """
        Move the mouse cursor to absolute coordinates.
        
        Args:
            x (int): Destination X coordinate.
            y (int): Destination Y coordinate.
            duration (float): Time in seconds to perform movement.
            tween (str|callable): Easing function or alias.
        """
        self._check_failsafe()
        
        if isinstance(tween, str):
            tween_func = self._TWEEN_MAP.get(tween, Tweens.linear)
        elif callable(tween):
            tween_func = tween
        else:
            tween_func = Tweens.linear
            
        start_x, start_y = self.position()
        dx, dy = x - start_x, y - start_y
        
        if duration <= 0:
            cautogui_core.move_mouse_abs(int(x), int(y))
            return

        start_time = time.perf_counter()
        while True:
            elapsed = time.perf_counter() - start_time
            if elapsed >= duration:
                break
            
            # Calculate progress (0.0 to 1.0)
            progress = tween(elapsed / duration)
            
            curr_x = start_x + int(dx * progress)
            curr_y = start_y + int(dy * progress)
            
            cautogui_core.move_mouse_abs(curr_x, curr_y)
            # Control frequency for smoothness
            time.sleep(0.001) 
        
        # Asegurar posición final
        cautogui_core.move_mouse_abs(int(x), int(y))
    def dragTo(self, x, y, duration=0.5):
        """drag the mouse from its current position to (x, y)."""
        self._check_failsafe()
        # MOUSEEVENTF_LEFTDOWN = 0x0002
        cautogui_core.mouse_event_raw(0x0002, 0, 0) 
        self.moveTo(x, y, duration)
        # MOUSEEVENTF_LEFTUP = 0x0004
        cautogui_core.mouse_event_raw(0x0004, 0, 0)
    
    VK_SHIFT = 0x10
    KEYEVENTF_KEYUP = 0x0002

    def press(self, key):
        """press and release a physical key."""
        vk = self._get_vk(key)
        needs_shift = self._needs_shift(key)

        if needs_shift:
            cautogui_core.key_event(self.VK_SHIFT, 0) # Shift Down

        cautogui_core.key_event(vk, 0)                # Key Down
        cautogui_core.key_event(vk, self.KEYEVENTF_KEYUP) # Key Up

        if needs_shift:
            cautogui_core.key_event(self.VK_SHIFT, self.KEYEVENTF_KEYUP) # Shift Up

    def write(self, text, interval=0.01):
        """text typing handling for uppercase and lowercase."""
        for char in text:
            self.press(char)
            if interval > 0:
                time.sleep(interval)

    def _get_vk(self, char):
        """convert a character to a Windows Virtual Key Code."""
        # Handle special characters
        special = {'enter': 0x0D, 'esc': 0x1B, 'tab': 0x09, ' ': 0x20}
        if char.lower() in special:
            return special[char.lower()]
        
        # For letters and numbers
        res = ctypes.windll.user32.VkKeyScanW(ord(char))
        return res & 0xFF

    def _needs_shift(self, char):
        """detect if the character requires the SHIFT key."""
        if len(char) > 1: return False
        res = ctypes.windll.user32.VkKeyScanW(ord(char))
        return (res >> 8) & 0x01
    
    def press(self, key):
        """Simulate pressing a physical key."""
        key = key.lower()
        if key in self.KEY_MAP:
            code = self.KEY_MAP[key]
        elif len(key) == 1:
            code = ord(key.upper())
        else:
            raise ValueError(f"Key not recognized: {key}")
        
        cautogui_core.press_key(code)

    def typewrite(self, text, interval=0.0):
        """write a string of text."""
        for char in text:
            self.press(char)
            if interval > 0:
                time.sleep(interval)

    def size(self):
        w = self.user32.GetSystemMetrics(78) # SM_CXVIRTUALSCREEN
        h = self.user32.GetSystemMetrics(79) # SM_CYVIRTUALSCREEN
        return (w, h)
    def locateAllOnScreen(self, image_path, confidence=0.9):
        img = Image.open(image_path).convert('RGBA')
        # Swap to BGRA for the C++ extension
        r, g, b, a = img.split()
        img_bgra = Image.merge("RGBA", (b, g, r, a))
        
        tw, th = img_bgra.size
        sw, sh = self.size()
        screen_bytes = cautogui_core.capture_all()

        # Return a list of tuples [(x,y), (x,y), ...]
        return cautogui_core.locate_all(screen_bytes, sw, sh, img_bgra.tobytes(), tw, th, confidence)
    def locateOnScreen(self, image_path, confidence=0.9, grayscale=False, region=None):
        """
        image_path: path to target
        confidence: 0.0 a 1.0 (tolerance)
        grayscale: True/False (for compatibility)
        region: (x, y, width, height) - Limit search to an area
        """
        # 1. Load and prepare template
        img = Image.open(image_path).convert('RGBA')
        
        # Swap to BGRA for the C++ extension
        r, g, b, a = img.split()
        img_bgra = Image.merge("RGBA", (b, g, r, a))
        tw, th = img_bgra.size
        templ_bytes = img_bgra.tobytes()

        # 2. Get screen capture
        sw, sh = self.size()
        screen_bytes = cautogui_core.capture_all()
        
        # If there is a region, the C++ extension will only search within those limits
        # region_data = (x_start, y_start, x_end, y_end)
        if region:
            # Convert region (x, y, w, h) to limits for the C++ loop
            rx, ry, rw, rh = region
            # Adjust virtual coordinates to local buffer
            v_left = ctypes.windll.user32.GetSystemMetrics(76)
            v_top = ctypes.windll.user32.GetSystemMetrics(77)
            
            search_area = (
                max(0, rx - v_left), 
                max(0, ry - v_top), 
                min(sw, rx - v_left + rw), 
                min(sh, ry - v_top + rh)
            )
        else:
            search_area = (0, 0, sw, sh)

        # 3. Call the C++ extension
        # The extension now receives: buffer, sw, sh, template, tw, th, conf, gray, search_area
        return cautogui_core.find_image(
            screen_bytes, sw, sh, 
            templ_bytes, tw, th, 
            confidence, 
            1 if grayscale else 0,
            search_area
        )
    def locateCenterOnScreen(self, image_path, confidence=0.9, grayscale=False, region=None):
        """
        Search for the image and return the center coordinates (x, y).
        Useful for passing directly to cautogui.click().
        """
        # 1. Search for the normal position (upper left corner)
        coords = self.locateOnScreen(image_path, confidence, grayscale, region)
        
        if coords:
            # 2. Open the image only to know its dimensions
            with Image.open(image_path) as img:
                tw, th = img.size
            
            # 3. Calculate the center
            center_x = coords[0] + (tw // 2)
            center_y = coords[1] + (th // 2)
            
            return (center_x, center_y)
        
        return None
    def displayMousePosition(self):
        """show the current mouse position in real-time (useful for debugging)."""
        print("Press Ctrl+C to exit.")
        try:
            while True:
                x, y = self.position()
                print(f"\rX: {str(x).ljust(5)} Y: {str(y).ljust(5)}", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDone.")
    def click(self, x=None, y=None, clicks=1, interval=0.1, button='left', duration=0.0, tween=Tweens.linear):
        """move the mouse to (x,y) with smooth movement and click."""
        if x is not None and y is not None:
            self.moveTo(x, y, duration=duration, tween=tween)
        
        # Map of buttons for SendInput
        down_flag = 0x0002 if button == 'left' else 0x0008
        up_flag = 0x0004 if button == 'left' else 0x0010
        
        for i in range(clicks):
            self._check_failsafe()
            cautogui_core.mouse_event_raw(down_flag, 0, 0)
            time.sleep(0.01) # Small delay for physical movement
            cautogui_core.mouse_event_raw(up_flag, 0, 0)
            if i < clicks - 1:
                time.sleep(interval)
    @staticmethod
    def mouseDown(button='left'):
        b = 0 if button == 'left' else 1
        cautogui_core.mouse_down(b)

    @staticmethod
    def mouseUp(button='left'):
        b = 0 if button == 'left' else 1
        cautogui_core.mouse_up(b)
cautogui = CAutoGUI()

# Exportar métodos de la instancia como funciones globales
_methods = [
    'click', 'displayMousePosition', 'locateCenterOnScreen', 
    'locateOnScreen', 'locateAllOnScreen', 'typewrite', 
    'press', 'write', 'dragTo', 'moveTo', 'position', 'size'
]
for name in _methods:
    globals()[name] = getattr(cautogui, name)

# Exportar Tweens individualmente
for name, func in CAutoGUI._TWEEN_MAP.items():
    globals()[name] = func.__func__