#include "ccircle.h"

/* TODO : Free gl handle */

typedef struct {
  PyObject_HEAD
  uint handle;
  int sx, sy;
} CC_Image;

static int CC_Image_Init ( CC_Image* self, PyObject* args ) {
  if (!CC_GLContext_Exists())
    Fatal("A window must be created before images can be loaded");

  cstr path;
  if (!PyArg_ParseTuple(args, "s", &path))
    return -1;

  int channels;
  uchar* data = CC_Image_Load(path, &self->sx, &self->sy, &channels);
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
    self->sx, self->sy, 0,
    channels == 3 ? GL_RGB : GL_RGBA,
    GL_UNSIGNED_BYTE,
    data);

  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  CC_Image_Free(data);
  return 0;
}

static void CC_Image_Draw_With_UVs (
  CC_Image* self,
  float x, float y,
  float sx, float sy,
  float u1, float v1,
  float u2, float v2,
  float angle )
{
  glEnable(GL_TEXTURE_2D);
  glBindTexture(GL_TEXTURE_2D, self->handle);
  glColor4f(1, 1, 1, 1);

  glMatrixMode(GL_MODELVIEW);
  glPushMatrix();
  glLoadIdentity();
  glTranslatef(0.5f * sx + x, 0.5f * sy + y, 0);
  glRotatef(angle, 0, 0, -1);
  glTranslatef(-0.5f * sx, -0.5f * sy, 0);

  glBegin(GL_QUADS);
  glTexCoord2f(u1, v1); glVertex2f(0, 0);
  glTexCoord2f(u1, v2); glVertex2f(0, sy);
  glTexCoord2f(u2, v2); glVertex2f(sx, sy);
  glTexCoord2f(u2, v1); glVertex2f(sx, 0);
  glEnd();

  glPopMatrix();
  glDisable(GL_TEXTURE_2D);
}

/* --- Image.draw ----------------------------------------------------------- */

static PyObject* CC_Image_Draw ( CC_Image* self, PyObject* args ) {
  float x, y, sx, sy;
  float angle = 0.0f;
  if (!PyArg_ParseTuple(args, "ffff|f", &x, &y, &sx, &sy, &angle))
    return 0;

  CC_Image_Draw_With_UVs(self, x, y, sx, sy, 0.0f, 0.0f, 1.0f, 1.0f, angle);
  Py_RETURN_NONE;
}

/* --- Image.drawSub -------------------------------------------------------- */

static PyObject* CC_Image_DrawSub ( CC_Image* self, PyObject* args ) {
  float x, y, sx, sy;
  float subX, subY, subSX, subSY;
  float angle = 0.0f;
  if (!PyArg_ParseTuple(args, "ffffffff|f",
       &x, &y, &sx, &sy, &subX, &subY, &subSX, &subSY, &angle))
    return 0;

  float u1 = subX / self->sx;
  float v1 = subY / self->sy;
  float u2 = (subX + subSX) / self->sx;
  float v2 = (subY + subSY) / self->sy;
  CC_Image_Draw_With_UVs(self, x, y, sx, sy, u1, v1, u2, v2, angle);
  Py_RETURN_NONE;
}

/* --- Image.getSize -------------------------------------------------------- */

static PyObject* CC_Image_GetSize( CC_Image* self, PyObject* args ) {
  return Py_BuildValue("(ii)", self->sx, self->sy);
}

/* -------------------------------------------------------------------------- */

static PyMethodDef methods[] = {
  { "draw", (PyCFunction)CC_Image_Draw, METH_VARARGS, 0 },
  { "drawSub", (PyCFunction)CC_Image_DrawSub, METH_VARARGS, 0 },
  { "getSize", (PyCFunction)CC_Image_GetSize, METH_VARARGS, 0 },
  { 0 },
};

static PyTypeObject CC_Image_PyType = {
  PyVarObject_HEAD_INIT(0, 0)
  "ccircle.Image",
  sizeof(CC_Image),
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
  methods,                            /* tp_methods */
  0,                                  /* tp_members */
  0,                                  /* tp_getset */
  0,                                  /* tp_base */
  0,                                  /* tp_dict */
  0,                                  /* tp_descr_get */
  0,                                  /* tp_descr_set */
  0,                                  /* tp_dictoffset */
  (initproc)CC_Image_Init,            /* tp_init */
  0,                                  /* tp_alloc */
  0,                                  /* tp_new */
};

/* -------------------------------------------------------------------------- */

void CC_Init_Image ( PyObject* self ) {
  CC_Image_PyType.tp_new = PyType_GenericNew;
  if (PyType_Ready(&CC_Image_PyType) < 0) Fatal("Failed to create image type");
  Py_INCREF(self);
  PyModule_AddObject(self, "Image", (PyObject*)&CC_Image_PyType);
}
