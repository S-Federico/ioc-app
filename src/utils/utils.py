import pandas as pd
from models.models import GraphData
from typing import Callable, Dict
from dateutil.parser import parse as parse_date

ALL_GRAPHS: Dict[int, GraphData] = {
    0: GraphData(
        id=0,
        title='IoC by indicator_type',
        type='bar',
        description='This graph shows how many IoC where collected grouped by indicator_type'
    ),
    1: GraphData(
        id=1,
        title='IoC by user',
        type='bar',
        description='This graph shows how many IoC where found by users'
    ),
    2: GraphData(
        id = 2,
        title='IoC by label',
        type='bar',
        description='This graph shows how many IoC where collected grouped by indicator_type'
    ),
    3: GraphData(
        id = 3,
        title='IoC discovered first by twitter',
        type='bar',
        description='This graph shows how many IoC where discovered first by twitter'
    ),
    4: GraphData(
        id = 4,
        title='Percentages of IoC\'s categories',
        type='bar',
        description='This graph shows the percentages of IoC\'s categories'
    ),
    5: GraphData(
        id = 5,
        title='Twitter after AlienVoult',
        type='bar',
        description='This graph shows the number of times Twitter comes after AlienVault'
    ),
    6: GraphData(
        id = 6,
        title='Twitter after Kaspersky',
        type='bar',
        description='This graph shows the number of times Twitter comes after Kaspersky'
    )

}

def ioc_by_indicatortype_data(full_df: pd.DataFrame) -> GraphData:
    df = full_df.groupby(['indicator_type'])['indicator'].count()
    graph_data = ALL_GRAPHS.get(0)
    graph_data.labels = list(df.index)
    graph_data.data = list(df)
    return graph_data


def ioc_by_user_data(full_df: pd.DataFrame) -> GraphData:
    df = full_df.groupby(['user'])['indicator'].count()
    graph_data = ALL_GRAPHS.get(1)
    graph_data.labels = list(df.index)
    graph_data.data = list(df)
    return graph_data


def ioc_by_label(full_df: pd.DataFrame) -> GraphData:
    df = full_df.groupby(['label'])['indicator'].count()    
    graph_data = ALL_GRAPHS.get(2)
    graph_data.labels = list(df.index)
    graph_data.data = list(df)
    return graph_data   

def ioc_got_first_by_twitter_data(full_df: pd.DataFrame) -> GraphData:
    dates = [index for index in list(full_df.columns) if '_date' in index]
    print(dates)
    dates.remove('twitter_date')

    df = full_df
    total_ioc = len(full_df)
    ioc_first_twitter = 0

    for index, value in df.iterrows():
        is_twitter_first = True
        for col in dates:
            if value['twitter_date'] < value[col]:
                is_twitter_first = False
                break
        if is_twitter_first:
            ioc_first_twitter += 1
    """
    for date in dates:
        print('Printing stuff:',df['twitter_date'], df[date])
        df = df[df['twitter_date'] > df[date]]
    ioc_first_twitter = len(df)
    """
    labels = ['first_twitter', 'first_other_platforms']
    data = [ioc_first_twitter, total_ioc - ioc_first_twitter]

    graph_data = ALL_GRAPHS.get(3)
    graph_data.labels = labels
    graph_data.data = data
    return graph_data



def ioc_categories_percentages(full_df: pd.DataFrame) -> GraphData:
    num_rows = full_df.shape[0]
    series = full_df.groupby(['indicator_type'])['indicator'].count()
    series = series.map(lambda elem : round(elem/num_rows*100, 2))
    graph_data = ALL_GRAPHS.get(4)
    graph_data.labels = list(series.index)
    graph_data.data = list(series)
    return graph_data

def twitter_after_alienvault(full_df: pd.DataFrame) -> GraphData:
    
    df= full_df
    df['tw_to_av'] = df['tw_to_av'].replace('None','0')
    df['tw_to_av'] = df['tw_to_av'].astype('float')
    df2= df[df["tw_to_av"] > 0]
    
    df = df2.groupby(['indicator_type'])['tw_to_av'].count()  
    
    print(df)
    graph_data = ALL_GRAPHS.get(5)
    graph_data.labels = list(df.index)
    graph_data.data = list(df)
    return graph_data

def twitter_after_kaspersky(full_df: pd.DataFrame) -> GraphData:
    
    df= full_df
    df['tw_to_k'] = df['tw_to_k'].replace('None','0')
    df['tw_to_k'] = df['tw_to_k'].astype('float')
    df2= df[df["tw_to_k"] > 0]
    
    df = df2.groupby(['indicator_type'])['tw_to_k'].count()  
    
    print(df)
    graph_data = ALL_GRAPHS.get(6)
    graph_data.labels = list(df.index)
    graph_data.data = list(df)
    return graph_data


#TODO: Add other functions for other graphs here!

GRAPH_DICT: Dict[int, Callable[[pd.DataFrame], GraphData]] = {
    0: ioc_by_indicatortype_data,
    1: ioc_by_user_data,
    2: ioc_by_label,
    3: ioc_got_first_by_twitter_data,
    4: ioc_categories_percentages,
    5: twitter_after_alienvault,
    6: twitter_after_kaspersky
}

def get_graph_data(full_df: pd.DataFrame, graph_id: int) -> GraphData:
    try:
        res = GRAPH_DICT.get(graph_id)(full_df)
        return res
    except Exception as e:
        print(e)
        return None

def get_all_graphs_reducted() -> list[GraphData]:
    return list(ALL_GRAPHS.values())
