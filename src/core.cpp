#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Una función simple para probar que C++ responde
static PyObject* test_connection(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("CAutoGUI: Engine C++ conectado con éxito!");
}

// Tabla de métodos que Python podrá ver
static PyMethodDef CAutoGuiMethods[] = {
    {"test", test_connection, METH_VARARGS, "Prueba la conexión entre Python y C++"},
    {NULL, NULL, 0, NULL}
};

// Definición del módulo
static struct PyModuleDef cautoguimodule = {
    PyModuleDef_HEAD_INIT,
    "cautogui_core", // Nombre del binario (.pyd o .so)
    "Core de alto rendimiento para DanckardAutoGUI",
    -1,
    CAutoGuiMethods
};

// Función de inicialización (Python la busca al hacer 'import')
PyMODINIT_FUNC PyInit_cautogui_core(void) {
    return PyModuleCreate(&cautoguimodule);
}