# Dexonline Python Parser
## Installation

In order to *install* the parser itself you can run this command.
```py
pip install DexonlineParser
```

Once you have installed the parser you can import it like this.
```py
from DexonlineParser import DexParser
```

This will allow you to start using the DexParser class.

---

## Implementation

The DexParser class has a very simple initiation:
```py
parsed = DexParser("cățel")
```

There are several attributes of the DexParser class that may be useful.

- `.word`: original input word used to initialize the object
- `.url`: url used for scraping information
- `.soup`: html code that is being scraped
- `.information`: scraped information, more in next section

The only function you will ever typically use with this class is the `.printInformation()` function as it digestibley outputs the information based on the type of word you inputted. 
```py
parsed.printInformation()
```

---

`object.information` itself is a large dictionary containing all the information. `object.information`'s structure varies by type the type of word you inputted. That being, if you input a *substantiv*, you will have a different structure then if you inputted an *adjectiv*. All three types of words, *subsantiv*, *adjectiv*, and *verb* have their own unique structure.

While they're each unique they all have the same starting structure, a `lemma`, `type`, and `definitions`.
Where they differ is the `inflection` part. As they all have their own separate conjugations and inflections, they have separate tables. 

On average around 5 definitions and their examples are displayed (`.printInformation()`) as to not "overflow" the screen. However, each dictionary can have upwards of 20 definitions. Please note though that the output of `.printInformation()` is quite wide so you're terminal must be quite wide.
Example, Substantiv: "Cățel"
```py
information = {
    'lemma': 'cățel',
    'definitions': {
        'definition 1': 'Pui de câine.',
        'examples 1': ['Luînd doi căței de la o cățea ce fătase de curînd, îi arătă doamnei sale. ISPIRESCU, I. 64.'],
        'definition 2': 'Pui de animal sălbatic (asemănător cu câinele).',
        'examples 2': ['Cățel de lup.'],
        'definition 3': 'Cu cățel, cu purcel = cu întreaga familie și cu tot avutul; cu tot ce are.',
        'examples 3': ['A plecat cu cățel, cu purcel.'],
        'definition 4': 'Om lingușitor și fără scrupule.',
        'examples 4': ['Unul ca Pascu și ca Mănescu, ca Ifrim și toți cățeii subprefectului... unii ca aceștia serbarea noastră n-au s-o tulbure. GALAN, Z. R. 27.'],
        'definition 5': 'Fiecare dintre părțile care compun căpățâna de usturoi.',
        'examples 5': ['Moșneagul se opri un moment din curățit cățeii de usturoi și mă privi nedumerit, fără să-mi răspundă. HOGAȘ, M. N. 66.', 'Vreo cîțiva căței de usturoi și vreo două cepe. Atîta era tot în casă. CONTEMPORANUL, III 922.']
    },
    'type': 'substantiv masculin',
    'inflection': {
        'nominativ-acuzativ': {
            'nearticulat': (['cățel'], ['căței']),
            'articulat': (['cățelul'], ['cățeii'])
        },
        'genitiv-dativ': {
            'nearticulat': (['cățel'], ['căței']),
            'articulat': (['cățelului'], ['cățeilor'])
        },
        'vocativ': {
            'nearticulat': (['cățelule', 'cățele'], ['cățeilor']),
            'articulat': ()
        }
    }
}
```

Example, Adjectiv: "Rău":
```py
{
  'lemma': 'repede',
  'definitions': [
    {
      'text': ' (Despre mișcări) Care se produce fără întârziere. ',
      'examples': [
        ' Omenirea merge într-un progres continuu a cărui mișcare e cu atât mai repede, cu cât mai mult înaintează. BĂLCESCU, O. II 10. '
      ]
    },
    {
      'text': ' (Despre lucruri în mișcare) Care se deplasează cu repeziciune, cu iuțeală; (despre ape) care curge cu repeziciune. ',
      'examples': [
        ' În vaduri ape repezi curg Și vuiet dau în cale, Iar plopi, în umedul amurg, Doinesc eterna jale. COȘBUC, P. I 191. ',
        ' Pîraie repezi s-azvîrl cu vuiet în Bistrița. VLAHUȚĂ, O. A. 417. '
      ]
    },
    {
      'text': ' (Despre picături, stropi etc.) Care cade iute, succedându-se rapid. ',
      'examples': [
        ' Ploaia cade-n repezi picuri. COȘBUC, P. I 119. ',
        ' Caii aleargă îndemnați de țipetele vizitiului, speriați de răpăitul stropilor cari cad, repezi și grei, ca o grindină de gloanțe. VLAHUȚĂ, R. P. 61. '
      ]
    },
    {
      'text': ' (Despre timp) Care trece (pentru cineva) cu repeziciune. ',
      'examples': [
        ' Anii mei repezi, viața-mi trăită Le văz grămadă în urmă-mi stînd. HELIADE, O. I 78. '
      ]
    },
    {
      'text': ' (Despre oameni și manifestările lor) Iute în mișcări. ',
      'examples': [
        ' Degetele repezi poartă acul fin. EMINESCU, O. IV 364. ',
        ' Caii repezi, ageri, cu coame răsfirate Cu nările aprinse, cu gurile spumate... La sunete de luptă, pe cîmp își luau zborul. ALEXANDRESCU, M. 30. ',
        ' Mă gîndeam la... băiatul plin de avînt, cu gesturile foarte repezi și nervoase. SADOVEANU, O. VIII 17. '
      ]
    },
    {
      'text': ' Cu pași repezi = în ritm rapid. ',
      'examples': [
        ' Industria construcțiilor mecanice s-a dezvoltat cu pași foarte repezi. SAHIA, U.R.S.S. 90. ',
        ' Gândăcel de culoare arămie, verde-deschis pe spate, cu puncte albe pe fiecare elitră (Cicindela campestris). '
      ]
    },
    {
      'text': ' (Despre ploaie, vânt etc.) Intens, puternic (și de scurtă durată). ',
      'examples': [
        ' Pe aicea nu umblă niciodată ciobanii, fiind un loc primejdios la vreme de ploi repezi, cad risipituri din păreți și omoară oile. SADOVEANU, F. J. 371. ',
        ' Supărările iubirii Sînt ca ploile cu soare: Repezi, dar cu cât mai repezi Cu atât mai trecătoare. TOPÎRCEANU, B. 56. '
      ]
    },
    {
      'text': ' (Despre agenți fizici) Care se manifestă cu putere dar nu durează mult; care trece iute. ',
      'examples': []
    },
    {
      'text': ' (Despre dealuri, planuri etc.) Foarte înclinat, în pantă. ',
      'examples': [
        ' Albia îngustă într-o parte se înalță drept, pe lângă mănăstire, se ridică într-o coamă repede. SADOVEANU, O. VII 204. ',
        ' Acoperișul de șindrilă destul de repede, căzând pe strășini în chip de coadă de rîndunică, e străbătut, cam în dreptul tinzii, de un soi de foișor. CĂLINESCU, I. C. 46. '
      ]
    },
    {
      'text': ' (Despre drumuri) Care duce la țintă în cel mai scurt timp. ',
      'examples': [
        ' Își chibzuia drumurile cele mai scurte și repezi. C. PETRESCU, A. R. 10. '
      ]
    }
  ],
  'type': 'adjectiv',
  'inflection': {
    'nominativ-acuzativ': {
      'masculine': {
        'nearticulat': (['repede'], ['repezi']),
        'articulat': (['repedele'], ['repezii'])
      },
      'feminine': {
        'nearticulat': (['repede'], ['repezi']),
        'articulat': (['repedea'], ['repezile'])
      }
    },
    'genitiv-dativ': {
      'masculine': {
        'nearticulat': (['repede'], ['repezi']),
        'articulat': (['repedelui'], ['repezilor'])
      },
      'feminine': {
        'nearticulat': (['repezi'], ['repezi']),
        'articulat': (['repezii'], ['repezilor'])
      }
    },
    'vocativ': {
      'masculine': {
        'nearticulat': (),
        'articulat': ()
      },
      'feminine': {
        'nearticulat': (),
        'articulat': ()
      }
    }
  }
}
```

Example, Verb: (a) fugi:
```py
{
  'lemma': 'fugi',
  'definitions': [
    {
      'text': 'La imperativ singular face narațiunea mai vie.',
      'examples': [
        'A se deplasa cu pași repezi, a se mișca iute într-o direcție, a merge în fugă.',
        'Fug caii, duși de spaimă, și vîntului s-aștern, Ca umbre străvezie ieșite din infern. EMINESCU, O. I 98.',
        'Ipate... își fură copilul din covățică... și fuge cu dînsul acasă. CREANGĂ, P. 173.',
        'Mihnea-ncalecă, calul său tropotă, Fuge ca vîntul; Sună pădurile, fîșîie frunzele, Geme pămîntul. BOLINTINEANU, O. 74.',
        'Zările se pierdeau într-o ceață ușoară spre care tremurau și fugeau parcă unde mărunte de lumină. SADOVEANU, O. V 505.',
        'Norii fugeau goniți de vînturile din înălțimi. GÎRLEANU, L. 41.',
        'Cît p-aci să puie zînele mîna pe ei. Și fugi, zînele după dînșii. ISPIRESCU, L. 164.'
      ]
    },
    {
      'text': '(Despre lapte și despre alte lichide) A da în foc (când fierbe).',
      'examples': [
        '(Urmat de determinări introduse prin prepoziția „după”) A urmări în fugă, a alerga pe urmele cuiva pentru a-l ajunge, pentru a-l prinde.'
      ]
    },
    {
      'text': 'A-i fugi (cuiva) ochii după cineva = a nu-și mai putea lua ochii de la cineva, a privi insistent, cu admirație, cu dor; a-i plăcea de cineva.',
      'examples': []
    },
    {
      'text': 'A-i fugi (cuiva) ochii pe ceva = a nu-și putea fixa privirea pe ceva (din cauza strălucirii sau a unei îmbinări de culori).',
      'examples': [
        'Femeia ceea are acum o tipsie de aur și o cloșcă de aur, cu puii tot de aur, așa de frumoși, de-ți fug ochii pe dînșii. CREANGĂ, P. 99.'
      ]
    },
    {
      'text': 'A-i fugi (cuiva) pământul de sub picioare, se spune când cineva își pierde echilibrul și este gata să cadă.',
      'examples': [
        'Simt că-mi fuge pămîntul de sub picioare și... dau să cad pe spate. CARAGIALE, O. II 312.'
      ]
    },
    {
      'text': 'A-i fugi (cuiva) pământul de sub picioare, se spune când cineva se simte pierdut, când își pierde cumpătul.',
      'examples': []
    }
  ],
  'type': 'verb',
  'inflection': {
    'infinitiv': '(a)fugi',
    'infinitiv lung': 'fugire',
    'participiu': 'fugit',
    'gerunziu': 'fugind',
    'first singular': ['fug', '(să)fug', 'fugeam', 'fugii', 'fugisem'],
    'second singular': ['fugi', '(să)fugi', 'fugeai', 'fugiși', 'fugiseși'],
    'third singular': ['fuge', '(să)fugă', 'fugea', 'fugi', 'fugise'],
    'first plural': ['fugim', '(să)fugim', 'fugeam', 'fugirăm', 'fugiserăm'],
    'second plural': ['fugiți', '(să)fugiți', 'fugeați', 'fugirăți', 'fugiserăți'],
    'third plural': ['fug', '(să)fugă', 'fugeau', 'fugiră', 'fugiseră']
  }
}
```
