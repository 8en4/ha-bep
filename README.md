# BEP Collectes pour Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![version](https://img.shields.io/badge/version-1.0.1-blue)
![maintained](https://img.shields.io/badge/maintained-yes-green)

Intégration Home Assistant pour suivre les **prochaines collectes de déchets BEP** (Bureau Économique de la Province de Namur) en Belgique.

---

## 📦 Fonctionnalités

Pour chaque type de collecte, cette intégration crée **2 capteurs** :

| Capteur | Description | Exemple |
|--------|-------------|---------|
| `Prochaine collecte XXX` | Date de la prochaine collecte | `2025-05-14` |
| `Jours avant collecte XXX` | Nombre de jours restants | `2 j` |

### Types de collectes supportés

- 🍃 **Organique** — déchets organiques
- ♻️ **PMC** — plastiques, métaux, cartons à boisson
- 📦 **Cartons** — cartons et papiers

---

## 🗺️ Zones couvertes

Toutes les communes couvertes par le réseau **BEP** en Province de Namur (Belgique).

---

## 🔧 Installation

### Via HACS (recommandé)

1. Ouvre **HACS** dans Home Assistant
2. Clique sur **Intégrations** → menu **⋮** → **Dépôts personnalisés**
3. Ajoute l'URL : `https://github.com/8en4/ha-bep`
4. Catégorie : **Intégration**
5. Clique **Ajouter**, puis installe **BEP Collectes**
6. Redémarre Home Assistant

### Installation manuelle

1. Copie le dossier `custom_components/bep` dans ton dossier `/config/custom_components/`
2. Redémarre Home Assistant

---

## ⚙️ Configuration

1. Va dans **Paramètres** → **Appareils et services** → **Ajouter une intégration**
2. Recherche **BEP Collectes**
3. Entre le nom de ta commune ou ton **code postal**
4. Sélectionne ta commune dans la liste
5. Clique **Valider** ✅

---

## 🏠 Exemple de carte Lovelace

```yaml
type: entities
title: Collectes BEP
entities:
  - entity: sensor.prochaine_collecte_organique
    name: Organique
  - entity: sensor.jours_avant_collecte_organique
    name: Jours restants
  - entity: sensor.prochaine_collecte_pmc
    name: PMC
  - entity: sensor.jours_avant_collecte_pmc
    name: Jours restants
  - entity: sensor.prochaine_collecte_cartons
    name: Cartons
  - entity: sensor.jours_avant_collecte_cartons
    name: Jours restants
```

---

## 🔄 Mise à jour des données

Les données sont actualisées toutes les **12 heures** automatiquement depuis l'API BEP.

---

## 🐛 Signaler un problème

Tu as un bug ou une suggestion ? Ouvre une [issue sur GitHub](https://github.com/8en4/ha-bep/issues).

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

*Données fournies par [BEP — Bureau Économique de la Province de Namur](https://bep.be)*
