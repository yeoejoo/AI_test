from flask import Flask, render_template_string, render_template
import folium
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

@app.route("/rest")
def rest():
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
    # graphHTML = fig.to_html(full_html=False, include_plotlyjs='cdn')
    # print(graphHTML)

    return graphJSON


def gm(country='강동구'):
    df = pd.read_excel("./E국제투자대조표.xlsx")  # [단위 : 백만달러]
    df = df.set_index("날짜")

    fig = px.line(df[df['country'] == country], x="year", y="gdpPercap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(fig.data[0])
    # fig.data[0]['staticPlot']=True

    return graphJSON



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