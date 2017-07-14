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

void CC_Init_Font   ( PyObject* );
void CC_Init_Image  ( PyObject* );
void CC_Init_Input  ( PyObject* );
void CC_Init_Sound  ( PyObject* );
void CC_Init_Window ( PyObject* );

bool   CC_GLContext_Exists ( void );
uchar* CC_Image_Load       ( cstr path, int* sx, int* sy, int* chan );
void   CC_Image_Free       ( uchar* );

void Fatal (cstr s);

#define Tau 6.28318531
#define Pi 3.14159265
#define Pi2 1.57079633f
#define Pi4 0.785398163f
#define Pi6 0.523598776f

#endif
