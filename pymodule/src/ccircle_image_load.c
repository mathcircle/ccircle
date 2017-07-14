#include "ccircle.h"

#define STB_IMAGE_IMPLEMENTATION
#include <stb/stb_image.h>

uchar* CC_Image_Load ( cstr path, int* sx, int* sy, int* chan ) {
  return stbi_load(path, sx, sy, chan, 0);
}

void CC_Image_Free ( uchar* data ) {
  stbi_image_free(data);
}
