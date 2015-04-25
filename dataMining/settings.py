__author__ = "Justin Milanovic"
__version__ = "1.0.0"
__email__ = "justinmilanovic@gmail.com"
__status__ = "Development"

from os import path

# Twitter: api keys
TWITTER_CONSUMER_KEY =""
TWITTER_CONSUMER_SECRET =""
TWITTER_ACCESS_TOKEN =""
TWITTER_ACCESS_TOKEN_SECRET = ""

# Twitter: pickel files
TWITTER_CURSOR_FILE = path.dirname(__file__) + '/data/twitter_cursor_output.p'
TWITTER_STREAM_FILE = path.dirname(__file__)  + '/data/twitter_stream_output.p'
TWITTER_CLEAN_DATA = path.dirname(__file__)  + '/data/twitter_clean_data.txt'

# Twitter: custom stop words file
TWITTER_CUSTOM_STOPWORDS = path.dirname(__file__)  + '/data/custom_stopwords.txt'

# Twitter: regex phrases
TWITTER_CUSTOM_PHRASES_LEFT = [' is hiring a ', ' is hiring ', ' is looking for a ', ' is looking for ', ' for ', ' are hiring a ', ' are hiring ', ' opportunity with ',]
TWITTER_CUSTOM_PHRASES_RIGHT = [' needed in ', ' needed ', ' at ', ' with ', ' opening at ']

# Twitter: NER files
STANFORD_NER = '/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'
STANFORD_NER_JAR = '/usr/share/stanford-ner/stanford-ner.jar'

# Twitter: regex expressions
TWITTER_PUNCTUATION = r"(\w*\?|\w*!|\s{0,1}-|\s{0,1};|\s{0,1}:|\s{0,1}\.|\s{0,1},|\s{0,1}\|)"
TWITTER_HASHTAGS = r"\s{0,1}#\w*"
TWITTER_ZIPCODE = r"(\s{1}\d+|\d+\s{1})"
TWITTER_MONEY = r"(\s{1}\$\d+\S*|\$\d+\S*\s{1})"
TWITTER_USERNAME = r"(\s{1}@\w*|\w*@\w+\s{1})"
TWITTER_HYPERLINKS = r"\s{0,1}http://\S*|\s{0,1}https://\S*"
TWITTER_BRACKETS = r"(\(|\)|\[|\])"
TWITTER_SQUARE_BRACKETS_TEXT = r"\s{0,1}\[(.+?)\]"
TWITTER_DASH_SLASH = r"(-|\/|\\)"
TWITTER_CUTOFF = r"\s{1}\w*\.{3}"
TWITTER_US_STATES = r"(\s{0,1}\w*, A[LKSZRAEP]|\s{0,1}\w*, C[AOT]|\s{0,1}\w*, D[EC]|\s{0,1}\w*, F[LM]|\s{0,1}\w*, G[AU]|\s{0,1}\w*, HI|\s{0,1}\w*, I[ADLN]|\s{0,1}\w*, K[SY]|\s{0,1}\w*, LA|M[ADEHINOPST]|\s{0,1}\w*, N[CDEHJMVY]|\s{0,1}\w*, O[HKR]|\s{0,1}\w*, P[ARW]|\s{0,1}\w*, RI|\s{0,1}\w*, S[CD]|\s{0,1}\w*, T[NX]|\s{0,1}\w*, UT|\s{0,1}\w*, V[AIT]|\s{0,1}\w*, W[AIVY])"
TWITTER_US_STATES_2_WORD = r"(\s{0,1}\w*\s\w*, A[LKSZRAEP]|\s{0,1}\w*\s\w*, C[AOT]|\s{0,1}\w*\s\w*, D[EC]|\s{0,1}\w*\s\w*, F[LM]|\s{0,1}\w*\s\w*, G[AU]|\s{0,1}\w*\s\w*, HI|\s{0,1}\w*\s\w*, I[ADLN]|\s{0,1}\w*\s\w*, K[SY]|\s{0,1}\w*\s\w*, LA|M[ADEHINOPST]|\s{0,1}\w*\s\w*, N[CDEHJMVY]|\s{0,1}\w*\s\w*, O[HKR]|\s{0,1}\w*\s\w*, P[ARW]|\s{0,1}\w*\s\w*, RI|\s{0,1}\w*\s\w*, S[CD]|\s{0,1}\w*\s\w*, T[NX]|\s{0,1}\w*\s\w*, UT|\s{0,1}\w*\s\w*, V[AIT]|\s{0,1}\w*\s\w*, W[AIVY])"
TWITTER_STATES = r"(Ala(bama|ska)|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|District of Columbia|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Miss(issippi|ouri)|Montana|Nebraska|Nevada|New (Hampshire|Jersey|Mexico|York)|North (Carolina|Dakota)|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South (Carolina|Dakota)|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia)"

# Twitter: List of regex expressions to run
TWITTER_REGEX = [TWITTER_MONEY, TWITTER_HYPERLINKS, TWITTER_HASHTAGS, TWITTER_USERNAME, TWITTER_BRACKETS, TWITTER_SQUARE_BRACKETS_TEXT, TWITTER_US_STATES, TWITTER_CUTOFF, TWITTER_PUNCTUATION, TWITTER_ZIPCODE, TWITTER_STATES]

#Google: api Keys
GOOGLE_API_KEYS = ["AIzaSyCHwlWEjEcdeH1KRnmIi9fq5Dnx2JBeVRw", "AIzaSyAqa0-CM0ZZ8hxTjLGZ52SxTZ9UjaTp72A"]

#Google: Search engine ID
GOOGLE_SEARCH_ENGINE_ID = "016745198537660285174:espiwqmbexg"

#Google: additional processing settings
GOOGLE_ADDITIONAL_PROCESSING = 0
GOOGLE_MANUAL_PROCESSING = 0

#Snippet Processing
GRAMMAR = """
            list: {(<NN|NNS|NNP|VB|VBG|JJ|CC|PRP|IN|TO>+<,>)+}
            and: {<NN|NNS|JJ|VB|IN|VBG>*<CC><NN|NNS|JJ|VB|IN|VBG>+}
            """
ADDITIONAL_STOP_WORDS_TITLES = ["list", "others", "benefits", "after", "uses", "use",
                           "jobs", "job", "professionals", "professionals" "occupations", "including",
                           "like", "such", "as", "interview", "various", "salary", "experience",
                           "facts", "enjoy", "industry", "professions", "number", "high-paying"]

ADDITIONAL_STOP_WORDS_SKILLS = ["list", "others", "benefits", "after", "uses", "use",
                           "jobs", "job", "professionals", "professionals" "occupations", "including",
                           "like", "such", "as", "interview", "various", "salary", "experience",
                           "facts", "enjoy", "industry", "professions", "number", "high-paying",
                           "skill", "skills", "get", "help"]

#Google: output files
#Used for saving if using the query function
#Used to load if using the process function
GOOGLE_TITLE_SNIPPET_FILENAME = "softwareEngineer"
GOOGLE_SKILL_SNIPPET_FILENAME = "softwareEngineerSkills"

#Google query titles
#Used to formulate queries
GOOGLE_JOB_TITLE = "software engineer"
GOOGLE_SKILL_TITLE = "software engineering"

#Google processing titles
#Used when processing snippets
GOOGLE_PROCESS_TITLE = "software engineer"

#Web Scraping funtionality
GET_FULL_SNIPPET = True
