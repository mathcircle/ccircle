#ifndef CCC_h
#define CCC_h

#include <Python.h>
#include <stdbool.h>

typedef char const* cstr;
typedef unsigned char uchar;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;

void ccircle_init_window ( PyObject* m );

#endif
