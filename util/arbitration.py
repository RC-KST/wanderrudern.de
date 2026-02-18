import os
from dataclasses import dataclass
import typing

names = [
    "Seytel, Paul",
    "Czemper, Tim",
    "Biastock, Stefan",
    "Tesch, Johanna",
    "Beilfuß, Martin",
    "Specht, Doris",
    "Seydel, Paul",
    "Beilfuß, Nirina",
    "Stuhlemmer, Marika",
    "Coesfeld, Florian",
    "Fisch, Carlos",
    "Schmidt-Lehmann, Thomas",
    "Hörmann, Til",
    "Sassin, Patrik",
    "Babendererde, David",
    "Pelzer, Simone",
    "Häberer, Ralf",
    "Strauß, Peter",
    "Wagner, Jochen",
    "Pietschmann, Silvia",
    "Liang, Jennifer",
    "Fuchs, Rufus",
    "Giese, Astrid",
    "Petri, Wolfgang",
    "Daun, Gundula",
    "Steinke, Marie",
    "Katte, Constantin",
    "Schneider, Corinna",
    "Schlichting, Timo",
    "Schmidt, Ulrich",
    "Siebert, Frithjof",
    "Burth, Felix",
    "Beilfuß, Sonia",
    "Scheriau, Karl",
    "Kotte, Marion",
    "Zimmer, Shayenne",
    "von Lehmann,",
    "Altmann, Claudia",
    "Schirm, Devin",
    "Fuchs, Frida",
    "Friedrich, Mario",
    "Kavakli, Melisa",
    "Waschki, Silke",
    "Braunger, Valentin",
    "Liang, Lisa",
    "Orquera, Gabriela",
    "Winter, Julien",
    "Böbs, Annekatrin",
    "Wille, Lena",
    "Stuhlemmer, York",
    "Lau, Holger",
    "Marr, Nico",
    "Marr, Alexandra",
    "Lehmkühler, Sinah",
    "Vohrer, Philipp",
    "Wendenburg, Clarissa",
    "Holdt, Gabriele",
    "Kühnel, Tim",
    "Hyzha, Vladyslav",
    "Götz, Michael",
    "Beversdorff, Malte",
    "Sternkopf, Esther",
    "Reimer, Birte",
    "Vadhavana, Krishna",
    "Hippchen, Teun",
    "Shostopal, Denys",
    "Sobiecki, Bartosz",
    "Schuke, Christian",
    "Kühnel, Tobias",
    "Taylor, Natalie",
    "Butt, Ishaq",
    "Maierhofer, Alexander",
    "Vohrer, Johann",
    "Taylor, Max",
    "Beilfuß, Jonathan",
    "Eyßell, Tim",
    "Post, Aurélie",
    "Streibel, Laurenz",
    "Zander, Daniela",
    "Fretzschner, Stephan",
    "Pilz, Oskar",
    "Genrich, Sandro",
    "Korn, Marina",
    "Adam, Joshua",
    "Reimer, Ulf",
    "Abdo, Almas",
    "Jeschke, Martina",
    "Czemper, Jan",
    "Däuper, Lotta",
    "Quabeck, Anne",
    "Weidlich, Melina",
    "Mann, Ines",
    "Riik, Uwe",
    "Dust, Philip",
    "Piper, Lena",
    "Wadewitz, Kai",
    "Bossin, Robert",
    "Schulze, Stefan",
    "Vohrer, Eva-Lotte",
    "Vohrer, Jakob",
    "Fischer, Gabriel",
    "Stoll, Jeffrey",
]

def main():
    names_splitted = list(map(lambda c: (c[1].strip(), c[0].strip()),
                              map(lambda c: c.split(','), names)))
    anon_state = ArbitrationState(iter(names_splitted))
    anon_state.compute_shorthands()
    print(anon_state.names_lookup)

class ArbitrationState:
    names_lookup: dict[tuple[str, str], str]

    def __init__(self, names: typing.Iterator[tuple[str, str]] = iter([])):
        self.names_lookup = {}
        self.add_names(names)

    def add_names(self: ArbitrationState, names: typing.Iterable[tuple[str, str]]):
        #dict(map(lambda c: (c, ""), names))
        for name in names: self.names_lookup[name] = ""

    def add_name(self: ArbitrationState, pre: str, post: str):
        self.names_lookup[(pre, post)] = ""

    def compute_shorthands(self: ArbitrationState) -> None:
        for key in self.names_lookup:
            self.names_lookup[key] = key[0]
        #shorthands = dict(map(lambda c: (c, c[0]), self.names_lookup))


        for key in self.names_lookup:
            short = self.names_lookup[key]

            identicals: list[tuple[tuple[str, str], str]] = []
            for ckey in self.names_lookup:
                if self.names_lookup[ckey] == short:
                    if len(ckey[1]) != 0:
                        identicals.append((ckey, ckey[1][0]))
            if len(identicals) == 1: continue

            while (any_names_identical(identicals)):
                for i in range(0, len(identicals)):
                    new_idx = len(identicals[i][1])
                    second_name = identicals[i][0][1]
                    identicals[i] = (identicals[i][0], second_name[0:new_idx+1])
            for ckey, appendix in identicals:
                self.names_lookup[ckey] += " " + appendix

    def lookup(self, name: tuple[str, str]) -> str:
        return self.names_lookup[name]


def any_names_identical(l: list[tuple[tuple[str, str], str]]) -> bool:
    for akey, ca in l:
        for bkey, cb in l:
            if akey == bkey: continue;
            if ca == cb: return True
    return False

def split_names(names: typing.Iterable[str], sep = ' ') -> typing.Iterable[tuple[str, str]]:
    return map(lambda c: (c[0].strip(), c[1].strip()),
               map(lambda name: name.split(sep, 1), names))



if __name__ == "__main__":
    main()
