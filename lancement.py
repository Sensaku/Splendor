from composants import *

pile_nobles = []
pioche_n1, pioche_n2, pioche_n3 = Pioche(1), Pioche(2), Pioche(3)


def initialisation():
	global pioche_n1, pioche_n2, pioche_n3, pioches
	global rouge, vert, bleu, noir, blanc, jaune, jetons
	nb_joueur = int(input("Quel est le nombre de joueur ?"))
	init_nobles(nb_joueur)
	rouge, vert, bleu, noir, blanc, jaune = PileJeton("Rouge", nb_joueur), PileJeton("Vert", nb_joueur), PileJeton(
		"Bleu", nb_joueur), PileJeton("Noir", nb_joueur), PileJeton("Blanc", nb_joueur), PileJeton("Jaune", nb_joueur),
	jetons = {"rouge": rouge, "vert": vert, "bleu": bleu, "noir": noir, "blanc": blanc, "jaune": jaune}
	pioches = {"1": pioche_n1, "2": pioche_n2, "3": pioche_n3}
	afficher_jeu()


def init_nobles(nj):
	nobles = [(3, 0, 0, 0, 4, 4),
	          (3, 0, 3, 0, 3, 3),
	          (3, 3, 3, 0, 3, 0),
	          (3, 0, 3, 3, 0, 3),
	          (3, 0, 0, 3, 3, 3),
	          (3, 4, 4, 0, 0, 0),
	          (3, 0, 0, 4, 0, 4),
	          (3, 4, 0, 0, 4, 0),
	          (3, 0, 4, 4, 0, 0),
	          (3, 3, 3, 3, 0, 0)]

	shuffle(nobles)
	global pile_nobles
	pile_nobles = [Noble(nobles[i][0], nobles[i][1], nobles[i][2], nobles[i][3], nobles[i][4], nobles[i][5]) for i in
	               range(nj + 1)]


def afficher_jeu(p1=pioche_n1, p2=pioche_n2, p3=pioche_n3):
	global pioche_n1, pioche_n2, pioche_n3
	print("Nobles disponibles :")
	for i, n in enumerate(pile_nobles):
		print(f"Noble {i + 1} --> {n}")

	print("------------------------------------------------")

	print("Cartes niveau 3 disponibles :")
	for i, n in enumerate(p3.cartes_visibles):
		print(f"Carte 1.{i + 1} --> {n}")

	print("------------------------------------------------")

	print("Cartes niveau 2 disponibles :")
	for i, n in enumerate(p2.cartes_visibles):
		print(f"Carte 2.{i + 1} --> {n}")

	print("------------------------------------------------")

	print("Cartes niveau 1 disponibles :")
	for i, n in enumerate(p1.cartes_visibles):
		print(f"Carte 3.{i + 1} --> {n}")


def piocherjeton(joueur, compteur, tour, interdit=[]):
	while compteur == 0:
		couleur: str = input(f"Quel jeton voulez vous en {tour}?\n"
		                     f"Jeton disponibles --> rouge: {rouge.nb_jetons} / vert: {vert.nb_jetons} / bleu: "
		                     f"{bleu.nb_jetons} / noir: {noir.nb_jetons} / blanc: {blanc.nb_jetons}")
		if couleur not in jetons or couleur == "jaune":
			print("Votre saisie est incorrect !\nVeuillez indiquez l'une des couleurs suivantes:")
			continue
		elif jetons[couleur].nb_jetons == 0:
			print("Il n'y a plus de jeton de cette couleur disponible\nVeuillez choisir une couleur disponible :")
			continue
		elif couleur in interdit:
			print(f"Vous avez déjà piocher un jeton {couleur}, vous ne pouvez pas en piocher un deuxième identique !")
		else:
			joueur.jetons[couleur] += 1
			jetons[couleur].nb_jetons -= 1
			compteur += 1
	return couleur


def pioche3jetons(joueur):
	compteur = 0
	couleur1 = piocherjeton(joueur, compteur, "premier")

	if sum(joueur.jetons.values()) == 10:
		print("Vous avez 10 jetons en mains, vous ne pouvez plus en prendre d'autres.")
		compteur += 10

	couleur2 = piocherjeton(joueur, compteur, "second", [couleur1])

	if sum(joueur.jetons.values()) == 10:
		print("Vous avez 10 jetons en mains, vous ne pouvez plus en prendre d'autres.")
		compteur += 10

	couleur3 = piocherjeton(joueur, compteur, "troisième", [couleur1, couleur2])

	print(f"Vous avez choisi un jeton {couleur1}, {couleur2} et {couleur3}."
	      f"Vous avez maintenant {joueur.jetons['rouge']} rouge(s), {joueur.jetons['vert']} vert(s), "
	      f"{joueur.jetons['bleu']} bleu(s), {joueur.jetons['noir']} noir(s) et {joueur.jetons['blanc']} blanc(s)")


def pioche2jetons(joueur):
	compteur = 0
	while compteur == 0:
		double_couleur: str = input(f"Quel jeton voulez vous en double?\n"
		                            f"Jeton disponibles --> rouge: {rouge.nb_jetons} / vert: {vert.nb_jetons} / bleu: "
		                            f"{bleu.nb_jetons} / noir: {noir.nb_jetons} / blanc: {blanc.nb_jetons}")
		if double_couleur not in jetons or double_couleur == "jaune":
			print("Votre saisie est incorrect !\nVeuillez indiquez l'une des couleurs suivantes:")
			continue
		elif jetons[double_couleur].nb_jetons < 4:
			print("Cette action n'est pas possible si il y a moins de 4 jetons de cette couleur disponibles\n"
			      "Veuillez choisir une couleur disponible :")
			continue
		else:
			joueur.jetons[double_couleur] += 1
			jetons[double_couleur].nb_jetons -= 1
			compteur += 1
	print(f"Vous avez choisi 2 jetons {double_couleur}."
	      f"Vous avez maintenant {joueur.jetons['rouge']} rouge(s), {joueur.jetons['vert']} vert(s), "
	      f"{joueur.jetons['bleu']} bleu(s), {joueur.jetons['noir']} noir(s) et {joueur.jetons['blanc']} blanc(s)")


def choisir_carte(joueur):
	pioche = pioches[input("De quel niveau est la carte que vous souhaitez ? (1, 2 ou 3?)")]
	numero = int(input("Quel est le numéro de la carte que vous souhaitez? (1, 2, 3 ou 4?)"))
	if joueur.jetons["rouge"] >= pioche.cartes_visibles[numero - 1].rouge and \
		joueur.jetons["vert"] >= pioche.cartes_visibles[numero - 1].vert and \
		joueur.jetons["bleu"] >= pioche.cartes_visibles[numero - 1].bleu and \
		joueur.jetons["noir"] >= pioche.cartes_visibles[numero - 1].noir and \
		joueur.jetons["blanc"] >= pioche.cartes_visibles[numero - 1].blanc:
		joueur.achete_carte(pioche, numero)
		# utiliser un marqueur pour dire que l'action est validé
	# elif comment gérer l'utilisation de jeton jaune?
	else:
		print("Vous n'avez pas les jetons nécéssaires pour cette carte.")
		# utiliser le marqueur pour indiquer que l'action n'est pas validé et reproposer les acions possible


initialisation()
bot = Joueur("Bot")
pioche3jetons(bot)
pioche3jetons(bot)
pioche3jetons(bot)
choisir_carte(bot)
bot.voir_main()
