#include "ccircle.h"

/* --- isKeyDown ------------------------------------------------------------ */

static PyObject*
ccircle_keydown ( PyObject* self, PyObject* args )
{
  char* key;
  int vk = -1;
  if (!PyArg_ParseTuple(args, "s", &key))
    return 0;

  int len = strlen(key);
  if (len == 0)
    return 0;
  for (int i = 0; i < len; ++i)
    key[i] = tolower(key[i]);

  if (len == 1) {
    char c = key[0];
    switch (c) {
      case 'a': vk = 0x41; break;
      case 'b': vk = 0x42; break;
      case 'c': vk = 0x43; break;
      case 'd': vk = 0x44; break;
      case 'e': vk = 0x45; break;
      case 'f': vk = 0x46; break;
      case 'g': vk = 0x47; break;
      case 'h': vk = 0x48; break;
      case 'i': vk = 0x49; break;
      case 'j': vk = 0x4A; break;
      case 'k': vk = 0x4B; break;
      case 'l': vk = 0x4C; break;
      case 'm': vk = 0x4D; break;
      case 'n': vk = 0x4E; break;
      case 'o': vk = 0x4F; break;
      case 'p': vk = 0x50; break;
      case 'q': vk = 0x51; break;
      case 'r': vk = 0x52; break;
      case 's': vk = 0x53; break;
      case 't': vk = 0x54; break;
      case 'u': vk = 0x55; break;
      case 'v': vk = 0x56; break;
      case 'w': vk = 0x57; break;
      case 'x': vk = 0x58; break;
      case 'y': vk = 0x59; break;
      case 'z': vk = 0x5A; break;
      default:
        return 0;
    }
  }
  
  else if (strcmp(key, "backspace") == 0)   vk = 0x08;
  else if (strcmp(key, "tab") == 0)         vk = 0x09;
  else if (strcmp(key, "enter") == 0 ||
           strcmp(key, "return") == 0)      vk = 0x0D;
  else if (strcmp(key, "esc") == 0   ||
           strcmp(key, "escape") == 0)      vk = 0x1B;
  else if (strcmp(key, "space") == 0 ||
           strcmp(key, "spacebar") == 0)    vk = 0x20;
  else if (strcmp(key, "left") == 0)        vk = 0x25;
  else if (strcmp(key, "up") == 0)          vk = 0x26;
  else if (strcmp(key, "right") == 0)       vk = 0x27;
  else if (strcmp(key, "down") == 0)        vk = 0x28;
  else
    return 0;

  return PyBool_FromLong(GetAsyncKeyState(vk));
}

/* --- isMouseDown ---------------------------------------------------------- */

static PyObject*
ccircle_mousedown ( PyObject* self, PyObject* args )
{
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
  { "isMouseDown", (PyCFunction)ccircle_mousedown, METH_VARARGS,
    "Return whether or not the given mouse button is down" },
  { "isKeyDown",   (PyCFunction)ccircle_keydown,   METH_VARARGS,
    "Return whether or not the given key is down" },
  { 0, 0, 0, 0 },
};

void ccircle_init_input ( PyObject* self )
{
  PyModule_AddFunctions(self, functions);
}
