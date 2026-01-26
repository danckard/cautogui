#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <windows.h>
#include <vector>
GdiplusStartupInput gdiplusStartupInput;
ULONG_PTR gdiplusToken;
GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
struct MonitorData {
    int x, y, w, h;
    bool is_primary;
};

BOOL CALLBACK EnumMonitorsProc(HMONITOR hMonitor, HDC hdcMonitor, LPRECT lprcMonitor, LPARAM dwData) {
    auto* monitors = reinterpret_cast<std::vector<MonitorData>*>(dwData);
    MONITORINFO mi;
    mi.cbSize = sizeof(mi);
    if (GetMonitorInfo(hMonitor, &mi)) {
        monitors->push_back({
            (int)mi.rcMonitor.left,
            (int)mi.rcMonitor.top,
            (int)(mi.rcMonitor.right - mi.rcMonitor.left),
            (int)(mi.rcMonitor.bottom - mi.rcMonitor.top),
            (bool)(mi.dwFlags & MONITORINFOF_PRIMARY)
        });
    }
    return TRUE;
}

static PyObject* get_monitors(PyObject* self, PyObject* args) {
    std::vector<MonitorData> monitors;
    EnumDisplayMonitors(NULL, NULL, EnumMonitorsProc, reinterpret_cast<LPARAM>(&monitors));
    PyObject* py_list = PyList_New(monitors.size());
    for (size_t i = 0; i < monitors.size(); ++i) {
        PyObject* dict = Py_BuildValue("{s:i, s:i, s:i, s:i, s:b}",
            "x", monitors[i].x, "y", monitors[i].y,
            "width", monitors[i].w, "height", monitors[i].h,
            "is_primary", monitors[i].is_primary);
        PyList_SetItem(py_list, i, dict);
    }
    return py_list;
}
static PyObject* key_event(PyObject* self, PyObject* args) {
    int vk, flags;
    if (!PyArg_ParseTuple(args, "ii", &vk, &flags)) return NULL;

    INPUT input = {0};
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = (WORD)vk;
    input.ki.dwFlags = flags;
    SendInput(1, &input, sizeof(INPUT));
    
    Py_RETURN_NONE;
}
static PyObject* capture_all(PyObject* self, PyObject* args) {
    int x = GetSystemMetrics(SM_XVIRTUALSCREEN);
    int y = GetSystemMetrics(SM_YVIRTUALSCREEN);
    int w = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    int h = GetSystemMetrics(SM_CYVIRTUALSCREEN);

    HDC hScreen = GetDC(NULL);
    HDC hDC = CreateCompatibleDC(hScreen);
    HBITMAP hBitmap = CreateCompatibleBitmap(hScreen, w, h);
    SelectObject(hDC, hBitmap);

    BitBlt(hDC, 0, 0, w, h, hScreen, x, y, SRCCOPY);

    BITMAPINFOHEADER bi = { sizeof(BITMAPINFOHEADER), w, -h, 1, 32, BI_RGB };
    std::vector<unsigned char> pixels(w * h * 4);
    GetDIBits(hDC, hBitmap, 0, h, pixels.data(), (BITMAPINFO*)&bi, DIB_RGB_COLORS);

    DeleteObject(hBitmap);
    DeleteDC(hDC);
    ReleaseDC(NULL, hScreen);

    return PyBytes_FromStringAndSize((char*)pixels.data(), pixels.size());
}
static PyObject* locate_all(PyObject* self, PyObject* args) {
    Py_buffer screen_buf, templ_buf;
    int s_w, s_h, t_w, t_h;
    float confidence;

    if (!PyArg_ParseTuple(args, "y*iiy*iif", &screen_buf, &s_w, &s_h, &templ_buf, &t_w, &t_h, &confidence))
        return NULL;

    unsigned char* screen = (unsigned char*)screen_buf.buf;
    unsigned char* templ = (unsigned char*)templ_buf.buf;
    int max_diff = (int)((1.0f - confidence) * 255);

    PyObject* results_list = PyList_New(0);
    int v_left = GetSystemMetrics(SM_XVIRTUALSCREEN);
    int v_top = GetSystemMetrics(SM_YVIRTUALSCREEN);

    for (int y = 0; y <= s_h - t_h; ++y) {
        for (int x = 0; x <= s_w - t_w; ++x) {
            bool match = true;
            for (int ty = 0; ty < t_h; ++ty) {
                for (int tx = 0; tx < t_w; ++tx) {
                    int s_ptr = ((y + ty) * s_w + (x + tx)) * 4;
                    int t_ptr = (ty * t_w + tx) * 4;

                    if (abs(screen[s_ptr] - templ[t_ptr]) > max_diff ||
                        abs(screen[s_ptr+1] - templ[t_ptr+1]) > max_diff ||
                        abs(screen[s_ptr+2] - templ[t_ptr+2]) > max_diff) {
                        match = false;
                        break;
                    }
                }
                if (!match) break;
            }

            if (match) {
                PyObject* pos = Py_BuildValue("(ii)", x + v_left, y + v_top);
                PyList_Append(results_list, pos);
                Py_DECREF(pos);
                
                
                x += (t_w - 1); 
            }
        }
    }

    PyBuffer_Release(&screen_buf);
    PyBuffer_Release(&templ_buf);
    return results_list;
}
static PyObject* press_key(PyObject* self, PyObject* args) {
    int key_code;
    if (!PyArg_ParseTuple(args, "i", &key_code)) return NULL;

    INPUT inputs[2] = {0};
    
    inputs[0].type = INPUT_KEYBOARD;
    inputs[0].ki.wVk = (WORD)key_code;
    
    inputs[1].type = INPUT_KEYBOARD;
    inputs[1].ki.wVk = (WORD)key_code;
    inputs[1].ki.dwFlags = KEYEVENTF_KEYUP;

    SendInput(2, inputs, sizeof(INPUT));
    Py_RETURN_NONE;
}
static PyObject* find_image(PyObject* self, PyObject* args) {
    Py_buffer screen_buf, templ_buf;
    int s_w, s_h, t_w, t_h, grayscale;
    float confidence;
    PyObject* region_obj;

    if (!PyArg_ParseTuple(args, "y*iiy*iifiO", &screen_buf, &s_w, &s_h, &templ_buf, &t_w, &t_h, &confidence, &grayscale, &region_obj))
        return NULL;

    int rx_start, ry_start, rx_end, ry_end;
    PyArg_ParseTuple(region_obj, "iiii", &rx_start, &ry_start, &rx_end, &ry_end);

    unsigned char* screen = (unsigned char*)screen_buf.buf;
    unsigned char* templ = (unsigned char*)templ_buf.buf;
    int max_diff = (int)((1.0f - confidence) * 255);

    for (int y = ry_start; y <= ry_end - t_h; ++y) {
        for (int x = rx_start; x <= rx_end - t_w; ++x) {
            bool match = true;
            for (int ty = 0; ty < t_h; ++ty) {
                for (int tx = 0; tx < t_w; ++tx) {
                    int s_ptr = ((y + ty) * s_w + (x + tx)) * 4;
                    int t_ptr = (ty * t_w + tx) * 4;

                    if (grayscale) {
                        int s_lum = (screen[s_ptr+2]*2 + screen[s_ptr+1]*5 + screen[s_ptr]) >> 3;
                        int t_lum = (templ[t_ptr+2]*2 + templ[t_ptr+1]*5 + templ[t_ptr]) >> 3;
                        if (abs(s_lum - t_lum) > max_diff) { match = false; break; }
                    } else {
                        if (abs(screen[s_ptr] - templ[t_ptr]) > max_diff ||
                            abs(screen[s_ptr+1] - templ[t_ptr+1]) > max_diff ||
                            abs(screen[s_ptr+2] - templ[t_ptr+2]) > max_diff) {
                            match = false; break;
                        }
                    }
                }
                if (!match) break;
            }
            if (match) {
                int v_left = GetSystemMetrics(SM_XVIRTUALSCREEN);
                int v_top = GetSystemMetrics(SM_YVIRTUALSCREEN);
                PyBuffer_Release(&screen_buf);
                PyBuffer_Release(&templ_buf);
                return Py_BuildValue("(ii)", x + v_left, y + v_top);
            }
        }
    }
    PyBuffer_Release(&screen_buf);
    PyBuffer_Release(&templ_buf);
    Py_RETURN_NONE;
}
static PyObject* move_mouse_abs(PyObject* self, PyObject* args) {
    int x, y;
    if (!PyArg_ParseTuple(args, "ii", &x, &y)) return NULL;

    // Get dimensions of the entire virtual desktop
    int v_left = GetSystemMetrics(SM_XVIRTUALSCREEN);
    int v_top = GetSystemMetrics(SM_YVIRTUALSCREEN);
    int v_width = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    int v_height = GetSystemMetrics(SM_CYVIRTUALSCREEN);

    INPUT input = {0};
    input.type = INPUT_MOUSE;
    
    // Normalization to 0 to 65535 (required by MOUSEEVENTF_ABSOLUTE)
    input.mi.dx = (long)((x - v_left) * (65536.0f / v_width));
    input.mi.dy = (long)((y - v_top) * (65536.0f / v_height));
    
    input.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK;

    SendInput(1, &input, sizeof(INPUT));
    Py_RETURN_NONE;
}
static PyObject* mouse_event_raw(PyObject* self, PyObject* args) {
    int dwFlags, x, y;
    if (!PyArg_ParseTuple(args, "iii", &dwFlags, &x, &y)) return NULL;

    INPUT input = {0};
    input.type = INPUT_MOUSE;
    input.mi.dx = x * (65535 / GetSystemMetrics(SM_CXVIRTUALSCREEN));
    input.mi.dy = y * (65535 / GetSystemMetrics(SM_CYVIRTUALSCREEN));
    input.mi.dwFlags = dwFlags | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK;

    SendInput(1, &input, sizeof(INPUT));
    Py_RETURN_NONE;
}
static PyObject* mouse_down(PyObject* self, PyObject* args) {
    // 0 para izquierdo, 1 para derecho
    int button;
    if (!PyArg_ParseTuple(args, "i", &button)) return NULL;

    if (button == 0) mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
    else mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0);

    Py_RETURN_NONE;
}

// Función para soltar el botón
static PyObject* mouse_up(PyObject* self, PyObject* args) {
    int button;
    if (!PyArg_ParseTuple(args, "i", &button)) return NULL;

    if (button == 0) mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    else mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0);

    Py_RETURN_NONE;
}
static PyMethodDef CAutoGuiMethods[] = {
    {"get_monitors", get_monitors, METH_VARARGS, "get all monitors"},
    {"capture_all", capture_all, METH_VARARGS, "capture all screen"},
    {"find_image", find_image, METH_VARARGS, "find an image in the buffer"},
    {"locate_all", locate_all, METH_VARARGS, "find all instances"},
    {"key_event", (PyCFunction)key_event, METH_VARARGS, "raw key event"},
    {"press_key", (PyCFunction)press_key, METH_VARARGS, "simulate pressing and releasing a physical key"},
    {"move_mouse_abs", (PyCFunction)move_mouse_abs, METH_VARARGS, "move mouse to an absolute position"},
    {"mouse_down", mouse_down, METH_VARARGS, "press mouse button"},
    {"mouse_up", mouse_up, METH_VARARGS, "release mouse button"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cautogui_core_module = {
    PyModuleDef_HEAD_INIT,
    "cautogui_core",
    "Internal C++ extension for high-performance UI automation.",
    -1,
    CAutoGuiMethods
};

PyMODINIT_FUNC PyInit_cautogui_core(void) {
    return PyModule_Create(&cautogui_core_module);
}