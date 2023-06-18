import pandas as pd 
import numpy as np
import uproot4 as uproot
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from itertools import chain
import multiprocessing as mp
import os
import ana_rates_lib as ana

def ana_features(Data, legends, configs, config_v6, spill = False):
    if spill:
        mult_tr = 1
        mult_snd = 1/(40*40)
    else:
        mult_tr = 66
        mult_snd = 66/(40*40)


    def get_param_label(config, iterate):
        params = ["dX_in", "dX_out", "dY_in", "dY_out", "gap_in", "gap_out"]
    #     params_dict = [i: params[i-8] for]
        it = 0
        while iterate > 0:
            if iterate < 8:
                out_param = f"dZ_{iterate}"
                break
            if iterate in range(8,14):
                out_param = params[iterate-8] + f"_{it}"
                break
            iterate -= 6
            it += 1
        return out_param

    def extract_sc_lengths(configs):
        SC_lens = []
        for config in configs:
            SC_lens.append(config[3]*2)
        return SC_lens

    def extract_rates(Data, plane_key):
        if plane_key:
            plane = 7
        else:
            plane = 1
        rates = []
        rates_err = []
        for data in Data:
            if plane != 7:
                cond_0 = "& x < 40 & x > -40 & y < 40 & y > -40"
                rates.append(data.query(f"plane == {plane}" + cond_0).W.sum())
                rates_err.append(np.sqrt(np.sum(np.square(data.query(f"plane == {plane}" + cond_0).W))))
            else:
#                 cond_0 = ""
                cond_0 = "& x < 200 & x > -200 & y < 300 & y > -300"
                rates.append(data.query(f"plane == {plane}" + cond_0).W.sum())
                rates_err.append(np.sqrt(np.sum(np.square(data.query(f"plane == {plane}" + cond_0).W))))
        return np.array(rates), np.array(rates_err)

    
    SC_lens = extract_sc_lengths(configs)
    tr_rates,tr_err = extract_rates(Data, 1)
    snd_rates, snd_err = extract_rates(Data, 0)
    
    df_vis = pd.DataFrame({"SC_lens": SC_lens, "tr_rate": tr_rates*mult_tr, "SND_rate":snd_rates*mult_snd, 
                           "configs": [get_param_label(config_v6, int(legend.split("_")[-2])) + "_" + legend.split("_")[-1] if legend != "config_05052023_v6_2023-05-29" else legend for legend in legends], "tr_err": tr_err*mult_tr, "snd_err": snd_err*mult_snd})

#     fig = px.scatter(df_vis, y="SND_rate [(Hz/cm^2)/day]", x="tr_rate", text="configs"
#                     )
    tr_max, tr_min = df_vis["tr_rate"].argmax(), df_vis["tr_rate"].argmin()
    snd_max, snd_min = df_vis["SND_rate"].argmax(), df_vis["SND_rate"].argmin()
    min_max_points = pd.DataFrame([df_vis.iloc[tr_max], df_vis.iloc[tr_min], df_vis.iloc[snd_max], df_vis.iloc[snd_min]])
#     print(df_vis["tr_rate"], "\n", 
#           df_vis["tr_rate"][1:-1], "\n", 
#           df_vis["tr_rate"][2:], "\n",
#           np.array(df_vis["tr_rate"][1:-1]) - np.array(df_vis["tr_rate"][2:]), "\n",
#           df_vis["tr_rate"][1:].values - df_vis["tr_rate"][:-1].values,
#         df_vis["SND_rate [(Hz/cm^2)/day]"][1:].values - df_vis["SND_rate [(Hz/cm^2)/day]"][:-1].values)
    print(df_vis)
#     fig = ff.create_quiver(df_vis["tr_rate"].iloc[:-1], df_vis["SND_rate [(Hz/cm^2)/day]"].iloc[:-1], 
#                            (-df_vis["tr_rate"].iloc[:-1].values + df_vis["tr_rate"].iloc[1:].values),
#                            (-df_vis["SND_rate [(Hz/cm^2)/day]"].iloc[:-1].values + df_vis["SND_rate [(Hz/cm^2)/day]"].iloc[1:].values),
#                           scale = .95,
#                           arrow_scale = 0.05,
#                           angle = np.pi/18)

    fig = go.Figure(data=go.Scatter(x=df_vis["tr_rate"], y=df_vis["SND_rate"], 
                             error_x = dict(type = 'data', array = df_vis["tr_err"]), 
                             error_y = dict(type = 'data', array = df_vis["snd_err"]),
                    mode='markers+text',
                    marker_size=12,
                    name='points'))

    fig.add_trace(go.Scatter(x=min_max_points["tr_rate"], y=min_max_points["SND_rate"], 
                             error_x = dict(type = 'data', array = min_max_points["tr_err"]), 
                             error_y = dict(type = 'data', array = min_max_points["snd_err"]),
                    mode='markers+text',
                    marker_size=12,
                    marker_color = "red",
                    name='points',
                    text = min_max_points["configs"]))
    
    fig.add_vline(x=df_vis["tr_rate"].iloc[0], line_width=3, line_dash="dash", line_color="red")
    fig.add_hline(y=df_vis["SND_rate"].iloc[0], line_width=3, line_dash="dash", line_color="red")
    
    fig.update_traces(textposition='top right')
    fig.update_layout(
        # title_text=title, # title of plot
        # showlegend=False,
        font=dict(size=18),
                width=1000,
                height=1000,
            plot_bgcolor='white'
        )
    fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
#             range = [200, 1500],
            title_text = "Muon flux at Tracking Stations [Muons/spill]"
        )
    fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            title_text = "Muon flux at SND plane 1 [(Muons/(40x40cm^2))/spill]",
            range = [0, 10]
        )
    fig.write_image("v6_scan.png")
    fig.write_image("v6_scan.pdf")
    # fig.show()


config_05052023_v6 = [70.0, 170.0, 0.0, 353.0780575329521, 125.08255586355432, 184.8344375295139, 150.19262843951793, 186.81232063446174, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 42.272041375581644, 45.68879164565739, 72.18387587325509, 8.0, 27.006281622278333, 16.244833417370145, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 24.79612428119684, 48.76386379332487, 8.000000000000052, 104.73165886004907, 15.799123331055451, 16.779328771191132, 3.000000000000501, 100.0, 242.0, 242.0, 2.0000000000000475, 4.800402845273522, 3.0000000000001097, 100.0, 8.0, 172.7285434564396, 46.82853656724763, 2.0000000000006546] 

legends_05 = ["config_05052023_v6_2023-05-29"]
Data_01 = ana.read_configs([os.path.join("SC_optimized_13052023_full_spill_flatten", filename) for filename in legends_05])


config_05052023_v6 = [70.0, 170.0, 0.0, 353.0780575329521, 125.08255586355432, 184.8344375295139, 150.19262843951793, 186.81232063446174, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 42.272041375581644, 45.68879164565739, 72.18387587325509, 8.0, 27.006281622278333, 16.244833417370145, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 24.79612428119684, 48.76386379332487, 8.000000000000052, 104.73165886004907, 15.799123331055451, 16.779328771191132, 3.000000000000501, 100.0, 242.0, 242.0, 2.0000000000000475, 4.800402845273522, 3.0000000000001097, 100.0, 8.0, 172.7285434564396, 46.82853656724763, 2.0000000000006546]


configs = []
for conf in range(len(config_05052023_v6)):
    if conf != 2 and conf < len(config_05052023_v6) - 1:
        configs.append(f"config_05052023_v6_scan_{conf}_0")
        configs.append(f"config_05052023_v6_scan_{conf}_1")
    elif conf == len(config_05052023_v6) - 1:
        configs.append(f"config_05052023_v6_scan_{conf}_0")
        configs.append(f"config_05052023_v6_scan_{conf}_1")
        
Data_scan = ana.read_configs([os.path.join("vector_scan_v6_1_flatten", filename + "_2023-05-28") for filename in configs])

configs = []
for conf in range(len(config_05052023_v6)):
    if conf != 2 and conf < len(config_05052023_v6) - 1:
        configs.append(f"config_05052023_v6_scan_{conf}_0")
        configs.append(f"config_05052023_v6_scan_{conf}_1")
    elif conf == len(config_05052023_v6) - 1:
        configs.append(f"config_05052023_v6_scan_{conf}_0")
        configs.append(f"config_05052023_v6_scan_{conf}_1")
        
        
config_05052023_v6_scan = {}
for conf in range(len(config_05052023_v6)):
    if conf != 2 and conf < len(config_05052023_v6) - 1:
        config_05052023_v6_scan[f"config_05052023_v6_scan_{conf}_0"] = config_05052023_v6[:conf] + [config_05052023_v6[conf] + 0.05*config_05052023_v6[conf]] + config_05052023_v6[conf+1:]
        config_05052023_v6_scan[f"config_05052023_v6_scan_{conf}_1"] = config_05052023_v6[:conf] + [config_05052023_v6[conf] - 0.05*config_05052023_v6[conf]] + config_05052023_v6[conf+1:]
    elif conf == len(config_05052023_v6) - 1:
        config_05052023_v6_scan[f"config_05052023_v6_scan_{conf}_0"] = config_05052023_v6[:conf] + [config_05052023_v6[conf] + 0.05*config_05052023_v6[conf]]
        config_05052023_v6_scan[f"config_05052023_v6_scan_{conf}_1"] = config_05052023_v6[:conf] + [config_05052023_v6[conf] - 0.05*config_05052023_v6[conf]]


not_working_index = [0, 1, 2]  + list(range(8,26)) + list(range(32,38)) + list(range(12, len(config_05052023_v6), 6)) + list(range(12, len(config_05052023_v6), 6)) + list(range(13, len(config_05052023_v6), 6))

working_configs = []
for conf in range(len(config_05052023_v6)):
    if conf in not_working_index: continue
    working_configs.append(f"config_05052023_v6_scan_{conf}_0") 
    working_configs.append(f"config_05052023_v6_scan_{conf}_1")

Data_dict = {config: Data_scan[i] for i, config in enumerate(configs)}
Data_scan_1 = []
configs_scan = []
for config in Data_dict:
    if config in working_configs:
        print(config)
        Data_scan_1.append(Data_dict[config])
        configs_scan.append(config_05052023_v6_scan[config])

ana_features(Data_01 + Data_scan_1, legends_05 + working_configs, [config_05052023_v6] + configs_scan, config_05052023_v6)