from flask import Flask, request
from flask import render_template
import pandas as pd
import folium
import json
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__) # flask 앱 생성
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(ROOT_DIR, 'static\\data\\last_df.xlsx')
GEO_PATH = os.path.join(ROOT_DIR, 'static\\data\\TL_SCCO_CTPRVN_WGS84.json')
LABEL = [['고용자수대비평균매매가', '고용자수', '아파트평균매매가격'], ['고용자수대비평균매매가', '고용자수', '아파트평균매매가격'], ['병원비율', '총병원수', '아파트평균매매가격'],['매매가대중교통비율', '일별평균대중교통사용자수', '아파트평균매매가격'], ['아파트/사설학원수', '사설학원수', '아파트평균매매가격']]
# 파일 연동
@app.route('/') # 라우팅, '/'는 접속 시, root 경로
def home(): # '/'과 매칭되는 함수 root 경로 시, 페이지에 작동할 메소드
    data = get_chart()
    return render_template('base.html', map=get_map(), data=data)

@app.route('/map')
def get_map():
    df_file = pd.read_excel(FILE_PATH, index_col=0)
    geo_str = json.load(open(GEO_PATH, encoding='utf-8'))

    types = request.args.get('types')
    location = request.args.get('location')

    if location != None:
        location = [i[1:-1] for i in location[1:-1].split(",")]
    if types == None:
        types = '0'
    if location in [None, ""]:
        location = []

    def print_map(location, types):
        if not location:
            map_df = df_file
        else:
            map_df = df_file.loc[location]

        label_list = LABEL[int(types)]

        map = folium.Map(
            height=680,
            location=[35.8002, 127.854],
            zoom_start=7)

        scroll_remove = '''
            <head><style> html { overflow-y: hidden; } </style></head>
        '''
        map.get_root().html.add_child(folium.Element(scroll_remove))

        map.choropleth(geo_data=geo_str,
                       data=map_df[label_list[0]],
                       columns=[map_df.index, map_df[label_list[0]]],
                       fill_color='PuRd',
                       key_on='feature.id')

        for sido, price, lat, lng in zip(map_df.index, map_df[label_list[2]], map_df['위도'], map_df['경도']):
            folium.Marker(
                location=[lat, lng],
                popup=f'<pre>{sido}<br/>평단가: {price}</pre>',
                icon=folium.Icon()
            ).add_to(map)
        return map

    html_data = print_map(location, types)._repr_html_()
    html_data = html_data[:46]+"absolute"+html_data[54:73]+"100%"+html_data[74:]
    return html_data

@app.route("/chart")
def get_chart():
    df_file = pd.read_excel(FILE_PATH, index_col=0)

    types = request.args.get('types')
    location = request.args.get('location')

    if location != None:
        location = [i[1:-1] for i in location[1:-1].split(",")]
    if types == None:
        types = '0'
    if location in [None, ""]:
        location = []

    if not location:
        map_df = df_file
    else:
        map_df = df_file.loc[location]

    label_list = LABEL[int(types)]

    x = list(map_df.index)
    y = [list(map_df[label_list[0]]), list(map_df[label_list[1]]), list(map_df[label_list[2]])]
    data = {'x': x, 'y': y, 'label':label_list}
    return data

if __name__ == '__main__':
    app.run()

