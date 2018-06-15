fast = """```  ______        _   
 |  ____|      | |  
 | |__ __ _ ___| |_ 
 |  __/ _` / __| __|
 | | | (_| \__ \ |_ 
 |_|  \__,_|___/\__|```
 """

aide_fast = fast +  u"""**Fast** est un jeu où vous devez retaper la chaîne de caractères choisie par le bot le plus rapidement possible. Faites `!fast <niveau>` pour déclancher le début du jeu.
__Niveau **1**__ : 10 à 20 caractères minuscules
__Niveau **2**__ : 10 à 20 caractères minuscules ou majuscules
__Niveau **3**__ : 10 à 20 caractères minuscules (avec ou sans accent), majuscules ou numériques
__Niveau **4**__ : 10 à 20 caractères minuscules (avec ou sans accent), majuscules, numériques ou spéciaux
__Niveau **5**__ : 20 à 30 caractères minuscules (avec ou sans accent), majuscules, numériques ou spéciaux
Bon courage \N{SMILING FACE WITH HORNS}"""

caracteres = ['abcdefghijklmnopqrstuvwxyz',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZaàbcçdeêëéèfghijklmnopqrstuùvwxyz0123456789',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZaàbcçdeêëéèfghijklmnopqrstuùvwxyz0123456789&"#\'{([-|_\\)]°+=}$*?,.;/:!']

feeds = ["https://korben.info/feed",
         "https://www.begeek.fr/feed",
         "http://blogmotion.fr/feed",
         "http://www.framboise314.fr/feed/", "http://www.journaldugeek.com/feed/",
         "https://thehackernews.com/feeds/posts/default",
         "https://usbeketrica.com/rss",
         "https://www.lemondeinformatique.fr/flux-rss/",
         "http://www.01net.com/rss/actualites/"]

pendu = ["""```
                       
                        
                        
                         
                          
                          
                         
                        
         
        ============```""", """```
            
           ||          
           ||          
           ||          
           ||         
           ||         
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||        
           ||        
           ||       
           ||       
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      
           || /       
           ||/       
           ||       
           ||       
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        
           ||        
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        O
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        O/
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||          \
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||        / \
           ||
           ||
           ||
        ============```"""]

ytCategories = {'1': 'Film & Animation', '2': 'Autos & Vehicles', '10': 'Music', '15': 'Pets & Animals', '17': 'Sports', '18': 'Short Movies', '19': 'Travel & Events', '20': 'Gaming', '21': 'Videoblogging', '22': 'People & Blogs', '23': 'Comedy', '24': 'Entertainment', '25': 'News & Politics', '26': 'Howto & Style', '27': 'Education', '28': 'Science & Technology', '30': 'Movies', '31': 'Anime/Animation', '32': 'Action/Adventure', '33': 'Classics', '34': 'Comedy', '35': 'Documentary', '36': 'Drama', '37': 'Family', '38': 'Foreign', '39': 'Horror', '40': 'Sci-Fi/Fantasy', '41': 'Thriller', '42': 'Shorts', '43': 'Shows', '44': 'Trailers'}