#include "ccircle.h"

typedef struct {
  PyObject_HEAD
  HWND hwnd;
  HGLRC hglc;
  bool quit;
} CC_Window;

static CC_Window* gWindowActive = 0;
static bool gCreatedContext = 0;

LRESULT CALLBACK CC_Window_Proc ( HWND self, UINT msg, WPARAM wp, LPARAM lp ) {
  switch(msg) {
    case WM_CLOSE:
      DestroyWindow(self);
      break;

    case WM_DESTROY: {
      PostQuitMessage(0);
      break;
    }

    case WM_KEYDOWN:
      if (wp == VK_ESCAPE) {
        DestroyWindow(self);
        break;
      }
      return DefWindowProc(self, msg, wp, lp);

    default:
     return DefWindowProc(self, msg, wp, lp);
  }
  return 0;
}

static int CC_Window_Init ( CC_Window* self, PyObject* args, PyObject* kwds ) {
  cstr title = "CC Window";
  int x = CW_USEDEFAULT;
  int y = CW_USEDEFAULT;
  uint sx = 640;
  uint sy = 480;

  if (!PyArg_ParseTuple(args, "|siiii", &title, &sx, &sy, &x, &y))
    return -1;

  HINSTANCE hinst = GetModuleHandle(0);
  static bool firstTime = true;
  /* Register window class. */
  if (firstTime) {
    firstTime = false;
    WNDCLASSEX wc = { 0 };
    wc.cbSize        = sizeof(WNDCLASSEX);
    wc.style         = CS_HREDRAW | CS_VREDRAW | CS_OWNDC;
    wc.lpfnWndProc   = (WNDPROC)CC_Window_Proc;
    wc.hInstance     = hinst;
    wc.hIcon         = LoadIcon(0, IDI_WINLOGO);
    wc.hCursor       = LoadCursor(0, IDC_ARROW);
    wc.lpszClassName = "CCircleWindow";
    wc.hIconSm       = LoadIcon(0, IDI_APPLICATION);

    if (!RegisterClassEx(&wc)) {
      Fatal("Failed to register window class");
      return -1;
    }
  }

  HWND hwnd = 0;
  /* Create window. */ {
    hwnd = CreateWindowEx(
      WS_EX_APPWINDOW | WS_EX_WINDOWEDGE,
      "CCircleWindow",
      title,
      WS_OVERLAPPEDWINDOW | WS_CLIPSIBLINGS | WS_CLIPCHILDREN,
      x, y,
      sx, sy,
      0, 0, hinst, 0);

    if (!hwnd) {
      Fatal("Failed to create window");
      return -1;
    }
  }

  /* Set pixel format to make window GL-compatible. */ {
    PIXELFORMATDESCRIPTOR pfd = {
      sizeof(PIXELFORMATDESCRIPTOR),
      1,
      PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER,
      PFD_TYPE_RGBA,
      24,
      0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0,
      32,
      0,
      0,
      PFD_MAIN_PLANE,
      0, 0, 0, 0,
    };

    HDC dc = GetDC(hwnd);
    int iPF = ChoosePixelFormat(dc, &pfd);
    if (!SetPixelFormat(dc, iPF, &pfd))
      Fatal("Failed to set window pixel format");
    ReleaseDC(hwnd, dc);
  }

  HGLRC hglc = 0;
  /* Create GL Context. */ {
    HDC dc = GetDC(hwnd);
    hglc = wglCreateContext(dc);
    if (!hglc)
      Fatal("Failed to create WGL context");
    if (!wglMakeCurrent(dc, hglc))
      Fatal("Failed to make WGL context current");
    gCreatedContext = true;
    ReleaseDC(hwnd, dc);
  }

  ShowWindow(hwnd, SW_SHOW);
  UpdateWindow(hwnd);

  glEnable(GL_POINT_SMOOTH);
  glEnable(GL_LINE_SMOOTH);
  glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
  glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
  glPointSize(2.0);
  glLineWidth(1.0);

  self->hwnd = hwnd;
  self->hglc = hglc;
  self->quit = false;
  return 0;
}

bool CC_GLContext_Exists ( void ) {
  return gCreatedContext;
}

static void CC_Window_SetViewport ( CC_Window* self ) {
  RECT vp;
  GetClientRect(self->hwnd, &vp);
  glViewport(vp.left, vp.top, vp.right - vp.left, vp.bottom - vp.top);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glTranslated(-1.0, 1.0, 0.0);
  glScaled(2.0 / (vp.right - vp.left), -2.0 / (vp.bottom - vp.top), 1.0);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
}

static void CC_Window_SetActive ( CC_Window* self ) {
  if (self != gWindowActive) {
    gWindowActive = self;
    HDC dc = GetDC(self->hwnd);
    wglMakeCurrent(dc, self->hglc);
    ReleaseDC(self->hwnd, dc);
    CC_Window_SetViewport(self);
  }
}

/* --- Window::clear -------------------------------------------------------- */

static PyObject* CC_Window_Clear ( CC_Window* self, PyObject* args ) {
  float r, g, b;
  if (!PyArg_ParseTuple(args, "fff", &r, &g, &b))
    return 0;

  CC_Window_SetActive(self);
  CC_Window_SetViewport(self);
  glClearColor(r, g, b, 1);
  glClear(GL_COLOR_BUFFER_BIT);
  Py_RETURN_NONE;
}

/* --- Window::drawCircle --------------------------------------------------- */

static PyObject* CC_Window_DrawCircle ( CC_Window* self, PyObject* args ) {
  float x, y, radius;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  if (!PyArg_ParseTuple(args, "fff|ffff", &x, &y, &radius, &r, &g, &b, &a))
    return 0;

  float fv = radius / 4.0f;
  fv = max(fv, 16.0f);
  fv = min(fv, 64.0f);
  int verts = (int)fv;
  fv = (float)verts;

  glBegin(GL_TRIANGLES);
  glColor4f(r, g, b, a);
  for (int i = 0; i < verts; ++i) {
    float angle1 = Tau * (float)(i + 0) / fv;
    float angle2 = Tau * (float)(i + 1) / fv;
    glVertex2f(x, y);
    glVertex2f(x + radius * cos(angle1), y + radius * sin(angle1));
    glVertex2f(x + radius * cos(angle2), y + radius * sin(angle2));
  }
  glEnd();
  Py_RETURN_NONE;
}

/* --- Window::drawLine ----------------------------------------------------- */

static PyObject* CC_Window_DrawLine ( CC_Window* self, PyObject* args ) {
  float x1, y1, x2, y2;
  float w = 2.0f;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  if (!PyArg_ParseTuple(args, "ffff|fffff", &x1, &y1, &x2, &y2, &w, &r, &g, &b, &a))
    return 0;

  CC_Window_SetActive(self);
  glLineWidth(w);
  glColor4f(r, g, b, a);
  glBegin(GL_LINES);
  glVertex2f(x1, y1);
  glVertex2f(x2, y2);
  glEnd();
  Py_RETURN_NONE;
}

/* --- Window::drawPoint ---------------------------------------------------- */

static PyObject* CC_Window_DrawPoint ( CC_Window* self, PyObject* args ) {
  float x, y;
  float s = 2.0f;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  if (!PyArg_ParseTuple(args, "ff|fffff", &x, &y, &s, &r, &g, &b, &a))
    return 0;

  CC_Window_SetActive(self);
  glPointSize(s);
  glColor4f(r, g, b, a);
  glBegin(GL_POINTS);
  glVertex2f(x, y);
  glEnd();
  Py_RETURN_NONE;
}

/* --- Window::drawRect ----------------------------------------------------- */

static PyObject* CC_Window_DrawRect ( CC_Window* self, PyObject* args ) {
  float x, y, sx, sy;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  if (!PyArg_ParseTuple(args, "ffff|ffff", &x, &y, &sx, &sy, &r, &g, &b, &a))
    return 0;

  CC_Window_SetActive(self);
  glColor4f(r, g, b, a);
  glBegin(GL_QUADS);
  glVertex2f(x, y);
  glVertex2f(x + sx, y);
  glVertex2f(x + sx, y + sy);
  glVertex2f(x, y + sy);
  glEnd();
  Py_RETURN_NONE;
}

/* --- Window::drawTri ------------------------------------------------------ */

static PyObject* CC_Window_DrawTri ( CC_Window* self, PyObject* args ) {
  float x1, y1;
  float x2, y2;
  float x3, y3;
  float r = 1.0f;
  float g = 1.0f;
  float b = 1.0f;
  float a = 1.0f;
  if (!PyArg_ParseTuple(args, "ffffff|ffff", &x1, &y1, &x2, &y2, &x3, &y3, &r, &g, &b, &a))
    return 0;

  CC_Window_SetActive(self);
  glColor4f(r, g, b, a);
  glBegin(GL_TRIANGLES);
  glVertex2f(x1, y1);
  glVertex2f(x2, y2);
  glVertex2f(x3, y3);
  glEnd();
  Py_RETURN_NONE;
}

/* --- Window::getMousePos -------------------------------------------------- */

static PyObject* CC_Window_GetMousePos ( CC_Window* self, PyObject* args ) {
  if (!self) return 0;
  POINT p;
  GetCursorPos(&p);
  ScreenToClient(self->hwnd, &p);
  return Py_BuildValue("(ii)", p.x, p.y);
}

/* --- Window::getSize ------------------------------------------------------ */

static PyObject* CC_Window_GetSize ( CC_Window* self, PyObject* args ) {
  if (!self) return 0;
  RECT rect;
  GetClientRect(self->hwnd, &rect);
  return Py_BuildValue("(ii)", rect.right - rect.left, rect.bottom - rect.top);
}

/* --- Window::hideMouse ---------------------------------------------------- */

static PyObject* CC_Window_HideMouse ( CC_Window* self, PyObject* args ) {
  if (!self) return 0;
  while (ShowCursor(false) > 0) {}
  Py_RETURN_NONE;
}

/* --- Window::isOpen ------------------------------------------------------- */

static PyObject* CC_Window_IsOpen ( CC_Window* self, PyObject* args ) {
  return PyBool_FromLong(self->quit ? 0L : 1L);
}

/* --- Window::setSize ------------------------------------------------------ */

static PyObject* CC_Window_SetSize ( CC_Window* self, PyObject* args ) {
  int sx, sy;
  if (!PyArg_ParseTuple(args, "ii", &sx, &sy))
    return 0;
  SetWindowPos(self->hwnd, 0, 0, 0, sx, sy, SWP_NOMOVE);
  Py_RETURN_NONE;
}

/* --- Window::showMouse ---------------------------------------------------- */

static PyObject* CC_Window_ShowMouse ( CC_Window* self, PyObject* args ) {
  if (!self) return 0;
  while (ShowCursor(true) <= 0) {}
  Py_RETURN_NONE;
}

/* --- Window::toggleMaximized ---------------------------------------------- */

static PyObject* CC_Window_ToggleMaximized ( CC_Window* self, PyObject* args ) {
  if (!self) return 0;
  WINDOWPLACEMENT wndpl;
  GetWindowPlacement(self->hwnd, &wndpl);
  if (wndpl.showCmd == SW_MAXIMIZE)
    ShowWindow(self->hwnd, SW_RESTORE);
  else
    ShowWindow(self->hwnd, SW_MAXIMIZE);
  Py_RETURN_NONE;
}

/* --- Window::update ------------------------------------------------------- */

static PyObject* CC_Window_Update ( CC_Window* self, PyObject* args ) {
  MSG msg;
  while (PeekMessage(&msg, 0, 0, 0, PM_REMOVE)) {
    if (msg.message == WM_QUIT) {
      self->quit = true;
      wglDeleteContext(self->hglc);
      Py_RETURN_NONE;
    } else {
      TranslateMessage(&msg);
      DispatchMessage(&msg);
    }
  }

  HDC dc = GetDC(self->hwnd);
  wglMakeCurrent(dc, self->hglc);
  SwapBuffers(dc);
  glClearColor(0.1, 0.1, 0.1, 1);
  glClear(GL_COLOR_BUFFER_BIT);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  ReleaseDC(self->hwnd, dc);

  Py_RETURN_NONE;
}

/* -------------------------------------------------------------------------- */

static PyMethodDef methods[] = {
  { "clear", (PyCFunction)CC_Window_Clear, METH_VARARGS, "Clear the entire window with the given color" },
  { "drawCircle", (PyCFunction)CC_Window_DrawCircle, METH_VARARGS, "Draw a circle in the window" },
  { "drawLine", (PyCFunction)CC_Window_DrawLine, METH_VARARGS, "Draw a line in the window" },
  { "drawPoint", (PyCFunction)CC_Window_DrawPoint, METH_VARARGS, "Draw a point in the window" },
  { "drawRect", (PyCFunction)CC_Window_DrawRect, METH_VARARGS, "Draw a rectangle in the window" },
  { "drawTri", (PyCFunction)CC_Window_DrawTri, METH_VARARGS, "Draw a triangle in the window" },
  { "getMousePos", (PyCFunction)CC_Window_GetMousePos, METH_NOARGS, "Get the position of the mouse cursor relative to the window" },
  { "getSize", (PyCFunction)CC_Window_GetSize, METH_NOARGS, "Get the size of window's drawable region" },
  { "hideMouse", (PyCFunction)CC_Window_HideMouse, METH_NOARGS, "Make the mouse cursor invisible inside the window" },
  { "isOpen", (PyCFunction)CC_Window_IsOpen, METH_NOARGS, "Return whether or not the window is still open" },
  { "setSize", (PyCFunction)CC_Window_SetSize, METH_VARARGS, "Set the size of the window" },
  { "showMouse", (PyCFunction)CC_Window_ShowMouse, METH_NOARGS, "Make the mouse cursor visible inside the window" },
  { "toggleMaximized", (PyCFunction)CC_Window_ToggleMaximized, METH_NOARGS, "Toggle the window's maximized state" },
  { "update", (PyCFunction)CC_Window_Update, METH_NOARGS, "Update the window, causing drawn elements to be shown" },
  { 0 },
};

static PyTypeObject CC_Window_PyType = {
  PyVarObject_HEAD_INIT(0, 0)
  "ccircle.Window",
  sizeof(CC_Window),
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
  "A Window",                         /* tp_doc */
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
  (initproc)CC_Window_Init,           /* tp_init */
  0,                                  /* tp_alloc */
  0,                                  /* tp_new */
};

/* -------------------------------------------------------------------------- */

void CC_Init_Window ( PyObject* self ) {
  CC_Window_PyType.tp_new = PyType_GenericNew;
  if (PyType_Ready(&CC_Window_PyType) < 0) Fatal("Failed to create Window type");
  Py_INCREF(self);
  PyModule_AddObject(self, "Window", (PyObject*)&CC_Window_PyType);
}
