from flask import Flask, render_template_string, render_template, request

import json
import pandas as pd
import numpy as np

#--- 시각화 관련
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly
import plotly.offline as pyo
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#--- 지도맵 관련
from folium.plugins import MarkerCluster
from folium import Marker


app = Flask(__name__)

@app.route("/")
def fullscreen():
    m = folium.Map()
    return m.get_root().render()

@app.route("/iframe")
def iframe():
    m = folium.Map()
    m.get_root().width  = "400px"
    m.get_root().height = "300px"
    iframe_map_html = m.get_root()._repr_html_()
    print(iframe_map_html)
    return render_template("iframe_page.html" , MY_IFRAME = iframe_map_html)

@app.route("/htmlpage")
def htmlpage():
    m = folium.Map(width=400,height=300)
    m.save('templates/map.html')
    return render_template('index.html')

@app.route("/plotlypage")
def plotlypage():
    #  ----------------------------------------------------------
    #  data:json
    #  ----------------------------------------------------------
    inv_df = pd.read_excel("./E국제투자대조표.xlsx")  # [단위 : 백만달러]
    inv_df = inv_df.set_index("날짜")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=inv_df.index, y=inv_df['대외금융부채'], name='대외금융부채'))
    fig.add_trace(go.Scatter(x=inv_df.index, y=inv_df['대외금융자산'], name='대외금융자산'))
    fig.add_trace(go.Scatter(x=inv_df.index, y=inv_df['순대외금융자산'], name='순대외금융자산'))
    fig.update_layout(
        width=1200,
        height=400,
        title_text="대외 금융자산 부채 추이",
        template="plotly_dark",
    )
    fig.update_xaxes(ticks="outside", dtick=1)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # print(fig.data[0])
    print(graphJSON)

    #  ----------------------------------------------------------
    #  htmlstr
    #  ----------------------------------------------------------
    graphHTML = fig.to_html(full_html=False, include_plotlyjs='cdn')
    print(graphHTML)

    return render_template('plotly_page.html'
                           , MY_PLOTLY_JSON=graphJSON
                           , MY_PLOTLY_HTML=graphHTML
                           )

@app.route('/plotly_json', methods=["get"])
def plotly_json():
    inv_df = pd.read_excel("./E국제투자대조표.xlsx")  # [단위 : 백만달러]
    fig = px.line(inv_df, x="날짜", y="대외금융부채")
    print(f"fig : {fig}")
    print(f"to_html() : {fig.to_html()}")
    print(f"to_json() : {fig.to_json()}")
    print(f"to_dict() : {fig.to_dict()}")
    print(f"to_plotly_json() : {fig.to_plotly_json()}")

    """
    The return type must be a string, dict, list, tuple with 
                              headers or status, Response instance, or WSGI callable, but it was a Figure.
    to_html        : html 문장으로 추출
    to_plotly_json : 파이썬의 dict로 추출
    to_json        : json형식으로 추출
    """
    return render_template('plotly_json.html',  MY_JSON=fig.to_json())
        

@app.route('/rest', methods=["get"])
def rest():
    return render_template('rest.html')


@app.route('/folium_rest', methods=["post"])
def folium_rest():
    v_search_name = request.args.get("search_NAME")
    print(v_search_name)
    if bool(v_search_name) == False:
        v_search_name = "중구"

    df = pd.read_csv("아파트명_좌표.csv")
    print(df.head())
    df = df[df['주소(시군구)'] == v_search_name]

    print(df.iloc[0,3], df.iloc[0,2])

    m = folium.Map(location=[df.iloc[0,3], df.iloc[0,2]], zoom_start=14, tiles='OpenStreetMap')
    mc = MarkerCluster()
    for _, row in df[['k-아파트명', '좌표X', '좌표Y']].iterrows():
        mc.add_child(
            Marker(location=[row['좌표Y'], row['좌표X']], popup=row['k-아파트명'])
        )
    m.add_child(mc)

    m.get_root().width = "800px"
    m.get_root().height = "400px"
    iframe_map_html = m.get_root()._repr_html_()
    #print(iframe_map_html)
    return iframe_map_html


# @app.route("/born")
# def born():
#     x = [i for i in range(100)]
#     y = [i for i in range(100)]
#     fig, ax = plt.subplots(figsize=(6, 6))
#     ax = sns.set(style="darkgrid")
#     sns.lineplot(x, y)
#     canvas = FigureCanvas(fig)
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     plt.close()
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode('utf8')
#     print(plot_url)
#     return render_template("multi.html", MY_PLT_URL=plot_url)
#     #return send_file(img, mimetype='img/png')  #<img src="{{ url_for('visualize') }}">
# <div><img src="data:image/png;base64, {{ MY_PLT_URL }}"></div>



if __name__ == "__main__":
    app.run(debug=True)