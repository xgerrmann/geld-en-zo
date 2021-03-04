---
title: Inkomstenbelasting
description: Hoe wordt de totale belasting op jouw inkomen berekend?
date: 2021-01-10
tags:
  - belasting
  - salaris
  - bruto
  - netto
layout: layouts/post.njk
---



Heffingskortingen worden toegelicht in [deze post](/posts/2020-12-24_heffingskortingen/).

uitleg berekening

speciaal tarief 

belasting 13e maand en vakantietoeslag

vakantietoeslag



app voor berekenen eigen inkomstenbelasting

* Optional incorporation of
  * Holiday allowance (8%)
  * Heffingskortingen



##### Output:

* Figuur
  * [x] Totale belasting naar toenemend inkomen (1e y-as)
  * [x] Procentuele belasting naar toenemend inkomen (2e y-as)
  * [ ] Speciaal tarief percentage naar toenemend inkomen
  * [ ] Optionally show/hide details (via CSS so no new calculations have to be performed)
* Tabel
  * Maandelijkse salaris
  * Belasting tarief
  * Netto inkomen
  * Resulterend belasting percentage (bruto - netto) / bruto





TODO:

- [x] Improve multi-page app structure
  https://dash.plotly.com/urls
- [x] Add selection of year(s)
- [ ] Improve style of checkbox (+label)
- [ ] Hide/show advanced details
- [ ] Show speciaal / bijzonder tarief
- [ ] Show tax brackets and rules
- [ ] Kolom per jaar en kolom per maand







## Hoe wordt de inkomstenbelasting berekend?

Heffingskortingen zijn kortingen op belasting. De heffingskortingen worden van jouw verzamelinkomen afgetrokken om zo tot je belastbare inkomen te komen.

<div style="text-align:center">$$I_v - K = I_b$$</div>

* $$I_v$$ is je verzamelinkomen
* $$K$$ is de som van alle heffingskortingen
* $$I_b$$ is jouw belastbare inkomen

* 

Bron: [Belastingdienst](https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/inkomstenbelasting/heffingskortingen_boxen_tarieven/heffingskortingen/totaaloverzicht/overzicht-heffingskortingen-2021)



## Speciaal tarief

Het speciaal tarief is een belastingstarief wat wordt geheven over het salaris dat bovenop je maandsalaris komt. Hieronder vallen:

* Vakantiegeld
* 13$^\text{e}$ maand
* Bonussen

Vaak denkt men dat men meer belasting betaalt over de bovenstaande inkomsten, dit tarief is namelijk vaak/altijd hoger dan het basis tarief van je belastingschijf. De reden dat het lijkt alsof je er meer belasting over betaalt is dat de heffingskortinen reeds zijn meegerekend in dit tarief. Een hoger salaris leidt, naast een hogere belasting, namelijk tot minder heffingskortingen.

##### Zo bepaal je de heffingskorting

bruto maandsalaris = bruto jaar salaris / 108% / 12







In de grafiek hieronder zie je het verloop van het speciale tarief voor een gegeven salaris.





## Bruto-netto tool

<iframe width="100%" height='1400pt' scrolling='no' src='https://personal-finance-app-300718.ew.r.appspot.com/income_taxes' style="border:0px"></iframe>
