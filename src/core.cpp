#define PY_SSIZE_T_CLEAN
#include <Python.h>

// --- Aquí va tu función test_connection que ya escribiste ---
static PyObject* test_connection(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("CAutoGUI: Engine C++ conectado con éxito!");
}

static PyMethodDef CAutoGuiMethods[] = {
    {"test", test_connection, METH_VARARGS, "Prueba la conexión"},
    {NULL, NULL, 0, NULL}
};

// --- EL CAMBIO ESTÁ AQUÍ ---
static struct PyModuleDef cautoguimodule = {
    PyModuleDef_HEAD_INIT,
    "cautogui_core", 
    NULL, 
    -1, 
    CAutoGuiMethods
};

// Esta función DEBE llamarse PyInit_ + nombre_del_modulo
PyMODINIT_FUNC PyInit_cautogui_core(void) {
    // CAMBIO CLAVE: Usamos PyModule_Create2 (la función real de la API) 
    // y pasamos PYTHON_API_VERSION explícitamente.
    return PyModule_Create2(&cautoguimodule, PYTHON_API_VERSION);
}