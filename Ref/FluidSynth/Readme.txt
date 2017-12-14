---- testplayer ----

testplayer is a Python program that can play midi files using a modified version of
FluidSynth-1.1.6.

A Python interface to FluidSynth and its internal midi player is available in
the file fluidsynth.py. It loads the (modified) fluidsynth library from the current
working directory. (to avoid a system default installation being used). The modifications
of fluidsynth enable 1) accurate positioning in the midi file and 2) setting the quality
level of the vorbis encoder.

These features are demonstrated by the GUI part of the player, which is in the file testplayer.py.
The main features are:
- play, pause, rewind
- accurate positioning of playback (to a position specified in midi-ticks, while playing
or paused)
- setting the quality level of vorbis encoding (0.0-1.0)
- fast saving of a rendition of the midi file to an ogg/vorbis file
- minimal GUI with Tkinter

For Windows a couple of other dll's are in the distribution that are needed by fluidsynth. Keep
all these dll's in one (the program's) directory.
For Linux these dependencies (libglib2.0-0, libsndfile1, libpulse0) are already installed
in Ubuntu 14.014 (trusty) for which the distributed libfluidsynth is compiled.

---- Download ----

Stand alone Win32 executable: testplayer_exe-3.zip
testplayer_exe-3.zip
The python scripts: testplayer_linux-3.zip
testplayer_linux-3.zip (with FluidSynth library compiled for Ubuntu 14.04)
The python scripts with FluidSynth library compiled for Win32: testplayer_win32-3.zip
testplayer_win32-3.zip
Changes to the source of FluidSynth-1.1.6: FluidSynth_changes-3.zip
FluidSynth_changes-3.zip

---- C-API ----

The following new C-API functions have been added to FluidSynth:
<pre>
FLUIDSYNTH_API void fluid_file_set_qual (fluid_file_renderer_t * r, double q);
Set the encoding quality to q (0.0-1.0)
--
FLUIDSYNTH_API int fluid_player_get_ticks (fluid_player_t *player);
Get the current position of the player in midi ticks
--
FLUIDSYNTH_API int fluid_player_seek (fluid_player_t *player, int mticks);
Seek to position mticks (midi ticks)
Due to the logic of Fluidsynth the actual seek is delayed to the next player callback.
(the delay should be well under 4 msec)
--
FLUIDSYNTH_API int fluid_player_load_midi (fluid_player_t *player);
Load the next midi file from the playlist
Fluidsynth itself loads midi files only on the fly during actual playback.
To determine the duration of a track before playing it, we need this function.
--
FLUIDSYNTH_API int fluid_player_track_duration (fluid_player_t *player, int track_num);
Get the duration in midi-ticks for track track_num (the midi file should be loaded first)
</pre>