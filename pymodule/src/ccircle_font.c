#include "ccircle.h"

#include <ft2build.h>
#include FT_FREETYPE_H
#include FT_GLYPH_H
#include FT_BITMAP_H

#define DEFAULT_FONT "res/FiraMono.ttf"
#define DEFAULT_FONT_SIZE 10

/* TODO : Free font data */

typedef struct {
  PyObject_HEAD
  FT_Library ft;
  FT_Face face;
} CC_Font;

static int CC_Font_Init ( CC_Font* self, PyObject* args ) {
  cstr path = DEFAULT_FONT;
  if (!PyArg_ParseTuple(args, "|s", &path))
    return -1;

  if (FT_Init_FreeType(&self->ft))
    Fatal("Failed to initialize FreeType library");
  if (FT_New_Face(self->ft, path, 0, &self->face))
    Fatal("Failed to load font");
  return 0;
}

static void CC_Font_GetTextSize_Impl ( CC_Font* self, cstr text, int size, int* sx, int* sy ) {
  int minX = INT_MAX, minY = INT_MAX;
  int maxX = INT_MIN, maxY = INT_MIN;

  int x = 0, y = 0;

  FT_Set_Pixel_Sizes(self->face, 0, 2 * size);
  FT_GlyphSlot slot = self->face->glyph;
  for (cstr pText = text; *pText; ++pText) {
    if (FT_Load_Char(self->face, *pText, FT_LOAD_FORCE_AUTOHINT | FT_LOAD_RENDER)) continue;
    int ox = x + slot->bitmap_left;
    int oy = y - slot->bitmap_top;
    uchar const* pBitmap = slot->bitmap.buffer;
    for (uint dy = 0; dy < slot->bitmap.rows; ++dy) {
      for (uint dx = 0; dx < slot->bitmap.width; ++dx) {
        int drawX = ox + dx;
        int drawY = oy + dy;
        if (pBitmap[dx] > 0) {
          minX = min(minX, drawX);
          maxX = max(maxX, drawX + 1);
          minY = min(minY, drawY);
          maxY = max(maxY, drawY + 1);
        }
      }
      pBitmap += slot->bitmap.pitch;
    }
    x += slot->advance.x >> 6;
  }

  *sx = (maxX - minX + 1);
  *sy = (maxY - minY + 1);
}

static void CC_Font_Draw_Impl (
  CC_Font* self,
  cstr text,
  int x, int y, int size,
  float r, float g, float b, float a)
{
  if (!CC_GLContext_Exists())
    Fatal("A window must be created before text can be drawn");

  GL_CHECK;
  FT_Set_Pixel_Sizes(self->face, 0, 2 * size);
  FT_GlyphSlot slot = self->face->glyph;
  for (cstr pText = text; *pText; ++pText) {
    if (FT_Load_Char(self->face, *pText, FT_LOAD_FORCE_AUTOHINT | FT_LOAD_RENDER)) continue;
    int ox = x + slot->bitmap_left;
    int oy = y - slot->bitmap_top;
    uchar const* pBitmap = slot->bitmap.buffer;
    glBegin(GL_QUADS);
    for (uint dy = 0; dy < slot->bitmap.rows; ++dy) {
      for (uint dx = 0; dx < slot->bitmap.width; ++dx) {
        int drawX = ox + dx;
        int drawY = oy + dy;
        glColor4f(r, g, b, (float)(a * sqrt((float)(pBitmap[dx] / 255.0f))));
        glVertex2i(drawX + 0, drawY + 0);
        glVertex2i(drawX + 0, drawY + 1);
        glVertex2i(drawX + 1, drawY + 1);
        glVertex2i(drawX + 1, drawY + 0);
      }
      pBitmap += slot->bitmap.pitch;
    }
    glEnd();
    x += slot->advance.x >> 6;
  }
  GL_CHECK;
}

/* --- Font.draw ------------------------------------------------------------ */

static PyObject* CC_Font_Draw ( CC_Font* self, PyObject* args ) {
  cstr text;
  float fx, fy;
  float fsize = DEFAULT_FONT_SIZE;
  float r = 1.0f, g = 1.0f, b = 1.0f, a = 1.0f;
  if (!PyArg_ParseTuple(args, "sff|fffff", &text, &fx, &fy, &fsize, &r, &g, &b, &a))
    return 0;

  CC_Font_Draw_Impl(self, text, (int)fx, (int)fy, (int)fsize, r, g, b, a);
  Py_RETURN_NONE;
}

/* --- Font.drawCentered ---------------------------------------------------- */

static PyObject* CC_Font_DrawCentered ( CC_Font* self, PyObject* args ) {
  cstr text;
  float fx, fy;
  float fsize = DEFAULT_FONT_SIZE;
  float r = 1.0f, g = 1.0f, b = 1.0f, a = 1.0f;
  if (!PyArg_ParseTuple(args, "sff|fffff", &text, &fx, &fy, &fsize, &r, &g, &b, &a))
    return 0;

  int sx, sy;
  CC_Font_GetTextSize_Impl(self, text, (int)fsize, &sx, &sy);
  CC_Font_Draw_Impl(self, text, (int)fx - sx / 2, (int)fy + sy / 2, (int)fsize, r, g, b, a);
  Py_RETURN_NONE;
}


/* --- Font.getTextSize ----------------------------------------------------- */

static PyObject* CC_Font_GetTextSize ( CC_Font* self, PyObject* args ) {
  cstr text;
  float fsize = DEFAULT_FONT_SIZE;
  
  if (!PyArg_ParseTuple(args, "s|f", &text, &fsize))
    return 0;

  int sx, sy;
  CC_Font_GetTextSize_Impl(self, text, (int)fsize, &sx, &sy);
  return Py_BuildValue("(ii)", sx, sy);
}

/* -------------------------------------------------------------------------- */

static PyMethodDef methods[] = {
  { "draw", (PyCFunction)CC_Font_Draw, METH_VARARGS, 0 },
  { "drawCentered", (PyCFunction)CC_Font_DrawCentered, METH_VARARGS, 0 },
  { "getTextSize", (PyCFunction)CC_Font_GetTextSize, METH_VARARGS, 0 },
  { 0 },
};


/* -------------------------------------------------------------------------- */

static PyTypeObject CC_Font_PyType = {
  PyVarObject_HEAD_INIT(0, 0)
  "ccircle.Font",
  sizeof(CC_Font),
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
  "A Font for Drawing Text",          /* tp_doc */
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
  (initproc)CC_Font_Init,             /* tp_init */
  0,                                  /* tp_alloc */
  0,                                  /* tp_new */
};

/* -------------------------------------------------------------------------- */

void CC_Init_Font ( PyObject* self ) {
  CC_Font_PyType.tp_new = PyType_GenericNew;
  if (PyType_Ready(&CC_Font_PyType) < 0)
    Fatal("Failed to create font type");
  PyModule_AddObject(self, "Font", (PyObject*)&CC_Font_PyType);
}
