#include "ccircle.h"

static PyMethodDef ccircle_methods[] = {
  { 0, 0, 0, 0 },
};

static struct PyModuleDef ccircle_module = {
  PyModuleDef_HEAD_INIT,
  "ccircle",
  0,
  -1,
  ccircle_methods,
};

void Fatal ( cstr s )
{
  MessageBox(0, s, "Fatal Error in CCircle Module", MB_OK);
  exit(0);
}

PyMODINIT_FUNC
PyInit_ccircle ( void )
{
  PyObject* self = PyModule_Create(&ccircle_module);
  if (self == 0)
    return 0;

  /* Submodule Initialization. */ {
    ccircle_init_image(self);
    ccircle_init_input(self);
    ccircle_init_window(self);
  }

  return self;
}
