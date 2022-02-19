import firebase_admin, hashlib
from firebase_admin import credentials
from firebase_admin import firestore
# firebaseの設定を読み込む
cred = credentials.Certificate("fushime-9ccc3-firebase-adminsdk-9vqsu-a9d6643f4e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def signin(username,password):
    doc_ref = db.collection(u'users').document(username)

    hash_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()
    doc_ref.set({
        u'password': hash_pass,
    })
    print(hash_pass)