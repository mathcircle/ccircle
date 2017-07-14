#include "ccircle.h"
#include <math.h>

#define SAMPLE_RATE 44100

/* TODO : Free sound data */

typedef struct {
  DWORD chunkID;       // 0x46464952 "RIFF" in little endian
  DWORD chunkSize;     // 4 + (8 + subChunk1Size) + (8 + subChunk2Size)
  DWORD format;        // 0x45564157 "WAVE" in little endian

  DWORD subChunk1ID;   // 0x20746d66 "fmt " in little endian
  DWORD subChunk1Size; // 16 for PCM
  WORD  audioFormat;   // 1 for PCM, 3 fot EEE floating point , 7 for μ-law
  WORD  channels;      // 1 for mono, 2 for stereo
  DWORD sampleRate;    // 8000, 22050, 44100, etc...
  DWORD byteRate;      // sampleRate * channels * bitsPerSample/8
  WORD  blockAlign;    // channels * bitsPerSample/8
  WORD  bitsPerSample; // number of bits (8 for 8 bits, etc...)

  DWORD subChunk2ID;   // 0x61746164 "data" in little endian
  DWORD subChunk2Size; // numSamples * channels * bitsPerSample/8 (this is the actual data size in bytes)
} WaveHeader;

typedef struct {
  PyObject_HEAD
  int size;
  int capacity;
  char* data;
} CC_Sound;

typedef int16_t SampleType;
const int Sample_Max = ((1 << (8 * (int)sizeof(SampleType) - 1)) - 1);

inline SampleType FloatToSample (float x) {
  x *= Sample_Max;
  if (x >  Sample_Max) return  Sample_Max;
  if (x < -Sample_Max) return -Sample_Max;
  return (SampleType)x;
}

inline static int SecToSample (float x) {
  return max(0, (int)(x * SAMPLE_RATE));
}

inline static SampleType* CC_Sound_GetSampleData ( CC_Sound* self ) {
  return (SampleType*)(self->data + sizeof(WaveHeader));
}

static void CC_Sound_Grow ( CC_Sound* self ) {
  self->capacity *= 2;
  self->data = realloc(self->data, sizeof(WaveHeader) + sizeof(SampleType) * self->capacity);
}

static void CC_Sound_Extend ( CC_Sound* self, int minSamples ) {
  if (self->size >= minSamples)
    return;
  while (self->capacity < minSamples)
    CC_Sound_Grow(self);
  memset(CC_Sound_GetSampleData(self) + self->size, 0, minSamples - self->size);
  self->size = minSamples;
}

/* -------------------------------------------------------------------------- */

static int CC_Sound_Init ( CC_Sound* self, PyObject* args ) {
  self->size = 0;
  self->capacity = SAMPLE_RATE;
  self->data = malloc(sizeof(WaveHeader) + sizeof(SampleType) * self->capacity);

  WaveHeader* wav    = (WaveHeader*)self->data;
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
  return 0;
}

/* -------------------------------------------------------------------------- */

static PyObject* CC_Sound_AddSample ( CC_Sound* self, PyObject* args ) {
  float fSample;
  if (!PyArg_ParseTuple(args, "f", &fSample))
    return 0;
  if (self->size == self->capacity)
    CC_Sound_Grow(self);
  CC_Sound_GetSampleData(self)[self->size++] = FloatToSample(fSample);
  Py_RETURN_NONE;
}

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
  SampleType* data = CC_Sound_GetSampleData(self) + startSample;
  for (int i = 0; i < durationSamples; ++i) {
    float t = (float)i / (float)SAMPLE_RATE;
    data[i] += FloatToSample(amp * sin(freq * t));
  }

  Py_RETURN_NONE;
}

static PyObject* CC_Sound_GetSample ( CC_Sound* self, PyObject* args) {
  int index;
  if (!PyArg_ParseTuple(args, "i", &index))
    return 0;
  if (index >= self->size)
    return 0;
  return PyFloat_FromDouble(
    (double)CC_Sound_GetSampleData(self)[index] / (double)Sample_Max);
}

static PyObject* CC_Sound_Play ( CC_Sound* self, PyObject* args ) {
  WaveHeader* wav    = (WaveHeader*)self->data;
  wav->subChunk2Size = self->size * wav->blockAlign;
  wav->chunkSize     = 4 + (8 + wav->subChunk1Size) + (8 + wav->subChunk2Size);
  PlaySound((char*)wav, 0, SND_MEMORY | SND_ASYNC);
  Py_RETURN_NONE;
}

/* -------------------------------------------------------------------------- */

static PyMethodDef methods[] = {
  { "addSample", (PyCFunction)CC_Sound_AddSample, METH_VARARGS, },
  { "addSine", (PyCFunction)CC_Sound_AddSine, METH_VARARGS, },
  { "getSample", (PyCFunction)CC_Sound_GetSample, METH_VARARGS, },
  { "play", (PyCFunction)CC_Sound_Play, METH_VARARGS, },
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

void CC_Init_Sound ( PyObject* self ) {
  CC_Sound_PyType.tp_new = PyType_GenericNew;
  if (PyType_Ready(&CC_Sound_PyType) < 0) Fatal("Failed to create sound type");
  Py_INCREF(self);
  PyModule_AddObject(self, "Sound", (PyObject*)&CC_Sound_PyType);
}
