#include "ccircle.h"
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

uchar* ccircle_image_load ( cstr path, int* sx, int* sy, int* chan )
{
  return stbi_load(path, sx, sy, chan, 0);
}

void ccircle_image_free ( uchar* data )
{
  stbi_image_free(data);
}
