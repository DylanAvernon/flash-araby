DESIGN

    The Database:
    
    The database consists of almost thirty tables. The base table contains the base form of all 
    verbs entered into the database and a unique numeric ID. The conjugation table of a single
    verb is split up into multiple tables, one for each form, with all the rows keyed to their 
    appropriate verb in the base table. 
    
    The method I use for searching the database and generating custom flashcard decks requires the
    use of many SQL tables. This structure allowed me to code a simple series of nested for-loops
    with error handling for the generation of all possible custom flashcard decks.
    
    Finally there are additional tables for recording user information like username, user id, and
    password. I used CS50's finance app for coding the sessions logic and hashing algorithms.
    
    The Application:
    
    There are many routes in this Flask application, however, the work horses of this application
    are /verbentry and /search. These routes contain the most coding and the more complicated
    bits of logic. 
    
    Verbentry can be divided into a few sections: 1) get input, 2) check input 2) retrieve verb forms,
    3) check input again, 4) enter verb-forms. It is necessary to check the input in two steps
    because certain tests must be run before making the url request, and some must be made afterwards.
    Basic checks like "is the input field blank" or "does the input consist of arabic characters"
    can be done before the url request and helps ensure that the appropriate webpage is accessed.
    Other checks must be done using the verb form retrieved from Reverso, such as querying the 
    database to ensure that the requested verb is not already in the database. The HTML input field
    and Reverso use two different encoding strategies for Arabic characters, this means that the 
    same Arabic verb will be interpreted as different if the program does not consistently use the
    verb-forms from Reverso. While the HTML encoding is sufficiently similar for producing an
    accurate url and retrieving the appropriate webpage, it is not sufficient for accurate 
    database queries or comparisons.
    
    Search contains the logic for retrieving the appropriate collection of verb-forms based on user
    specifications. The function passes this collection to an HTML file that will display the 
    custom deck. The centerpiece of this function is the nested for-loops that generate a series 
    of queries and append the results to a list. Some of the queries return errors because they are 
    invalid. This is by design and a necessary evil. I am able to handle these errors with the 
    "try - except - else" statement in Python.
    
    The last exciting bit of this application is the implementation of the flash card tool. It
    incorporates Python, Jinja, HTML, JS, and CSS. Python queries the database and generates 
    the custom list of verb forms. It passes the array to an HTML file using Jinja. A Jinja
    for-loop transfers the verb forms from a Python list into a JS array. This array is then
    passed to a JS function that generates the flash cards and formats each string dynamically
    so that they are always perfectly centered. I accomplished this task by writing logic for
    measuring the height and width of each string, adjusting the margins accordingly, and then
    placing the string on the card.
    
    