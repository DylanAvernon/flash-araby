DOCUMENTATION
    
    Error Checking:
    
    For checking my project for accuracy, you can visit 
    https://conjugator.reverso.net/conjugation-arabic.html, access one of the verb conjugation 
    tables, add that same verb to my database using my application, and compare the flash card
    decks it generates with the verb conjugation tables on Reverso.
    
    Motivation:
    
    My project was motivated by a problem that I faced when participating in Arabic conversation
    classes. My teachers would often use unfamiliar vocabularly that I wanted to study further
    and become familiar with its usage and conjugation. The Arabic language has a robust verb
    conjugation system, and it would take me hours to produced a deck of flashcards for studying
    even a single verb. When I began this project, my goal was to produce an application that
    would automate the laborious process of flashcard geneartion so that I could focus on
    familiarizing myself with the verb forms rather than spend most of my time making the cards.

    The Database:
    
    This application relies on a SQLite database for storing verb forms, saving a users information
    and genearting flash card decks. Before running the application you must start the database.
    You can accomplish this by typing "python startdb.py" in the command terminal. It should
    produce a SQLite database called "verbs.db". Inside this database are almost thirty tables,
    most of them store verb forms, but some store user information, and keep track of who is
    studying what.
    
    The Application:
    
    Start the application by typing the command "flask run" in the command terminal after you have
    navigated to the appropriate directory.
    
    The Website:
    
    Once you open the website, you will be directed to the login page. You will need to register
    first, so click the register link in the top left-hand corner next to the application logo.
    Type in your username and password, and click submit. You will be directed back to the login
    page where you can use your username and password to login.
    
    You will find yourself at your lerner's homepage, which contains some information about the
    various functionalities of the application and a list of verbs you are studying. The list will
    be empty, but as you add new verbs you can review the full list at the lerner's homepage.
    
    The add and delete verbs pages are straight forward. You can add any Arabic verb that is 
    available on the website https://conjugator.reverso.net/conjugation-arabic.html. I suggest
    being as specific as possible when entering your arabic verb by including all the vowel markers
    especially the shadda, but the application will still produce a match even without these 
    diacritics. Without the shadda you will mostly likely access the verb tables belonging
    to the shadda-less verb. So if you want to study درّس for example, you must include the shadda 
    character. The delete verbs page will only allow you to delete verbs you are currently studying.
    
    The new decks page is a little more complicated because it allows you to specify a subset of
    a verbs conjugation table for focused study. You can chose to study one verb form or the entire
    conjugation table. You are also free to specify groups such as all 1st person present verb forms
    or all dual verb forms, or all feminine verb forms. Be as specific as you want by selecting 
    multiple options, or select nothing at all to view the entire table. You will then be directed 
    to another page where you will find your customized flash card deck waiting you to use. The 
    front side contains the verb (فعل) and the back side contains the appropriate pronoun (ضمير). 
    You can move to the next verb form by clicking the button that says "click me." You can 
    inspect the back-side of the card by hovering your cursor over the flash card.
    
    Once you are done, you can return to the new decks page to create a new deck of flash cards,
    navigate to the add verbs page to add additional verbs, or simply logout if you are finished.

