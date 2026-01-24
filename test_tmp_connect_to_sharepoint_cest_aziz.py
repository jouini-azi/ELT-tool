from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from io import BytesIO
import pandas as pd
print('hiba')
# 1️⃣ Authentification
authcookie = Office365('https://mohetn.sharepoint.com/sites/test8195/Shared%20Documents/excel/Classeur2.xls', username='hiba.dhouib@djerba.r-iset.tn', password='IsetDSI123*-+*-+').GetCookies()

# 2️⃣ Connexion au site
site = Site('https://mohetn.sharepoint.com/sites/test8195', version=Version.v365, authcookie=authcookie)

# 3️⃣ Accès au dossier
folder = site.Folder('https://mohetn.sharepoint.com/sites/test8195/Shared%20Documents/excel/Classeur2.xls')  # chemin relatif du dossier

# 4️⃣ Lister les fichiers
files = folder.files
print(files)  # liste des fichiers dans le dossier

# 5️⃣ Récupérer un fichier précis
file_content = folder.get_file('Classeur2.xlsx')
df = pd.read_excel(BytesIO(file_content))
print(df.head())
