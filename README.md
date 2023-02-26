# SpotifyTimer
Countdown timer that fades and pauses the Spotify application on MacOS

The GUI is a timer interface. It contains Start and Stop buttons and text fields for hours, minutes and seconds.
When stopped, the user can enter the countdown time in whatever time denomination they want.

When started, the GUI locks the fields to prevent user entry and displays a 'running' state by turning the display pink. The start button also displays a disabled state.

When the countdown reaches zero, a hardcoded 'action' is triggered. This consists of the following Applescripted 'events':
Spotify remembers its current volume level (somewhere between 0 and 100)
Fades from current level to 0 using a linear iteration.
Pauses
Resets the level to the remembered level.
After the event is complete, the user entry fields are unlocked and the start button is reset.

-------- Known Issues ---------
There are occasions when clicking the 'About' button turns the Start button to its disabled light green colour. Clicking the 'About' button between rundown and action execution seems to make this scenario more likely. Regardless of this, the start button remains clickable as normal.


----- Possible upcoming features and Roadmap ------
Add 'Alarm Mode' - instead of using a countdown, the user can choose the action to occur at a time on any given day in the future.

Make the software not specific to any one application (such as Spotify)

Introduce a choice of fade events and options - fade up, fade down, fade shapes: linear, log, S-curve etc, fade over x secs

Add multiple Actions that can occur at different stages of the countdown

The ability to fire multiple events as a single 'action' to be referred to as a 'Salvo'

Introduce audio mixing capability

Introduce the ability to route application audio

Read timecode

Display frames, milliseconds, etc



