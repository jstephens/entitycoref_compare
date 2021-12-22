from flask import Flask, render_template,request
import plotly
import json
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

from plotly.colors import n_colors
app = Flask(__name__)

@app.route('/')
def index():
    feature =  'In Our Time'
    bar = create_plot(feature)
    return render_template('index.html', plot=bar)

def create_plot(feature):      
    featurefile = feature.replace(' ','_')
    
    if 'Pride' in feature:
        datafile = './input/'+featurefile+'_v1_gcloud.csv'
        datasource = pd.read_csv(datafile,names=['Chapter','Character','Entity','Salience','Sentiment Score','Sentiment Magnitude'])
        
        chapter_list = list(range(1, max(datasource['Chapter'])))
        
        charactersource = './input/'+featurefile+'_characters.csv'
        characterdf = pd.read_csv(charactersource,names=['Names'])
        characters = characterdf['Names'].tolist()
        
        datasource = datasource.groupby(['Chapter','Character','Sentiment Score']).agg({'Sentiment Score': 'count'}).rename(columns={'Sentiment Score': 'count'}).reset_index()
        datasource['Sentiment Score'] = datasource['Sentiment Score'].round(2)
           
        array_dict = {}
        
        for chap in chapter_list:
            for character in characters:
                datasource1 = datasource.loc[datasource['Chapter'] == chap]              
                array_dict[f'x_{chap}_{character}'] = datasource1[datasource['Character']==character]['Sentiment Score']
                array_dict[f'y_{chap}_{character}'] = datasource1[datasource1['Character']==character]['count']
                array_dict[f'y_{chap}_{character}'] = (array_dict[f'y_{chap}_{character}'] - array_dict[f'y_{chap}_{character}'].min()) \
                                    / (array_dict[f'y_{chap}_{character}'].max() - array_dict[f'y_{chap}_{character}'].min())
        fig = go.Figure()
    
        for index, character in enumerate(characters):
            fig.add_trace(go.Scatter(
                                    x=[-1, 1], y=np.full(2, len(characters)-index),
                                    mode='lines',
                                    line_color='white'))
            
            fig.add_trace(go.Scatter(
                                    x=array_dict[f'x_7_{character}'],
                                    y=array_dict[f'y_7_{character}'] + (len(characters)-index) + 0.4,
                                    fill='tonexty',
                                    name=f'{character}'))
            
            # plotly.graph_objects' way of adding text to a figure
            fig.add_annotation(
                                x=-1,
                                y=len(characters)-index,
                                text=f'{character}',
                                showarrow=False,
                                yshift=10)
        
        framesarr = []
        for t in chapter_list:
            for i, c in enumerate(characters):    
                frame = go.Frame(data=[go.Scatter(
                                    x=[-1, 1], y=np.full(2, len(characters)-index),
                                    mode='lines',
                                    line_color='white'),
                                        go.Scatter(
                                                x=array_dict[f'x_{t}_{c}'],
                                                y=array_dict[f'y_{t}_{c}'] + (len(characters)-i) + 0.4,
                                                fill='tonexty',
                                                name=f'{c}')])
            framesarr.append(frame)
        fig.frames = framesarr
        
        
        print(fig.frames)
        
        fig.update_layout(
             showlegend=False,
             xaxis=dict(title='Weighted Sentiment Score'),
             yaxis=dict(showticklabels=False),
             updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None]),
                             dict(label="Pause",
                                  method="animate",
                                  args=[None,
                                       {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                        "transition": {"duration": 5}}],
                                 )])]
             )
        
    elif 'Hobbit' in feature:     
        datafile = './input/'+featurefile+'_v1_gcloud.csv'
        datasource = pd.read_csv(datafile,names=['Chapter','Character','Entity','Salience','Sentiment Score','Sentiment Magnitude'])
        
        chapter_list = list(range(1, int(max(datasource['Chapter']))))
        
        charactersource = './input/'+featurefile+'_characters.csv'
        characterdf = pd.read_csv(charactersource,names=['Names'])
        characters = characterdf['Names'].tolist()
        
        datasource = datasource.groupby(['Chapter','Character','Sentiment Score']).agg({'Sentiment Score': 'count'}).rename(columns={'Sentiment Score': 'count'}).reset_index()
        datasource['Sentiment Score'] = datasource['Sentiment Score'].round(2)
           
        array_dict = {}
        
        for chap in chapter_list:
            for character in characters:
                datasource1 = datasource.loc[datasource['Chapter'] == chap]              
                array_dict[f'x_{chap}_{character}'] = datasource1[datasource['Character']==character]['Sentiment Score']
                array_dict[f'y_{chap}_{character}'] = datasource1[datasource1['Character']==character]['count']
                array_dict[f'y_{chap}_{character}'] = (array_dict[f'y_{chap}_{character}'] - array_dict[f'y_{chap}_{character}'].min()) \
                                    / (array_dict[f'y_{chap}_{character}'].max() - array_dict[f'y_{chap}_{character}'].min())
        fig = go.Figure()
        
        for index, character in enumerate(characters):
            if array_dict[f'x_7_{character}'].size == 0:
                fig.add_trace(go.Violin(x=array_dict[f'x_7_{character}'],name=character,visible=False))
            else:
                fig.add_trace(go.Violin(x=array_dict[f'x_7_{character}'],name=character))
    
        frames = []
        for t in chapter_list:
            for i, c in enumerate(characters):
                titletext = "Chapter "+str(t)
                frames.append(go.Frame(data=[go.Violin(x=array_dict[f'x_{t}_{character}'])],layout=go.Layout(title_text=titletext)))
                    
        
        fig.frames = frames
        fig.update_traces(orientation='h', side='positive', width=3, points=False)
        fig.update_layout(
             showlegend=False,
             xaxis=dict(title='Weighted Sentiment Score'),
             updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None]),
                             dict(label="Pause",
                                  method="animate",
                                  args=[None,
                                       {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                        "transition": {"duration": 5}}],
                                 )])]
             )
        
        
        
    elif 'Anna' in feature:        
        fig = go.Figure(
        data=[go.Scatter(x=[0, 1], y=[0, 1])],
        layout=go.Layout(
            xaxis=dict(range=[0, 5], autorange=False),
            yaxis=dict(range=[0, 5], autorange=False),
            title="Start Title",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        frames=[go.Frame(data=[go.Scatter(x=[1, 2], y=[1, 2])]),
                go.Frame(data=[go.Scatter(x=[1, 4], y=[1, 4])],layout=go.Layout(title_text="End Title2")),
                go.Frame(data=[go.Scatter(x=[3, 4], y=[3, 4])],
                         layout=go.Layout(title_text="End Title"))]
    )

    elif 'Crime' in feature:
        data = (np.linspace(1, 2, 12)[:, np.newaxis] * np.random.randn(12, 200) +
            (np.arange(12) + 2 * np.random.random(12))[:, np.newaxis])

        colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 12, colortype='rgb')
        
        fig = go.Figure()
        for data_line, color in zip(data, colors):
            fig.add_trace(go.Violin(x=data_line, line_color=color))
        
        fig.update_traces(orientation='h', side='positive', width=3, points=False)
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)

    else:
        A = np.random.randn(30).reshape((15, 2))
        centroids = np.random.randint(10, size=10).reshape((5, 2))
        clusters = [1, 2, 3, 4, 5]
        colors = ['red', 'green', 'blue', 'yellow', 'magenta']
        
        fig = go.Figure(
            data=[go.Scatter(x=A[:3][:,0],
                             y=A[:3][:,1],
                             mode='markers',
                             name='cluster 1',
                             marker_color=colors[0]),
                  go.Scatter(x=[centroids[0][0]],
                             y=[centroids[0][1]],
                             mode='markers',
                             name='centroid of cluster 1',
                             marker_color=colors[0],
                             marker_symbol='x')
                 ],
            layout=go.Layout(
                xaxis=dict(range=[-10, 10], autorange=False),
                yaxis=dict(range=[-10, 10], autorange=False),
                title="Start Title",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None]),
                             dict(label="Pause",
                                  method="animate",
                                  args=[None,
                                       {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                                 )])]
            ),
            frames=[
            go.Frame(
            data=[go.Scatter(x=A[:3][:,0],
                             y=A[:3][:,1],
                             mode='markers',
                             name='cluster 1',
                             marker_color=colors[0]),
                  go.Scatter(x=[centroids[0][0]],
                             y=[centroids[0][1]],
                             mode='markers',
                             name='centroid of cluster 1',
                             marker_color=colors[0],
                             marker_symbol='x')
                 ]),
            go.Frame(
                data=[
                    go.Scatter(x=A[:3][:,0],
                               y=A[:3][:,1],
                               mode='markers',
                               name='cluster 2',
                               marker_color=colors[1]),
                    go.Scatter(x=[centroids[1][0]],
                               y=[centroids[1][1]],
                               mode='markers',
                               name='centroid of cluster 2',
                               marker_color=colors[1],
                               marker_symbol='x')
                ]),
            go.Frame(
                data=[
                    go.Scatter(x=A[3:5][:,0],
                               y=A[3:5][:,1],
                               mode='markers',
                               name='cluster 3',
                               marker_color=colors[2]),
                    go.Scatter(x=[centroids[2][0]],
                               y=[centroids[2][1]],
                               mode='markers',
                               name='centroid of cluster 3',
                               marker_color=colors[2],
                               marker_symbol='x')
                ]),
            go.Frame(
                data=[
                    go.Scatter(x=A[5:8][:,0],
                               y=A[5:8][:,1],
                               mode='markers',
                               name='cluster 4',
                               marker_color=colors[3]),
                go.Scatter(x=[centroids[3][0]],
                           y=[centroids[3][1]],
                           mode='markers',
                           name='centroid of cluster 4',
                           marker_color=colors[3],
                           marker_symbol='x')]),
            go.Frame(
                data=[
                    go.Scatter(x=A[8:][:,0],
                               y=A[8:][:,1],
                               mode='markers',
                               name='cluster 5',
                               marker_color=colors[4]),
                    go.Scatter(x=[centroids[4][0]],
                               y=[centroids[4][1]],
                               mode='markers',
                               name='centroid of cluster 5',
                               marker_color=colors[4],
                               marker_symbol='x')
                ]),
            ])
        
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON= create_plot(feature)
    return graphJSON

if __name__ == '__main__':
    app.run()
