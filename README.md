# Wanderrudern Website

Dies ist das Wanderrudern.de Website-Gerüst für den Static Site Generator Hugo

# Hilfe für das Bearbeiten von Berichten

- Berichte liegen unter /content/berichte
- Bitte im Jahr einsortieren
- [Markdown Guide](https://www.markdownguide.org/cheat-sheet/)
- [Frontmatter Guide (yaml)](https://quickref.me/yaml)

# Taxonomies
- Typen: "marathon", "wanderfahrt", "veranstaltung", "schulung"

# Voraussetzung zur Nutzung offline

- Git Versioning Tool
- Hugo Cli für die Erstellung und das Testen von lokalen Änderungen
- npm für tailwind css Paket


# TODOs
- [ ] Sponsoren

# Nutzung

## Seiten-Layout und Basisnutzung

Alle Seiten nutzen [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) als Formatierungssprache.
Basis-Formatierung ist damit möglich, wird aber größtenteils von der Seite übernommen (Absätze, Überschriften, Stichpunkte, Bilder, Links).

## Frontmatter

Jede Seite besitzt am oberen Ende eine Sammlung strukturierter Daten.
Sie werden in der ersten Zeile und direkt nach der letzten Zeile der Daten durch eine Zeile der folgenden Form abgetrennt:

```
---
```

Sie werden im YAML-Datenformat ([Cheatsheet](https://quickref.me/yaml.html) [Längere Version](https://www.hackingnote.com/en/cheatsheets/yaml/)) formatiert.

### Frontmatter allgemein

Für alle Seiten gibt es bestimmte Werte, die den Inhalt und das Verhalten der Seite beeinflussen.

- `weight` (Ganzzahl): Gibt das Gewicht an, mit dem die Seiten sortiert werden. Niedrigere Nummer wird weiter nach vorne einsortiert, nur bei *nicht* zeitgeordneten Seiten hat dies einen Einfluss
- `draft` (`true` oder `false`): Wenn `true`, wird der Bericht bzw. die Seite nicht veröffentlicht, falls nicht vorhanden oder `false`, wird der Post veröffentlicht
- `title`: Titel der Seite. Er wird außerdem als Überschrift im Text eingefügt, keine zusätzliche Überschrift muss im Text hinzugefügt werden.
- `date`: Veröffentlichungsdatum des Posts, muss im Format `YYYY-MM-TT` angegeben werden.


### Frontmatter für Berichte

- `author`: Gibt den Autor des Posts an, hier wird meist nur der Vorname angegeben.
- `begin`: Gibt das Start-Datum einer Fahrt an, gleiches Datums-Format wie `date`
- `end`: Gibt das End-Datum einer Fahrt an, gleiches Datums-Format wie `date`
- `gewässer`: eine Liste aus Gewässernamen, auf der der Bericht stattfand, alle *klein* geschrieben, neue Gewässer werden automatisch mit erstellt.
- `länder`: eine Liste der Länder, in denen der Bericht stattfand, alle *klein* geschrieben, neue länder werden automatisch mit erstellt.
- `typen`: Ein Fahrtentyp, sollte einer von `marathon`, `schulung`, `veranstaltung` oder `wanderfahrt` sein, *alles klein*
- `images`: eine Liste aus Bildern, die in der Gallerie angezeigt werden sollen
  - `src`: Der Dateipfad zum Bild
  - `title`: Der Titel, der der Datei zugeordnet werden soll.


_Beispiel eines Frontmatter-Abschnitts eines Berichtes_:

```markdown
---
draft: false
title: Testfahrt
author: "Stefan"
begin: 2025-05-02
end: 2025-05-04
date: 2025-05-20
gewässer:
- rhein
länder:
- deutschland
typen: marathon
images:
- src: images/boot_fertig.jpg
  title: Boot fertig vorbereitet
- src: images/neuwied_vorbeifahrt.jpg
  title: Vorbeifahrt beim Start der 45km-Strecke in Neuwied
---

Markdown Text hier
```

### Frontmatter für Ausschreibungen

- `author`: Siehe [Frontmatter für Berichte](#Frontmatter-für-Berichte)
- `begin`: Siehe [Frontmatter für Berichte](#Frontmatter-für-Berichte)
- `end`: Siehe [Frontmatter für Berichte](#Frontmatter-für-Berichte)
- `images`: Siehe [Frontmatter für Berichte](#Frontmatter-für-Berichte)


## Shortcodes

Shortcodes sind Hilfskonstrukte, um Nutzern mehr Einfluss auf das Aussehen der Seite über Markdown hinaus zu ermöglichen.

Ein paar Shortcode-Snippets könnten so aussehen:

```
{{< video "./images/video.mp4" >}}

{{< column-layout >}}
{{% col %}}
- 1. Spalte
{{% /col %}}
{{% col %}}
- 2. Spalte
{{% /col %}}
{{< /column-layout >}}
```


Oben sind alle Varianten von Shortcodes dargestellt, die auftreten können:

- `{{< ... >}}`: Shortcodes, die in sich geschlossen einen Zweck erfüllen (z.B. wie oben ein Video einbetten)
- `{{< ... >}}{{< /... >}}`: Shortcodes, die weitere Shortcodes enthalten und somit geschachtelt werden können, kein Markdown im inneren Block erlaubt bzw. kann zu unvorhergesehenen Ergebnissen führen.
- `{{% ... %}}Markdown hier!{{% /... %}}`: Shortcodes, die Markdown innerhalb des Blockes erlauben, Prozentzeichen erlauben das rendern von Markdown-Code, mit spitzen Klammern, wird der Text unbearbeitet eingefügt, was oft zu falschen Ergebnissen führt.

Mithilfe dieser Varianten lassen sich viele nützliche Funktionen einbinden, wie zum Beispiel ein 2-Spalten Layout (siehe unten)

### `center`

Text mittig formatieren

Nutzung:
```markdown
{{% center %}}
Dieser Text wird mittig angezeigt!
{{% /center %}}
```


### `column-layout`

2-Spalten Layout

Nutzung:
```
{{< column-layout >}}
{{% col %}}
## Linke Spalte
{{% /col %}}
{{% col %}}
## Rechte Spalte
{{% /col %}}
{{< /column-layout >}}
```


### `csv-to-table`

CSV-Resourse als Tabelle formatieren

optionaler `nohead`-Parameter: der grüne Kopf der Tabelle wird nicht gerendert (für Tabellen ohne Kopf)

Nutzung:
```
{{< csv-to-table "pfad/zur/datei.csv" "nohead" >}}
```


### `gallery`

Rendert eine Gallerie mit Dateien, die im Frontmatter unter dem Punkt `images` angegeben wurde, siehe [Frontmatter für Berichte](#Frontmatter-für-Berichte).

Im Frontmatter:

```yaml
images:
- title: "image title here"
  src: "relative path to image here (images/image_name_here.jpg)"
```

Nutzung:
```
{{< gallery >}}
```

### `map`

Zeigt eine interaktive Karte mit einem optionalen Marker an einer angegebenen Position mit gegebenem Zoom-Level und Höhe der Karte

Optional: `height`, `zoom`

Nutzung:
```
{{< map height="20rem" lat=[nr] long=[nr] text="" zoom=13 >}}
```

### `newest-upcoming`

Zeigt die neuesten Ausschreibungen.

Anzahl wird über die `config.yaml` im Feld `params.home.news_count` konfiguriert.

Nutzung:
```
{{< newest-upcoming >}}
```

### `previous-news-and-reports`

Zeigt die neuesten Berichte und Neuigkeiten.

Anzahl wird über die `config.yaml` im Feld `params.home.trip_announcement_count` konfiguriert.

```
{{< previous-news-and-reports >}}
```

### `separator`

Fügt eine horizontale Trennlinie ein

Nutzung:
```
{{< separator >}}
```

### `slider`

Zeigt einen Homepage-Slider.

Die Slider-ID ist nur relevant für mehrere Slider pro Seite, darf aber nur einmal pro Seite existieren, muss gesetzt sein und darf keine Leerzeichen enthalten.

Nutzung:
```
{{< slider id="eineindeutige-id-hier" >}}
    {{< slider-entry
        text="Text des Eintrages"
        img="pfad/zum/bild.png"
        href="link/zu/post" >}}
{{< /slider >}}
```

### `v`

Fügt vertikalen Abstand ein.

Nutzung
```
{{< v "height-as-number" >}}
```

### `video`

Bettet ein Video ein.

Nutzung:

```
{{< video "pfad/zu/video.mp4" >}}
```

### `vorstand-email`

Fügt einen Link zu einer Vorstands-EMail mit gegebenem Amtsnamen ein.
Das Amt muss mit einem aus der Konfigurationsdatei `config.yaml` unter `params.vorstand.position` übereinstimmen.

Nutzungsbeispiel innerhalb einer Verlinkung:
```
[Vorstand](mailto:{{< vorstand-email "1. Vorstand" >}})
```

### `vorstand-table`

Fügt eine Tabelle mit allen Vorstandsmitgliedern ein.

Die Vorstands-Daten werden aus der Seitenkonfiguration abgeleitet (`config.yaml`: `params.vorstand`)

Nutzung:
```
{{< vorstand-table >}}
```

## Menü

Das Menü wird über die Einstellungsdatei `config.yaml` unter dem Punkt `menus` gesteuert, dort werden die Einträge, die Hierarchie und die Links zu den entsprechenden Unterseiten spezifiziert.
