<h1>Projet de Validation d'Emails</h1>

Ce projet vise à valider des adresses emails en utilisant des vérifications de syntaxe, des enregistrements MX et la délivrabilité des emails. Les résultats des vérifications sont stockés dans une base de données SQLite.

<h3>Prérequis :</h3>

Avant de commencer, assurez-vous d'avoir les bibliothèques Python suivantes installées :
<li>smtplib</li>
<li>email-validator</li>
<li>dnspython</li>
<li>sqlite3</li>

<h3>Vous pouvez installer email-validator et dnspython en utilisant pip :</h3>

    pip install email-validator dnspython

<h3>Structure du Projet :</h3>
create_database(): Fonction pour créer une base de données SQLite et insérer des données d'emails aléatoires pour les tests.
validate_email_syntax(email): Fonction pour valider la syntaxe d'un email.
check_mx_record(domain): Fonction pour vérifier les enregistrements MX d'un domaine.
verify_email_deliverability(email): Fonction pour vérifier la délivrabilité d'un email en utilisant SMTP.
store_results_in_db(email, syntax_result, mx_result, deliverability_result): Fonction pour stocker les résultats des vérifications dans la base de données.
validate_email_address(email): Fonction principale pour valider un email et stocker les résultats dans la base de données.
<h3>Utilisation :</h3>

Étape 1 : Créer la base de données
La fonction create_database() crée une base de données SQLite nommée email_validation.db et y insère des emails de test aléatoires.

Étape 2 : Valider les emails
La fonction validate_email_address(email) effectue les vérifications de syntaxe, les enregistrements MX et la délivrabilité pour chaque email, puis stocke les résultats dans la base de données.

 