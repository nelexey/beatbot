def fade_audio_segment(audio_segment, duration=0):

        if duration <= 0: return audio_segment
        
        faded_in = audio_segment.fade(from_gain=-120, duration=duration, start=0) # ms

        faded_out = faded_in.fade(to_gain=-120, duration=duration, start=len(audio_segment)-duration) # ms

        return faded_out