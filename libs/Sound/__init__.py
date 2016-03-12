from kivy import Logger
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_gstplayer import SoundGstplayer
from kivy.resources import resource_find


class MySoundGstplayer(SoundGstplayer):
    @staticmethod
    def extensions():
        return ('wav', 'ogg', 'mp3', 'm4a', 'aac')


class MySoundLoader(SoundLoader):
    @staticmethod
    def load(filename):
        """Load a sound, and return a Sound() instance."""
        rfn = resource_find(filename)
        if rfn is not None:
            filename = rfn

        ext = filename.split('.')[-1].lower()
        if '#' in ext:
            ext = ext.split('#')[-1].lower()
        elif '?' in ext:
            ext = ext.split('?')[0]
        for classobj in SoundLoader._classes:
            if ext in classobj.extensions():
                return classobj(source=filename)
        Logger.warning('Audio: Unable to find a loader for <%s>' %
                       filename)
        return None


MySoundLoader.register(MySoundGstplayer)
