import subprocess


def is_spotify_running():
    process = subprocess.Popen('pgrep Spotify', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    if len(my_pid) != 0:
        return True
    else:
        return False
    
    
def open_spotify():
    subprocess.call(
    ["/usr/bin/open", "-g", "-a", "/Applications/Spotify.app"]
    )
    

def asrun(ascript):
# "Run the given AppleScript and return the standard output."
    osa = subprocess.run(['/usr/bin/osascript', '-'], input=ascript, text=True, capture_output=True)
    if osa.returncode == 0:
        return osa.stdout.rstrip()
    else:
        raise ChildProcessError(f'AppleScript: {osa.stderr.rstrip()}')
 
 
def asquote(astr):
    # "Return the AppleScript equivalent of the given string."
    astr = astr.replace('"', '" & quote & "')
    return '"{}"'.format(astr)


def fade_down_Spotify():
    asrun('''
tell application "Spotify"
	set initalVolume to get sound volume
	set theVolume to initalVolume
	repeat until theVolume is less than or equal to 0
		set theVolume to theVolume - 1
		set sound volume to theVolume
		delay 0.15
	end repeat
	pause
    delay 0.1
	set sound volume to initalVolume
end tell
          ''')
    

