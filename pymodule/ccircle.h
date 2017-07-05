#ifndef CCircle_h
#define CCircle_h

#include <Python.h>
#include <windows.h>
#include <GL/gl.h>
#include <stdbool.h>

typedef char const* cstr;
typedef unsigned char uchar;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;

void ccircle_init_image  ( PyObject* );
void ccircle_init_input  ( PyObject* );
void ccircle_init_window ( PyObject* );

void Fatal (cstr s);

uchar* ccircle_image_load ( cstr path, int* sx, int* sy, int* chan );
void   ccircle_image_free ( uchar* );

#endif
