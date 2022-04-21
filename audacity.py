# -*- coding: utf-8 -*-

import json
import os
import time
from pipeclient import PipeClient


class Audacity():

    def __init__(self):
        self.client = PipeClient()
        self.timeout = 10
        self.clear()

    def _do_command(self, command):
        """Do the command. Return the response."""
        response = ''
        start = time.time()
        self.client.write(command)

        while response == '':
            time.sleep(0.1)  # allow time for reply
            if time.time() - start > self.timeout:
                response = 'PipeClient: Reply timed-out.'
            else:
                response = self.client.read()
        return response

    def clear(self):
        self._do_command("SelectAll")
        self._do_command("RemoveTracks")
        self.reference_clips_length = -1

    def play_record(self, reference_sample=""):
        """Import track and record to new track.
        Note that a stop command is not required as playback will stop at end of selection.
        """
        if reference_sample == "":
            script_dir = os.path.abspath(os.path.dirname(__file__))
            samples_dir =  os.path.join(script_dir, 'samples')
            reference_sample = os.path.join(samples_dir, 'silence-10sec.wav')

        self._do_command(f"Import2: Filename={reference_sample}")
        self._do_command('Select: Track=0')
        self._do_command('SelTrackStartToEnd')

        # Our imported file has one clip. Find the length of it.
        clipsinfo = self._do_command('GetInfo: Type=Clips')
        clipsinfo = clipsinfo[:clipsinfo.rfind('BatchCommand finished: OK')]

        clips = json.loads(clipsinfo)
        self.reference_clips_length = clips[0]['end'] - clips[0]['start']

        # Now we can start recording.
        self._do_command('Record2ndChoice')
        print('Sleeping until recording is complete...')
        time.sleep(self.reference_clips_length + 0.1)

    def truncate_silence(self) -> bool:
        # we must have a reference clip loaded
        if self.reference_clips_length < 0:
            return False

        # TODO: This might need some fixes
        compress=50
        independent=0
        minimum=0.005
        threshold=-40
        truncate=0.005

        self._do_command('Select: Track=1 mode=Set')
        self._do_command('SelectAll')
        self._do_command(f"TruncateSilence: Action=\"Truncate Detected Silence\" Compress=\"{compress}\" Independent=\"{independent}\" Minimum=\"{minimum}\" Threshold=\"{threshold}\" Truncate=\"{truncate}\"")

        # check after the truncate if we have a working track
        clipsinfo = self._do_command('GetInfo: Type=Clips')
        clipsinfo = clipsinfo[:clipsinfo.rfind('BatchCommand finished: OK')]

        clips = json.loads(clipsinfo)
        truncate_clip_length = clips[0]['end'] - clips[0]['start']

        # minimum of 100ms
        if truncate_clip_length < 0.1:
            return False

        if truncate_clip_length < self.reference_clips_length:
            return True
        return False

    def export(self, filename):
        """Export the new track, and deleted both tracks."""
        self._do_command('Select: Track=1 mode=Set')
        self._do_command('SelTrackStartToEnd')
        self._do_command(f"Export2: Filename={filename} NumChannels=1.0")
        self.clear()