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

void Fatal ( cstr s ) {
  MessageBox(0, s, "Fatal Error in CCircle Module", MB_OK);
  exit(0);
}

void CC_GL_CheckError ( char const* file, int line ) {
  GLenum e = glGetError();
  char const* eStr = 0;
  switch (e) {
    case GL_INVALID_ENUM:
      eStr = "GL_INVALID_ENUM"; break;
    case GL_INVALID_VALUE:
      eStr = "GL_INVALID_VALUE"; break;
    case GL_INVALID_OPERATION:
      eStr = "GL_INVALID_OPERATION"; break;
    case GL_OUT_OF_MEMORY:
      eStr = "GL_OUT_OF_MEMORY"; break;
  }

  if (eStr) {
    char buff[256];
    snprintf(buff, sizeof(buff), "[%s:%d] OpenGL Error: %s", file, line, eStr);
    Fatal(buff);
  }
}

PyMODINIT_FUNC
PyInit_ccircle ( void ) {
  PyObject* self = PyModule_Create(&ccircle_module);
  if (self == 0)
    return 0;

  /* Submodule Initialization. */ {
    CC_Init_Font(self);
    CC_Init_Image(self);
    CC_Init_Input(self);
    CC_Init_Sound(self);
    CC_Init_Window(self);
  }

  return self;
}
