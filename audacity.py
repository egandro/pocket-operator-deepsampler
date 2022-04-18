# -*- coding: utf-8 -*-

import json
import time
from pipeclient import PipeClient


class Audacity():

    def __init__(self):
        self.client = PipeClient()
        self.timeout = 10

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

    def play_record(self, filename):
        """Import track and record to new track.
        Note that a stop command is not required as playback will stop at end of selection.
        """
        self._do_command(f"Import2: Filename={filename}")
        self._do_command("Select: Track=0")
        self._do_command("SelTrackStartToEnd")

        # Our imported file has one clip. Find the length of it.
        clipsinfo = self._do_command("GetInfo: Type=Clips")
        clipsinfo = clipsinfo[:clipsinfo.rfind('BatchCommand finished: OK')]

        clips = json.loads(clipsinfo)
        duration = clips[0]['end'] - clips[0]['start']

        # Now we can start recording.
        self._do_command("Record2ndChoice")
        print('Sleeping until recording is complete...')
        time.sleep(duration + 0.1)

    def export(self, filename):
        """Export the new track, and deleted both tracks."""
        self._do_command("Select: Track=1 mode=Set")
        self._do_command("SelTrackStartToEnd")
        self._do_command(f"Export2: Filename={filename} NumChannels=1.0")
        self._do_command("SelectAll")
        self._do_command("RemoveTracks")