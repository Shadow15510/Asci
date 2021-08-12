from asci_lib import *

print("Opus 1 (v1.1b):\n'Le Secret d'Asci'\nNouvelle partie:\n>>> asci()\nSinon entrez le code:\n>>> asci('...')")

def asci(code="0.100.1.1"):
	game = Asci(code, 1)
	game.mainloop()
