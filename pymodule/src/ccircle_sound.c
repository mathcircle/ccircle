#include "ccircle.h"
#include <math.h>

#define SAMPLE_RATE 44100
 
/* TODO : Free sound data */

typedef struct {
  PyObject_HEAD
  int size;
  int capacity;
  float* samples;
  char* buffer;
} CC_Sound;

typedef struct {
  DWORD chunkID;
  DWORD chunkSize;
  DWORD format;

  DWORD subChunk1ID;
  DWORD subChunk1Size;
  WORD  audioFormat;
  WORD  channels;
  DWORD sampleRate;
  DWORD byteRate;
  WORD  blockAlign;
  WORD  bitsPerSample;

  DWORD subChunk2ID;
  DWORD subChunk2Size;
} WaveHeader;

typedef int16_t SampleType;
const int Sample_Max = ((1 << (8 * (int)sizeof(SampleType) - 1)) - 1);
const float fSampleRate = (float)SAMPLE_RATE;

/* -------------------------------------------------------------------------- */

/* Convert a float to SampleType. Input is clamped to [-1, 1]. */
inline SampleType FloatToSample (float x) {
  x *= Sample_Max;
  if (x >  Sample_Max) return  Sample_Max;
  if (x < -Sample_Max) return -Sample_Max;
  return (SampleType)x;
}

/* Convert a time value in seconds to a sample index using SAMPLE_RATE. */
inline static int SecToSample (float x) {
  return max(0, (int)(x * SAMPLE_RATE));
}

/* Double the capacity of the sound's sample buffer. */
static void CC_Sound_Grow ( CC_Sound* self ) {
  self->capacity *= 2;
  self->samples = realloc(self->samples, sizeof(float) * self->capacity);
}

/* Ensure that the sound contains at least minSamples. Any samples that must be
 * added to achieve the target will be initialized to 0. */
static void CC_Sound_Extend ( CC_Sound* self, int minSamples ) {
  if (self->size >= minSamples)
    return;
  while (self->capacity < minSamples)
    CC_Sound_Grow(self);
  memset(self->samples + self->size, 0, sizeof(float) * (minSamples - self->size));
  self->size = minSamples;
}

/* -------------------------------------------------------------------------- */

static int CC_Sound_Init ( CC_Sound* self, PyObject* args ) {
  self->size = 0;
  self->capacity = SAMPLE_RATE;
  self->samples = malloc(sizeof(float) * self->capacity);
  self->buffer = 0;
  return 0;
}

/* --- Sound.addSample ------------------------------------------------------ */

static PyObject* CC_Sound_AddSample ( CC_Sound* self, PyObject* args ) {
  float sample;
  if (!PyArg_ParseTuple(args, "f", &sample))
    return 0;
  if (self->size == self->capacity)
    CC_Sound_Grow(self);
  self->samples[self->size++] = sample;
  Py_RETURN_NONE;
}

/* --- Sound.addSaw --------------------------------------------------------- */

static PyObject* CC_Sound_AddSaw ( CC_Sound* self, PyObject* args) {
  float start, duration, freq, amp;
  if (!PyArg_ParseTuple(args, "ffff", &start, &duration, &freq, &amp))
    return 0;
  if (start < 0.0f || duration <= 0.0f)
    return 0;

  int startSample = SecToSample(start);
  int durationSamples = SecToSample(duration);
  CC_Sound_Extend(self, startSample + durationSamples - 1);

  float* pSamples = self->samples + startSample;
  for (int i = 0; i < durationSamples; ++i) {
    float t = (float)i / fSampleRate;
    *(pSamples++) += amp * (2.0f * fmod(t * freq, 1.0) - 1.0f);
  }

  Py_RETURN_NONE;
}

/* --- Sound.addSine -------------------------------------------------------- */

static PyObject* CC_Sound_AddSine ( CC_Sound* self, PyObject* args) {
  float start, duration, freq, amp;
  if (!PyArg_ParseTuple(args, "ffff", &start, &duration, &freq, &amp))
    return 0;
  if (start < 0.0f || duration <= 0.0f)
    return 0;

  int startSample = SecToSample(start);
  int durationSamples = SecToSample(duration);
  CC_Sound_Extend(self, startSample + durationSamples - 1);

  freq *= Tau;
  float* pSamples = self->samples + startSample;
  for (int i = 0; i < durationSamples; ++i) {
    float t = (float)i / fSampleRate;
    *(pSamples++) += amp * sin(freq * t);
  }

  Py_RETURN_NONE;
}

/* --- Sound.getSample ------------------------------------------------------ */

static PyObject* CC_Sound_GetSample ( CC_Sound* self, PyObject* args) {
  int index;
  if (!PyArg_ParseTuple(args, "i", &index))
    return 0;
  if (index >= self->size)
    return 0;
  return PyFloat_FromDouble(self->samples[index]);
}

/* --- Sound.play ----------------------------------------------------------- */

static PyObject* CC_Sound_Play ( CC_Sound* self, PyObject* args ) {
  if (!self->buffer) {
    self->buffer = malloc(sizeof(WaveHeader) + self->size * sizeof(SampleType));

    float* pNative = self->samples;
    SampleType* pConverted = (SampleType*)(self->buffer + sizeof(WaveHeader));
    for (int i = 0; i < self->size; ++i)
      *(pConverted++) = FloatToSample(*pNative++);

    WaveHeader* wav    = (WaveHeader*)self->buffer;
    wav->chunkID       = 0x46464952;
    wav->format        = 0x45564157;
    wav->subChunk1ID   = 0x20746d66;
    wav->subChunk1Size = 16;
    wav->audioFormat   = 1;
    wav->channels      = 1;
    wav->sampleRate    = SAMPLE_RATE;
    wav->bitsPerSample = 8 * sizeof(SampleType);
    wav->byteRate      = wav->sampleRate * wav->channels * (wav->bitsPerSample / 8);
    wav->blockAlign    = wav->channels * (wav->bitsPerSample / 8);
    wav->subChunk2ID   = 0x61746164;
    wav->subChunk2Size = self->size * wav->blockAlign;
    wav->chunkSize     = 4 + (8 + wav->subChunk1Size) + (8 + wav->subChunk2Size);
  }

  PlaySound(self->buffer, 0, SND_MEMORY | SND_ASYNC);
  Py_RETURN_NONE;
}

/* -------------------------------------------------------------------------- */

static PyMethodDef methods[] = {
  { "addSample", (PyCFunction)CC_Sound_AddSample, METH_VARARGS, 0 },
  { "addSaw", (PyCFunction)CC_Sound_AddSaw, METH_VARARGS, 0 },
  { "addSine", (PyCFunction)CC_Sound_AddSine, METH_VARARGS, 0 },
  { "getSample", (PyCFunction)CC_Sound_GetSample, METH_VARARGS, 0 },
  { "play", (PyCFunction)CC_Sound_Play, METH_VARARGS, 0 },
  { 0 },
};

static PyTypeObject CC_Sound_PyType = {
  PyVarObject_HEAD_INIT(0, 0)
  "ccircle.Sound",
  sizeof(CC_Sound),
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
  "A Sound",                          /* tp_doc */
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
  (initproc)CC_Sound_Init,            /* tp_init */
  0,                                  /* tp_alloc */
  0,                                  /* tp_new */
};

/* -------------------------------------------------------------------------- */

void CC_Init_Sound ( PyObject* self ) {
  CC_Sound_PyType.tp_new = PyType_GenericNew;
  if (PyType_Ready(&CC_Sound_PyType) < 0) Fatal("Failed to create sound type");
  Py_INCREF(self);
  PyModule_AddObject(self, "Sound", (PyObject*)&CC_Sound_PyType);
}
