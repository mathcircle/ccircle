#include "ccircle.h"

/* TODO : Free gl handle */

typedef struct {
  PyObject_HEAD
  uint handle;
} ccircle_image_t;

static int
ccircle_image_init ( ccircle_image_t* self, PyObject* args )
{
  cstr path;
  if (!PyArg_ParseTuple(args, "s", &path))
    return -1;

  int sx, sy, channels;
  uchar* data = ccircle_image_load(path, &sx, &sy, &channels);
  if (!data)
    return -1;

  if (channels != 3 && channels != 4) {
    Fatal("Image type unsupported: must have 3 or 4 channels");
    return -1;
  }

  glGenTextures(1, &self->handle);
  glBindTexture(GL_TEXTURE_2D, self->handle);
  glPixelStorei(GL_PACK_ALIGNMENT, 1);
  glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
  glTexImage2D(GL_TEXTURE_2D,
    0,
    GL_RGBA8,
    sx, sy, 0,
    channels == 3 ? GL_RGB : GL_RGBA,
    GL_UNSIGNED_BYTE,
    data);

  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  ccircle_image_free(data);

  return 0;
}

/* --- Image::draw ---------------------------------------------------------- */

/* TODO : Should take a window object and make sure the window's GL context is
 *        current. */

static PyObject*
ccircle_image_draw ( ccircle_image_t* self, PyObject* args )
{
  float x, y, sx, sy;
  if (!PyArg_ParseTuple(args, "ffff", &x, &y, &sx, &sy))
    return 0;

  glEnable(GL_TEXTURE_2D);
  glBindTexture(GL_TEXTURE_2D, self->handle);
  glColor4f(1, 1, 1, 1);
  glBegin(GL_QUADS);
  glTexCoord2f(0, 0); glVertex2f(x, y);
  glTexCoord2f(0, 1); glVertex2f(x, y + sy);
  glTexCoord2f(1, 1); glVertex2f(x + sx, y + sy);
  glTexCoord2f(1, 0); glVertex2f(x + sx, y);
  glEnd();
  glDisable(GL_TEXTURE_2D);
  Py_RETURN_NONE;
}

/* -------------------------------------------------------------------------- */

static PyMethodDef ccircle_image_methods[] = {
  { "draw", (PyCFunction)ccircle_image_draw, METH_VARARGS,
    "Draw the image to the current window" },
  { 0 },
};


/* -------------------------------------------------------------------------- */

static PyTypeObject ccircle_image_pytype = {
  PyVarObject_HEAD_INIT(0, 0)
  "ccircle.Image",
  sizeof(ccircle_image_t),
  0,                                  /* tp_itemsize */
  0,                                  /* tp_dealloc */
  0,                                  /* tp_print */
  0,                                  /* tp_getattr */
  0,                                  /* tp_setattr */
  0,                                  /* tp_reserved */
  0,                                  /* tp_repr */
  0,                                  /* tp_as_number */
  0,                                  /* tp_as_sequence */
  0,                                  /* tp_as_mapping */
  0,                                  /* tp_hash  */
  0,                                  /* tp_call */
  0,                                  /* tp_str */
  0,                                  /* tp_getattro */
  0,                                  /* tp_setattro */
  0,                                  /* tp_as_buffer */
  Py_TPFLAGS_DEFAULT,                 /* tp_flags */
  "A 2D Image",                       /* tp_doc */
  0,                                  /* tp_traverse */
  0,                                  /* tp_clear */
  0,                                  /* tp_richcompare */
  0,                                  /* tp_weaklistoffset */
  0,                                  /* tp_iter */
  0,                                  /* tp_iternext */
  ccircle_image_methods,              /* tp_methods */
  0,                                  /* tp_members */
  0,                                  /* tp_getset */
  0,                                  /* tp_base */
  0,                                  /* tp_dict */
  0,                                  /* tp_descr_get */
  0,                                  /* tp_descr_set */
  0,                                  /* tp_dictoffset */
  (initproc)ccircle_image_init,       /* tp_init */
  0,                                  /* tp_alloc */
  0,                                  /* tp_new */
};

/* -------------------------------------------------------------------------- */

void ccircle_init_image ( PyObject* self )
{
  ccircle_image_pytype.tp_new = PyType_GenericNew;
  if (PyType_Ready(&ccircle_image_pytype) < 0)
    Fatal("Failed to create image type");
  PyModule_AddObject(self, "Image", (PyObject*)&ccircle_image_pytype);
}
