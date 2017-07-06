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
} ccircle_font_t;

static int
ccircle_font_init ( ccircle_font_t* self, PyObject* args )
{
  cstr path = DEFAULT_FONT;
  if (!PyArg_ParseTuple(args, "|s", &path))
    return -1;

  if (FT_Init_FreeType(&self->ft))
    Fatal("Failed to initialize FreeType library");
  if (FT_New_Face(self->ft, path, 0, &self->face))
    Fatal("Failed to load font");
  return 0;
}

/* --- Font::draw ---------------------------------------------------------- */

/* TODO : Should take a window object and make sure the window's GL context is
 *        current. */

static PyObject*
ccircle_font_draw ( ccircle_font_t* self, PyObject* args )
{
  cstr text;
  float fx, fy;
  float fsize = DEFAULT_FONT_SIZE;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  
  if (!PyArg_ParseTuple(args, "sff|fffff", &text, &fx, &fy, &fsize, &r, &g, &b, &a))
    return 0;

  int x = (int)fx;
  int y = (int)fy;
  int size = (int)fsize;

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
        glColor4f(r, g, b, a * sqrt((float)(pBitmap[dx] / 255.0f)));
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

  Py_RETURN_NONE;
}

/* -------------------------------------------------------------------------- */

static PyMethodDef ccircle_font_methods[] = {
  { "draw", (PyCFunction)ccircle_font_draw, METH_VARARGS,
    "Draw the given string of text to the current window" },
  { 0 },
};


/* -------------------------------------------------------------------------- */

static PyTypeObject ccircle_font_pytype = {
  PyVarObject_HEAD_INIT(0, 0)
  "ccircle.Font",
  sizeof(ccircle_font_t),
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
  ccircle_font_methods,              /* tp_methods */
  0,                                  /* tp_members */
  0,                                  /* tp_getset */
  0,                                  /* tp_base */
  0,                                  /* tp_dict */
  0,                                  /* tp_descr_get */
  0,                                  /* tp_descr_set */
  0,                                  /* tp_dictoffset */
  (initproc)ccircle_font_init,       /* tp_init */
  0,                                  /* tp_alloc */
  0,                                  /* tp_new */
};

/* -------------------------------------------------------------------------- */

void ccircle_init_font ( PyObject* self )
{
  ccircle_font_pytype.tp_new = PyType_GenericNew;
  if (PyType_Ready(&ccircle_font_pytype) < 0)
    Fatal("Failed to create font type");
  PyModule_AddObject(self, "Font", (PyObject*)&ccircle_font_pytype);
}
