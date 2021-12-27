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
FILE_PATH = os.path.join(ROOT_DIR, 'static\\data\\er_edu_hos.xlsx')
GEO_PATH = os.path.join(ROOT_DIR, 'static\\data\\TL_SCCO_CTPRVN_WGS84.json')

# 파일 연동
@app.route('/') # 라우팅, '/'는 접속 시, root 경로
def home(): # '/'과 매칭되는 함수 root 경로 시, 페이지에 작동할 메소드
    data = get_chart()
    return render_template('base.html', map=get_map(), data=data)

@app.route('/map')
def get_map():
    # file_path = 'C:\\Users\\Playdata\\PycharmProjects\\RealEstate_DataAnalysis\\RealEstate\\app\\static\\data\\er_ap_job_df.xlsx'
    er_ap_job_df = pd.read_excel(FILE_PATH, index_col=0)
    # geo_path = 'C:\\Users\\Playdata\\PycharmProjects\\RealEstate_DataAnalysis\\RealEstate\\app\\static\\data\\TL_SCCO_CTPRVN_WGS84.json'
    geo_str = json.load(open(GEO_PATH, encoding='utf-8'))

    types = request.args.get('types')
    location = request.args.get('location')
    if types == None:
        types = '0'
    if location == None:
        location = []

    def print_map(location, types):
        if not location:
            map_df = er_ap_job_df
        else:
            map_df = er_ap_job_df.loc[location]
        map = folium.Map(
            height=680,
            location=[35.8002, 127.854],
            zoom_start=7)

        scroll_remove = '''
            <head><style> html { overflow-y: hidden; } </style></head>
        '''
        map.get_root().html.add_child(folium.Element(scroll_remove))

        map.choropleth(geo_data=geo_str,
                       data=map_df['고용자수대비평균매매가'],
                       columns=[map_df.index, map_df['고용자수대비평균매매가']],
                       fill_color='PuRd',
                       key_on='feature.id')

        for sido, price, lat, lng in zip(map_df.index, map_df['아파트평균매매가격'], map_df['위도'], map_df['경도']):
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
    # file_path = 'C:\\Users\\Playdata\\PycharmProjects\\RealEstate_DataAnalysis\\RealEstate\\app\\static\\data\\er_ap_job_df.xlsx'
    er_ap_job_df = pd.read_excel(FILE_PATH, index_col=0)
    x = list(er_ap_job_df.index)
    y = [list(er_ap_job_df['고용자수대비평균매매가']), list(er_ap_job_df['고용자수']), list(er_ap_job_df['아파트평균매매가격'])]
    label = ['고용자수대비평균매매가', '고용자수', '아파트평균매매가격']
    data = {'x': x, 'y': y, 'label':label}
    return data

if __name__ == '__main__':
    app.run()

