#ifndef CCircle_h
#define CCircle_h

#include <Python.h>
#include <stdbool.h>

typedef char const* cstr;
typedef unsigned char uchar;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;

void ccircle_init_input  ( PyObject* );
void ccircle_init_window ( PyObject* );

static void Fatal (cstr s) { }

#endif
