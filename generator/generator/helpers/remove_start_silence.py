def remove_start_silence(audio, silence_thresh=-40):
    try:
        # Найдите индекс первого сегмента, не являющегося тишиной
        start_idx = next((i for i, seg in enumerate(audio) if seg.dBFS > silence_thresh), None)

        if start_idx is not None:
            # Обрежьте тишину в начале аудио

            audio_trimmed = audio[start_idx:]
            # Silence deleted.
            return audio_trimmed
        else:
            # No silence found.
            return
    except Exception as e:
        # If unable to delete silence from audio. Returning same audio...
        return audio
