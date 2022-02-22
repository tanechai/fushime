# import datetime
# from operator import itemgetter
# from functions.importance import Importance
# from numpy import unsignedinteger

# # 予定の追加、削除、取得を行うクラス
# class schedule_manager:

#     def __init__(self,id,db):
#         self.id = id
#         self.db = db

#     # 予定を追加する
#     def add(self,subject:str,year:unsignedinteger,month:unsignedinteger,date:unsignedinteger,importance:Importance):
#         self.db.collection(u'users').document(self.id).collection(u'schedules').add({
#             u'subject': subject,
#             u'year': year,
#             u'month': month,
#             u'date': date,
#             u'importance': importance,
#         })
    
#     # 予定を削除する
#     def delete(self,schedule_id):
#         self.db.collection(u'users').document(self.id).collection(u'schedules').document(schedule_id).delete()

#     # 全ての予定をリストで取得する
#     def get_all(self)->list:
        
#         docs = self.db.collection(u'users').document(self.id).collection(u'schedules').stream() # 全ドキュメントを取得
        
#         # 各ドキュメントをリストにする
#         schedules = []
#         for doc in docs:
#             dict_doc = doc.to_dict() # ドキュメントを辞書型に変換
#             dict_doc[u'id'] = doc.id # 辞書型ドキュメントにidの追加
#             schedules.append(dict_doc) # リストに追加
        
#         schedules =  sorted(schedules,key=itemgetter('year','month','date')) # 昇順に並び替え
        
#         return schedules
    
#     # 今日以降のn個目までの予定をリストで取得する
#     def get_up_to_nth(self,nth:unsignedinteger)->list:
        
#         schedules = self.get_all() # 全ての予定を取得

#         filtered = list(filter(lambda x: True if datetime.date(x[u'year'],x[u'month'],x[u'date']) >= datetime.date.today() else False ,schedules)) # 今日以降の予定だけ取り出す
        
#         return filtered[0:nth] # n個目までの予定を返す
