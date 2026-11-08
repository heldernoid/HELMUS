"""Describing words and the closed classes: adjectives and adverbs, and every function word (pronouns, articles,
determiners, prepositions, conjunctions, auxiliaries and modals with their contractions, question words), number
words, days, months, seasons and common interjections. Hand-written.

adjectives() only for words whose rule-made -er, -est and -ly are all natural (nice nicer nicest nicely); longer
adjectives (more beautiful, not beautifuller) and those with odd forms go in words() with their real forms listed:
"beautiful beautifully", "good better best well". Contractions are listed with and without the apostrophe
(dont don't), since people type both."""
from gen.vocab import adjectives, words

# ===============================================================================================================
# (1) adjectives whose -er, -est and -ly come by the rules
# ===============================================================================================================

# feelings and moods
adjectives("""happy unhappy sad glad mad angry lucky unlucky grumpy cranky moody jumpy edgy giddy cheery merry
sleepy hungry thirsty sick calm proud brave bold fond tense weary wary needy greedy nosy cocky sassy salty petty
grouchy sulky touchy testy feisty sappy snappy uneasy queasy woozy dizzy teary leery peppy perky groggy huffy grim
glum smug meek sore""")

# personality: kind, mean and everything between
adjectives("""nice kind mean smart dumb stupid wise clever bright sharp quick slow lazy busy rude polite cruel crazy
weird odd strange witty nasty sweet humble gentle simple noble subtle able feeble nimble fierce tough rough harsh
stern strict sane lame shrewd brash rash blunt frank curt terse crude lewd quiet loud noisy cheeky crafty sneaky
shifty bossy fussy picky choosy clingy pushy preachy snarky quirky wacky zany kooky nutty loopy batty goofy nerdy
geeky dorky corny cheesy catty bitchy chatty flirty sporty arty brainy gutsy gruff prim naughty haughty flighty
mighty worthy unworthy hardy sturdy plucky spunky canny uncanny wily freaky""")

# looks and bodies
adjectives("""pretty cute hot handsome fat thin slim skinny chubby plump lean short tiny huge large neat tidy untidy
messy scruffy shaggy hairy bald fair dark sexy fit strong weak stocky lanky scrawny brawny bony puny pudgy dumpy
frumpy leggy rosy ruddy dainty sweaty curvy""")

# money, price, worth
adjectives("""cheap rich poor wealthy healthy unhealthy thrifty stingy fancy classy flashy trashy tacky snazzy
swanky spiffy nifty natty dressy posh plush lush showy""")

# size, shape, depth, distance
adjectives("""wide narrow deep shallow broad flat round near steep thick dense vast high low tight loose bumpy lumpy
hollow close sparse scant slight ample great grand bulky chunky hefty""")

# weather and temperature
adjectives("""cold warm cool icy sunny cloudy rainy windy snowy foggy stormy misty muggy wet damp mild balmy breezy
hazy frosty gloomy dreary dusky gusty steamy sultry soggy starry""")

# touch and texture
adjectives("""soft hard smooth silky fluffy fuzzy sticky slimy slippery greasy oily crunchy crispy chewy juicy
creamy squishy mushy grainy gritty itchy scratchy stiff firm tender crisp springy spongy stretchy furry scaly sandy
rocky stony muddy dusty rusty grimy dirty filthy clean frizzy bushy baggy saggy""")

# taste and smell
adjectives("""sour bitter spicy tasty yummy bland fresh ripe smelly stinky fishy fruity zesty tangy minty smoky
meaty hearty savory savoury boozy milky fizzy musty""")

# light, sight and sound
adjectives("""dim light faint shiny glossy murky blurry hoarse husky raspy squeaky creaky tinny""")

# how things are: quality, ease, safety, truth
adjectives("""fine rare common dear sure real safe unsafe clear plain pure free easy tricky handy heavy brief bare
scarce tame wild steady unsteady ready hasty shaky risky pesky dodgy sketchy shady seedy flaky crappy shitty lousy
gross foul bleak stark grave vague apt deft swift brisk keen late""")

# comfort, mess, condition
adjectives("""comfy cozy cosy roomy stuffy drafty draughty leaky shabby tatty ratty grubby mucky yucky icky soapy
foamy""")

# more -y adjectives for things and people
adjectives("""funny runny whiny thorny tawny bloody woody wordy tardy gaudy bawdy rowdy trendy bendy dandy jerky
funky clunky frisky dreamy grassy glassy mossy brassy gassy drowsy jazzy sleazy wheezy catchy patchy twitchy gushy
cushy spiny briny hilly frilly chilly curly surly cuddly scary racy lacy bouncy saucy mousy weedy speedy pasty
crusty trusty puffy craggy buggy""")

# other short adjectives
adjectives("""blind coarse deaf frail moist numb quaint slack sleek slick snug stout taut trim wan staunch tart lax""")

# ===============================================================================================================
# (2) short adjectives whose forms the rules get wrong: listed in full
# ===============================================================================================================

# irregular comparison
words("""good better best well bad worse worst badly far farther farthest further furthest littler littlest fewer
fewest old older oldest elder eldest ill""")

# -er and -est fine, but no -ly in use (or an -ly that means something else)
words("""big bigger biggest small smaller smallest tall taller tallest long longer longest young younger youngest
fast faster fastest fun funner funnest red redder reddest raw rawer rawest fake faker fakest""")

# ending in -ll, -le, -ue or a lone -y, where the rules would misspell a form
words("""full fuller fullest fully dull duller dullest dully shrill shriller shrillest shrilly chill chiller
chillest still stiller stillest pale paler palest palely stale staler stalest vile viler vilest vilely whole wholly
true truer truest truly due duly shy shyer shyest shyly sly slyer slyest slyly dry drier driest dryer dryest dryly
drily spry spryer spryest wry wryly sheer sheerly gooey gooier gooiest dopey dopier dopiest pricey pricier priciest
dicey dicier diciest phony phoney phonier phoniest homey homier homiest""")

# adjectives that end in -ly themselves
words("""friendly friendlier friendliest unfriendly lonely lonelier loneliest lovely lovelier loveliest ugly uglier
ugliest likely likelier likeliest unlikely lively livelier liveliest deadly deadlier deadliest costly costlier
costliest silly sillier silliest early earlier earliest holy holier holiest bubbly wobbly wobblier wobbliest prickly
pricklier prickliest wrinkly crumbly sparkly squiggly jolly jollier jolliest burly burlier unruly elderly orderly
disorderly cowardly heavenly ghastly ghostly kindlier manly manlier womanly homely homelier lowlier sicklier timely
untimely beastly saintly scholarly shapely motherly fatherly brotherly sisterly neighborly neighbourly worldly
earthly godly ungodly stately leisurely courtly comely gangly measly""")

# right, wrong and a few other plain ones
words("""right rightly wrong wrongly upset eager eagerly proper properly improper improperly chic sole solely mere
merely utter utterly dire direly severe severely sincere sincerely insincere mature immature extreme extremely
supreme supremely obscure obscurely secure securely insecure insecurely naive naively""")

# colors (no -ly in use), shades and the -ish words
words("""blue bluer bluest green greener greenest yellow yellower orange purple purpler pink pinker pinkest brown
browner black blacker blackest white whiter whitest gray grey grayer greyer beige teal turquoise aqua maroon navy
violet indigo lavender lilac magenta crimson scarlet burgundy golden gold silver silvery bronze copper ivory cream
khaki olive mint peach coral salmon tan rainbow neon pastel colorless colourless blonde blond brunette ginger auburn
reddish bluish blueish greenish yellowish brownish pinkish purplish grayish greyish whitish blackish orangey oldish
youngish smallish biggish longish tallish shortish""")

# ===============================================================================================================
# (3) longer adjectives (they take "more" and "most"), each with its -ly form where one is in use
# ===============================================================================================================

# -ful
words("""beautiful beautifully careful carefully helpful helpfully hopeful hopefully thankful thankfully grateful
gratefully cheerful cheerfully colorful colourful colorfully colourfully peaceful peacefully powerful powerfully
successful successfully unsuccessful unsuccessfully useful usefully wonderful wonderfully awful awfully painful
painfully playful playfully respectful respectfully disrespectful disrespectfully stressful thoughtful thoughtfully
truthful truthfully faithful faithfully joyful joyfully mindful mindfully meaningful meaningfully skillful skilful
skillfully skilfully tasteful tastefully distasteful wasteful wastefully harmful harmfully hateful hatefully
forgetful forgetfully fearful fearfully graceful gracefully disgraceful disgracefully delightful delightfully
dreadful dreadfully doubtful doubtfully resentful resentfully regretful regretfully restful shameful shamefully
spiteful spitefully boastful boastfully watchful watchfully youthful youthfully eventful uneventful fruitful
fruitfully fruitless lawful lawfully unlawful unlawfully rightful rightfully sinful plentiful plentifully merciful
mercifully pitiful pitifully fanciful dutiful dutifully masterful forceful forcefully mournful mournfully tearful
tearfully woeful woefully blissful blissfully deceitful deceitfully insightful neglectful purposeful purposefully
soulful soulfully wishful wishfully bashful bashfully""")

# -less
words("""careless carelessly helpless helplessly hopeless hopelessly useless uselessly endless endlessly homeless
pointless pointlessly harmless harmlessly fearless fearlessly heartless heartlessly mindless mindlessly restless
restlessly reckless recklessly ruthless ruthlessly selfless selflessly shameless shamelessly sleepless speechless
spotless spotlessly thoughtless thoughtlessly tireless tirelessly worthless clueless cluelessly countless priceless
timeless flawless flawlessly effortless effortlessly breathless breathlessly jobless lifeless limitless meaningless
needless needlessly painless painlessly powerless relentless relentlessly seamless seamlessly senseless senselessly
shapeless spineless tactless tasteless toothless weightless childless friendless aimless aimlessly baseless
boundless faceless gutless hapless heedless merciless mercilessly nameless pitiless motionless odorless odourless
penniless doubtless wireless cordless sugarless sleeveless strapless backless brainless witless humorless humourless
loveless joyless cheerless fatherless motherless""")

# -ous
words("""nervous nervously famous famously infamous serious seriously curious curiously dangerous dangerously
delicious deliciously anxious anxiously jealous jealously generous generously obvious obviously previous previously
variously enormous enormously ridiculous ridiculously gorgeous gorgeously fabulous fabulously hilarious hilariously
mysterious mysteriously numerous religious religiously furious furiously glorious gloriously precious gracious
graciously ungracious spacious cautious cautiously conscious consciously unconscious unconsciously ambitious
ambitiously suspicious suspiciously courageous courageously outrageous outrageously disastrous disastrously envious
enviously ferocious ferociously hideous hideously humorous humorously joyous joyously luxurious luxuriously
marvelous marvellous marvelously marvellously monstrous nauseous notorious notoriously obnoxious obnoxiously ominous
ominously pompous pompously rigorous rigorously spontaneous spontaneously strenuous tedious tediously tremendous
tremendously vicious viciously virtuous zealous adventurous adventurously anonymous anonymously continuous
continuously contagious delirious devious dubious dubiously fictitious flirtatious frivolous harmonious hazardous
ingenious ingeniously malicious maliciously meticulous meticulously miraculous miraculously mischievous
mischievously momentous mountainous nutritious oblivious poisonous preposterous prestigious prosperous rambunctious
rebellious ravenous ravenously scandalous scrupulous unscrupulous scrumptious simultaneous simultaneously studious
superstitious treacherous tumultuous unanimous unanimously vigorous vigorously voluptuous wondrous callous
conspicuous conspicuously inconspicuous fortuitous gluttonous gregarious homogeneous impervious incredulous
ludicrous ludicrously luminous melodious obsequious perilous precarious precariously presumptuous pretentious
raucous sumptuous tenuous vivacious cantankerous salacious audacious audaciously capricious""")

# -ive
words("""active actively inactive passive passively creative creatively positive positively negative negatively
expensive expensively inexpensive attractive attractively unattractive aggressive aggressively effective effectively
ineffective defensive defensively offensive offensively impressive impressively unimpressive massive massively
sensitive sensitively insensitive excessive excessively exclusive exclusively extensive extensively intensive
intuitive intuitively productive productively unproductive counterproductive protective protectively competitive
competitively supportive talkative destructive decisive decisively indecisive expressive inclusive innovative
interactive inventive objective objectively subjective subjectively perceptive persuasive persuasively possessive
progressive relative relatively repetitive respective respectively selective selectively submissive alternative
alternatively comprehensive conservative conservatively constructive constructively cooperative cumulative
descriptive distinctive distinctively elusive explosive impulsive impulsively informative intrusive lucrative
manipulative obsessive obsessively pensive primitive provocative reflective responsive unresponsive restrictive
secretive secretively seductive suggestive tentative tentatively attentive attentively inattentive addictive abusive
abrasive affirmative captive collective collectively consecutive consecutively deceptive deceptively definitive
definitively disruptive evasive exhaustive festive furtive furtively imaginative instinctive instinctively
inquisitive pervasive preventive proactive proactively receptive retroactive defective native expansive""")

# -al
words("""normal normally abnormal natural naturally unnatural actual actually usual usually unusual unusually
special specially especially personal personally general generally typical typically total totally final finally
local locally social socially legal legally illegal illegally original originally formal formally informal
informally casual casually equal equally unequal central centrally critical critically physical physically mental
mentally emotional emotionally political politically practical practically impractical logical logically illogical
magical magically musical musically medical medically national nationally international internationally professional
professionally unprofessional traditional traditionally additional additionally essential essentially exceptional
exceptionally financial financially global globally ideal ideally individual individually initial initially
intentional intentionally unintentional unintentionally internal internally external externally literal literally
mutual mutually occasional occasionally official officially unofficial optional partial partially impartial
potential potentially rational rationally irrational seasonal sexual sexually spiritual spiritually technical
technically tropical verbal verbally virtual virtually visual visually vital vitally brutal brutally crucial
crucially fatal fatally loyal loyally disloyal royal royally fundamental fundamentally environmental experimental
instrumental monumental sentimental sentimentally accidental accidentally coincidental incidental incidentally
horizontal horizontally vertical vertically identical identically classical comical comically cynical cynically
ethical ethically unethical historical historically hysterical hysterically radical radically tactical theoretical
theoretically hypothetical hypothetically whimsical economical economically clinical clinically conventional
conventionally unconventional eventual eventually factual gradual gradually habitual habitually intellectual
intellectually manual manually marginal marginally minimal minimally neutral neutrally annual annually perpetual
perpetually punctual punctually substantial substantially superficial superficially trivial universal universally
unconditional unconditionally conditional controversial commercial commercially confidential confidentially
beneficial cordial cordially digital digitally dual frugal frugally immortal mortal moral morally immoral liberal
liberally oral orally phenomenal phenomenally regal rural skeptical sceptical skeptically sceptically surgical
theatrical theatrically tribal viral vocal vocally colossal abysmal abysmally dismal dismally civil civilly uncivil
evil""")

# -ic
words("""basic basically tragic tragically specific specifically scientific scientifically realistic realistically
unrealistic dramatic dramatically romantic romantically fantastic fantastically terrific terrifically automatic
automatically classic iconic ironic ironically sarcastic sarcastically enthusiastic enthusiastically unenthusiastic
energetic energetically pathetic pathetically sympathetic sympathetically unsympathetic authentic authentically
artistic athletic chaotic democratic dynamic economic electric electronic epic epically exotic generic genetic
graphic graphically heroic heroically historic idiotic magnetic manic melodic metallic mystic narcissistic nostalgic
optimistic optimistically pessimistic pessimistically organic organically patriotic photogenic poetic poetically
problematic public publicly psychotic sporadic sporadically static strategic strategically systematic systematically
toxic traumatic aesthetic aesthetically ecstatic emphatic emphatically eccentric frantic frantically gigantic hectic
hygienic majestic idealistic materialistic simplistic characteristic characteristically charismatic diplomatic
diplomatically domestic drastic drastically elastic ethnic fanatic linguistic moronic neurotic pragmatic
pragmatically psychedelic robotic rustic scenic sonic symbolic symbolically therapeutic volcanic acidic alcoholic
allergic angelic arctic atomic barbaric bombastic catastrophic cinematic cosmic cryptic cryptically dyslexic erratic
erratically euphoric galactic gothic holistic intrinsic intrinsically lyrical periodic periodically platonic
prolific psychic stoic academic academically analytic analytical analytically apologetic apologetically arthritic
asthmatic autistic bureaucratic chronic chronically comic""")

# -able and -ible
words("""comfortable comfortably uncomfortable uncomfortably possible possibly impossible impossibly terrible
terribly horrible horribly incredible incredibly responsible responsibly irresponsible irresponsibly reasonable
reasonably unreasonable unreasonably available unavailable acceptable acceptably unacceptable adorable adorably
affordable agreeable believable unbelievable unbelievably capable capably incapable considerable considerably
dependable desirable undesirable enjoyable favorable favourable favorably favourably unfavorable flexible inflexible
inevitable inevitably invisible visible visibly legible illegible miserable miserably notable notably noticeable
noticeably probable improbable predictable predictably unpredictable reliable reliably unreliable remarkable
remarkably respectable sensible sensibly suitable suitably unsuitable valuable vulnerable understandable
understandably undeniable undeniably admirable admirably applicable avoidable unavoidable unavoidably bearable
unbearable unbearably breakable unbreakable charitable debatable disposable durable edible inedible excitable
fashionable fashionably unfashionable formidable honorable honourable honorably honourably dishonorable hospitable
inhospitable imaginable unimaginable accessible inaccessible audible inaudible compatible incompatible credible
credibly curable incurable deplorable despicable disagreeable doable eligible ineligible enviable excusable
inexcusable inexcusably fallible infallible feasible forgivable unforgivable gullible habitable impeccable
impeccably indispensable inflatable invaluable irritable justifiable knowledgeable laughable laughably likable
likeable unlikable lovable loveable unlovable manageable unmanageable memorable unmemorable negotiable palatable
passable permissible personable plausible plausibly implausible portable presentable profitable unprofitable
questionable questionably readable unreadable recognizable recognisable unrecognizable regrettable regrettably
relatable reputable reversible irreversible irreversibly sociable unsociable stable stably unstable tangible
intangible tolerable intolerable unthinkable usable unusable viable washable wearable workable unworkable
inseparable insatiable approachable unapproachable comparable comparably incomparable irresistible irresistibly
indestructible invincible susceptible incomprehensible fixable unfixable bendable foldable rechargeable replaceable
irreplaceable reusable shareable stackable adjustable sustainable unsustainable renewable""")

# -ent and -ant
words("""different differently indifferent indifferently important importantly unimportant confident confidently
intelligent intelligently unintelligent patient patiently impatient impatiently decent decently indecent innocent
innocently efficient efficiently inefficient sufficient sufficiently insufficient excellent excellently brilliant
brilliantly elegant elegantly pleasant pleasantly unpleasant unpleasantly significant significantly insignificant
relevant irrelevant constant constantly consistent consistently inconsistent independent independently dependent
apparent apparently evident evidently frequent frequently infrequent permanent permanently recent recently current
currently urgent urgently violent violently nonviolent silent silently absent ancient arrogant arrogantly abundant
abundantly adamant adamantly ambivalent benevolent blatant blatantly buoyant competent competently incompetent
convenient conveniently inconvenient defiant defiantly deficient diligent diligently distant distantly dominant
eloquent eloquently extravagant extravagantly fluent fluently fragrant gallant hesitant hesitantly ignorant imminent
inherent inherently insistent intermittent intermittently lenient militant negligent nonchalant nonchalantly
obedient obediently disobedient opulent persistent persistently prevalent prominent prominently prudent radiant
redundant reluctant reluctantly resilient resistant stagnant succulent tolerant intolerant transparent turbulent
vacant vibrant vigilant coherent incoherent complacent equivalent fervent fervently flamboyant flagrant flagrantly
fraudulent fraudulently impudent indignant indignantly insolent magnificent magnificently malignant nonexistent
omnipresent pertinent poignant poignantly pregnant proficient subsequent subsequently stringent transient triumphant
triumphantly valiant extroverted introverted""")

# -ing adjectives
words("""amazing amazingly interesting interestingly uninteresting boring boringly exciting excitingly unexciting
annoying annoyingly surprising surprisingly unsurprisingly shocking shockingly disgusting disgustingly embarrassing
embarrassingly frustrating frustratingly confusing confusingly charming charmingly loving lovingly caring uncaring
stunning stunningly astonishing astonishingly convincing convincingly unconvincing depressing depressingly
disappointing disappointingly encouraging encouragingly discouraging fascinating fascinatingly frightening
frighteningly inspiring uninspiring overwhelming overwhelmingly refreshing refreshingly relaxing satisfying
satisfyingly unsatisfying terrifying terrifyingly thrilling worrying worryingly heartbreaking heartbreakingly
heartwarming insulting irritating irritatingly knowing knowingly unknowingly willing willingly unwilling unwillingly
promising pleasing revealing striking strikingly tempting threatening threateningly touching understanding fitting
fittingly exhausting alarming alarmingly appalling appallingly captivating compelling compellingly daring daringly
deafening demanding devastating devastatingly dazzling distressing entertaining exhilarating gripping grueling
gruelling haunting hauntingly humiliating inviting invigorating mesmerizing mesmerising outstanding outstandingly
overbearing pressing rewarding soothing soothingly sparkling startling startlingly thriving unassuming upsetting
welcoming unwelcoming calming comforting comfortingly disturbing disturbingly intimidating intriguing intriguingly
maddening maddeningly nauseating outgoing easygoing hardworking breathtaking breathtakingly mouthwatering""")

# -ed adjectives: feelings (with their -ly where it is used)
words("""excited excitedly unexcited tired bored interested uninterested disinterested worried worriedly scared
annoyed confused confusedly surprised shocked amazed disappointed embarrassed frustrated stressed relaxed pleased
displeased satisfied dissatisfied unsatisfied ashamed determined determinedly concerned unconcerned delighted
depressed exhausted frightened horrified impressed unimpressed inspired motivated unmotivated overwhelmed puzzled
relieved terrified thrilled devoted devotedly heartbroken homesick lovesick starving stuffed hungover sober tipsy
drunk wasted stoked pumped hyped psyched bummed peeved pissed miffed fed offended insulted hurt jaded spoiled spoilt
obsessed hooked addicted attached detached conflicted torn content contented discontented""")

# -ed adjectives: how people and things are
words("""reserved reservedly supposed supposedly alleged allegedly marked markedly decided decidedly undecided
assured assuredly undoubted undoubtedly hurried hurriedly unhurried heated heatedly guarded guardedly reported
reportedly repeated repeatedly pointed pointedly expected unexpected unexpectedly advanced complicated uncomplicated
sophisticated unsophisticated dedicated detailed educated uneducated experienced inexperienced qualified unqualified
talented untalented skilled unskilled gifted crowded overcrowded wicked wickedly naked rugged ruggedly ragged jagged
crooked beloved learned aged blessed cursed doomed damned broken unbroken frozen rotten hidden open openly closed
sudden suddenly wooden woolen woollen molten stolen sunken swollen shaven unshaven drunken mistaken forsaken
forgotten unspoken outspoken organized organised disorganized disorganised unorganized focused unfocused balanced
unbalanced biased unbiased limited unlimited related unrelated renowned celebrated distinguished refined polished
civilized civilised unprecedented unparalleled unrivaled unrivalled varied assorted mixed muddled tangled twisted
bent curved rounded packed jammed loaded stacked deserted abandoned isolated secluded sheltered crowned armed
unarmed""")

# -ate, -ite, -ete and other Latin-shaped adjectives
words("""accurate accurately inaccurate inaccurately adequate adequately inadequate appropriate appropriately
inappropriate inappropriately approximate approximately compassionate compassionately considerate considerately
inconsiderate deliberate deliberately delicate delicately desperate desperately fortunate fortunately unfortunate
unfortunately immediate immediately intimate intimately legitimate legitimately illegitimate moderate moderately
obstinate passionate passionately dispassionate private privately separate separately ultimate ultimately intricate
intricately irate literate illiterate ornate innate affectionate affectionately articulate articulately inarticulate
corporate desolate disparate elite temperate proportionate disproportionate obsolete complete completely incomplete
concrete discrete discreet discreetly indiscreet absolute absolutely entire entirely definite definitely indefinite
indefinitely infinite infinitely finite exquisite exquisitely favorite favourite impolite impolitely trite contrite
remote remotely obtuse profuse profusely diffuse abstruse concise concisely precise precisely imprecise intense
intensely immense immensely diverse adverse adversely inverse reverse perverse obese verbose morose grotesque
grotesquely picturesque unique uniquely antique opaque oblique bizarre bizarrely divine genuine genuinely feminine
masculine pristine routine benign foreign alien fertile infertile fragile futile hostile juvenile mobile agile
docile versatile volatile senile sterile alive elaborate elaborately serene serenely obscene obscenely humane
humanely inhumane mundane insane insanely profane""")

# -id, -some and other two-syllable adjectives that take more and most
words("""solid solidly valid invalid rapid rapidly vivid vividly timid timidly humid horrid splendid splendidly
candid candidly rigid rigidly frigid lucid lucidly morbid placid sordid putrid fluid human humanly inhuman random
randomly awesome awesomely lonesome wholesome gruesome tiresome troublesome quarrelsome cumbersome honest honestly
dishonest dishonestly modest modestly immodest earnest earnestly robust robustly unjust unjustly abstract compact
intact exact exactly inexact correct correctly incorrect incorrectly perfect perfectly imperfect direct directly
indirect indirectly distinct distinctly indistinct extinct succinct succinctly abrupt abruptly corrupt bankrupt
overt overtly covert covertly inert alert expert expertly secret secretly upright outright downright forthright
absurd absurdly awkward awkwardly wayward untoward modern average savage savagely complex deluxe lavish lavishly
selfish selfishly unselfish childish childishly foolish foolishly stylish stylishly boyish girlish feverish
feverishly outlandish sluggish sluggishly squeamish ticklish peevish prudish snobbish devilish fiendish garish
ghoulish hellish impish skittish amateurish cartoonish bookish standoffish aware unaware afraid alone asleep awake
alike aloof ablaze afloat aglow amiss askew awry adrift astray aghast akin ajar""")

# -ary and -ory
words("""ordinary ordinarily extraordinary extraordinarily necessary necessarily unnecessary unnecessarily contrary
temporary temporarily primary primarily secondary voluntary voluntarily involuntary arbitrary arbitrarily customary
legendary literary military momentary momentarily monetary mandatory obligatory preliminary sanitary unsanitary
solitary stationary visionary satisfactory unsatisfactory compulsory contradictory derogatory introductory
elementary complimentary complementary imaginary revolutionary evolutionary honorary planetary sedentary hereditary
exemplary culinary dietary documentary extracurricular""")

# opinions and reactions
words("""superb superbly okay ok mediocre atrocious atrociously cringe cringey cringy legit crap trash garbage meh
fire lit dope rad bomb bonkers nuts unreal surreal bananas berserk gnarly spectacular spectacularly sensational
sensationally stellar superior inferior premium primo""")

# importance, sameness, number and order
words("""major minor main chief key principal paramount foremost same similar similarly dissimilar single double
triple quadruple multiple only lone singular plural sundry overall net extra spare excess leftover former latter
prior last penultimate""")

# time
words("""instant instantly regular regularly irregular irregularly daily weekly monthly yearly hourly nightly
quarterly biweekly present presently future overdue upcoming ongoing belated belatedly premature prematurely eternal
eternally everlasting lifelong longtime vintage retro outdated dated updated newfangled""")

# truth and certainty
words("""certainly uncertain uncertainly unsure fictional false falsely untrue bogus counterfeit""")

# difficulty and effort
words("""difficult challenging straightforward straightforwardly laborious chilled laidback""")

# body and health
words("""unwell injured wounded bloated acute disabled mute paralyzed paralysed muscular unfit overweight
underweight petite slender freckled tanned sunburned sunburnt wrinkled bearded pierced tattooed dead vegan
vegetarian pescatarian lactose""")

# food and drink
words("""homemade handmade appetizing appetising unappetizing filling fattening cooked uncooked undercooked
overcooked burnt burned roasted toasted baked fried grilled steamed boiled smoked iced carbonated nonalcoholic decaf
caffeinated bottomless gourmet""")

# tech, school and work
words("""online offline electrical technological educational mathematical freelance unemployed employed retired
graduate undergraduate postgraduate beginner intermediate amateur senior junior wired glitchy laggy""")

# places and the world
words("""urban suburban coastal inland touristy popular unpopular unknown known overseas worldwide nationwide
statewide citywide northern southern eastern western north south east west northeast northwest southeast southwest
northerly southerly easterly westerly upstate downstate midwestern""")

# more adjectives the rules handle
adjectives("""new empty guilty sorry sound creepy spooky clumsy sloppy moldy mouldy mellow vain snobby bratty ditzy
artsy toasty""")

# position, kind and other everyday adjectives
words("""blank chemical cultural industrial federal regional fellow female male front top bottom middle inner outer
upper left joint live living magic parallel prime rival standard thorough thoroughly amusing amusingly conceivable
conceivably inconceivable inconceivably converse conversely inexplicable inexplicably invariable invariably
unquestionable unquestionably everyday faraway coincidentally figuratively metaphorically""")

# un- and -ar adjectives
words("""unfair unfairly unkind unkindly unwise unwisely unclear unclean unafraid unable uncommon uncommonly
familiar familiarly unfamiliar peculiar peculiarly particular particularly circular rectangular triangular vulgar
vulgarly polar solar lunar nuclear molecular cellular bipolar""")

# shape and evenness, and adjectives that take "more"
words("""leathery rubbery powdery peppery buttery garlicky lemony sugary watery jittery shadowy malty yeasty teeny
teensy square oval spherical cylindrical angular pointy symmetrical asymmetrical lopsided level evenly uneven
unevenly giant mini miniature jumbo humongous ginormous mammoth itty bitty cramped lukewarm tepid scorching boiling
freezing sweltering pungent rancid chocolatey tattered muffled tuneful""")

# people and relationships
words("""married unmarried divorced engaged widowed gay straight bisexual lesbian queer transgender nonbinary
stubborn stubbornly cunning hypocritical judgmental judgemental nonjudgmental opinionated trustworthy untrustworthy
praiseworthy noteworthy newsworthy worthwhile conceited entitled hyper uptight paranoid outdoorsy sinister eerie
eerily haunted broke""")

# ===============================================================================================================
# (4) adverbs the rules do not make
# ===============================================================================================================

# time and frequency
words("""now then today tonight tomorrow yesterday soon sooner soonest soonish already oft straightaway erstwhile
hitherto thereupon forthwith anon just ago afterwards afterward beforehand meanwhile nowadays someday sometime
sometimes always never ever forever often oftentimes seldom twice thrice again anymore anytime overnight continually
formerly thereafter henceforth hereafter tonite""")

# place and direction
words("""yonder thereabouts hereabouts afield abreast astride aloft northward southward eastward westward skyward
seaward upstream downstream upriver downriver underfoot backstage offstage onstage onscreen offscreen here there
everywhere anywhere somewhere nowhere elsewhere everyplace someplace anyplace home abroad away back forward forwards
backward backwards upward upwards downward downwards inward inwards outward outwards onward onwards homeward
sideways upstairs downstairs indoors outdoors nearby apart aside ahead uphill downhill uptown downtown midway
halfway aboard ashore afar aloud anew afresh aground offshore overhead underground underwater upside""")

# degree and amount
words("""very quite rather too almost also overly unduly altogether ultra uber somewhat super mega hella way mostly
partly mainly chiefly increasingly decreasingly progressively damn darn freaking frickin fricking friggin effing""")

# certainty, opinion and attitude
words("""maybe perhaps probably seemingly presumably admittedly arguably lowkey highkey deadass""")

# connecting and sentence adverbs
words("""however therefore thus hence namely albeit notwithstanding etc ie eg accordingly consequently likewise
furthermore moreover otherwise regardless nonetheless nevertheless anyway anyways anyhow anywho somehow someway
instead indeed else whereby thereby therein thereof herein hereby wherein whereabouts whatsoever whoever whomever
firstly secondly thirdly lastly together""")

# manner
words("""verbatim gratis versa bona fide nevermind underway midweek clockwise counterclockwise anticlockwise
lengthwise crosswise edgewise barefoot evermore insofar sans circa re anti awhile nigh onboard inbound outbound ish
whereupon wherefore whence thence alright aright nonstop pronto afoot amok amuck aplenty galore apiece doubly triply
singly partway upfront firsthand secondhand offhand overboard headfirst headlong bodily jointly reciprocally
purposely grudgingly begrudgingly""")

# ===============================================================================================================
# (5) function words
# ===============================================================================================================

# personal pronouns, possessives and reflexives (with the chat spellings)
words("""i me my mine myself you your yours yourself yourselves he him his himself she her hers herself it its
itself we us our ours ourselves ourself they them their theirs themselves themself one oneself ones em u ur ya yall
y'all ye thee thou thy thine""")

# indefinite and other pronouns, with their possessive forms
words("""someone somebody something anyone anybody anything everyone everybody everything noone nobody nothing none
each other another whatnot someone's somebody's something's anyone's anybody's anything's everyone's everybody's
everything's nobody's nothing's one's other's another's else's someones somebodys somethings anyones anybodys
everyones everybodys everythings nobodys nothings""")

# articles and determiners
words("""a an the this that these those some any no every either neither both all half several many much few little
more most less least enough such what which whatever whichever own certain various plenty lots""")

# prepositions
words("""about above across after against along alongside amid amidst among amongst around as at atop before behind
below beneath beside besides between betwixt beyond but by concerning considering despite down during except
excluding following for from in including inside into like minus next of off on onto opposite out outside over past
per plus regarding since than through throughout thru till til to toward towards under underneath unlike until unto
up upon versus vs via with within without worth""")

# conjunctions
words("""and or nor so yet because cause cuz cos coz although though tho altho even if unless whereas while whilst
whether once when whenever where wherever lest provided providing supposing""")

# question words
words("""who why how whose whom wat wut""")

# be, have, do and the modals
words("""be am is are was were been being do does did done doing have has had having will would shall should can
could may might must ought need needs dare used""")

# contractions: with the apostrophe and without (as people type them)
words("""i'm im i've ive i'll i'd id you're youre you've youve you'll youll you'd youd he's hes he'll he'd hed she's
shes she'll shell she'd shed it's it'll itll it'd itd we're we've weve we'll we'd wed they're theyre they've theyve
they'll theyll they'd theyd that's thats that'll thatll that'd thatd there's theres there'll therell there'd thered
there're here's heres what's whats what're whatre what'll whatll what'd whatd what've whatve who's whos who'll wholl
who'd whod who've whove where's wheres where'd whered where've when's whens when'd why's whys why'd whyd how's hows
how'd howd how'll howll let's lets isn't isnt aren't arent wasn't wasnt weren't werent don't dont doesn't doesnt
didn't didnt haven't havent hasn't hasnt hadn't hadnt won't wont wouldn't wouldnt can't cant couldn't couldnt
shouldn't shouldnt mustn't mustnt mightn't needn't neednt shan't shant ain't aint would've wouldve could've couldve
should've shouldve might've mightve must've mustve ma'am maam o'clock oclock""")

# spoken shortenings of auxiliaries
words("""gonna wanna gotta hafta hasta oughta tryna finna lemme gimme dunno kinda sorta outta lotta coulda woulda
shoulda musta mighta gotcha betcha whatcha watcha dontcha didja wouldja couldja y'know""")

# ===============================================================================================================
# (6) numbers, days, months, seasons
# ===============================================================================================================

# cardinal numbers (the compounds are typed as two words, or with a hyphen that splits them)
words("""zero two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen
eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion
hundreds thousands millions billions trillions dozen dozens score nil nought naught zillion zillions gazillion
bajillion kajillion umpteen twos threes fours fives sixes sevens eights nines tens twenties thirties forties fifties
sixties seventies eighties nineties teens""")

# ordinals and fractions
words("""first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth
fifteenth sixteenth seventeenth eighteenth nineteenth twentieth thirtieth fortieth fiftieth sixtieth seventieth
eightieth ninetieth hundredth thousandth millionth billionth umpteenth nth halves quarter quarters thirds fourths
fifths tenths hundredths thousandths couple pair pairs 1st 2nd 3rd 4th 5th 6th 7th 8th 9th 10th 11th 12th 13th 14th
15th 16th 17th 18th 19th 20th 21st 22nd 23rd 24th 25th 26th 27th 28th 29th 30th 31st""")

# days of the week
words("""monday tuesday wednesday thursday friday saturday sunday mondays tuesdays wednesdays thursdays fridays
saturdays sundays mon tue tues thu thur thurs fri sat sun weekday weekdays weekend weekends weeknight weeknights""")

# months
words("""january february march april june july august september october november december jan feb mar apr jun jul
aug sep sept oct nov dec""")

# seasons and times of day
words("""spring summer fall autumn winter springs summers autumns winters springtime summertime wintertime autumnal
wintry wintery summery pm noon midnight midday dawn dusk sunrise sunset""")

# ===============================================================================================================
# (7) interjections
# ===============================================================================================================

words("""oh ohh ah ahh aah wow woah whoa oops whoops oopsie yay yey hooray hurray hurrah yippee woohoo woo ugh argh
hmm hm um umm uh uhh er erm eh huh duh doh ouch ow yikes eek phew whew shh shush psst ahem aha gee jeez geez gosh
golly dang heck hell alas bravo cheers congrats voila tada bingo boo booyah welp aw aww ooh mm mmm blah pfft tsk
hmph ew eww yuck yum oi oy ahoy hiya howdy hey hi hello bye goodbye yes not yeah yep nope nah amen please thanks
thank pardon shoot shucks rats crikey blimey whoopsie whoopee hallelujah""")
