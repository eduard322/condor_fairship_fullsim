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

# def read_root_files(dir_name, fileName = "output_full.root"):
#     data1 = EOS_DATA + dir_name
#     basePath = sorted(Path(data1).glob(f'**/{fileName}'))
#     Data = []
#     for base_elem in basePath:
#         file = uproot.open(base_elem)
#         Data_0 = pd.DataFrame({key: file['tree;1'][key].array(library="np") for key in file['tree;1'].keys()})
#         Data.append(Data_0)
#     return pd.concat(Data, ignore_index=True)

EOS_PUBLIC = "/eos/experiment/ship/user/edursov/"
EOS_DATA = "/eos/user/e/edursov/ship_data/"        

def read_root_file(base_elem):
#     print(f"reading {base_elem}...")
    file = uproot.open(base_elem)
    Data_0 = pd.DataFrame({key: file['tree;1'][key].array(library="np") for key in file['tree;1'].keys()})
    return Data_0

def read_root_files_parallel(dir_name, fileName = "output_full.root"):
    EOS_DATA = "/eos/user/e/edursov/ship_data/"
    data1 = EOS_DATA + dir_name
    print(f"{data1}")
#     return data1
    basePath = sorted(Path(data1).glob(f'**/{fileName}'))
    print("{} files to read in {}".format(len(basePath), data1))
    with mp.Pool(processes=mp.cpu_count()) as pool:
        Data = pool.map(read_root_file, basePath)
    return pd.concat(Data, ignore_index=True)

def read_configs(configs, fileName = "output_full.root"):
    Data = []
    for config in configs:
        Data.append(read_root_files_parallel(config, fileName))
    return Data


def plot_arrays_from_params(paramsShield, is_sc=False, return_fig=False):
    dZ = paramsShield[0:8]
    dX_in = paramsShield[8::6]
    dX_out = paramsShield[9::6]
    dY_in = paramsShield[10::6]
    dY_out = paramsShield[11::6]
    gap_in = paramsShield[12::6]
    gap_out = paramsShield[13::6]

    yGaps = []
    xGaps=[]
    
    plot_z = []
    plot_x = []
    plot_y = []
    
    for i in range(2, 8):
        yGaps = yGaps + [-dY_in[i], dY_in[i], dY_out[i], -dY_out[i], -dY_in[i], None]
        xGaps = xGaps + [dX_in[i], dX_in[i]+gap_in[i], dX_out[i]+gap_out[i] , dX_out[i], dX_in[i], None]
        c_z = 0 if len(plot_z) == 0 else plot_z[-3]
        plot_z = plot_z + [c_z+10, c_z+10, c_z+10 + 2*dZ[i], c_z + 10 + 2*dZ[i], c_z + 10, None]
        if is_sc and i == 3:
            plot_x = plot_x + [-(4*dX_in[i]+gap_in[i]), (4*dX_in[i]+gap_in[i]), (4*dX_out[i]+gap_out[i]), -(4*dX_out[i]+gap_out[i]), -(4*dX_in[i]+gap_in[i]), None]
            plot_y = plot_y + [-(3*dX_in[i]+dY_in[i]), (3*dX_in[i]+dY_in[i]), (3*dX_out[i]+dY_out[i]), -(3*dX_out[i]+dY_out[i]), -(3*dX_in[i]+dY_in[i]), None]
        else:
            plot_x = plot_x + [-(2*dX_in[i]+gap_in[i]), (2*dX_in[i]+gap_in[i]), (2*dX_out[i]+gap_out[i]), -(2*dX_out[i]+gap_out[i]), -(2*dX_in[i]+gap_in[i]), None]
            plot_y = plot_y + [-(dX_in[i]+dY_in[i]), (dX_in[i]+dY_in[i]), (dX_out[i]+dY_out[i]), -(dX_out[i]+dY_out[i]), -(dX_in[i]+dY_in[i]), None]
    return([plot_x, plot_y, plot_z, xGaps, yGaps])
        
def plot_shield_from_verts_part(plot_verts, is_sc, what_to_plot, fig, row, col):
    gap_color = 'rgba(168, 235, 203, 0.5)'
    up_color = 'rgba(255,99,71, 0.8)'
    down_color = 'rgba(135,206,250, 0.8)'
    x, y, z, gap_x, gap_y = plot_verts
    
    zMax = np.max([ik for ik in z if ik is not None])
    zMin = np.min([ik for ik in z if ik is not None])
    half_position = np.argwhere(np.invert([np.isscalar(xi) for xi in x])).flatten()[2]
#     print(half_position)
#     print(half_position)
    if what_to_plot==0:
        if is_sc:
            gap_x = gap_x[:half_position-6] + gap_x[half_position:]
            data = [
                go.Scatter(x=z[:half_position-6], y=x[:half_position-6], fill="toself", fillcolor=up_color, line_color=up_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False),
                go.Scatter(x=z[half_position:], y=x[half_position:], fill="toself", fillcolor=down_color, line_color=down_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False), 
                go.Scatter(x=z[:half_position-6] + z[half_position:], y=gap_x, fill="toself", fillcolor=gap_color, line_color=gap_color, marker=dict(opacity=0), showlegend = False),
                go.Scatter(x=z[:half_position-6] + z[half_position:], y=[-p if p else None for p in gap_x], fill="toself", fillcolor=gap_color, line_color=gap_color, marker=dict(opacity=0), showlegend = False)
                   ]
        else:
            data = [
                go.Scatter(x=z[:half_position], y=x[:half_position], fill="toself", fillcolor=up_color, line_color=up_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False),
                go.Scatter(x=z[half_position:], y=x[half_position:], fill="toself", fillcolor=down_color, line_color=down_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False), 
                go.Scatter(x=z, y=gap_x, fill="toself", fillcolor=gap_color, line_color=gap_color, marker=dict(opacity=0), showlegend = False),
                go.Scatter(x=z, y=[-p if p else None for p in gap_x], fill="toself", fillcolor=gap_color, line_color=gap_color, marker=dict(opacity=0), showlegend = False)
                   ]
        for lines in data:
            fig.add_trace(lines,
                row=row, col=col)
    
            # Update xaxis properties
        fig.update_xaxes(range=[zMin, zMax+50], row=row, col=col)
        # Update yaxis properties
        fig.update_yaxes(title_text='X [cm]', range=[-330, 330], row=row, col=col)

        
    else:
        if is_sc:
            gap_y = gap_y[:half_position-6] + gap_y[half_position:]
            data=[
            go.Scatter(x=z[:half_position-6], y=y[:half_position-6], fill="toself", fillcolor=up_color, line_color=up_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False),
            go.Scatter(x=z[half_position:], y=y[half_position:], fill="toself", fillcolor=down_color, line_color=down_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False), 
            go.Scatter(x=z[:half_position-6] + z[half_position:], y=gap_y, fill="toself", fillcolor=gap_color, line_color=gap_color, marker=dict(opacity=0), showlegend = False)
               ]
        else:
            data=[
            go.Scatter(x=z[:half_position], y=y[:half_position], fill="toself", fillcolor=up_color, line_color=up_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False),
            go.Scatter(x=z[half_position:], y=y[half_position:], fill="toself", fillcolor=down_color, line_color=down_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False), 
            go.Scatter(x=z, y=gap_y, fill="toself", fillcolor=gap_color, line_color=gap_color, marker=dict(opacity=0), showlegend = False)
               ]

        for lines in data:
            fig.add_trace(lines,
            row=row, col=col) 
        fig.update_xaxes(title_text='Z [cm]', range=[zMin, zMax+50], row=row, col=col)
        # Update yaxis properties
        fig.update_yaxes(title_text='Y [cm]', range=[-330, 330], row=row, col=col)
def plot_tr_p_hists_full_1(Data_hist, figg, title, y_label, mult, row, col):

    FLUX = []
    planes = [0,1,2,7]
    query_all = ["P < 10", "P > 10 & P < 150", "P > 150"]

    for plane in planes:
        if plane != 7:
            cond_0 = "& x < 20 & x > -20 & y < 20 & y > -20"
        else:
            cond_0 = ""
        FLUX.append([Data_hist.query(cond + f"& plane == {plane}" + cond_0).W.sum()*mult for cond in query_all])
#     FLUX = np.array(FLUX).T
    
#### fixed fields
    x0 = ["T1 & (T2 or T3) & T4"]
#     x0 = ["Total"]
    x0 = [f"SND_{i}" for i in range(3)] + ["Tracking Stations"]
    x = query_all
    #     x = legends
    def flux_tot(flux):
        SUM = 0
        for f in flux:
            SUM += f
        return SUM
    
    total_flux = [flux_tot(FLUX[i]) for i in range(len(planes))]
    
    figg.add_trace(go.Histogram(histfunc='sum', y=total_flux, x=x0, name= "Total"),
                      row = row,
                      col = col)

    for j in range(3):
        figg.add_trace(go.Histogram(histfunc='sum', y=np.array(FLUX).T[j], x=x0, name= query_all[j]),
                  row = row,
                  col = col)

    figg.update_yaxes(title_text=y_label, type="log", row=row, col=col)


def plot_table(Data_hist, figg, title, y_label, mult, snd_flux, spill, row, col):
    if spill:
        spill_mult = 1
    else:
        spill_mult = 68
    rates_40x40 = Data_hist.query(f"plane == {snd_flux} & x < 20 & x > -20 & y < 20 & y > -20").W.sum()*mult*spill_mult
    rates_80x80 = Data_hist.query(f"plane == {snd_flux} & x < 40 & x > -40 & y < 40 & y > -40").W.sum()*mult
    rates_per_cm_40x40 = rates_40x40/(40*40)
    rates_per_cm_80x80 = rates_80x80/(80*80)
    rates_per_day_40x40 = rates_per_cm_40x40*5e6/1000
    rates_per_day_80x80 = rates_per_cm_40x40*5e6/1000
    figg.add_trace(go.Table(
    header=dict(values=['Rates', "Values"],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='center',
                font=dict(color='black', size=20),
                height=80),
    cells=dict(values=[["Rates [Hz]", "Rates [Hz/cm^2]", "Rates [(Hz/cm^2)/day]"], # 1st column
                       ["%.3f" % rates_40x40, "%.3f" % rates_per_cm_40x40, "%.3f" % rates_per_day_40x40]], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='center',
                font=dict(color='black', size=20),
                height=80)),
                  row = row,
                  col = col)
    
#     figg.add_trace(go.Table(
#     header=dict(values=['SND entrance', 'SND center'],
#                 line_color='darkslategray',
#                 fill_color='lightskyblue',
#                 align='left'),
#     cells=dict(values=[[100, 90, 80, 90], # 1st column
#                        [95, 85, 75, 95]], # 2nd column
#                line_color='darkslategray',
#                fill_color='lightcyan',
#                align='left')))
    
def show_config(Data, legends, configs, y_label, is_sc, show_table, mult, snd_flux = 0, out_folder = "default_folder"):
        if not show_table:
            fig = make_subplots(rows=2, cols=2, subplot_titles=legends,
                                specs=[[{}, {"rowspan": 2}],
                                [{}, None]],
                               vertical_spacing = 0.05,
                               horizontal_spacing = 0.15)
            for i, shield in enumerate(configs):
                plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 0, fig, i+1, 1)
                plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 1, fig, i+2, 1)
            for j, filename in enumerate(legends):
                plot_tr_p_hists_full_1(Data[j], fig, title = legends[j], y_label = y_label, mult = mult, row = j+1, col = 2)
        else:
            snd_type = "SND entrance" if not snd_flux else "SND center"
            fig = make_subplots(rows=2, cols=2, subplot_titles=legends + [None, None, snd_type],
                                specs=[[{"type": "scatter"}, {"type": "histogram"}],
                                   [{"type": "scatter"}, {"type": "table"}]],
                               vertical_spacing = 0.1,
                               horizontal_spacing = 0.15)
            for i, shield in enumerate(configs):
                plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 0, fig, i+1, 1)
                plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 1, fig, i+2, 1)
            for j, filename in enumerate(legends):
                plot_tr_p_hists_full_1(Data[j], fig, title = legends[j], y_label = y_label, mult = mult, row = j+1, col = 2)
                plot_table(Data[j], fig, title = legends[j], y_label = y_label, mult = mult, snd_flux = snd_flux, spill = False, row = j+2, col = 2)
        fig.update_layout(
        # title_text=title, # title of plot
        # showlegend=False,
        font=dict(size=18),
                width=2000,
                height=1000,
        title_text="Muon flux rates",
            plot_bgcolor='white',
            barmode='group'
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        if not os.path.exists(f"./{out_folder}"):
            os.makedirs(f"./{out_folder}")
        fig.write_html(f"./{out_folder}/{legends}.html")
        fig.show()
        

def draw_scatter_plots(Data, legends, configs):
    def extract_sc_lengths(configs):
        SC_lens = []
        for config in configs:
            SC_lens.append(config[3]*2)
        return SC_lens

    def extract_rates(Data, plane_key):
        if plane_key:
            plane = 7
        else:
            plane = 0
        rates = []
        for data in Data:
            if plane != 7:
                cond_0 = "& x < 40 & x > -40 & y < 40 & y > -40"
                rates.append(data.query(f"plane == {plane}" + cond_0).W.sum()*68*5e6/(1000*(80*80)))
            else:
                cond_0 = ""
                rates.append(data.query(f"plane == {plane}" + cond_0).W.sum()*68)
        return rates

    
    SC_lens = extract_sc_lengths(configs)
    tr_rates = extract_rates(Data, 1)
    snd_rates = extract_rates(Data, 0)
    
    df_vis = pd.DataFrame({"SC_lens": SC_lens, "tr_rate": tr_rates, "SND_rate [(Hz/cm^2)/day]":snd_rates, 
                           "configs": [legend[7:18] for legend in legends]})
    fig = px.scatter(df_vis, x="SC_lens", y="tr_rate", 
                     color = "SND_rate [(Hz/cm^2)/day]", size = "SND_rate [(Hz/cm^2)/day]", size_max=60,
                     text="configs"
                    )
    fig.update_traces(textposition='top center')
    fig.update_layout(
        # title_text=title, # title of plot
        # showlegend=False,
        font=dict(size=18),
                width=2000,
                height=1000,
            plot_bgcolor='white'
        )
    fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            title_text = "SC length [cm]"
        )
    fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            title_text = "Muon flux at Tracking Stations [a.u.]"
        )
#     fig.write_image("fig1.png")
    fig.show()
    

    
def draw_snd_vs_tr(Data, legends, configs):
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
        return rates, rates_err

    
    SC_lens = extract_sc_lengths(configs)
    tr_rates,tr_err = extract_rates(Data, 1)
    snd_rates, snd_err = extract_rates(Data, 0)
    
    df_vis = pd.DataFrame({"SC_lens": SC_lens, "tr_rate": tr_rates, "SND_rate [(Hz/cm^2)/day]":snd_rates, 
                           "configs": [legend.split("_")[-2] for legend in legends]})
#     fig = px.scatter(df_vis, y="SND_rate [(Hz/cm^2)/day]", x="tr_rate", text="configs"
#                     )
    
#     print(df_vis["tr_rate"], "\n", 
#           df_vis["tr_rate"][1:-1], "\n", 
#           df_vis["tr_rate"][2:], "\n",
#           np.array(df_vis["tr_rate"][1:-1]) - np.array(df_vis["tr_rate"][2:]), "\n",
#           df_vis["tr_rate"][1:].values - df_vis["tr_rate"][:-1].values,
#         df_vis["SND_rate [(Hz/cm^2)/day]"][1:].values - df_vis["SND_rate [(Hz/cm^2)/day]"][:-1].values)
    print(df_vis)
    fig = ff.create_quiver(df_vis["tr_rate"].iloc[:-1], df_vis["SND_rate [(Hz/cm^2)/day]"].iloc[:-1], 
                           (-df_vis["tr_rate"].iloc[:-1].values + df_vis["tr_rate"].iloc[1:].values),
                           (-df_vis["SND_rate [(Hz/cm^2)/day]"].iloc[:-1].values + df_vis["SND_rate [(Hz/cm^2)/day]"].iloc[1:].values),
                          scale = .95,
                          arrow_scale = 0.05,
                          angle = np.pi/18)
    
    fig.add_trace(go.Scatter(x=df_vis["tr_rate"]*68, y=df_vis["SND_rate [(Hz/cm^2)/day]"]*68/(40*40), 
                             error_x = dict(type = 'data', array = np.array(tr_err)*68), 
                             error_y = dict(type = 'data', array = np.array(snd_err)*68/(40*40)),
                    mode='markers+text',
                    marker_size=12,
                    name='points',
                            text = df_vis["configs"]))
    
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
            title_text = "Muon flux at Tracking Stations [a.u.]"
        )
    fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            title_text = "SND_rate [a.u.]",
            range = [0, 10]
        )
#     fig.write_image("fig1.png")
    fig.show()
    

    
def ana_features(Data, legends, configs):
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
        return rates, rates_err

    
    SC_lens = extract_sc_lengths(configs)
    tr_rates,tr_err = extract_rates(Data, 1)
    snd_rates, snd_err = extract_rates(Data, 0)
    
    df_vis = pd.DataFrame({"SC_lens": SC_lens, "tr_rate": tr_rates, "SND_rate [(Hz/cm^2)/day]":snd_rates, 
                           "configs": [legend.split("_")[-2] for legend in legends]})
#     fig = px.scatter(df_vis, y="SND_rate [(Hz/cm^2)/day]", x="tr_rate", text="configs"
#                     )
    
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

    fig = go.Figure(data=go.Scatter(x=df_vis["tr_rate"]*68, y=df_vis["SND_rate [(Hz/cm^2)/day]"]*68/(40*40), 
                             error_x = dict(type = 'data', array = np.array(tr_err)*68), 
                             error_y = dict(type = 'data', array = np.array(snd_err)*68/(40*40)),
                    mode='markers+text',
                    marker_size=12,
                    name='points'))
    
    fig.add_vline(x=df_vis["tr_rate"].iloc[0]*68, line_width=3, line_dash="dash", line_color="red")
    fig.add_hline(x=df_vis["SND_rate [(Hz/cm^2)/day]"]*68/(40*40), line_width=3, line_dash="dash", line_color="red")
    
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
            title_text = "Muon flux at Tracking Stations [a.u.]"
        )
    fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            title_text = "SND_rate [a.u.]",
            range = [0, 10]
        )
#     fig.write_image("fig1.png")
    fig.show()


def shield_animation(Data, legends, configs, y_label, is_sc, show_table, mult, snd_flux = 0, out_folder = "default_folder"):  
    def extract_sc_lengths(configs):
        SC_lens = []
        for config in configs:
            SC_lens.append(config[3]*2)
        return SC_lens

    def extract_rates(Data, plane_key):
        if plane_key:
            plane = 7
        else:
            plane = 0
        rates = []
        for data in Data:
            if plane != 7:
                cond_0 = "& x < 40 & x > -40 & y < 40 & y > -40"
                rates.append(data.query(f"plane == {plane}" + cond_0).W.sum()*68*5e6/(1000*(40*40)))
            else:
                cond_0 = ""
                rates.append(data.query(f"plane == {plane}" + cond_0).W.sum()*68)
        return rates

    
    SC_lens = extract_sc_lengths(configs)
    tr_rates = extract_rates(Data, 1)
    snd_rates = extract_rates(Data, 0)
    
    df_vis = pd.DataFrame({"SC_lens": SC_lens, "tr_rate": tr_rates, "SND_rate [(Hz/cm^2)/day]":snd_rates, 
                           "configs": [legend[7:18] for legend in legends]})
    
    
    
    fig = make_subplots(rows=2, cols=2, subplot_titles=legends,
                                specs=[[{}, {"rowspan": 2}],
                                [{}, None]],
                               vertical_spacing = 0.05,
                               horizontal_spacing = 0.15)
    for i, shield in enumerate(configs):
            plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 0, fig, i+1, 1)
            plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 1, fig, i+2, 1)
    for j, filename in enumerate(legends):
            plot_tr_p_hists_full_1(Data[j], fig, title = legends[j], y_label = y_label, mult = mult, row = j+1, col = 2)
    fig.update_layout(
    # title_text=title, # title of plot
    # showlegend=False,
    font=dict(size=18),
            width=2000,
            height=1000,
    title_text="Muon flux rates",
        plot_bgcolor='white',
        barmode='group'
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
        )
    
    
    
    fig = px.scatter(df_vis, y="SND_rate [(Hz/cm^2)/day]", x="tr_rate", 
                     color = "SND_rate [(Hz/cm^2)/day]", size = "SND_rate [(Hz/cm^2)/day]", size_max=60,
                     text="configs"
                    )

    fig.show()
    
def draw_snd_extrapolate(Data, title, distance = 1000.):
    def check_projection(df, z_plane):
        x = df["x"] - (df["z"] - pd.Series([z_plane]*len(df["z"])))*df["px"]/df["pz"]
        y = df["y"] - (df["y"] - pd.Series([z_plane]*len(df["y"])))*df["py"]/df["pz"]
        return x,y, df["W"]
#         if (-(shield_x + 10) < x and x < (shield_x + 10)) and (-(shield_y + 10)< y and y < (shield_y + 10)):
#             return (True, x, y)
#         else:
#             return (False, x, y)

    df_plane_0 = Data[0].query("plane == 0")
    extra_df = []
    W_list = []
    z_range = np.linspace(df_plane_0["z"].mean(), df_plane_0["z"].mean() + distance, 10)
    for z in z_range:
        x,y,W = check_projection(df_plane_0, z)
        W_list.append(pd.DataFrame({"x": x, "y": y, "W": W}).query("x < 20 & x > -20 & y < 20 & y > -20").W.sum())
        
    
    
    fig = px.scatter(x=[z - df_plane_0["z"].mean() for z in z_range], y=W_list)
    fig.update_traces(textposition='top center')
    fig.update_layout(
        title_text=title, # title of plot
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
            title_text = "Distance from the SND_0 [cm]"
        )
    fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            title_text = "Muons/spill"
        )
#     fig.write_image("fig1.png")
    fig.show()
    
 

def make_hist2d(Data, title, config, box):
#     df_snd = Data[0].query("plane == 0")
    df_tr = Data[0].query("plane == 7")
    for i in range(3):
        df_snd = Data[0].query(f"plane == {i}")
        fig, ax = plt.subplots(figsize = (8,8), dpi = 200)
    #     fig.suptitle(title + f". {config}", fontsize = 18)
        h = ax.hist2d(df_snd["x"], df_snd["y"], weights = df_snd["W"], 
                         bins = 200, norm=mpl.colors.LogNorm(),
#                          range=((-100,100),(-100,100)),
                         cmap = plt.cm.jet)
        border_2 = patches.Rectangle((-20,-20), 40, 40, linewidth=3, edgecolor='r', facecolor='none')
        if box:
            ax.add_patch(border_2)
        ax.set_xlabel("X [cm]", fontsize = 16)
        ax.set_title(f"Muon flux at SND Plane {i}", fontsize = 16)
        ax.set_ylabel("Y [cm]", fontsize = 16)
        ax.legend()
        fig.colorbar(h[3], ax=ax)
    fig, ax = plt.subplots(figsize = (8,8), dpi = 200)
    h = ax.hist2d(df_tr["x"], df_tr["y"], weights = df_tr["W"], 
               bins = 200, norm=mpl.colors.LogNorm(), 
                   range=((-550,550),(-550,550)),
                   cmap=plt.cm.jet)
    data = image.imread('Tr1_pic_1.png')
    ax.imshow(data, extent=[-320,327,-470,484])
    ax.set_title(f"Muon flux at Tracking Stations", fontsize = 16)
#     ax[1].axvline(x = -200, color = 'r')
#     ax[1].axvline(x = 200, color = 'r')
    ax.set_xlabel("X [cm]", fontsize = 16)
    ax.set_ylabel("Y [cm]", fontsize = 16)
    ax.patch.set_facecolor('white')
    ax.patch.set_alpha(1)
    fig.colorbar(h[3], ax=ax, fraction=0.046, pad=0.04)

def make_heatmap(self):
        h =  r.TH2D("Heatmap. " + self.title, "Heatmap." + self.title, 20, -120, 120, 20, -260, 260)
        h.FillN(len(self.Data_hist["x"]), 
                array("d", self.Data_hist["x"]), 
                array("d", self.Data_hist["y"]), 
                array("d", self.Data_hist["W"]))
        c  = r.TCanvas("Heatmap." + self.title,"Heatmap." + self.title,0,0,2000,2000)
        r.gPad.SetLogz()
        h.SetMarkerSize(0.75)
        r.gStyle.SetPaintTextFormat(".0e")
        h.GetXaxis().SetTitle("X, cm")
        h.GetYaxis().SetTitle("Y, cm")
        h.GetZaxis().SetTitle("Hz")
        h.Draw("COLZTEXT")

        box = r.TBox(-40, -40, 40, 40)
        box.SetLineColor(r.kRed)
        box.SetFillStyle(0)
        box.SetLineWidth(2)
        box.Draw("SAME")

        box1 = r.TBox(-60,-170, 60,170)
        box1.SetLineColor(r.kRed)
        box1.SetFillStyle(0)
        box1.SetLineWidth(2)
        box1.Draw("SAME")
        #c.SetWindowSize(1200, 1200)
        c.Draw()
        c.SaveAs("heatmap_{0}.pdf".format(self.title.replace(" ", "_")))
    
def plot_tr_p_hists_full(Dataset, label, legends, key = 0, set_bins = 30, histtype = "bar", alpha = 1.0, color_err = "blue", line_width = 1.5, point_key = 0, marker_size = 5):
    plt.style.use('default')
    colors = ["blue", "orange", "green", "red", "pink"]
#     if not point_key:
#         FMT = ["b."]*len(filenames)
#     else:
#         FMT = ["o", "h", "x"]

    FLUX = []
    query_all = ["P < 10", "P > 10 & P < 150", "P > 150"]
    fig, ax = plt.subplots(figsize = (8,16), dpi = 250)  
    for iterate, Data_hist in enumerate([Data.query("plane == 7") for Data in Dataset]):
        FLUX.append([Data_hist.query(cond).W.sum() for cond in query_all])
        if key:
            _, bin_size = np.histogram(Data_hist.query("P <= 300")["P"], set_bins)
            bin_size = float(bin_size[2:3] - bin_size[1:2])
        if not key:
            label_y = "Hz"
            legend_label = "kHz"
            bin_size = 1.
        else:
            label_y = "Rates [Hz/{:.0f}(GeV/c)]".format((bin_size))
            legend_label = " kHz"
            bin_size = 1.
            Data_hist["W"] = Data_hist["W"]/bin_size
        entries, bins, _ = ax.hist(Data_hist["P"], weights = Data_hist["W"],
                                   bins = set_bins,
                                   range = [0,300],
                                   alpha = alpha,
                                   histtype = histtype,
                                   color = colors[iterate],
                                   linewidth=line_width,
                                   label = legends[iterate] + "Muon rate: {:.0f} {legend}".format((Data_hist["W"].sum()*(bin_size)/1000), legend = legend_label))
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        #legends["ECN3_shield"] = CDS + "Muons from shield: {:.0f} {legend}".format((Data_shield["W"].sum()*(bin_size)/1000), legend = legend_label)
        Data_hist['cut'] = pd.cut(Data_hist["P"], bins=bins)
        errors = Data_hist.groupby(['cut']).agg(lambda x: np.sqrt(np.sum(np.square(x))))
        errors = errors["W"]
        ax.errorbar(bin_centers, entries, yerr=errors, fmt=".", ecolor = "black")
        #ax.scatter(bin_centers, entries, s = marker_size, 
        #              label =  legends[iterate] + "Muon rate: {:.0f} {legend}".format((Data_hist["W"].sum()*(bin_size)/1000), legend = legend_label))

    

    ax.set_xlabel("P [GeV/c]", fontsize = 14)
    ax.set_title("T1 muon momentum in tracker histogram", fontsize = 16)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(1)
    ax.set_yscale("log")
    ax.set_ylim([1e0, 1e6])
    ax.set_ylabel(label_y, fontsize = 16)    
    #ax.legend([legends["ECN3_shield"], legends["ECN3_walls"], legends["CDS_shield"], legends["CDS_walls"]])
    ax.legend()
    fig.savefig(label.replace(" ", "_") + "_P_hist.pdf")
    fig.show()
    fig.savefig(label.replace(" ", "_") + "_P_hist.pdf")
    fig.show()
    
#### fixed fields
    x0 = ["T1 & (T2 or T3) & T4"]
#     x0 = ["Total"]
    x = query_all
    #     x = legends
    figg = go.Figure()
    def flux_tot(flux):
        SUM = 0
        for f in flux:
            SUM += f
        return SUM

    for i in range(len(Dataset)):
        figg.add_trace(go.Histogram(histfunc='sum', y=[flux_tot(FLUX[i])], x=x0, name= legends[i] + "Total"))

    for j in range(3):
        for i in range(len(Dataset)):
            figg.add_trace(go.Histogram(histfunc='sum', y=[FLUX[i][j]], x=x0, name= legends[i] + query_all[j]))
    figg.update_layout(
        title_text='Muon track rates in Tracking Stations', # title of plot
        #xaxis_title_text='Value', # xaxis label
        yaxis_title_text='Muons/spill', # yaxis label
        bargap=0.05, # gap between bars of adjacent location coordinates
        bargroupgap=0.05, # gap between bars of the same location coordinates
        width=1500,
        height=1400,
        font=dict(size=22),
        plot_bgcolor='white'
    )

    figg.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    figg.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    figg.update_yaxes(type="log")
    figg.show()
    
    FLUX_dict = {legend: {query:FLUX[i][j] for j, query in enumerate(query_all)} for i, legend in enumerate(legends)}
    for i, key in enumerate(FLUX_dict.keys()):
        FLUX_dict[key]["Total"] = flux_tot(FLUX[i])
    print(FLUX_dict)
    return FLUX_dict
    

def vis_all(Data, legends, configs, y_label = "Muons/spill", is_sc = True, show_table = False, mult = 1, snd_flux = 0, out_folder = "default_folder"):
    for i in range(len(legends)):
        show_config([Data[i]], [legends[i]], [configs[i]], y_label, is_sc, show_table, mult, snd_flux, out_folder = out_folder)
        
    