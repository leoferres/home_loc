###############################################################################
#    This program by L Ferres & L Pappalardo is in the public
#    domain and freely copyable.  (or, if there were problems, in the
#    errata --- see http://leoferres.info/programs.html) If you find
#    any bugs, please report them immediately to: lferres@udd.cl
###############################################################################
#
# FILE NAME: hdas.py
#
# PURPOSE: These algorithms (algo1-algo5) calculate home detection
# given a dataset of CDR/XDR/CPRs, one per line. The other two algos
# (algo6-algo7) are a "work identification" version of home detection
# algos 4 and 5. These are based on Vanhoof 2018:
#
# Vanhoof, M., Reis, F., Ploetz, T., & Smoreda, Z. (2018). Assessing
# the quality of home detection from mobile phone data for official
# statistics. In Journal of Official Statistics (Vol. 34,
# pp. 935–960). https://doi.org/10.2478/jos-2018-0046
#
# Creation date: 2020-10-09 14:03:43 -0300
#
###############################################################################


# some auxiliary functions

def _merge_and_sort(stream_df, user, gb=None):
    if gb is None:
        gb = ['device', 'activity', 'tower']
    res = pd.merge(stream_df, user,
                   how='left', on='device').dropna()
    return res.sort_values(gb, ascending=False)


def _filter_times(stream_df, start, end):
    return stream_df.between_time(start_time=start,
                                  end_time=end,
                                  include_start=True,
                                  include_end=False)

# the home detection algorithms

def algo1(tframe, user, a1km, a1km_df, stream):
    df = tframe.groupby(['device',
                         'tower']).size().reset_index(name='activity')
    df = _merge_and_sort(df, user)
    df['stream'] = stream
    df['algorithm'] = 'algo1'
    return df

def algo2(tframe, user, a1km, a1km_df, stream):
    tframe['dates'] = tframe['datetime'].dt.date
    df = (tframe.groupby(['device', 'tower'])['dates']
          .nunique()
          .reset_index(name='activity'))
    df = _merge_and_sort(df, user)
    df['stream'] = stream
    df['algorithm'] = 'algo2'
    return df

def algo3(tframe, user, a1km, a1km_df, stream):
    tframe = tframe.set_index('datetime')
    tframe = _filter_times(tframe, '19:00', '07:00').reset_index()
    df = algo1(tframe, user, a1km, a1km_df, stream)
    df['stream'] = stream
    df['algorithm'] = 'algo3'
    return df

def algo4(tframe, user, a1km, a1km_df, stream):
    df = tframe[tframe['tower'].isin(list(a1km.keys()))]
    df = df.groupby(['device',
                     'tower']).size().reset_index(name='activity')
    df = pd.merge(a1km_df, df, left_on='tower2', right_on='tower')
    df = df.groupby(['device',
                     'tower1'])['activity'].sum().reset_index(name='activity')
    df = df.rename(columns={'tower1': 'tower'})
    df = _merge_and_sort(df, user)
    df['stream'] = stream
    df['algorithm'] = 'algo4'
    return df


def algo5(tframe, user, a1km, a1km_df, stream):
    tframe = tframe.set_index('datetime')
    tframe = _filter_times(tframe, '19:00', '07:00').reset_index()
    df = algo4(tframe, user, a1km, a1km_df, stream)
    df['stream'] = stream
    df['algorithm'] = 'algo5'
    return df


def algo6(tframe, user, a1km, a1km_df, stream):
    tframe = tframe.set_index('datetime')
    tframe = _filter_times(tframe, '07:00', '19:00').reset_index()
    df = algo1(tframe, user, a1km, a1km_df, stream)
    df['stream'] = stream
    df['algorithm'] = 'algo6'
    return df

def algo7(tframe, user, a1km, a1km_df, stream):
    tframe = tframe.set_index('datetime')
    tframe = _filter_times(tframe, '7:00', '19:00').reset_index()
    df = algo4(tframe, user, a1km, a1km_df, stream)
    df['stream'] = stream
    df['algorithm'] = 'algo7'
    return df

