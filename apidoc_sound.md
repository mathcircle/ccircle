# CCircle Module Documentation: Sound

## [Back to Index](index)

## Class : ccircle.Sound

## `ccircle.Sound() -> new Image`
  Create a new, empty sound.

## `sound.addSample(value) -> None`
  Append a single sample to the sound. The sample `value` will be clamped to the
  range `[-1, 1]`.

## `sound.addSine(start, duration, freq, amp) -> None`
  Add a sine wave of frequency `freq` and amplitude `amp` to the sound's sample
  buffer. The wave will begin at `start` seconds and last for `duration` seconds.
  If the wave would extend beyond the sound's current duration, then the sound
  is extended with zero-valued samples to accommodate the entirety of the wave
  before the wave is added.

  _Note that the wave is added to sample values -- it does not overwrite
  existing samples, so multiple overlapping calls of this function can be used
  for additive synthesis._

## `sound.getSample(index) -> float`
  Return the value of the sample at `index`; the value will be in `[-1, 1]`.

## `sound.play() -> None`
  Play the sound's sample buffer through the default audio device. This call
  is asynchronous -- it does not wait for the sound to finish playing before
  returning.

  Currently, playing a sound will stop any other sound that was still playing,
  so it not possible to play multiple sounds at once except by mixing them
  into the same Sound object.
