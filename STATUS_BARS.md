# Status Bars and Dynamic Wallpapers

Most desktop environments or window manager setups include a status bar showing the time/notifications etc.

Many dynamic wallpapers change their background from using light colors during the day to darker colors during the night.
One example is the infamous [MacOS Mojave Wallpaper](https://dynamicwallpaper.club/wallpaper/r1olj9zggjl).

If your status bar is transparent this may lead to issues regarding the contrast between the text and the background.

![status_bar_contrast.png](https://raw.githubusercontent.com/boi4/dynwalls/master/misc/status_bar_contrast.png)

This can be avoided by creating a wrapper script around the command you would usually pass to `dynwalls setcmd` that changes the text-color of your statusbar depending on the new image and then reloads it.

Reloading the bar can be either done by restarting your window manager (which can be distracting if that happens while you work on something), or by sending a signal or issuing a command to reload the bar (this is only supported by some status bars).

Some examples on how to restart your status bar:

* *Polybar*: https://github.com/polybar/polybar/issues/563#issuecomment-337982846
* *i3status-rust*: https://github.com/greshake/i3status-rust/issues/302#issuecomment-616252985

An example for a python script that computes the brightness of the upper 5-pixel border of the image, sets the font and reloads i3status-rs can be found in the `misc` folder in the repository.
