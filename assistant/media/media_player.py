import os
import vlc
from utils.logger import log

class MediaPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.current_media = None

    def play_media(self, file_path):
        """
        Play a media file.
        """
        if not os.path.exists(file_path):
            log(f"File does not exist: {file_path}", "error")
            return

        self.current_media = self.instance.media_new(file_path)
        self.player.set_media(self.current_media)
        self.player.play()
        log(f"Playing media: {file_path}", "info")

    def pause(self):
        """
        Pause the currently playing media.
        """
        if self.player.is_playing():
            self.player.pause()
            log("Media paused.", "info")

    def resume(self):
        """
        Resume the paused media.
        """
        if not self.player.is_playing():
            self.player.play()
            log("Media resumed.", "info")

    def stop(self):
        """
        Stop the currently playing media.
        """
        self.player.stop()
        log("Media stopped.", "info")

    def get_status(self):
        """
        Get the current status of the media player.
        """
        if self.player.is_playing():
            return "Playing"
        elif self.current_media:
            return "Paused"
        else:
            return "Stopped"

if __name__ == "__main__":
    player = MediaPlayer()
    test_file = "/Users/vishal_pansare/Downloads/test.wav"

    try:
        player.play_media(test_file)
        input("Press Enter to pause...")
        player.pause()
        input("Press Enter to resume...")
        player.resume()
        input("Press Enter to stop...")
        player.stop()
    except Exception as e:
        log(f"Error with media player: {e}", "error")
