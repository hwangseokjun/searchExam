from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.fd9eu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/mnt', methods=['GET']) # /mnt로 키워드를 받아 산의 상세 설명에서 일치 결과를 찾아냅니다.
def mnt_get():
   doc = [] # 검색을 마친 자료가 들어갈 배열입니다.
   mnt_receive = request.args.get('mnt_give') # Ajax에서 mnt_give로 보낸 데이터를 받습니다.
   mountains = list(db.mnt_info.find({},{'_id':False})) # 산의 전체 목록을 mountains 변수로 받아옵니다.
   for mountain in mountains:
      if mnt_receive in mountain['mnt_desc']: # 산의 세부 설명에서 mnt_receive로 받은 검색어를 찾아봅니다.
         doc.append(mountain) # 일치하는 명산의 번호를 doc 배열에 집어넣습니다.
   search_list = {'search_list':doc} # API로 전달할 수 있는 자료에 배열 형태는 없으므로, 딕셔너리로 만들어야 합니다.
   return jsonify({'search_list':search_list, 'msg':'검색완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)