#include "ccircle.h"
#include <structmember.h>

typedef struct {
  float r, g, b, a;
} RGBA;

typedef struct {
  PyObject_HEAD
  uint handle;
  int sx, sy;
  RGBA* data;
} CC_Image;

static void CC_Image_Dealloc( CC_Image* self ) {
  glDeleteTextures(1, &self->handle);
  free(self->data);
  self->data = 0;
  Py_TYPE(self)->tp_free((PyObject*)self);
}

static int CC_Image_Init ( CC_Image* self, PyObject* args ) {
  if (!CC_GLContext_Exists())
    Fatal("Image.__init__: A window must be created before images can be loaded");

  cstr path;
  if (!PyArg_ParseTuple(args, "s", &path))
    return -1;

  FILE* file = fopen(path, "r");
  if (!file)
    Fatal("Image.__init__: Failed to load image (file does not exist)");
  fclose(file);

  int channels;
  uchar* data = CC_Image_Load(path, &self->sx, &self->sy, &channels);
  if (!data)
    Fatal("Image.__init__: Failed to load image (unsupported image format)");

  if (channels != 3 && channels != 4)
    Fatal("Image.__init__: Failed to load image (unsupported channel format -- only 3 or 4 channels supported)");

  GL_CHECK;
  glGenTextures(1, &self->handle);
  glBindTexture(GL_TEXTURE_2D, self->handle);
  glPixelStorei(GL_PACK_ALIGNMENT, 1);
  glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
  glTexImage2D(GL_TEXTURE_2D,
    0,
    GL_RGBA8,
    self->sx,
    self->sy,
    0,
    channels == 3 ? GL_RGB : GL_RGBA,
    GL_UNSIGNED_BYTE,
    data);

  self->data = malloc(self->sx * self->sy * sizeof(RGBA));
  glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT, self->data);

  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  GL_CHECK;
  CC_Image_Free(data);
  return 0;
}

static void CC_Image_Draw_With_UVs (
  CC_Image* self,
  float x, float y,
  float sx, float sy,
  float u1, float v1,
  float u2, float v2,
  float angle,
  float r, float g, float b, float a)
{
  GL_CHECK;
  glEnable(GL_TEXTURE_2D);
  glBindTexture(GL_TEXTURE_2D, self->handle);
  glColor4f(r, g, b, a);

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
  GL_CHECK;
}

static void CC_Image_Upload ( CC_Image* self ) {
  glBindTexture(GL_TEXTURE_2D, self->handle);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self->sx, self->sy, 0, GL_RGBA, GL_FLOAT, self->data);
  glBindTexture(GL_TEXTURE_2D, 0);
}

static void CC_Image_Color_To_Alpha ( CC_Image* self, float r, float g, float b ) {
  RGBA* pData = self->data;
  int size = self->sx * self->sy;
  for (int i = 0; i < size; ++i) {
    if (pData->r == r && pData->g == g && pData->b == b)
      pData->a = 0;
    pData++;
  }
  CC_Image_Upload(self);
}

/* --- Image.draw ----------------------------------------------------------- */

static PyObject* CC_Image_Draw ( CC_Image* self, PyObject* args ) {
  float x, y, sx, sy;
  float angle = 0.0f;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  if (!PyArg_ParseTuple(args, "ffff|fffff", &x, &y, &sx, &sy, &angle, &r, &g, &b, &a))
    return 0;

  CC_Image_Draw_With_UVs(self, x, y, sx, sy, 0.0f, 0.0f, 1.0f, 1.0f, angle, r, g, b, a);
  Py_RETURN_NONE;
}

/* --- Image.drawSub -------------------------------------------------------- */

static PyObject* CC_Image_DrawSub ( CC_Image* self, PyObject* args ) {
  float x, y, sx, sy;
  float subX, subY, subSX, subSY;
  float angle = 0.0f;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  if (!PyArg_ParseTuple(args, "ffffffff|fffff",
       &x, &y, &sx, &sy, &subX, &subY, &subSX, &subSY, &angle, &r, &g, &b, &a))
    return 0;

  float u1 = subX / self->sx;
  float v1 = subY / self->sy;
  float u2 = (subX + subSX) / self->sx;
  float v2 = (subY + subSY) / self->sy;
  CC_Image_Draw_With_UVs(self, x, y, sx, sy, u1, v1, u2, v2, angle, r, g, b, a);
  Py_RETURN_NONE;
}

/* --- Image.eraseRed ------------------------------------------------------- */

static PyObject* CC_Image_EraseRed ( CC_Image* self, PyObject* args ) {
  CC_Image_Color_To_Alpha(self, 1, 0, 0);
  Py_RETURN_NONE;
}

static PyObject* CC_Image_EraseGreen ( CC_Image* self, PyObject* args ) {
  CC_Image_Color_To_Alpha(self, 0, 1, 0);
  Py_RETURN_NONE;
}

static PyObject* CC_Image_EraseBlue ( CC_Image* self, PyObject* args ) {
  CC_Image_Color_To_Alpha(self, 0, 0, 1);
  Py_RETURN_NONE;
}

static PyObject* CC_Image_EraseWhite ( CC_Image* self, PyObject* args ) {
  CC_Image_Color_To_Alpha(self, 1, 1, 1);
  Py_RETURN_NONE;
}

/* --- Image.getPixel ------------------------------------------------------- */

static PyObject* CC_Image_GetPixel( CC_Image* self, PyObject* args) {
  int x, y;
  if (!PyArg_ParseTuple(args, "ii", &x, &y))
    return 0;
  if (x < 0 || y < 0 || x >= self->sx || y >= self->sy)
    Fatal("Image.getPixel: Pixel coordinates are out-of-bounds");

  RGBA* c = self->data + self->sx * y + x;
  return Py_BuildValue("(ffff)", c->r, c->g, c->b, c->a);
}

/* --- Image.getSize -------------------------------------------------------- */

static PyObject* CC_Image_GetSize( CC_Image* self, PyObject* args ) {
  return Py_BuildValue("(ii)", self->sx, self->sy);
}

/* --- Image.recolor -------------------------------------------------------- */

static PyObject* CC_Image_Recolor( CC_Image* self, PyObject* args ) {
  float r0, r1;
  float g0, g1;
  float b0, b1;
  float tolerance = 1.0f / 128.0f;
  if (!PyArg_ParseTuple(args, "ffffff|f", &r0, &g0, &b0, &r1, &g1, &b1, &tolerance))
    return 0;

  RGBA* pData = self->data;
  int size = self->sx * self->sy;
  for (int i = 0; i < size; ++i) {
    float dr = (float)fabs(pData->r - r0);
    float dg = (float)fabs(pData->g - g0);
    float db = (float)fabs(pData->b - b0);
    float dMax = max(dr, max(dg, db));
    if (dMax <= tolerance) {
      pData->r = r1;
      pData->g = g1;
      pData->b = b1;
    }
    pData++;
  }

  CC_Image_Upload(self);
  Py_RETURN_NONE;
}

/* -------------------------------------------------------------------------- */

static PyMemberDef members[] = {
    { "width", T_INT, offsetof(CC_Image, sx), 0, "image width in pixels" },
    { "height", T_INT, offsetof(CC_Image, sy), 0, "image height in pixels" },
    { 0 },
};

static PyMethodDef methods[] = {
  { "draw", (PyCFunction)CC_Image_Draw, METH_VARARGS, 0 },
  { "drawSub", (PyCFunction)CC_Image_DrawSub, METH_VARARGS, 0 },
  { "eraseRed", (PyCFunction)CC_Image_EraseRed, METH_VARARGS, 0 },
  { "eraseGreen", (PyCFunction)CC_Image_EraseGreen, METH_VARARGS, 0 },
  { "eraseBlue", (PyCFunction)CC_Image_EraseBlue, METH_VARARGS, 0 },
  { "eraseWhite", (PyCFunction)CC_Image_EraseWhite, METH_VARARGS, 0 },
  { "getPixel", (PyCFunction)CC_Image_GetPixel, METH_VARARGS, 0 },
  { "getSize", (PyCFunction)CC_Image_GetSize, METH_VARARGS, 0 },
  { "recolor", (PyCFunction)CC_Image_Recolor, METH_VARARGS, 0 },
  { 0 },
};

static PyTypeObject CC_Image_PyType = {
  PyVarObject_HEAD_INIT(0, 0)
  "ccircle.Image",
  sizeof(CC_Image),
  0,                                  /* tp_itemsize */
  (destructor)CC_Image_Dealloc,       /* tp_dealloc */
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
  members,                            /* tp_members */
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
