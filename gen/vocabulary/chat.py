"""What a dictionary lacks but chat is full of: internet slang and abbreviations, interjections and spelled sounds,
first names, places, nationalities and languages, brands, apps, games, sports and holidays. Hand-written; mostly
words() (exact forms, listed in full), nouns() where a plain plural is natural."""
from gen.vocab import nouns, words

# ---------------------------------------------------------------------------------------------------------------
# (1) internet slang, abbreviations, interjections, spelled sounds
# ---------------------------------------------------------------------------------------------------------------

# laughing
words("""lol lolol lololol lols lolz loll lul lel lmao lmaoo lmfao lmfaoo rofl roflmao lmk haha hahaha hahahaha
hah heh hehe hehehe heheh hihi jaja jajaja kek xd xdd ahaha ahahaha bahaha bwahaha mwahaha muahaha
teehee lolsob""")

# chat abbreviations, older and current
words("""ngl tbh tbf idk idc idek idgaf imo imho smh fr frfr rn ttyl ttys brb bbl bbiab gtg g2g afk omg omfg omw
wtf wth wtaf ftw fml fyi btw tho thx tx ty tyvm tysm np nvm nm ikr irl jk jw nsfw sfw tldr tl dr ama
til eli hbu wbu wyd hmu ily ilysm ilu luv tmi pov afaik iirc icymi ftfy oc op dm dms dmed dming dmd pm
pms pmd ppl peeps pls plz plss plox srsly srs prolly probs def defo deffo obvi obv obvs totes cuz coz
cos bc bcuz becuz bcs thru gonna wanna gotta kinda sorta lemme gimme dunno ya yah yea yeah yeh yep yup
yuh ye nah naw nope mhm uhuh uhhuh ok okay okey okie okk kk kay oki okayy alr ight aight sry
sowwy soz rly rlly ofc ofcourse bday hbd gn gm gnight nite tonite tmrw tmr tmrow tomoz 2moro yday ystd
wkend wknd sec secs mins hr hrs abt ab w wo b4 l8r l8 gr8 m8 str8 any1 some1 no1 cya cu cyl ur u r y k
n b4n ltns tc ttfn xoxo xox xo xx xxx asap aka diy faq rsvp eta tba tbd etc idt idts ig igs ik iykyk
iyk wdym wym wdyt hru sup wassup wazzup whatsup wsup ssup yo yoyo oml ong ongod istg wyll lowk highk fs
fsho fosho fasho bruv innit bloke mate cheers""")

# current slang
words("""sus suss cap nocap bet bussin rizz rizzed rizzing rizzler delulu slay slayed slaying slays lowkey
highkey vibe vibes vibing vibed vibey vibin yeet yeeted yeeting yeets stan stans stanned stanning simp
simps simped simping simpin mid based cringe cringey cringy ratio ratioed npc npcs goat goated sheesh
oof ope bruh bro bros broski brah bra dude dudes fam yall yallz yinz youse finna tryna boutta bouta
aint deadass dead periodt period purr sksksk ate slaps slapped bop bops banger bangers fire lit
litty drip dripped drippy flex flexed flexing flexin glowup glow salty shook shooketh tea spill extra
basic bougie boujee ghosted ghosting ghost lurk lurking lurker troll trolled trolling trolls noob noobs
n00b newb newbie pwned pwn gg ggs ez wp glhf gl hf clutch nerf nerfed buff buffed meta grind grinding
grindset sigma alpha beta chad chads karen karens boomer boomers zoomer zoomers millennial millennials
genz gen gamer gamers rage ragequit copium hopium cope seethe mald malding touchgrass ick icks
situationship talkingstage bffs bff bestie besties bae boo hun hon babe bbg cutie shawty shorty homie
homies dawg dog cuh fella gurl girlie girly bish l dub dubs fax facts valid hella mad wicked hecka
hecking heckin dope sick rad gnarly tubular legit legitly totally fomo yolo swag swaggy bling thicc
chonk chonky chungus smol beeg doggo pupper floof borb snek boi bois sadge pog poggers pogchamp kekw
monka omegalul lulw hype hyped vibecheck skibidi gyatt fanum tax mewing mew aura aurafarming ohio rizzy
unc cooked cooking crash out crashout locked lockin lockedin demure mindful brat bratty mother
mothering iconic icon queen king kween yass yas yasss yaaas slayy stfu gtfo dgaf gtfoh af asf asl bffr
iwtv ts gng twin twinn opp opps oppa unalive pressed sending wig snatched gagged serving serve ratiod
mewed""")

# interjections and spelled sounds
words("""hmm hmmm hm mm mmm mmhm mhmm uh uhh uhm um umm erm er ah ahh ahhh aah oh ohh ooh oooh oo ooo eh meh huh
ha ugh ughh urgh argh arg aargh gah grr grrr pfft pff pft psh pshh tsk tch welp whelp whew phew yay
yayy yaay woo woot woohoo wahoo yahoo yippee hooray hurray huzzah aw aww awww eww ew ewww yuck yikes
yeesh oops whoops oopsie whoopsie uhoh ow ouch owie oww booo bam boom pow wham kaboom zoom vroom whoosh
swoosh splat thud bonk boop beep ding dong buzz zzz zz shh shhh psst ahem achoo hiccup burp blah
blahblah yada whatev whatevs bleh blech bleugh blegh ack gasp sigh facepalm shrug yawn hiya heya hey
heyy heyyy hii hiii hai hallo hullo howdy ello oi oy oye bye byee byeee buhbye bai toodles ciao adios
aloha namaste shalom salaam hola bonjour konnichiwa sayonara arigato gracias merci danke ja oui si nein
nyet amen hallelujah bravo encore voila eureka gesundheit mazel tov mamma mia la ole yeehaw giddyup uwu
owo umu ono bwah nya nyaa rawr rawrr meow woof bark oink moo quack baa neigh hiss ribbit tweet chirp
squee eep eek yelp wheee whee wee yowza zoinks jinkies jeez geez gee golly gosh dang darn drat shoot
shucks heck frick fricking freaking frickin freakin dagnabbit crikey blimey bloody ruddy bah humbug
pshaw""")

# emoticon words and emoji names people type out
words("""emoji emojis emoticon emoticons smiley smileys kaomoji gif gifs jif meme memes memer memed meming xp
lenny tableflip thumbsup thumbsdown heart hearts skull crying sob pleading clown eyes eyeroll wink
winky blush smirk frown tongue""")

# ---------------------------------------------------------------------------------------------------------------
# (2) first names (US, all genders and backgrounds) - so a name is never 'corrected' to another word
# ---------------------------------------------------------------------------------------------------------------

# names: classic and common men's
words("""james john robert michael william david richard joseph thomas charles christopher daniel matthew
anthony mark donald steven paul andrew joshua kenneth kevin brian george timothy ronald edward jason
jeffrey ryan jacob gary nicholas eric jonathan stephen larry justin scott brandon benjamin samuel
gregory alexander frank patrick raymond jack dennis jerry tyler aaron jose adam nathan henry douglas
zachary peter kyle ethan walter noah jeremy christian keith roger terry gerald harold sean austin carl
arthur lawrence dylan jesse jordan bryan billy joe bruce gabriel logan albert willie alan juan wayne
elijah randy roy vincent ralph eugene russell bobby mason philip louis harry howard fred travis jimmy
johnny victor martin ernest phillip todd craig shawn curtis stanley leonard dale manuel rodney lee
allen clarence marvin glenn derek jeffery luis jay barry dean warren corey troy mike tom bill bob jim
joey tony nick matt chris dan danny dave steve jon ben sam alex andy josh jake luke zach zack max nate
pete rick rob ted tim will greg jeff ken ron don ray jeremiah hunter connor caleb isaac owen evan cole
carter wyatt landon gavin chase blake hayden colton cooper grayson easton jaxon jackson liam lucas
oliver aiden aidan jayden brayden kayden camden parker levi lincoln miles asher theo theodore leo ezra
hudson silas jasper atlas axel beckett bennett brooks declan everett finn finley graham harrison jude
kai knox luca maverick nolan oscar rhett ronan rowan ryder sawyer tucker weston xavier zane bentley
braxton brody bryce cade cody colby dakota dalton damian dawson drew garrett grant griffin holden jace
jaden jared jax kaden kingston kolton lane maddox malcolm marshall micah paxton preston reid ricky
riley rory roman sebastian spencer tanner trent trevor tristan wade wesley wilson zander august amos
abel abraham ambrose barrett beau boone bradley brady brent bryson calvin cameron casey clark clay
clayton clint clinton colin conner conor curt damon darren darryl dustin dwight edgar elliot elliott
emmett felix fletcher forrest franklin gage gideon gordon hank hector herbert hugh hugo ian ivan jamie
jarrod jerome jimmie joel jonah jonas judah julian julius karl keegan kendall kent kirk kurt lance
landen lonnie lyle marcus mario marty maurice melvin milo morgan neil nelson norman otis perry quentin
quinn reggie reginald rex ricardo rocco roderick ross rudy russ salvador seth shane sheldon simon
sterling stuart sullivan vance vaughn vernon wallace ward wendell wiley wilbur willis zeke zion""")

# names: classic and common women's
words("""mary patricia jennifer linda elizabeth barbara susan jessica sarah lisa nancy betty margaret sandra
ashley kimberly emily donna michelle carol amanda dorothy melissa deborah stephanie rebecca sharon
laura cynthia kathleen amy angela shirley anna brenda pamela emma nicole helen samantha katherine
christine debra rachel carolyn janet catherine maria heather diane ruth julie olivia joyce virginia
victoria kelly lauren christina joan evelyn judith megan andrea cheryl hannah jacqueline martha gloria
teresa ann sara madison frances kathryn janice jean abigail alice judy sophia grace denise amber doris
marilyn danielle beverly isabella theresa diana natalie brittany charlotte marie kayla alexis lori ava
amelia harper ella abby addison aubrey audrey aurora avery bella brooklyn camila chloe claire clara
delilah eleanor eliana ellie emilia everly evie gabriella genesis gianna hailey hazel isla ivy jade
josephine kennedy kinsley layla leah lillian lily lucy luna madeline maya mila naomi nevaeh nora
paisley penelope piper ruby sadie savannah scarlett serenity skylar sofia stella violet willow zoe zoey
alaina alana alexa alexandra alicia alison allison alyssa amara anastasia angelina annabelle annie
april aria ariana ariel ashlyn autumn bailey becky beth bethany bianca bonnie brianna bridget brooke
caitlin callie cara carla carly carmen caroline cassandra cassidy cassie cecilia celeste chelsea cindy
claudia colleen courtney crystal daisy dana daphne dawn delaney destiny dolores eden elaine elena eliza
ellen eloise elsie erica erika erin esther eva faith fiona gabby gemma georgia gina gwen gwendolyn
haley harley harmony heidi holly hope irene iris jackie jane jasmine jenna jenny jill jo joanna jocelyn
jodie josie joy julia juliana juliet june kara kate katelyn katie kathy kaylee keira kelsey kendra kim
kira kristen kristin kylie lacey leila lena leslie lila liliana lilly lindsay lindsey liz liza lola
lorraine louise lucia lydia lyla mackenzie macy maddie madelyn maggie makayla mallory mandy margot
mariah marissa marley mckenzie meg melanie melody meredith mikayla miranda molly monica nadia nina
noelle norah paige paula peggy penny phoebe priscilla rachael raven reagan rebekah regina renee rita
robin rosa rose rosemary rosie roxanne sabrina sally selena shannon shelby sienna sierra simone sloane
sophie stacy summer susie sydney tabitha tamara tara taylor tess tessa tiffany tina tracy trinity
valerie vanessa vera veronica vicky vivian wendy whitney yvonne zara zelda""")

# names: shared and newer unisex
words("""reese sage river skyler skye charlie frankie emerson peyton blair ellis emery jules kerry marlowe
oakley phoenix remy remington shea shiloh sutton tatum winter wren brett carson dallas devon jody lou
mckinley ollie sasha stevie toni jaime kris pat""")

# names: hispanic and latino
words("""carlos jesus miguel antonio alejandro francisco javier pedro diego fernando jorge eduardo roberto
rafael mateo santiago emiliano leonardo andres angel adrian raul ramon rodrigo pablo cesar sergio
alberto armando arturo enrique ernesto felipe gerardo guillermo gustavo ignacio joaquin julio lorenzo
marco marcos nicolas octavio omar orlando rene ruben tomas alonso benicio dante elias gael iker thiago
valentino guadalupe juana ana valentina ximena valeria mariana gabriela daniela natalia paola alejandra
adriana beatriz blanca catalina cristina esperanza fernanda graciela ines isabel josefina juanita
leticia lorena luz marisol martina mercedes paloma pilar raquel rocio rosario silvia yesenia yolanda
esmeralda araceli brisa dulce estrella itzel jimena karina lupita maribel marisa nayeli perla reyna
salma yadira""")

# names: black american and newer american
words("""jamal darnell deshawn tyrone malik andre jalen jaylen jayson darius terrence lamar marquis rashad
demetrius dominique kareem khalil trevon tremaine jermaine dwayne devonte deandre keshawn kendrick
quincy cedric cornelius desmond donovan isaiah jabari kwame lebron marcellus kenji kobe amari zaire
jaylin jaxson legend messiah prince major aaliyah aisha ebony imani jada keisha kiara latoya monique
nia shanice shaniqua tanisha tiana tamika diamond essence precious kenya india africa ayanna eboni
jazmine jazmin kenyatta lashonda latasha latisha laquisha nyla zuri amani kamari ayesha jaida janelle
jayla kaliyah khloe kiana nyah shaniya tiara""")

# names: asian american, south asian, middle eastern, african, european and others
words("""wei li ming jun hao yan lin chen mei xiao yu jing hui ling lei feng hong yang jian bao hiroshi takeshi
yuki haruto ren sora yuto akira aiko hana yuna sakura emi kaito riku minjun jiho seojun jimin jisoo
minji seoyeon soyeon hyun joon min sung young nguyen minh anh linh thanh trang huong quang tuan duc raj
rahul arjun rohan vikram amit anil sanjay suresh ravi ajay vijay krishna aditya ananya priya deepa
divya kavya neha pooja riya sanjana shreya sneha anjali aarav vihaan ishaan sai advait aryan dev nikhil
pranav varun kiran meera lakshmi sita radha nisha asha isha mohammed muhammad mohamed ahmed ahmad ali
hassan hussein ibrahim yusuf youssef khalid karim tariq hamza bilal zaid amir samir nasser rashid
mustafa mahmoud said fatima zainab maryam noor nour yasmin yasmine amira huda rania samira dina farah
lina mariam moshe avi yosef yael noa tamar shira rivka ari kofi kojo chidi chinedu emeka obi tunde femi
segun ade ayo chioma ngozi adaeze folake nkechi zawadi amina abena dmitri sergei alexei nikolai
vladimir yuri boris igor oleg anya natasha olga svetlana tatiana irina katya galina pierre jacques luc
francois giuseppe giovanni luigi paolo matteo alessandro francesca giulia chiara hans fritz klaus
jurgen johann helga greta ingrid lars sven erik nils astrid freya sigrid seamus niamh siobhan aoife
ciara colm callum hamish fergus ewan alistair mhairi morag dmitry bogdan piotr jakub zofia agnieszka
kalani keoni leilani makana malia""")

# ---------------------------------------------------------------------------------------------------------------
# (3) places, nationalities, languages
# ---------------------------------------------------------------------------------------------------------------

# us states (the multi-word ones by their parts) and their postal abbreviations
words("""alabama alaska arizona arkansas california colorado connecticut delaware florida hawaii idaho illinois
indiana iowa kansas kentucky louisiana maine maryland massachusetts michigan minnesota mississippi
missouri montana nebraska nevada new hampshire jersey mexico york north south carolina oklahoma oregon
pennsylvania rhode island tennessee texas utah vermont west washington wisconsin wyoming columbia dc
puerto rico guam al ak az ar ca co ct de fl ga hi id il ia ks ky md ma mi mn ms mo mt ne nv nh nj ny nc
nd or pa ri sc sd tn ut vt va wa wv wi wy pr usa us america states cali socal norcal philly vegas nola
chitown nyc sf atl dmv pnw tri midwest midwestern east coast bay area""")

# us cities and towns (the multi-word ones by their parts)
words("""los angeles chicago houston philadelphia san jacksonville fort worth columbus indianapolis seattle
denver boston el paso nashville detroit city portland las memphis louisville baltimore milwaukee
albuquerque tucson fresno sacramento mesa atlanta omaha springs raleigh miami long beach oakland
minneapolis tulsa tampa arlington orleans wichita cleveland bakersfield anaheim honolulu santa
riverside corpus christi lexington henderson stockton saint st cincinnati pittsburgh greensboro
anchorage plano irvine newark durham chula vista toledo petersburg laredo chandler lubbock scottsdale
reno buffalo gilbert glendale winston salem chesapeake norfolk fremont garland irving hialeah richmond
boise spokane baton rouge tacoma bernardino modesto fontana des moines moreno clarita fayetteville
birmingham oxnard rochester port lucie grand rapids huntsville salt lake frisco yonkers amarillo
huntington mckinney montgomery augusta akron little rock tempe overland prairie tallahassee cape coral
mobile knoxville shreveport worcester ontario vancouver sioux falls chattanooga brownsville lauderdale
providence newport rancho cucamonga peoria oceanside elk grove pembroke pines garden cary collins
corona springfield alexandria hayward clarksville lakewood lancaster salinas palmdale hollywood
springdale macon sunnyvale pomona killeen escondido pasadena naperville bellevue joliet murfreesboro
midland rockford paterson bridgeport torrance mcallen syracuse surprise denton roseville thornton
miramar mesquite olathe dayton carrollton waco orange fullerton charleston visalia hampton gainesville
cedar heights stamford concord hartford lafayette athens berkeley boulder burbank malibu hills palo
alto cupertino mountain view menlo marina venice queens bronx manhattan staten harlem hoboken albany
ithaca princeton cambridge somerville annapolis bethesda tysons georgetown asheville myrtle hilton head
key keys destin sarasota naples clearwater daytona boca raton palm aspen vail taos sedona flagstaff
yuma juneau fairbanks maui oahu kona hilo napa sonoma tahoe yosemite monterey carmel ventura cruz
bozeman missoula billings cheyenne fargo bismarck duluth arbor flint lansing kalamazoo green evanston
dearborn champaign urbana bloomington davenport topeka branson galveston odessa abilene harrisburg
allentown scranton erie burlington bangor nantucket cod vineyard plymouth lowell provo ogden laramie fe""")

# countries (the multi-word ones by their parts)
words("""afghanistan albania algeria andorra angola antigua barbuda argentina armenia australia austria
azerbaijan bahamas bahrain bangladesh barbados belarus belgium belize benin bhutan bolivia bosnia
herzegovina botswana brazil brunei bulgaria burkina faso burundi cambodia cameroon canada verde central
african republic chile china colombia comoros congo costa rica croatia cuba cyprus czech czechia
denmark djibouti dominica dominican ecuador egypt equatorial guinea eritrea estonia eswatini swaziland
ethiopia fiji finland france gabon gambia germany ghana greece grenada guatemala bissau guyana haiti
honduras hungary iceland indonesia iran iraq ireland israel italy ivory jamaica japan kazakhstan
kiribati korea kosovo kuwait kyrgyzstan laos latvia lebanon lesotho liberia libya liechtenstein
lithuania luxembourg madagascar malawi malaysia maldives mali malta islands mauritania mauritius
micronesia moldova monaco mongolia montenegro morocco mozambique myanmar burma namibia nauru nepal
netherlands holland zealand nicaragua niger nigeria macedonia norway oman pakistan palau palestine
panama papua paraguay peru philippines poland portugal qatar romania russia rwanda kitts nevis
grenadines samoa marino sao tome principe saudi arabia senegal serbia seychelles leone singapore
slovakia slovenia solomon somalia sudan spain sri lanka suriname sweden switzerland syria taiwan
tajikistan tanzania thailand timor togo tonga trinidad tobago tunisia turkey turkiye turkmenistan
tuvalu uganda ukraine emirates uae uk britain england scotland wales united kingdom uruguay uzbekistan
vanuatu vatican venezuela vietnam yemen zambia zimbabwe greenland kong macau tibet bermuda aruba
curacao tahiti caribbean scandinavia europe asia oceania antarctica arctic balkans siberia sahara
middle latin americas eurasia""")

# world cities (the multi-word ones by their parts)
words("""london paris tokyo beijing shanghai delhi mumbai bombay bangalore bengaluru kolkata chennai hyderabad
karachi lahore islamabad dhaka seoul busan osaka kyoto yokohama taipei manila jakarta bangkok hanoi
saigon ho chi kuala lumpur melbourne brisbane perth adelaide auckland wellington toronto montreal
calgary ottawa edmonton winnipeg quebec halifax guadalajara monterrey tijuana cancun havana bogota
medellin lima buenos aires rio janeiro paulo brasilia caracas quito berlin munich hamburg frankfurt
cologne vienna zurich geneva amsterdam rotterdam brussels madrid barcelona seville valencia lisbon
porto rome milan florence turin istanbul ankara moscow kyiv kiev warsaw krakow prague budapest
bucharest belgrade zagreb dublin belfast edinburgh glasgow manchester liverpool leeds bristol oxford
copenhagen stockholm oslo helsinki reykjavik cairo lagos abuja nairobi addis ababa johannesburg town
durban casablanca marrakech tunis accra dakar kinshasa dubai abu dhabi doha riyadh jeddah mecca medina
tehran baghdad beirut damascus amman jerusalem tel aviv kabul tashkent almaty ulaanbaatar kathmandu
colombo shenzhen guangzhou chengdu wuhan xian nanjing hangzhou pyongyang phnom penh vientiane yangon
bali phuket marseille lyon nice bordeaux salzburg ibiza mallorca""")

# nationalities and peoples (nouns: americans, mexicans)
nouns("""american mexican canadian brazilian argentinian argentine colombian venezuelan peruvian chilean cuban
rican salvadoran guatemalan honduran nicaraguan jamaican haitian bahamian australian austrian belgian
bulgarian croatian estonian european hungarian indonesian italian korean latvian lithuanian malaysian
mongolian moroccan nigerian norwegian persian romanian russian serbian syrian ukrainian algerian
egyptian ethiopian kenyan ghanaian somali sudanese tanzanian ugandan asian indian pakistani bangladeshi
afghan iranian iraqi israeli jordanian lebanese palestinian yemeni emirati qatari kuwaiti filipino
filipina thai cambodian laotian samoan hawaiian texan californian floridian yorker southerner
northerner midwesterner latino latina latinx hispanic arab german greek dane swede pole slovak slovene
scot brit icelander kiwi aussie yank yankee alaskan canuck""")

# nationalities and languages without a plural in common use (words: exactly as written)
words("""english british french spanish portuguese chinese japanese vietnamese taiwanese burmese nepalese
senegalese congolese irish scottish welsh dutch swiss swedish danish finnish polish slovenian turkish
kurdish arabic hebrew yiddish hindi urdu bengali punjabi gujarati marathi tamil telugu kannada
malayalam sinhala farsi pashto dari mandarin cantonese hokkien tagalog lao khmer malay swahili amharic
yoruba igbo hausa zulu xhosa afrikaans esperanto creole patois gaelic navajo cherokee lakota ojibwe
inuit maori quechua guarani aztec mayan inca celtic nordic norse viking scandinavian slavic baltic
balkan anglo saxon pacific islander indigenous native aboriginal bosnian albanian armenian georgian
azerbaijani kazakh uzbek tibetan uyghur hmong""")

# ---------------------------------------------------------------------------------------------------------------
# (4) brands, apps, games, platforms, products, sports
# ---------------------------------------------------------------------------------------------------------------

# apps and platforms
words("""tiktok tiktoks tiktoker tiktokers instagram insta snapchat snap snaps snapped snapping snapstreak
discord youtube youtuber youtubers yt netflix hulu disney disneyplus hbo peacock paramount crunchyroll
spotify pandora soundcloud applemusic itunes twitch twitter tweets tweeted tweeting x reddit redditor
redditors subreddit subreddits facebook fb messenger whatsapp telegram signal wechat line kakao viber
skype facetime imessage tumblr pinterest linkedin threads bluesky mastodon vine vsco bereal tinder
bumble hinge grindr okcupid match uber lyft doordash grubhub postmates instacart airbnb venmo cashapp
paypal zelle robinhood coinbase duolingo quizlet canva gmail outlook bing google googled googling
wikipedia wiki imdb amazon ebay etsy craigslist shein temu wish alibaba aliexpress chatgpt gpt openai
claude anthropic gemini copilot siri cortana bixby midjourney wattpad goodreads kindle audible substack
patreon onlyfans kickstarter gofundme roku chromecast firestick slack teams notion trello dropbox
icloud onedrive wifi bluetooth hotspot""")

# tech companies and devices
words("""apple microsoft samsung sony nintendo tesla nvidia intel amd ibm dell hp lenovo asus acer huawei xiaomi
oneplus motorola nokia lg pixel iphone iphones ipad ipads ipod ipods imac imacs macbook macbooks
airpods airpod applewatch android androids galaxy chromebook chromebooks thinkpad alienware razer
logitech corsair steelseries gopro fitbit garmin beats bose jbl sonos windows mac macos ios linux
ubuntu chrome firefox safari edge excel powerpoint photoshop spacex starlink xbox playstation ps ps2
ps3 ps4 ps5 psp psvita vita wii wiiu switch gameboy nes snes gamecube oculus quest vr steam steamdeck
epic""")

# games
words("""minecraft fortnite roblox valorant overwatch apex legends league dota csgo cs counterstrike callofduty
warzone halo gta pokemon pikachu sonic kirby metroid smash splatoon animal crossing tetris pacman sims
skyrim fallout elden ring darksouls souls witcher cyberpunk diablo warcraft wow hearthstone starcraft
rocket among amongus fallguys pubg freefire genshin impact hades undertale terraria stardew valley
hollow knight cuphead portal doom tf2 rainbow siege rust ark dayz palworld baldurs gate bg3 mtg magic
yugioh pokemongo chess checkers sudoku wordle monopoly uno scrabble jenga twister clue candyland catan
dnd dungeons dragons warhammer fifa madden nba2k 2k mlb nhl rocketleague fnaf poppy playtime geoguessr
osu hitman tomb raider uncharted spiderman batman superman marvel avengers ironman starwars jedi sith
yoda trek pokedex""")

# stores, restaurants, food and drink brands
words("""walmart target costco kroger publix safeway albertsons aldi lidl wegmans heb meijer trader joes
wholefoods whole foods sams club bestbuy homedepot lowes ikea macys nordstrom kohls jcpenney sears
tjmaxx marshalls gap oldnavy uniqlo forever21 hollister abercrombie aeropostale sephora ulta nike
adidas puma reebok converse vans jordans yeezy yeezys crocs uggs skechers newbalance underarmour
lululemon patagonia northface supreme gucci prada chanel vuitton balenciaga versace dior rolex cvs
walgreens riteaid dollar tree general dollarama gamestop mcdonalds mcdonald mcds maccas burger wendys
tacobell taco bell kfc subway chipotle chickfila popeyes arbys dairy dq whataburger innout shake shack
fiveguys jackinthebox carls culvers starbucks dunkin dunkies timhortons timmies panera pizza hut
dominos papajohns littlecaesars olivegarden applebees chilis ihop dennys wafflehouse crackerbarrel
outback redlobster wild wings bww pandaexpress panda express wingstop raisingcanes canes jollibee qdoba
moes coke cocacola pepsi sprite fanta drpepper mtn dew mountaindew gatorade powerade redbull monster
celsius prime bang lacroix starburst skittles snickers twix kitkat reeses mms oreo oreos doritos
cheetos takis pringles lays fritos funyuns ruffles hersheys nutella cheerios froot loops frosted flakes
pop tarts poptarts eggo lunchables ramen cup noodles spam kraft heinz velveeta jello pocky boba""")

# cars and vehicles
words("""toyota honda ford chevy chevrolet dodge jeep ram gmc cadillac buick chrysler nissan mazda subaru
hyundai kia volkswagen vw audi bmw benz porsche ferrari lamborghini lambo maserati bugatti volvo lexus
acura infiniti mitsubishi rivian prius civic corolla camry accord mustang camaro corvette wrangler f150
ducati kawasaki yamaha vespa""")

# sports leagues, events, a few big team nicknames
words("""nfl nba wnba mls ncaa ufc wwe nascar pga lpga uefa espn olympics olympic olympian olympians paralympics
superbowl super bowl worldcup world worldseries march madness finals playoffs wimbledon formula f1 indy
indycar xgames premier laliga bundesliga seriea lakers celtics warriors bulls knicks nets heat spurs
mavs mavericks rockets suns clippers sixers 76ers raptors bucks cavs cavaliers nuggets thunder
grizzlies pelicans hawks hornets pistons pacers wizards kings jazz blazers timberwolves wolves cowboys
patriots packers steelers eagles giants jets chiefs bears raiders niners 49ers broncos seahawks
dolphins bills ravens bengals browns colts texans titans jaguars jags saints falcons panthers
buccaneers bucs vikings lions commanders cardinals rams chargers yankees mets dodgers redsox sox cubs
braves astros phillies padres mariners orioles brewers twins guardians tigers royals rangers angels
athletics marlins nationals nats pirates reds rockies diamondbacks dbacks rays bluejays jays bruins
canadiens habs leafs blackhawks penguins flyers capitals caps oilers flames canucks avalanche avs
islanders devils sabres sharks ducks predators preds lightning barca arsenal tottenham juventus juve
psg bayern inter messi ronaldo""")

# a handful of public figures chat may mention by name
words("""trump biden obama bush kamala harris musk elon zuckerberg bezos gates swift swiftie swifties beyonce
rihanna drake kanye bieber eminem billie eilish oprah kardashian kardashians mrbeast pewdiepie einstein
shakespeare christ god allah buddha claus""")

# ---------------------------------------------------------------------------------------------------------------
# (5) holidays and culture words
# ---------------------------------------------------------------------------------------------------------------

# holidays and days
words("""thanksgiving thanksgivings christmas christmases xmas christmastime christmasy christmassy christmaseve
halloween halloweens hanukkah chanukah hannukah ramadan eid easter easters passover purim yom kippur
rosh hashanah diwali holi lunar newyear year years eve nye kwanzaa juneteenth valentines valentine
galentines memorial labor veterans presidents mlk independence fourth july cinco mayo mardi gras
carnival oktoberfest stpatricks patricks paddys groundhog earth mothers fathers grandparents boxing
advent lent ash wednesday good friday sunday pentecost epiphany solstice equinox dia muertos
quinceanera quince bar bat mitzvah mitzvahs sabbath shabbat sukkot lohri navratri durga puja vesak
nowruz songkran tet obon pride blackfriday cybermonday spring break prom homecoming graduation
commencement""")

# religions and culture words
words("""christians christianity catholic catholics catholicism protestant protestants baptist baptists
methodist methodists lutheran lutherans presbyterian mormon mormons evangelical evangelicals orthodox
jewish jew jews judaism muslim muslims islam islamic hindu hindus hinduism buddhist buddhists buddhism
sikh sikhs sikhism jain taoism taoist shinto atheist atheists agnostic agnostics pagan pagans wiccan
bible quran koran torah talmud gospel church mosque synagogue temple menorah dreidel latkes kosher
halal iftar suhoor diya rangoli rudolph reindeer elf elves mistletoe eggnog gingerbread stocking
stockings grinch scrooge frosty jackolantern lantern trick treat trickortreat costume costumes pilgrim
pilgrims cornucopia anime manga otaku kpop jpop kdrama kdramas cosplay cosplayer cosplays fandom
fandoms fanfic fanfics fanart shipping ship otp waifu husbando weeb weebs isekai shonen shojo hiphop
rap rapper rappers edm emo goth gothic punk grunge indie hipster hipsters bts blackpink hogwarts potter
hobbit gandalf frodo narnia pixar dreamworks ghibli woke dei lgbt lgbtq lgbtqia queer trans nonbinary
enby cis cisgender pronouns""")
