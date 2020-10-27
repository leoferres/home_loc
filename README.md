# home_loc

Home location/detection algorithms for mobile phone streams

## Intro

**WARNING**: This is experimental software and is provided *as is*. If
there are any bugs/errors/etc. don't hesitate to write a pull request.

This is the implementation of the 5 algorithms described in

Vanhoof, M., Reis, F., Ploetz, T., & Smoreda, Z. (2018). Assessing the
quality of home detection from mobile phone data for official
statistics. In Journal of Official Statistics (Vol. 34,
pp. 935–960). https://doi.org/10.2478/jos-2018-0046

that we used in our paper:

Luca Pappalardo, Leo Ferres, Manuel Sacasa, Ciro Cattuto, Loreto
Bravo. 2020. An Evaluation of Home Location Identification
Algorithms For Mobile Phone Datasets Using "Ground Truth". 
https://arxiv.org/abs/2010.08814

They all take, as input, a dataframe (`tframe`) of CD-like records of
the form

`<hash, tower, timestamp>`,

as described in the paper, where `hash` is the anonymyzed phone
number, `tower` is some tower identifier (there's no need of lat/lon
here), and the `time` is the timestamp of the event. XDR, and CPR can
follow the same tuple/schema.

The argument `user` is a dataframe that contains each user's home
address (in lat/lon), and the three nearest towers (using some measure
of distance, we used *k*-nearest neighbors).

The argument `a1km_df` is a dataframe that contains *all* the towers
that are 1km away from each other, in a dictionary like `ABCD1':
['SDFC4', 'LUCA1', 'CIRO1']`, meanwhile, `a1k_df` is simply `a1k` in
"dataframe" format, or flattened out like:

```
	tower1	tower2
0	ABCD1	SDFC4
1	ABCD1	LUCA1
2	ABCD1	CIRO1
```

Finally, `stream` is a string that identifies the mobile phone stream:
'cdr', 'xdr' and 'cpr' in our case.

Not all arguments are used in all the functions, they're there for
convenience to our running of experiments, just so we don't have to
call each one with a different signature and we simply store them in a
list. The real signature of the functions are as follows:

``` python
    algo1_df = algo1(data[a], U, stream=streams[a])
    algo2_df = algo2(data[a], U, stream=streams[a])
    algo3_df = algo3(data[a], U, stream=streams[a])
    algo4_df = algo4(data[a], U, a1k, a1k_df, stream=streams[a])
    algo5_df = algo5(data[a], U, a1k, a1k_df, stream=streams[a])
    algo6_df = algo6(data[a], U, stream=streams[a])
    algo7_df = algo5(data[a], U, a1k, a1k_df, stream=streams[a])
```

assuming we load streams as something like:

``` python
streams = ["cdr", "xdr", "cpr"]
data = []
for s in streams:
    data.append(pd.read_csv(f"output/{s}_normalized.csv",
                            parse_dates=["datetime"]))
```

