"""Everyday English words Helmus reads as themselves. The typo rule (engine/helmus.py, _near) takes an unknown word one
edit from a known word for a typo of it; without this list, ordinary words the detectors happen not to use were read
as other words ("worry" as "sorry", "reason" as "season", "better" as "letter"). Only words of five letters or more
matter to the rule. Written by hand, from what people say in a quick chat; no outside word list."""
from gen.dsl import known

WHY = "an everyday word, read as itself and never as a typo of another word"

known("""
about above abroad absolutely accept accident account across action active actor actual actually added adding
address admit adult advance advice afraid after afternoon again against agree ahead alarm album alive allow allowed
almost alone along already alright although always amazing among amount angel angle angry animal ankle annoyed
another answer anxious anybody anymore anyone anything anyway anywhere apart apartment apple apply appointment april
argue argument around arrive artist asked asking asleep attack attention august aunt autumn avoid awake award aware
awesome awful awkward
babies backpack bacon badly baking balance balloon banana bands barely baseball basement basic basically basket
bathroom battery battle beach beans beard beautiful became because become becoming bedroom before began begin
beginning behind being believe belong below bench beside besides better between beyond bigger biggest birds
birthday biscuit bitter black blame blank blanket blind block blood blouse board boats bodies boring born borrow
bother bottle bottom bought bounce bowling brain brand brave bread break breakfast breath breathe brick bridge brief
bright bring broke broken brother brought brown brush bubble bucket budget build building built bunch burger burn
burned burning burnt business busy butter button buying
cabin cable calling calls calm camera camping cancel candle candy cannot capital captain career careful carry carrot
cartoon castle catch caught cause ceiling celebrate center central certain chain chair chance change changed
changing channel chapter charge charger charming chase cheap cheaper cheat check cheese chess chest chicken child
children chill chilling chips choice choose chose chosen church circle cities class classic clean cleaning clear
clearly clever click client climb clock close closed closer closet cloth clothes cloud cloudy coach coast coffee
colder collect college color colour comes comfy coming comment common company compare complain complete completely
computer concert confused contact contest control cookie cookies cooking corner correct costs couch cough could
count counter country couple course cousin cover cozy crack crazy cream create credit cried crowd crowded cruel
crying culture curious current curtain cutting
daddy daily damage dance dancer dancing danger dangerous daring darker dating daughter dealing death decide decided
deeply degree delete delivery dentist depends design desk dessert detail device diary dicey diesel diet differ
difference different difficult dinner direct direction dirty disagree discord dishes distance divide doctor doesnt
doing dollar dollars donut double doubt dozen drama drank drawing dream dreams dress dressed drink drinking drive
driver driving dropped drove drunk during dying
eager early earlier earth easier easily eaten eating editing effort eight eighteen either elbow elder eleven else
email empty ended ending enemy energy engine enjoy enjoyed enough enter entire episode equal error escape essay even
evening event events every everybody everyday everyone everything everywhere exact exactly exam example excited
exciting excuse exercise exist expect expensive explain extra
facts failed fairly faith falling false family famous fancy farmer father fault favor fears feeling feelings fellow
fewer field fifteen fifth fifty fight fighting figure filled final finally finger finish finished first fishing
fixed flight floor flower flowers follow followed food football forest forever forget forgot forgotten formal forth
forty forward found fourteen fourth freak freedom freeze french fresh friday fridge fried friend friendly friends
fright front frozen fruit funny furniture further future
gaming garage garden gather gently ghost giant given gives giving glass glasses gloves going golden goodbye gotten
grade grades grand grandma grandpa grass great greatest green greet groceries grocery ground group growing grown
guess guessing guest guitar
habit hairs half handle hands hanging happen happened happening happens happier happy harder hardly having heard
heart heavy height hello helped helpful helping herself hidden hiding higher highway himself history hobby holding
holiday holidays homework honest honestly honey hoodie hoping horse hospital hotel hours house houses however huge
human humor hundred hungry hurry hurts husband
ideas image imagine important inside instead interest interested internet invite island itself
jacket january jeans jelly joined joking journey judge juice july jumped jumping junior
keeping kidding killed kinda kitchen kitten knees knife knock knowing known
label ladder language large larger later laugh laughing launch lawyer layer lazy leader learn learned learning least
leave leaving left legal lemon length lesson letter letters level library light liked likely likes limit listen
listening little lived lives living local locked lonely longer looked looking loose lose losing lost loud lovely
lover lower lucky lunch lying
machine madam magic mainly major making manage manager march market married matter maybe meaning meant measure
media meeting member memory mental message messed metal middle might mighty minute minutes mirror missed missing
mistake mixed model modern moment monday money monkey month months moody morning mostly mother motor mountain mouse
mouth moved movie movies moving music myself
naked named names narrow nasty nation nature nearby nearly needed needs neighbor neither nephew nervous never newer
newest night nights nineteen ninety nobody noise noisy normal north nothing notice novel number numbers nurse
object obviously ocean october offer office often older online opened opening opinion orange order other others
otherwise ought ourselves outside overall owner
packed pages paint painting pants paper parent parents party passed passing pasta paying peace people pepper
perfect perhaps period person phone photo photos piano picked picture pictures piece pillow pizza place placed
plane plans plant plants plastic plate played player playing please pleased plenty pocket point police polite
pool poor popular pretty price prices print prison private prize probably problem problems promise proper proud
prove public pulled punch purple purpose pushed putting
quick quickly quiet quietly quite
rabbit radio raining rainy raise rather reach react reading ready really reason reasons recent recently record
reply report rescue resting return rich riding right river roast robot rocks rolled roommate round route rubber
rules running
sadly safer salad salty sample sandwich saturday sauce saved saving saying scared scary school science scored
scream screen search season second secret seeing seems seen selling semester sending sense serious seriously
server service settle seven seventeen several shake shall shape share shirt shoes shopping short shorts should
shoulder shout showed shower shows sibling siblings sick signed silent silly simple since singer singing single
sister sitting sixteen sixty sized skate skiing skills sleep sleeping sleepy slept slice slightly slowly small
smaller smart smell smile smoke snack snacks sneaky snow snowing social socks softly solid somebody someday somehow
someone something sometimes somewhere songs sorry sound sounds south space speak speaking special speed spell
spend spending spent spicy spoke spoon sport sports spring square stairs stand standing stare start started
starting state station stays steak steal steps stick still stomach stone stood stopped store stores storm story
straight strange stranger street stress stretch strict strong stuck student students studied study studying stuff
stupid style subject sucks sudden suddenly sugar summer sunday sunny super supper supply suppose supposed surely
surprise sweater sweet swimming
table taken takes taking talent talked talking taste tasty taught teach teacher teaching team tears teeth telling
tells temple tenth terms terrible test texas texted texting thank thanks thats their theirs them themselves there
these thing things think thinking third thirsty thirteen thirty those though thought thousand three threw throat
through throw thursday ticket tight tiger timer tired title toast today together toilet tomato tomorrow tongue
tonight touch tough towel tower town track trade traffic train trash travel treat trick tried tries trouble truck
truly trust truth trying tuesday turned turning twelve twenty twice under uncle understand unless until upset
upstairs usual usually
vacation value video videos village visit visiting voice wait waited waiting wake waking walked walking wallet
wanted wanting wants warm warmer washing watch watched watching water wearing weather wedding wednesday weekend
weekends weeks weight weird welcome whatever wheel whenever where wherever whether which while whisper white whole
whose window windows winner winter wishes within without woman women wonder wonderful woods words worked worker
working works world worried worry worse worst worth would wrong wrote
yeah yearly years yellow yesterday young younger yours yourself youth
""", WHY)
