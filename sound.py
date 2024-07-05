SOUND = A0

pinMode(SOUND,"INPUT")

volume = grovepi.analogRead(SOUND)
