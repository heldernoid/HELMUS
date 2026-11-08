"""Common nouns of everyday English, written by hand: the things, people, places and ideas people name in casual chat.
Regular plurals come from the rules in gen.vocab; odd plurals are in irregular_nouns(); nouns that are only ever
singular (advice, furniture) or only ever plural (jeans, scissors) are in words(), exactly as written."""
from gen.vocab import nouns, irregular_nouns, words

# irregular plurals
irregular_nouns({
    "man": "men", "woman": "women", "child": "children", "person": "people persons", "foot": "feet",
    "tooth": "teeth", "goose": "geese", "mouse": "mice mouses", "louse": "lice", "ox": "oxen", "die": "dice",
    "grandchild": "grandchildren", "stepchild": "stepchildren", "godchild": "godchildren",
    "brother": "brothers brethren", "penny": "pennies pence",
    # -f / -fe -> -ves
    "leaf": "leaves", "loaf": "loaves", "half": "halves", "calf": "calves", "wolf": "wolves", "shelf": "shelves",
    "elf": "elves", "self": "selves", "thief": "thieves", "knife": "knives", "wife": "wives", "life": "lives",
    "scarf": "scarves scarfs", "hoof": "hooves hoofs", "dwarf": "dwarves dwarfs", "wharf": "wharves wharfs",
    "sheaf": "sheaves", "housewife": "housewives", "midwife": "midwives", "bookshelf": "bookshelves",
    "werewolf": "werewolves", "pocketknife": "pocketknives", "penknife": "penknives", "afterlife": "afterlives",
    # -man -> -men
    "policeman": "policemen", "policewoman": "policewomen", "fireman": "firemen", "businessman": "businessmen",
    "businesswoman": "businesswomen", "salesman": "salesmen", "saleswoman": "saleswomen", "chairman": "chairmen",
    "chairwoman": "chairwomen", "fisherman": "fishermen", "postman": "postmen", "mailman": "mailmen",
    "snowman": "snowmen", "gentleman": "gentlemen", "spokesman": "spokesmen", "spokeswoman": "spokeswomen",
    "cameraman": "cameramen", "craftsman": "craftsmen", "freshman": "freshmen", "sportsman": "sportsmen",
    "doorman": "doormen", "repairman": "repairmen", "handyman": "handymen", "milkman": "milkmen",
    "congressman": "congressmen", "congresswoman": "congresswomen", "caveman": "cavemen", "madman": "madmen",
    "frontman": "frontmen", "middleman": "middlemen", "foreman": "foremen", "workman": "workmen",
    "horseman": "horsemen", "weatherman": "weathermen", "stuntman": "stuntmen", "linesman": "linesmen",
    "garbageman": "garbagemen", "deliveryman": "deliverymen", "countryman": "countrymen", "kinsman": "kinsmen",
    "nobleman": "noblemen", "clergyman": "clergymen", "seaman": "seamen", "airman": "airmen",
    "serviceman": "servicemen", "servicewoman": "servicewomen", "alderman": "aldermen", "chairperson": "chairpersons",
    "anchorman": "anchormen", "boogeyman": "boogeymen", "bogeyman": "bogeymen", "superwoman": "superwomen",
    "everyman": "everymen", "henchman": "henchmen", "marksman": "marksmen", "gunman": "gunmen", "cowman": "cowmen",
    "layman": "laymen", "watchman": "watchmen", "statesman": "statesmen", "townsman": "townsmen",
    # same in the plural
    "sheep": "sheep", "deer": "deer", "fish": "fish fishes", "moose": "moose", "bison": "bison",
    "salmon": "salmon salmons", "trout": "trout trouts", "cod": "cod cods", "aircraft": "aircraft",
    "spacecraft": "spacecraft", "hovercraft": "hovercraft", "series": "series", "species": "species",
    "offspring": "offspring", "swine": "swine", "shrimp": "shrimp shrimps", "squid": "squid squids",
    "tuna": "tuna tunas", "goldfish": "goldfish goldfishes", "catfish": "catfish catfishes",
    "jellyfish": "jellyfish jellyfishes", "starfish": "starfish starfishes", "shellfish": "shellfish",
    "swordfish": "swordfish", "elk": "elk elks", "buffalo": "buffalo buffaloes buffalos", "means": "means",
    "headquarters": "headquarters", "barracks": "barracks", "crossroads": "crossroads", "corps": "corps",
    "chassis": "chassis", "docuseries": "docuseries",
    # latin and greek plurals
    "analysis": "analyses", "crisis": "crises", "basis": "bases", "thesis": "theses", "diagnosis": "diagnoses",
    "hypothesis": "hypotheses", "oasis": "oases", "synopsis": "synopses", "emphasis": "emphases",
    "parenthesis": "parentheses", "prognosis": "prognoses", "neurosis": "neuroses", "psychosis": "psychoses",
    "axis": "axes", "ellipsis": "ellipses", "paralysis": "paralyses", "cactus": "cacti cactuses",
    "fungus": "fungi funguses", "nucleus": "nuclei", "stimulus": "stimuli", "radius": "radii radiuses",
    "syllabus": "syllabi syllabuses", "alumnus": "alumni", "alumna": "alumnae", "focus": "focuses foci",
    "octopus": "octopuses octopi", "hippopotamus": "hippopotamuses hippopotami", "platypus": "platypuses",
    "medium": "media mediums", "curriculum": "curricula curriculums", "datum": "data", "bacterium": "bacteria",
    "memorandum": "memoranda memorandums", "millennium": "millennia millenniums", "symposium": "symposia symposiums",
    "criterion": "criteria", "phenomenon": "phenomena", "index": "indexes indices", "appendix": "appendices appendixes",
    "matrix": "matrices matrixes", "vertex": "vertices vertexes", "vortex": "vortices vortexes",
    "larva": "larvae", "antenna": "antennas antennae", "formula": "formulas formulae", "vertebra": "vertebrae",
    "cherub": "cherubs cherubim", "genus": "genera", "corpus": "corpora", "opus": "opera opuses",
    "stigma": "stigmas stigmata", "schema": "schemas schemata", "maximum": "maximums maxima",
    "minimum": "minimums minima", "spectrum": "spectra spectrums", "addendum": "addenda", "referendum": "referendums referenda",
    "ultimatum": "ultimatums", "aquarium": "aquariums aquaria", "terrarium": "terrariums",
    "plateau": "plateaus plateaux", "bureau": "bureaus bureaux", "chateau": "chateaus chateaux",
    "tableau": "tableaux tableaus", "gateau": "gateaux gateaus",
    # plurals the rules would get wrong
    "quiz": "quizzes", "fez": "fezzes", "whiz": "whizzes", "stomach": "stomachs", "tech": "techs",
    "epoch": "epochs", "monarch": "monarchs", "patriarch": "patriarchs", "matriarch": "matriarchs",
    "eunuch": "eunuchs", "loch": "lochs", "czar": "czars", "passerby": "passersby", "runnerup": "runnersup",
    "motherinlaw": "mothersinlaw", "soliloquy": "soliloquies", "colloquy": "colloquies",
})

# words with no plural (mass nouns), or only a plural form
words("""
advice information wildlife furniture luggage baggage equipment homework housework knowledge news research evidence
music traffic weather garbage rubbish trash luck health wealth happiness sadness loneliness laughter
violence poverty pollution electricity software hardware malware spyware feedback stuff jewelry jewellery
machinery scenery clothing footwear underwear sportswear swimwear knitwear outerwear sleepwear nightwear
merchandise cutlery silverware crockery tableware cookware glassware bakeware stationery mail
jeans pants trousers shorts leggings tights pajamas pyjamas scissors sunglasses goggles binoculars
pliers tongs tweezers headphones earphones overalls knickers panties briefs boxers trunks undies sweatpants
sweats joggers chinos khakis slacks dungarees suspenders clippers shears
physics mathematics maths math economics politics ethics athletics gymnastics aerobics acoustics statistics
linguistics genetics electronics robotics mechanics logistics graphics
thanks congratulations congrats regards surroundings premises belongings savings earnings
whereabouts remains goods riches odds amends cahoots
chaos cosmos diabetes measles mumps herpes rabies blues pilates checkers gps sms gramps grits
masters outdoors overseas woods customs minutes arts
""")

# the house and its rooms
nouns("""
house home apartment condo condominium flat room bedroom bathroom restroom washroom kitchen kitchenette hallway hall
lounge den basement cellar attic loft garage carport porch veranda balcony patio deck terrace yard backyard
courtyard garden lawn driveway walkway fence gate gatepost hedge roof rooftop gutter chimney wall floor
floorboard ceiling stair staircase stairway stairwell step doorstep threshold banister railing door doorway
doorbell doorknob knob handle doormat hinge window windowpane windowsill sill curtain drape blind shutter
closet cupboard cabinet drawer pantry larder laundry corridor lobby foyer entrance entryway exit elevator lift
escalator ladder fireplace hearth mantel mantelpiece furnace heater radiator vent fan thermostat boiler pipe
plumbing faucet tap sink washbasin basin drain plughole toilet loo potty urinal shower showerhead bath bathtub tub
jacuzzi sauna mirror towel washcloth flannel rug carpet mat tile wallpaper paint outlet socket switch
plug wire cord bulb lightbulb lamp lampshade light chandelier nursery playroom study library office workshop
studio shed greenhouse conservatory barn stable kennel doghouse birdhouse treehouse mailbox letterbox postbox
doorframe skylight wardrobe dormer alcove nook cubby utility guestroom suite annex extension
""")

# furniture
nouns("""
chair table desk sofa couch settee loveseat armchair recliner stool barstool footstool bench pew bed bunk
bunkbed mattress pillow cushion blanket sheet duvet quilt comforter bedspread pillowcase headboard
crib cot cradle bassinet dresser chest tallboy sideboard buffet hutch bookcase nightstand
ottoman pouf futon hammock rocker highchair beanbag counter countertop worktop island shelving rack coatrack
hatstand stand tv television screen console credenza vanity cabinetry trunk footlocker daybed
""")

# things around the house
nouns("""
clock alarm vase frame photo picture poster painting print candle candlestick candleholder ashtray ornament
decoration knickknack souvenir plant houseplant pot planter basket bin trashcan wastebasket dustbin bucket
pail mop broom dustpan vacuum hoover sponge cloth rag duster brush scrubber bleach detergent softener soap
shampoo conditioner toothpaste toothbrush floss mouthwash razor shaver comb hairbrush hairdryer straightener
curler deodorant antiperspirant perfume cologne lotion moisturizer moisturiser sunscreen sunblock tissue
kleenex napkin serviette hanger peg clothespin clothesline hamper key lock keychain keyring padlock remote
battery charger adapter fuse doorstop calendar diary notepad
bookmark magnet makeup lipstick mascara eyeliner eyeshadow foundation concealer blush
blusher powder polish nailfile tweezer hairpin scrunchie
bandaid sewing needle thread thimble button pincushion iron
washer dryer incense diffuser humidifier dehumidifier
purifier nightlight flashlight torch matchbox lighter
toolbox junk clutter mess
""")

# the kitchen
nouns("""
fridge refrigerator freezer oven stove stovetop hob cooker microwave toaster kettle blender mixer juicer
dishwasher grill griddle fryer coffeemaker coffeepot
pan saucepan skillet frypan wok casserole lid tray baking platter plate dish bowl cup mug
glass tumbler goblet wineglass saucer jug pitcher carafe decanter bottle jar can tin carton container
box bag teapot teacup teabag fork spoon teaspoon tablespoon chopstick ladle spatula whisk grater
peeler masher colander strainer sieve funnel opener corkscrew cork utensil gadget
placemat tablecloth apron mitt potholder glove foil clingfilm thermos flask lunchbox cooler
icebox coaster board pin skewer toothpick straw doily cookbook recipe
timer scale breadbox breadbin dishrack drainer dishcloth scourer spice
""")

# meals and cooking
nouns("""
food meal breakfast brunch lunch luncheon dinner supper tea snack dessert pudding appetizer starter entree
main side course ingredient portion serving helping bite mouthful taste flavor flavour leftover
takeout takeaway delivery feast banquet picnic barbecue bbq cookout potluck diet calorie protein
carb carbohydrate fat fiber fibre vitamin mineral nutrient sugar salt grain cereal crumb slice chunk scoop
dollop sprinkle pinch dash cube wedge strip spoonful handful cupful
""")

# bread, baking and sweet things
nouns("""
bread toast roll bun bagel croissant muffin biscuit cookie cracker pretzel cake cupcake cheesecake pie tart
pastry donut doughnut pancake waffle crepe scone brownie flapjack baguette sourdough rye pita tortilla
wrap naan cornbread breadstick crouton danish strudel eclair macaron macaroon meringue shortbread
gingerbread churro fritter dumpling flour dough yeast batter crust icing frosting
glaze filling topping candy sweet chocolate lollipop lolly gum bubblegum marshmallow caramel toffee
fudge licorice liquorice jellybean gummy truffle praline nougat mint peppermint popsicle sundae
milkshake shake smoothie custard jello jelly trifle mousse sorbet sherbet gelato cone parfait
syrup honey jam marmalade nutella spread treat
""")

# main foods
nouns("""
rice pasta noodle spaghetti macaroni lasagna lasagne ravioli tortellini penne fettuccine linguine gnocchi
risotto paella couscous quinoa polenta pizza burger hamburger cheeseburger sandwich sub hoagie
panini hotdog corndog taco burrito quesadilla nacho enchilada fajita tamale salsa guacamole chip crisp fry
sushi sashimi ramen pho curry soup stew broth chowder chili gumbo goulash omelet omelette
frittata quiche salad coleslaw slaw dressing sauce gravy ketchup catsup mustard mayo mayonnaise relish pickle
vinegar oil butter margarine ghee cheese cheddar mozzarella parmesan feta brie cream yogurt yoghurt milk
egg bacon ham sausage salami pepperoni chorizo prosciutto jerky steak beef pork lamb mutton veal chicken
turkey duck venison meat meatball meatloaf patty fillet filet rib wing drumstick nugget tender kebab kabob
gyro falafel hummus tofu tempeh seitan spring eggroll wonton bao teriyaki kimchi
bibimbap tempura udon miso samosa biryani tikka korma dal daal chutney poppadom crab lobster oyster clam
mussel scallop prawn calamari anchovy sardine herring mackerel haddock halibut tilapia bass caviar
roe seafood fishcake popcorn granola oatmeal porridge muesli cornflake bran
toastie cheesesteak mac stuffing roast
""")

# fruit, vegetables, nuts, herbs and spices
nouns("""
fruit apple banana orange grape grapefruit lemon lime peach pear plum cherry berry strawberry blueberry
raspberry blackberry cranberry gooseberry elderberry melon watermelon cantaloupe honeydew pineapple mango
papaya kiwi kiwifruit coconut apricot fig date pomegranate avocado tangerine clementine mandarin satsuma
nectarine raisin prune sultana currant olive lychee guava passionfruit dragonfruit persimmon quince
rhubarb starfruit jackfruit durian plantain citrus peel rind pit stone pip core
vegetable veggie veg potato tomato carrot onion shallot scallion garlic clove pepper chilli jalapeno
capsicum cucumber lettuce cabbage spinach kale arugula rocket chard broccoli cauliflower celery corn sweetcorn
cob pea bean lentil chickpea soybean edamame mushroom zucchini courgette eggplant aubergine pumpkin squash
gourd radish beet beetroot turnip parsnip rutabaga swede yam asparagus artichoke leek okra
sprout watercress fennel cress
herb basil parsley cilantro coriander oregano thyme rosemary sage dill chive tarragon
ginger cinnamon nutmeg vanilla paprika cumin turmeric saffron cardamom allspice seasoning
peppercorn sweetener
nut peanut almond cashew walnut pecan pistachio hazelnut chestnut macadamia acorn seed sunflower sesame
""")

# drinks
nouns("""
drink beverage water juice soda pop lemonade limeade orangeade coffee espresso latte
cappuccino mocha americano macchiato frappe decaf cocoa chai matcha kombucha
beer lager ale stout ipa wine champagne prosecco cocktail mocktail margarita martini
mojito liquor spirit whiskey whisky bourbon scotch vodka rum gin tequila brandy cognac sake cider booze
alcohol shot pint keg round refill sip gulp slurp ice energy
""")

# clothes and accessories
nouns("""
outfit garment shirt tshirt tee blouse top tank camisole sweater jumper pullover hoodie sweatshirt
cardigan vest waistcoat jacket coat blazer parka anorak windbreaker suit tuxedo tux tie necktie bowtie dress
skirt miniskirt gown robe bathrobe nightgown nightie onesie romper jumpsuit pajama pyjama
trouser jean jogger legging sock stocking shoe boot sneaker trainer sandal slipper heel stiletto flipflop
loafer clog moccasin wellie welly hat cap beanie beret fedora sombrero helmet hood visor bandana headband
wristband mitten belt buckle zipper zip velcro pocket collar sleeve cuff hem seam lace shoelace
bra bralette lingerie thong boxer brief bikini swimsuit wetsuit leotard uniform
costume jersey kit tracksuit raincoat overcoat poncho shawl cape cloak kimono sari kilt bib
watch wristwatch bracelet bangle necklace chain choker earring stud ring pendant locket brooch anklet
jewel purse handbag clutch tote wallet backpack rucksack satchel suitcase briefcase
umbrella lens contact wig hairpiece toupee accessory size label tag fabric pattern
stripe polka dot fashion style trend look
""")

# the body
nouns("""
body head face hair eye eyeball eyebrow brow eyelash lash eyelid pupil iris ear earlobe nose nostril
mouth lip tongue cheek chin jaw jawline forehead temple neck throat nape shoulder arm armpit underarm
elbow forearm wrist hand finger thumb fingernail fingertip nail knuckle palm fist breast boob nipple
back spine waist hip belly tummy navel bellybutton butt bum bottom buttock leg thigh knee kneecap shin
ankle toe toenail sole limb skin bone muscle tendon ligament joint blood vein artery heart lung liver
kidney brain nerve organ bladder intestine gut bowel colon pancreas ribcage skull skeleton
pelvis cell gene hormone sweat tear breath pulse heartbeat freckle mole birthmark wrinkle pimple zit
spot blackhead scar tattoo piercing beard mustache moustache goatee stubble sideburn dimple curl fringe
bang ponytail braid plait dreadlock mullet haircut hairstyle hairline complexion figure posture
voice saliva spit snot drool vomit puke pee poop urine poo fart burp hiccup yawn sneeze cough wink blink
smile grin frown laugh giggle scream shout whisper sigh groan gasp
""")

# health and medicine
nouns("""
illness disease sickness cold flu fever temperature headache migraine stomachache bellyache
toothache backache earache heartburn pain ache injury wound cut bruise scrape scratch burn sunburn blister
rash itch bump lump swelling sprain strain fracture break infection virus germ bug allergy asthma
cancer stroke tumor tumour seizure concussion symptom condition disorder syndrome treatment cure
remedy medicine medication med pill tablet capsule drug dose dosage prescription vaccine vaccination jab
booster injection syringe bandage plaster cast sling brace crutch cane wheelchair walker
stretcher ambulance hospital clinic pharmacy chemist drugstore surgery operation procedure checkup physical
appointment therapy rehab physio physiotherapy recovery anxiety depression stress insomnia nausea diarrhea
diarrhoea constipation hangover pregnancy birth labor labour miscarriage period cramp acne eczema
dandruff wart cavity crown root retainer inhaler thermometer stethoscope xray scan
mri ultrasound test result ward emergency icu sample donor transplant
disability addiction overdose relapse wellness fitness nutrition hygiene immunity antibody antibiotic
painkiller aspirin ibuprofen paracetamol supplement lozenge ointment
pandemic epidemic outbreak quarantine lockdown mask covid coronavirus chickenpox
malaria pneumonia bronchitis tonsillitis strep
""")

# family and relationships
nouns("""
human guy girl boy kid baby infant newborn toddler teen teenager adolescent adult grownup elder senior
youth minor family household parent mother father mom mum mommy mummy mama mamma momma ma dad daddy papa pa
son daughter sister sibling bro sis twin triplet grandparent grandmother grandfather grandma gran granny nana
nan grandpa grandad granddad grandson granddaughter aunt auntie
aunty uncle cousin nephew niece husband hubby spouse partner fiance fiancee bride groom bridesmaid
boyfriend girlfriend bf gf ex crush relative relation kin stepmother stepfather stepmom stepdad
stepson stepdaughter stepbrother stepsister stepparent godmother godfather godparent
godson goddaughter orphan widow widower bachelor bachelorette spinster friend bestie buddy pal mate dude
homie bff chum companion acquaintance neighbor neighbour roommate housemate flatmate classmate schoolmate
teammate coworker colleague stranger guest host hostess visitor enemy foe rival ally follower
member owner tenant landlord landlady lodger generation ancestor descendant heir sweetheart lover darling
babe sweetie soulmate couple marriage wedding engagement proposal divorce separation breakup affair
fling hookup romance relationship friendship partnership honeymoon anniversary custody adoption
""")

# jobs and professions
nouns("""
job career profession occupation trade teacher professor prof tutor student principal headmaster
headmistress headteacher lecturer coach instructor mentor doctor doc physician nurse dentist vet
veterinarian pharmacist surgeon paramedic medic firefighter officer cop detective sheriff deputy
constable soldier sailor marine pilot captain driver chauffeur trucker cabbie mechanic engineer architect
builder carpenter joiner plumber electrician painter decorator gardener landscaper farmer rancher miner
baker butcher chef cook waiter waitress server bartender barman barmaid barista cashier clerk teller
receptionist secretary assistant manager director executive ceo cfo cto founder cofounder entrepreneur
salesperson accountant bookkeeper banker broker trader investor lawyer attorney solicitor barrister judge
juror jury politician president senator mayor governor minister diplomat ambassador councillor councilor
journalist reporter correspondent editor writer author poet novelist screenwriter playwright artist
illustrator animator sculptor musician singer songwriter rapper drummer guitarist bassist pianist violinist
dancer ballerina actor actress comedian comic magician clown producer photographer filmmaker designer
programmer developer dev coder hacker scientist researcher physicist biologist astronomer
mathematician economist historian psychologist psychiatrist therapist counselor counsellor librarian
janitor caretaker cleaner maid nanny babysitter housekeeper butler tailor seamstress hairdresser barber
stylist beautician manicurist model athlete player referee umpire influencer streamer youtuber blogger
vlogger podcaster gamer intern apprentice trainee volunteer employee employer worker staff boss supervisor
freelancer contractor consultant analyst technician guard bodyguard bouncer courier messenger
dispatcher operator laborer labourer shopkeeper storekeeper vendor dealer merchant retailer wholesaler
supplier realtor agent recruiter hr admin administrator coordinator organizer organiser planner
strategist marketer advertiser publicist spokesperson translator interpreter linguist priest pastor
vicar rabbi imam monk nun preacher missionary chaplain astronaut explorer inventor
surveyor inspector auditor attendant steward stewardess flight crew porter valet
lifeguard ranger undertaker mortician coroner pathologist optician optometrist
chiropractor dietitian nutritionist pediatrician paediatrician dermatologist cardiologist
radiologist anesthesiologist neurologist gynecologist specialist resident
""")

# school and studying
nouns("""
school preschool kindergarten college university uni academy campus class classroom lesson lecture
seminar tutorial module subject homeroom assignment project essay paper report exam
examination midterm final grade mark score diploma degree certificate qualification graduation semester
term trimester quarter year schedule timetable textbook workbook notebook exercise book page chapter
paragraph sentence word letter alphabet pencil pen biro eraser rubber sharpener ruler marker highlighter
crayon chalk chalkboard blackboard whiteboard projector locker binder folder stapler staple paperclip glue
tape calculator dictionary thesaurus encyclopedia atlas map globe science history geography
biology chemistry geology astronomy algebra geometry calculus trigonometry arithmetic psychology philosophy
sociology anthropology literature poetry grammar spelling vocabulary language drama gym recess
playtime lunchtime cafeteria canteen lab laboratory auditorium gymnasium dorm dormitory
major scholarship grant tuition fee loan sophomore junior graduate grad undergrad
undergraduate postgrad phd doctorate dean faculty department detention
suspension expulsion attendance absence registration enrollment enrolment admission application
transcript gpa credit prom yearbook reunion homecoming trip club
debate presentation deadline revision cram
note flashcard summary outline draft dissertation citation reference bibliography footnote
""")

# work and the office
nouns("""
work workplace branch meeting conference call zoom email inbox outbox
message memo task team division unit company business firm corporation corp
startup enterprise agency organization organisation institution nonprofit charity client
customer contract deal agreement negotiation salary wage pay paycheck paycheque payslip payroll
bonus raise promotion demotion interview resume cv applicant candidate position vacancy opening
role title shift overtime vacation holiday leave commute cubicle workstation
computer printer copier photocopier fax scanner shredder file document spreadsheet slide
chart graph diagram budget plan strategy goal target objective milestone kpi metric sale market
marketing advertising ad advert advertisement campaign commercial brand logo slogan product service industry
factory warehouse depot assembly production manufacturer output supply demand stock
inventory shipment order invoice quote estimate pitch launch release
feature requirement spec specification policy protocol guideline regulation compliance audit
review appraisal evaluation assessment complaint request approval signature form paperwork
bureaucracy workload backlog agenda reminder notice
announcement newsletter bulletin noticeboard boardroom committee shareholder stakeholder
merger acquisition layoff redundancy resignation retirement pension benefit perk insurance
union strike protest workforce personnel recruitment hiring
onboarding training orientation internship apprenticeship gig hustle freelance
""")

# money, banking and shopping
nouns("""
money cash coin bill banknote dollar cent nickel dime buck grand euro pound currency change
bank account card debit debt mortgage rent fine tax interest saving
price cost expense expenditure income revenue profit loss payment installment instalment deposit
withdrawal transfer transaction balance statement check cheque receipt refund rebate discount
coupon voucher bargain tip gratuity allowance investment share bond
fund dividend atm cashpoint fortune bankruptcy inflation recession economy finance
cashback reward point loyalty membership subscription bitcoin crypto cryptocurrency stash
shop store supermarket grocery grocer marketplace mall boutique bakery
deli delicatessen bookstore bookshop florist newsagent kiosk stall booth convenience
cafe coffeeshop restaurant diner bistro eatery bar pub tavern saloon
nightclub pizzeria steakhouse cart trolley checkout till
register aisle carrier queue line shopper
barcode sticker purchase package parcel shipping postage return exchange warranty guarantee
item freebie gift present wrapping bow ribbon catalog catalogue brochure
flyer leaflet menu tab
""")

# transport and travel
nouns("""
car auto automobile vehicle truck lorry van minivan suv jeep pickup bus minibus taxi cab uber train
subway metro tube underground tram streetcar bike bicycle cycle motorcycle motorbike scooter moped
skateboard longboard rollerskate skate plane airplane aeroplane airliner jet helicopter chopper glider
balloon blimp boat ship ferry yacht canoe kayak raft sailboat rowboat speedboat motorboat dinghy cruise
liner submarine spaceship shuttle tractor bulldozer crane forklift firetruck
limo limousine convertible sedan hatchback wagon caravan camper rv trailer road street avenue
boulevard highway freeway motorway expressway interstate lane path pathway trail sidewalk pavement
footpath crosswalk crossing zebra intersection junction roundabout bridge overpass underpass
tunnel gridlock stoplight signal sign station stop
terminal airport airstrip runway platform track rail railway railroad ticket fare pass
passport visa passenger commuter seat seatbelt wheel tire tyre engine
motor brake gear gearbox accelerator pedal horn headlight taillight indicator blinker bumper
bonnet windshield windscreen wiper dashboard license licence numberplate
parking carpark gas petrol diesel fuel mile kilometer
kilometre speed journey ride voyage tour route satnav detour
accident crash collision breakdown puncture toll pothole curb kerb roadwork
traveler traveller tourist backpacker holidaymaker sightseeing itinerary destination departure arrival
delay layover stopover connection security border
jetlag hotel hostel motel inn resort campsite reservation booking
""")

# nature, land and water
nouns("""
nature earth world planet land ground soil dirt mud sand dust rock pebble boulder gravel mountain
mount peak summit hill hilltop valley canyon gorge ravine cliff cave cavern volcano crater desert dune
forest woodland jungle rainforest grove orchard field meadow pasture prairie plain
savanna tundra swamp marsh bog wetland isle beach shore seashore coast coastline seaside sea ocean
lake pond pool lagoon reservoir river stream creek brook waterfall wave tide current bay gulf
cove harbor harbour peninsula glacier iceberg snow slope ridge horizon landscape view
countryside wilderness environment ecosystem habitat climate atmosphere air oxygen fire
flame smoke ash ember spark lava magma earthquake quake tsunami landslide avalanche wildfire bushfire
eruption erosion fossil crystal gem ore coal
""")

# plants and trees
nouns("""
tree bush shrub flower bud blossom bloom twig bark seedling sapling grass weed
moss vine petal stem stalk thorn pollen sap rose daisy tulip lily orchid violet dandelion daffodil
lavender jasmine poppy lotus carnation marigold buttercup clover shamrock hydrangea geranium begonia
peony magnolia hibiscus bluebell snowdrop honeysuckle heather oak pine maple willow birch cedar elm
beech spruce fir redwood sequoia cypress sycamore poplar holly ivy fern succulent bamboo
toadstool algae seaweed hay crop harvest wheat barley oat cotton tobacco hemp vineyard
flowerbed compost fertilizer fertiliser pinecone conker
""")

# weather and the sky
nouns("""
sun moon star sky cloud rain raindrop drizzle downpour snowflake snowfall snowstorm
blizzard hail hailstone sleet fog mist haze smog wind breeze gust gale storm thunderstorm thunder lightning
tornado twister hurricane cyclone typhoon monsoon flood drought heatwave rainbow sunshine sunlight sunrise
sunset sundown sunup dawn daybreak dusk twilight shade shadow celsius fahrenheit
forecast humidity frost dew icicle puddle slush daylight moonlight starlight eclipse heat chill
warmth season summer autumn fall winter springtime summertime wintertime
""")

# space and science
nouns("""
universe space galaxy comet asteroid meteor meteorite orbit alien ufo
satellite telescope gravity atom molecule electron proton neutron
particle element compound substance chemical acid solution mixture liquid solid vapor vapour steam
experiment theory law equation calculation measurement observation discovery invention
microscope magnifier beaker testtube specimen chromosome organism
evolution extinction carbon emission radiation wavelength frequency force
motion velocity mass weight volume density pressure friction voltage
circuit magnetism machine robot device technology
""")

# animals
nouns("""
animal creature beast pet dog puppy pup doggy doggo pooch hound mutt cat kitten kitty puss pussycat
bunny rabbit hare hamster gerbil ferret rat squirrel chipmunk horse pony stallion mare foal
donkey mule cow bull heifer cattle steer goat pig piglet hog boar sow hen rooster cockerel
chick duckling bird parrot parakeet budgie canary pigeon dove crow raven magpie sparrow robin
finch wren starling blackbird bluebird jay cardinal eagle hawk falcon vulture condor owl swan flamingo
penguin ostrich emu peacock seagull gull pelican stork heron kingfisher woodpecker hummingbird
toucan bat bear grizzly panda koala fox coyote jackal hyena lion lioness tiger leopard cheetah
jaguar panther cougar puma lynx bobcat elephant giraffe rhino rhinoceros hippo monkey ape gorilla
chimp chimpanzee orangutan baboon lemur kangaroo wallaby raccoon skunk possum opossum otter beaver
badger weasel stoat mink hedgehog porcupine shrew vole sloth armadillo anteater camel llama alpaca
yak antelope gazelle reindeer caribou walrus seal sealion shark whale dolphin porpoise orca eel stingray
ray turtle tortoise frog toad tadpole newt salamander lizard snake serpent cobra python viper
rattlesnake gecko iguana chameleon crocodile croc alligator gator dinosaur dino dragon unicorn
mermaid insect ant bee bumblebee honeybee wasp hornet fly housefly mosquito gnat midge butterfly moth
beetle ladybug ladybird firefly dragonfly spider tarantula worm earthworm caterpillar cocoon snail slug
grasshopper cricket locust cockroach roach flea tick mite termite scorpion centipede millipede pest
critter mammal reptile amphibian rodent predator prey herd flock pack swarm litter nest hive web
burrow lair cage leash tail paw claw fur feather beak tusk mane whisker
fin gill shell antler snout pouch
""")

# sports and exercise
nouns("""
sport game match ref supporter stadium arena court
ball racket racquet net hoop win defeat victory draw league
tournament championship trophy medal playoff semifinal quarterfinal
football soccer basketball baseball softball volleyball tennis golf hockey rugby lacrosse boxing
wrestling karate judo taekwondo kickboxing mma fencing archery badminton pingpong bowling snooker
billiard dart chess checker yoga workout rep set routine marathon
triathlon race sprint lap relay jog run hike walk climb dive swim kick
throw catch tackle foul penalty corner header dunk layup touchdown inning
timeout halftime goalie goalkeeper keeper quarterback catcher striker forward
defender midfielder winger skipper rookie veteran mvp champion champ underdog opponent
competitor contestant spectator crowd cheerleader mascot surfboard ski snowboard sled sledge
toboggan pad kneepad shinpad whistle stopwatch scoreboard sideline dugout
treadmill dumbbell barbell kettlebell rope trampoline cardio
record skill technique tactic
""")

# games, toys and hobbies
nouns("""
toy doll dollhouse teddy puzzle jigsaw block kite yoyo frisbee marble
dice domino monopoly riddle trivia crossword
sudoku swing seesaw sandbox sandpit playground hobby pastime
craft knitting crochet embroidery pottery drawing sketch doodle photography
gardening cooking fishing hunting camping hiking birdwatching collecting stamp collection
scrapbook journal origami drone magic trick bet gamble lottery raffle casino
poker blackjack roulette slot jackpot karaoke bingo arcade pinball laser
paintball rollercoaster carousel funfair fair carnival circus
""")

# phones, computers and the internet
nouns("""
phone smartphone cellphone mobile telephone landline payphone handset cable headphone
earphone earbud headset speaker microphone mic webcam camera router modem wifi hotspot
bluetooth internet website site webpage homepage link hyperlink url domain browser
search app program programme firmware
database network directory download upload update upgrade
install installation uninstall password passcode username login logon signin signup profile
bio setting preference notification alert text dm pm voicemail ringtone chat
emoji emoticon gif meme post repost comment reply like dislike retweet tweet
following feed timeline story livestream channel subscriber video vid clip
pic pfp avatar selfie screenshot screencap filter hashtag mention forum subreddit blog vlog
podcast bot chatbot ai algorithm code glitch error freeze lag ping latency bandwidth
spam scam phishing hack firewall antivirus vpn encryption backup cache
attachment cursor icon popup toolbar sidebar scrollbar dropdown
checkbox desktop storage memory gigabyte megabyte meg
kilobyte terabyte byte bit pixel resolution microchip processor cpu gpu ram rom usb drive
disk ssd keyboard keypad spacebar touchscreen trackpad touchpad stylus laptop
pc netbook monitor display
controller joystick gamepad handheld vr emulator mod patch dlc expansion
level stage quest mission character loot drop achievement checkpoint save respawn spawn
noob newbie pro smartwatch tracker
port hdmi dataset
coding programming script function variable loop array string compiler
command prompt input interface api plugin widget template theme font
shortcut hotkey copy paste autocorrect typo spellcheck
alias nickname gamertag creator content
uploader viewer click clickbait banner livestreamer
""")

# media, entertainment and the arts
nouns("""
movie film flick show episode ep finale teaser sequel prequel
remake reboot spinoff franchise cartoon anime manga novel ebook audiobook
paperback hardback hardcover magazine mag newspaper tabloid article headline column editorial
rating critic genre comedy romcom horror thriller mystery action
adventure fantasy scifi western musical documentary animation sitcom
reality gameshow broadcast
radio dj presenter anchor newsreader audience listener reader
celebrity celeb idol superstar villain hero heroine protagonist antagonist sidekick
part scene plot storyline twist ending spoiler cliffhanger subplot screenplay dialogue
subtitle caption cameo extra stunt special effect cgi location premiere
screening showing blockbuster flop hit classic masterpiece award
nomination song tune melody harmony rhythm beat tempo lyric chorus verse hook intro outro
album single mixtape remix cover playlist vinyl cassette cd dvd bluray stereo
band group duo trio quartet choir orchestra concert festival rave setlist encore
amp amplifier instrument guitar piano keyboardist drum drumkit violin viola
cello fiddle flute recorder trumpet trombone saxophone sax clarinet oboe harp ukulele uke banjo mandolin
harmonica accordion synth synthesizer tuba xylophone tambourine triangle cymbal bagpipe
rap hiphop metal punk jazz country folk reggae soul funk disco techno edm
opera ballet theater theatre play performance rehearsal audition talent dance
art artwork portrait sculpture statue photograph exhibition
exhibit gallery museum canvas easel paintbrush palette poem rhyme haiku tale fairytale
fable legend myth saga epic blurb trilogy
challenge prank short reel fandom fanbase fanfic fanart cosplay
""")

# feelings and the mind
nouns("""
feeling emotion mood vibe joy delight glee bliss cheer sorrow grief misery despair
gloom anger rage fury wrath temper fear terror dread panic fright phobia worry concern
tension love affection fondness adoration hate hatred loathing disgust contempt
jealousy envy pride ego shame guilt embarrassment humiliation regret remorse relief hope optimism
pessimism boredom excitement thrill enthusiasm eagerness surprise shock amazement awe wonder
confusion curiosity passion desire lust longing craving urge trust doubt suspicion faith belief
confidence courage bravery cowardice kindness generosity patience impatience respect gratitude
appreciation sympathy empathy compassion pity mercy humor humour fun pleasure enjoyment comfort peace calm
serenity satisfaction contentment disappointment frustration annoyance irritation resentment bitterness
insecurity vulnerability sensitivity intuition instinct hunch impression attitude personality
temperament trait quality flaw virtue vice strength weakness habit quirk mindset
motivation inspiration ambition determination willpower discipline concentration attention
awareness consciousness mind thought idea notion recollection nostalgia dream daydream
nightmare imagination creativity intelligence wisdom wit genius stupidity ignorance sanity
madness insanity wellbeing heartbreak heartache trauma
""")

# ideas, reasons and other abstract nouns
nouns("""
reason problem issue trouble question answer mistake fault blame truth lie fib secret fact
opinion viewpoint perspective purpose meaning sense wish choice decision option
alternative chance fate destiny risk danger hazard threat safety freedom liberty right
rule justice injustice power control effort attempt try success failure
progress improvement difference similarity advantage disadvantage drawback value
worth quantity amount number shape color colour extent kind type sort
variety version way method approach system process situation circumstance state
status duty responsibility obligation tradition custom experience
ability capability capacity potential existence culture
society community nation government war conflict fight battle argument
quarrel disagreement discussion conversation talk joke pun rumor rumour gossip
hint clue example instance case proof concept principle religion god
goddess heaven hell paradise ghost angel devil demon monster zombie vampire witch wizard
fairy spell curse miracle prayer blessing sin karma aura
detail aspect factor characteristic piece section segment
percentage proportion ratio rate average total sum majority minority whole third
beginning start end finish middle center centre edge front surface
inside outside interior exterior direction north south east west left distance length width
height depth area gap hole place region zone
cause consequence outcome impact influence response reaction
association context background origin source
structure framework design scheme
event occasion incident occurrence
struggle difficulty obstacle barrier limit boundary
opportunity possibility probability likelihood certainty uncertainty guess assumption
expectation prediction comparison contrast distinction definition
explanation description instruction offer suggestion
recommendation warning promise compromise arrangement
permission consent refusal rejection denial excuse apology criticism compliment
praise punishment revenge forgiveness
behavior behaviour manner conduct activity movement gesture expression appearance image
reputation fame glory honor honour dignity rank privilege
need want priority
""")

# society, law, crime and politics
nouns("""
crime criminal robber burglar burglary robbery theft murder murderer killer assassin victim witness
suspect culprit gang gangster mafia mob thug bully vandal vandalism shoplifter shoplifting fraud
scammer con conman kidnapping kidnapper hostage ransom hijacker terrorist terrorism attack assault
abuse harassment bribe bribery corruption smuggler weapon gun pistol
rifle shotgun bullet ammo ammunition bomb explosive grenade sword dagger blade arrow spear shield
police arrest warrant handcuff trial courtroom verdict
prison jail inmate prisoner convict parole probation bail lawsuit
charge accusation allegation testimony alibi motive investigation fingerprint dna
republic kingdom empire democracy dictatorship monarchy king queen
prince princess duke duchess lord lady knight emperor empress royal
chancellor congress senate parliament council party election vote
voter ballot poll act amendment constitution citizen
citizenship immigrant immigration refugee asylum taxpayer
protester riot rally march demonstration revolution rebellion rebel coup
army navy military troop general colonel lieutenant sergeant private
treaty ceasefire truce invasion surrender
flag anthem embassy sanction alliance federation
""")

# people in general (descriptions and roles)
nouns("""
individual idiot fool moron jerk loser winner
weirdo creep freak nerd geek dork jock hipster rockstar
beginner expert professional amateur novice master addict
hater leader participant attendee
user patient local native foreigner
expat villager townie
introvert extrovert optimist pessimist realist perfectionist workaholic chatterbox liar
cheat cheater troublemaker brat saint sinner coward
survivor buyer seller consumer pedestrian cyclist rider
""")

# time
nouns("""
time moment second sec minute min hour day daytime night nighttime midday morning afternoon evening
noon midnight week weekday weekend fortnight month decade century era age eon aeon
phase today tonight tomorrow yesterday sunday monday tuesday wednesday thursday
friday saturday weeknight birthday bday
vacay getaway lifetime childhood adulthood boyhood girlhood adolescence past
future duration interval pause
rush hurry hourglass countdown
eve celebration festivity bash shindig gathering
christmas xmas easter halloween thanksgiving hanukkah diwali ramadan eid valentine
""")

# months (proper names, but time words people type in lowercase)
words("""
january february april may june july august september october november december
jan feb mar apr jun jul aug sep sept oct nov dec
""")

# places in a town
nouns("""
town city village hamlet suburb neighborhood neighbourhood district downtown uptown midtown
square park plaza building skyscraper tower
highrise church mosque synagogue cathedral chapel shrine monastery convent
cinema
salon barbershop spa laundromat launderette
farm ranch zoo castle palace fort fortress courthouse
cemetery graveyard funeral
daycare orphanage shelter foodbank
carwash dealership showroom venue
fairground waterpark campground fountain
monument memorial landmark alley alleyway culdesac
dock pier marina lighthouse boardwalk promenade waterfront riverside lakeside
bypass ringroad
slum ghetto estate tenement suburbia metropolis capital
""")

# materials
nouns("""
material wood timber lumber plank plywood plastic steel gold silver copper bronze brass
aluminum aluminium lead zinc platinum titanium chrome mercury cardboard
textile wool cashmere silk satin leather suede denim nylon polyester
spandex lycra velvet corduroy fleece linen felt tweed latex concrete
cement brick granite slate limestone clay ceramic porcelain china wax foam
styrofoam diamond pearl gemstone ruby emerald sapphire amethyst opal jade quartz
yarn twine mesh tar asphalt varnish
resin putty grout sealant ink dye grease gasoline kerosene charcoal
coke graphite gel grit
""")

# tools and hardware
nouns("""
tool hammer screw screwdriver wrench spanner drill saw chainsaw axe ax hatchet shovel spade
rake hoe trowel hose sprinkler wheelbarrow lawnmower mower trimmer strimmer stepladder bolt
measure chisel sandpaper
clamp vise
toolkit generator compressor pump jack crowbar mallet pick pickaxe sledgehammer
scalpel scissor cutter
roller scaffold scaffolding caulk lever pulley
axle valve nozzle
meter gauge dial crank
""")

# containers, shapes and amounts
nouns("""
crate vial packet
sack envelope barrel
circle rectangle oval cross curve spiral
sphere cylinder pyramid knot zigzag plaid grid
dozen hundred thousand million billion trillion zillion gazillion digit numeral zero
pair bunch batch lot load heap pile stack bundle
row layer tier cluster
inch metre centimeter centimetre millimeter millimetre kilogram kilo gram
lb ounce oz ton tonne liter litre milliliter gallon quart
percent fraction decimal dimension acre hectare kilowatt watt volt
mph kph
""")

# language and communication
nouns("""
phrase idiom saying proverb accent dialect slang
jargon verb noun adjective adverb pronoun preposition conjunction vowel consonant syllable
symbol punctuation comma semicolon apostrophe hyphen
exclamation quotation bracket asterisk ampersand underscore
abbreviation acronym initial pronunciation translation synonym antonym
fluency speech remark
postcard invitation invite greeting farewell goodbye
phonecall ask
name surname address postcode zipcode
""")

# everyday things and general objects
nouns("""
thing object thingy thingamajig doohickey gizmo whatsit
keepsake memento treasure prize
cigarette cig ciggie cigar vape vaper blunt
stick pole rod beam panel slab
crack dent stain smudge splash drip leak spill
noise sound silence echo boom thud beep buzz
smell scent odor odour stink stench aroma fragrance
touch feel texture
tint hue black white red blue yellow purple pink brown grey gray
""")

# places in the world (general nouns, not names)
nouns("""
province county territory continent
hemisphere equator tropic compass
homeland motherland hometown birthplace
""")

# parties, events and social life
nouns("""
christening baptism gala reception ceremony
parade firework meetup hangout
sleepover slumber playdate
housewarming stag
rsvp confetti
""")

# religion and beliefs
nouns("""
bible koran quran scripture gospel psalm hymn
sermon worship prophet disciple apostle
christian catholic protestant muslim jew hindu buddhist atheist agnostic believer
meditation ritual sabbath altar
""")

# home life and chores
nouns("""
chore errand cleaning ironing vacuuming shopping
list todo checklist repair maintenance
renovation remodel grime mold mould
""")

# chat and internet talk nouns
nouns("""
take rant
convo msg txt swipe
fam squad friendo
troll stan simp fanboy fangirl normie boomer zoomer millennial
flex wishlist binge streak throwback
situationship
rando
""")

# daily life
nouns("""
sleep nap naptime bedtime rest hug cuddle kiss help care use support practice payday carpool icebreaker
joyride makeover meltdown setback setup lineup lookout lifesaver lifeline outage ripoff showdown spotlight
standoff standby turnout upbringing worldview downside upside flashback shakeup
""")

# more general nouns
nouns("""
death development education matter official population access accommodation addition administration aim appeal
authority base beauty behalf bell burden cabin camp category chief claim combination commission communication
competition component conclusion contest contribution count cry damage darkness decline defense defence disaster
efficiency employment encounter entertainment entry escape ethic exposure favor favour favourite favorite fiction
finding fold funding gain glance glimpse growth guidance guide harm highlight hire honesty housing humanity hunger
identity illusion illustration importance increase independence indication initiative inquiry enquiry insight
inspection intention interaction introduction involvement judgment judgement jump knock lack leadership
legislation lifestyle logic management manufacturing margin mill mine mode narrative norm offence offense
opposition ownership pace participation passage perception poison popularity possession preparation presence
prevention privacy property prospect protection provision publication pursuit range ranking reading recognition
recording reduction reflection reform replacement representation representative rescue resistance resource
restriction rise scope selection sequence session settlement sight sponsor standard steal stretch survey survival
teaching tendency timing tone topic tourism transition transport transportation turn unity usage variation venture
violation vision visit waste welcome welfare writing
""")
