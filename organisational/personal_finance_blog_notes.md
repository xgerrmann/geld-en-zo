## Topics

- Inkomstenbelasting
- Heffingskortingen
- Bijzonder tarief (vakantiegeld en bonussen)
- Hypotheken
  - Vormen
  - Combinaties
- Jaarruimte en reserveringsruimte
- Vermogensbelasting
  - schijven
  - groene beleggingen
  - Vrijstelling voor beleggingen in pensieonrekening





TODO:

* som van belasting en kortingen mag niet negatief zijn (de kortingen worden niet uitbetaald)
* Effectieve heffingskorting kan ook in analyse worden berekend (tax vs gross income)



Berekening belasting (en salaris)

totaal = 108% (incl vakantietoeslag)

Bereken maandelijks salaris

bruto maandelijks = 100%/12



TODO:

* [x] Finish simulation V1.

* Generate basic plots

* Write article

* [ ] Set up website
  * [x] Set up in such a way that alows widgets / interactive stuff (e.g. plots)
  * [ ] Javascript frontend, python backend listening to API requests
  * [x] Publish on Github pages
  * [ ] Write content
  * [ ] Create graphs
  * [ ] Outsource making a video
  
* [ ] Set up google app engine + Dash

  https://www.phillipsj.net/posts/deploying-dash-to-google-app-engine/



Make sure clean setup is properly working from scratch

* Website only works nicely after a yarn dev
  * run with --entrypoint sleep ... 1000
  * then exec -it into container
  * then yarn dev
  * 



https://xgerrmann.github.io/



Improvements:

* Add tests
* Properly implement holiday allowance
* Add bonus functionality
* Fix / enable mortgage



Requirements

* Able to have interactive calculators (e.g. https://www.berekenhet.nl/werk-en-inkomen/bruto-netto-salaris.html)
* Able to have blogposts
* 'simulator' can be on a separate dedicated page (possibly in an iFrame)
* python web-app

INclude web app (google app engine) in static website



## Belasting berekeningen optie 1

##### Bereken netto maandelijks

* DMV 100% bruto salaris, bereken het netto jaarsalaris
* deel dit door 12



##### Bereken netto vakantietoeslag

* Bruto vakantietoeslag = 100% * 8%
* Bereken nieuw **netto** jaarsalaris incl bruto vakantietoeslag (met heffingskortingen ed)
* Trek daar het **netto** jaarsalaris excl vakantietoeslag vanaf
* Dit verschil is de **netto** vakantietoeslag
* Hier kan ook berekend worden hoeveel % er uiteindelijk wordt betaald over de vakantietoeslag



# Belasting berekeningen optie 2

* 





# Belasting berekeningen optie 3

trek alle aftrekposten van je bruto salaris af (resultaat is minder overzicht in de componenten)





# Aftrekbare kosten - eigen woning

https://www.belastingdienst.nl/wps/wcm/connect/nl/koopwoning/content/eigen-woning-aftrekbare-kosten

Periodieke betalingen voor erfpacht, opstal of beklemming zijn aftrekbaar.

> Als u de rechten van erfpacht, opstal of beklemming afkoopt, is de rente over de lening die u afsluit om de afkoopsom te financieren, meestal  wel aftrekbaar.

En nog veel meer



##### Onbelast sparen voor aflossing hypotheek

https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/woning/uw_hypotheek_of_lening/sparen_voor_de_aflossing_van_uw_hypotheek/sparen_voor_de_aflossing_van_uw_hypotheek

U kunt banksparen met een ‘spaarrekening eigen woning’ of  ‘beleggingsrecht eigen woning’. U betaalt dan maandelijks of 1 keer per  jaar een bedrag waarmee u spaart of belegt voor de aflossing van uw  eigenwoningschuld.  



##### Jaar- en reserveringsruimte

https://www.banksparen.nl/pensioen-lijfrente/informatie/reserveringsruimte.aspx

> Binnen de reserveringsruimte geldt wel een maximumbedrag per jaar.



https://www.belastingdienst.nl/bibliotheek/handboeken/html/boeken/FISIN2019/fiscale_informatie_2019-uitgaven_voor_inkomensvoorzieningen.html

> Jaarruimte 2019 hangt af van de situatie in 2018



###### Maximale reserveringsruimte

https://www.belastingdienst.nl/bibliotheek/handboeken/html/boeken/FISIN2019/fiscale_informatie_2019-uitgaven_voor_inkomensvoorzieningen.html

> De opgebouwde reserveringsruimte is in 2019 maximaal 17% van uw premiegrondslag in 2019. Bovendien geldt er een maximumbedrag                              dat afhangt van uw leeftijd:                           
>
> - Bent u geboren na 31 augustus 1962? Dan kan uw reserveringsruimte in 2019 niet hoger zijn dan € 7.254.



> U mag alleen premies en stortingen aftrekken in het jaar waarin u deze hebt betaald.



### Bijzonder tarief

https://meerbudget.nl/bijzonder-tarief/

"verrekeningspercentage loonheffingskorting"

Bijzondere tarief is een construct om de persoon die het salaris ontvangt niet achteraf veel belasting te hoeven laten betalen. Omdat de loonheffingskorting en de arbeidsheffingskorting afnemen met toenemend salaris is door het extra salaris er recht op minder van deze kortingen. Hierdoor moet wordt dit verschil met het extra salaris verrekend waardoor het 'lijkt' alsof het extra salaris extra belast wordt.



Is berekening vakantiegeld correct? -> Ja

108% 8%





# Website titels

geld

slim

slimmer

meer

jong

milennial

verstandig

rijk

hypotheek

belasting

kapitaal

vermogen

groei

leven

beter

kwaliteit

handig

trucs

inzicht

snel

sneller

beter

rijker

persoonlijk

groei

slimgeld

minderbelasting

belasting en jij

belasting enzo

geld enzo

mindyourmoney





# Voorbeeldberekening belasting

Jaarsalaris (totaal, 108%): 55.002,24 (van salarisstrook)

100%: 50.928

Maand: 4.244 (klopt met salarisstrook)

Vakantietoeslag: 4074.24 



Berekening netto:

Belastingschijf:



