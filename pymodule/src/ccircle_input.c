#include "ccircle.h"

/* --- isKeyDown ------------------------------------------------------------ */

static bool gKeyState[256] = { 0 };
static bool gLastKeyState[256] = { 0 };

void CC_Keyboard_Update ( void ) {
  memcpy(gLastKeyState, gKeyState, sizeof(gKeyState));
}

void CC_SetKeyState ( int vk, bool down ) {
  gKeyState[vk] = down;
}

static int CC_GetKeyCode ( char* key ) {
  int len = strlen(key);
  if (len == 0)
    return 0;
  for (int i = 0; i < len; ++i)
    key[i] = tolower(key[i]);

  if (len == 1) {
    char c = key[0];
    switch (c) {
      case '0': return 0x30;
      case '1': return 0x31;
      case '2': return 0x32;
      case '3': return 0x33;
      case '4': return 0x34;
      case '5': return 0x35;
      case '6': return 0x36;
      case '7': return 0x37;
      case '8': return 0x38;
      case '9': return 0x39;

      case 'a': return 0x41;
      case 'b': return 0x42;
      case 'c': return 0x43;
      case 'd': return 0x44;
      case 'e': return 0x45;
      case 'f': return 0x46;
      case 'g': return 0x47;
      case 'h': return 0x48;
      case 'i': return 0x49;
      case 'j': return 0x4A;
      case 'k': return 0x4B;
      case 'l': return 0x4C;
      case 'm': return 0x4D;
      case 'n': return 0x4E;
      case 'o': return 0x4F;
      case 'p': return 0x50;
      case 'q': return 0x51;
      case 'r': return 0x52;
      case 's': return 0x53;
      case 't': return 0x54;
      case 'u': return 0x55;
      case 'v': return 0x56;
      case 'w': return 0x57;
      case 'x': return 0x58;
      case 'y': return 0x59;
      case 'z': return 0x5A;
    }
    return 0;
  }
  
  else if (strcmp(key, "backspace") == 0)   return 0x08;
  else if (strcmp(key, "tab") == 0)         return 0x09;
  else if (strcmp(key, "enter") == 0 ||
           strcmp(key, "return") == 0)      return 0x0D;
  else if (strcmp(key, "esc") == 0   ||
           strcmp(key, "escape") == 0)      return 0x1B;
  else if (strcmp(key, "space") == 0 ||
           strcmp(key, "spacebar") == 0)    return 0x20;
  else if (strcmp(key, "left") == 0)        return 0x25;
  else if (strcmp(key, "up") == 0)          return 0x26;
  else if (strcmp(key, "right") == 0)       return 0x27;
  else if (strcmp(key, "down") == 0)        return 0x28;

  return 0;
}

static PyObject* CC_KeyDown ( PyObject* self, PyObject* args ) {
  char* key;
  if (!PyArg_ParseTuple(args, "s", &key))
    return 0;
  int vk = CC_GetKeyCode(key);
  if (vk == 0)
    Fatal("ccircle.isKeyDown: Invalid key");

  return PyBool_FromLong(gKeyState[vk] ? 1 : 0);
}

static PyObject* CC_KeyPressed ( PyObject* self, PyObject* args ) {
  char* key;
  if (!PyArg_ParseTuple(args, "s", &key))
    return 0;
  int vk = CC_GetKeyCode(key);
  if (vk == 0)
    Fatal("ccircle.wasKeyPressed: Invalid key");

  return PyBool_FromLong((gKeyState[vk] && !gLastKeyState[vk]) ? 1 : 0);
}

static PyObject* CC_KeyReleased ( PyObject* self, PyObject* args ) {
  char* key;
  if (!PyArg_ParseTuple(args, "s", &key))
    return 0;
  int vk = CC_GetKeyCode(key);
  if (vk == 0)
    Fatal("ccircle.wasKeyReleased: Invalid key");

  return PyBool_FromLong((!gKeyState[vk] && gLastKeyState[vk]) ? 1 : 0);
}

/* --- isMouseDown ---------------------------------------------------------- */

static PyObject* CC_MouseDown ( PyObject* self, PyObject* args ) {
  char* button;
  int vk = -1;
  if (!PyArg_ParseTuple(args, "s", &button))
    return 0;

  int len = strlen(button);
  if (len == 0)
    return 0;
  for (int i = 0; i < len; ++i)
    button[i] = tolower(button[i]);

  if (false) {}
  else if (strcmp(button, "left") == 0)    vk = 0x01;
  else if (strcmp(button, "right") == 0)   vk = 0x02;
  else if (strcmp(button, "middle") == 0)  vk = 0x04;
  else if (strcmp(button, "x1") == 0)      vk = 0x05;
  else if (strcmp(button, "x2") == 0)      vk = 0x06;
  else
    return 0;

  return PyBool_FromLong(GetAsyncKeyState(vk));
}

/* -------------------------------------------------------------------------- */

static PyMethodDef functions[] = {
  { "isMouseDown",    (PyCFunction)CC_MouseDown,   METH_VARARGS, 0 },
  { "isKeyDown",      (PyCFunction)CC_KeyDown,     METH_VARARGS, 0 },
  { "wasKeyPressed",  (PyCFunction)CC_KeyPressed,  METH_VARARGS, 0 },
  { "wasKeyReleased", (PyCFunction)CC_KeyReleased, METH_VARARGS, 0 },
  { 0, 0, 0, 0 },
};

void CC_Init_Input ( PyObject* self ) {
  PyModule_AddFunctions(self, functions);
}
