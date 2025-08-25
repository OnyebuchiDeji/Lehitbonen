### Date: Wednesday 30th July, 2025


##  Lehitbonen להתבונן

It means "to contemplate" or "to gaze"

That is what this app is for. It's essentially my Shading Language 'playing' app.

I use it where I do not have access to my computer to practice the GLSL shading language including
any ideas I may come up with. Because of the contemplation that goes behind understanding how to use
GLSL to create patterns, I named the app Lehitbonen


##  Base

Here, I use Kivy's OpenGL setup and Kivy's GUI to create an application where
I can write GLSL code to create glsl art runnable on my phone. It is capable of selecting which
GLSL code to load and run from a certain directory from which it lists all the loadable GLSL
files.

Finally, when loaded so that I can edit its contents, I can also click the run button which runs the GLSL code on the Screen area above, which can be maximized (to full screen) and minimized. There is a normal RUN
button, and a RUN and SAVE button. The latter, once run, saves the GLSL video on the screen as a .mp4 file.

Moreover, both in the full screen and out of it, in a small taskbar directly below the screen area (part of the display area/element/gui), is a button that when clicked takes a snapshot of the screen, saving a picture of whatever pattern is generated.

The images and videos are named in this format: "GLSLFILENAME-fileformat(vid,img)-count-datetime.(mp4/png)"
count is kept by an internal counter