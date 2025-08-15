#!/usr/bin/env python3
import os
import gi
import subprocess
import threading

# Suppress MESA-INTEL debug noise and avoid deprecated GL renderer warnings
os.environ["MESA_NO_ERROR"] = "1"
os.environ["MESA_DEBUG"] = "silent"
# Use Cairo renderer to avoid Vulkan and removed GL renderer warnings
os.environ["GSK_RENDERER"] = "cairo"

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Gio


class YouTubeDownloader(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="YouTube Video Downloader & Converter")
        self.set_default_size(845, 220)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5,
                       margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        self.set_child(vbox)

        grid = Gtk.Grid(column_homogeneous=False, row_spacing=8, column_spacing=10)
        vbox.append(grid)

        grid.attach(Gtk.Label(label="YouTube URL:", xalign=0), 0, 0, 1, 1)
        self.url_entry = Gtk.Entry(hexpand=True)
        grid.attach(self.url_entry, 1, 0, 1, 1)
        paste_button = Gtk.Button(label="Paste URL from Clipboard")
        paste_button.connect("clicked", self.paste_url_from_clipboard)
        grid.attach(paste_button, 2, 0, 1, 1)

        grid.attach(Gtk.Label(label="Output Folder:", xalign=0), 0, 1, 1, 1)
        self.output_entry = Gtk.Entry(hexpand=True)
        grid.attach(self.output_entry, 1, 1, 1, 1)
        select_folder_button = Gtk.Button(label="Select Output Folder")
        select_folder_button.connect("clicked", self.select_folder)
        grid.attach(select_folder_button, 2, 1, 1, 1)

        grid.attach(Gtk.Label(label="Output Filename:", xalign=0), 0, 2, 1, 1)
        self.filename_entry = Gtk.Entry(hexpand=True)
        grid.attach(self.filename_entry, 1, 2, 1, 1)

        self.format_combo = Gtk.DropDown(model=Gtk.StringList.new(["Convert to MP3", "Download as MP4"]))
        self.format_combo.set_selected(0)
        grid.attach(self.format_combo, 2, 2, 1, 1)

        res_audio_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox.append(res_audio_hbox)

        res_audio_hbox.append(Gtk.Label(label="Select Resolution (MP4):"))
        self.resolution_combo = Gtk.DropDown(model=Gtk.StringList.new(["1080p", "720p", "480p", "360p", "240p"]))
        self.resolution_combo.set_selected(0)
        res_audio_hbox.append(self.resolution_combo)

        res_audio_hbox.append(Gtk.Label(label="Select Audio Quality (MP3):"))
        self.audio_quality_combo = Gtk.DropDown(model=Gtk.StringList.new(["320kbps", "256kbps", "192kbps", "128kbps", "64kbps"]))
        self.audio_quality_combo.set_selected(2)
        res_audio_hbox.append(self.audio_quality_combo)

        self.playlist_check = Gtk.CheckButton(label="Download Entire Playlist")
        self.playlist_check.connect("toggled", self.toggle_filename_entry)
        res_audio_hbox.append(self.playlist_check)

        self.status_label = Gtk.Label(label="")
        vbox.append(self.status_label)

        hbox_controls2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, halign=Gtk.Align.FILL, hexpand=True)
        download_button = Gtk.Button(label="Download", hexpand=True)
        download_button.connect("clicked", self.download_video)
        hbox_controls2.append(download_button)

        stop_download_button = Gtk.Button(label="Stop Download", hexpand=True)
        stop_download_button.connect("clicked", self.stop_download)
        hbox_controls2.append(stop_download_button)

        vbox.append(hbox_controls2)

        self.download_process = None
        self.should_stop_download = False

    def paste_url_from_clipboard(self, _btn):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.read_text_async(None, self._on_clipboard_text)

    def _on_clipboard_text(self, clipboard, res):
        url = clipboard.read_text_finish(res)
        if url:
            self.url_entry.set_text(url)

    def select_folder(self, _btn):
        dialog = Gtk.FileDialog(title="Select Output Folder")
        dialog.select_folder(self, None, self._on_folder_selected)

    def _on_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
        except GLib.Error:
            return
        if folder:
            path = folder.get_path()
            self.output_entry.set_text(path if path else folder.get_uri())

    def toggle_filename_entry(self, widget):
        is_checked = widget.get_active()
        self.filename_entry.set_sensitive(not is_checked)
        if is_checked:
            self.filename_entry.set_text("")

    def update_status(self, message):
        GLib.idle_add(self.status_label.set_text, message)

    def stop_download(self, _btn):
        if self.download_process:
            self.should_stop_download = True
            self.download_process.terminate()
            self.update_status("Download stopped manually.")
        else:
            self.update_status("No active download to stop.")

    def run_yt_dlp(self, command, output_filename):
        self.download_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.set_title("Now downloading...")
        for line in self.download_process.stdout:
            if self.should_stop_download:
                break
            self.update_status(line.strip())

        self.download_process.wait()
        if not self.should_stop_download and self.download_process.returncode == 0:
            self.update_status("Download completed successfully.")
        elif self.should_stop_download:
            self.update_status("Download stopped.")
        else:
            self.update_status("Download failed, make sure to input a valid URL.")

        self.set_title("YouTube Video Downloader & Converter")
        self.download_process = None

    def _dropdown_text(self, dropdown):
        model = dropdown.get_model()
        pos = dropdown.get_selected()
        return model.get_string(pos) if pos != Gtk.INVALID_LIST_POSITION else None

    def download_video(self, _btn):
        self.should_stop_download = False
        url = self.url_entry.get_text()
        output_folder = self.output_entry.get_text()
        output_filename = self.filename_entry.get_text()
        output_format = self._dropdown_text(self.format_combo)
        resolution = self._dropdown_text(self.resolution_combo)
        audio_quality = self._dropdown_text(self.audio_quality_combo)
        download_playlist = self.playlist_check.get_active()

        if not output_filename:
            output_filename = '%(title)s'

        if not url or not output_folder:
            self.update_status("Error: Please fill in the URL and the output folder.")
            return

        common_options = []
        if not download_playlist:
            common_options.append("--no-playlist")

        if output_format == "Convert to MP3":
            command = ["yt-dlp", "-f", "bestaudio", url, "--extract-audio", "--audio-format", "mp3",
                       "--audio-quality", audio_quality,
                       "-o", os.path.join(output_folder, f"{output_filename}.%(ext)s")] + common_options
        elif output_format == "Download as MP4":
            fmt_code = f"bestvideo[height<={resolution[:-1]}]+bestaudio/best"
            command = ["yt-dlp", "-f", fmt_code, url,
                       "-o", os.path.join(output_folder, f"{output_filename}.%(ext)s"),
                       "--merge-output-format", "mp4"] + common_options
        else:
            self.update_status("Error: Unsupported format selected.")
            return

        threading.Thread(target=self.run_yt_dlp, args=(command, output_filename)).start()


class YouTubeApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.ytdlp_gui")

    def do_activate(self):
        win = YouTubeDownloader(self)
        win.present()


if __name__ == "__main__":
    app = YouTubeApp()
    app.run()
