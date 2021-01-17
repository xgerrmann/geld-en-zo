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

heffingskortingen

belastingdruk naar toenemend inkomen



app voor berekenen eigen inkomstenbelasting

* Optional incorporation of
  * Holiday allowance (8%)
  * Heffingskortingen

##### Inputs

* [ ] Selecteer jaar
  Evt optie om meerdere jaren toe te voegen en te vergelijken?
* [ ] Invoer van salaris
* [ ] Checkbox voor 



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

- [ ] Improve multi-page app structure
  https://dash.plotly.com/urls
- [ ] Add selection of year(s)
- [ ] Improve style of checkbox (+label)
- [ ] Hide/show advanced details







## Hoe wordt de inkomstenbelasting berekend?

Heffingskortingen zijn kortingen op belasting. De heffingskortingen worden van jouw verzamelinkomen afgetrokken om zo tot je belastbare inkomen te komen.

<div style="text-align:center">$$I_v - K = I_b$$</div>

* $$I_v$$ is je verzamelinkomen
* $$K$$ is de som van alle heffingskortingen
* $$I_b$$ is jouw belastbare inkomen

* 

Bron: [Belastingdienst](https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/inkomstenbelasting/heffingskortingen_boxen_tarieven/heffingskortingen/totaaloverzicht/overzicht-heffingskortingen-2021)

## Bruto-netto tool

<iframe width="100%" height='1400pt' scrolling='no' src='https://personal-finance-app-300718.ew.r.appspot.com/income_taxes' style="border:0px"></iframe>

rm _si	