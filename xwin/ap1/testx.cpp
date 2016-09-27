#include <X11/Xlib.h>
#include <unistd.h>
/*
http://stackoverflow.com/questions/5299989/x11-xlib-h-not-found-in-ubuntu
*/

main()
{
  // Open a display.
  Display *d = XOpenDisplay(0);

  if ( d )
    {
      // Create the window
      Window w = XCreateWindow(d, DefaultRootWindow(d), 0, 0, 200,
                   100, 0, CopyFromParent, CopyFromParent,
                   CopyFromParent, 0, 0);

      // Show the window
      XMapWindow(d, w);
      XFlush(d);

      // Sleep long enough to see the window.
      sleep(10);
    }
  return 0;
}
