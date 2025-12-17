import speech_recognition as sr


def start_speech_engine():
    # Initialize Recognizer
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("\n=======================================")
    print("   AI Speech-to-Text Engine Active")
    print("=======================================")
    print(">> Instructions: Speak clearly in English.")
    print(">> Press 'Ctrl+C' in the terminal to stop.\n")

    with mic as source:
        # Dynamic noise adjustment
        print(">> Calibrating background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(">> Ready! Listening...\n")

        while True:
            try:
                print("Listening...", end="\r")

                # Listen with a timeout to avoid hanging
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                print("Processing... ", end="\r")

                # Use Google Web Speech API
                text = recognizer.recognize_google(audio)

                print(f"\n✅ Recognized Text: {text}")
                print("---------------------------------------")

            except sr.WaitTimeoutError:
                # No speech detected within timeout
                pass
            except sr.UnknownValueError:
                # Speech was unintelligible
                print("\n  Could not understand audio. Try again.")
                print("---------------------------------------")
            except sr.RequestError as e:
                print(f"\n Network/API Error: {e}")
            except KeyboardInterrupt:
                print("\n>> Stopping Engine...")
                break


if __name__ == "__main__":
    start_speech_engine()