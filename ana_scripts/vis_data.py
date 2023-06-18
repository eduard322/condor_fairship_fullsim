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

EOS_PUBLIC = "/eos/experiment/ship/user/edursov/"
EOS_DATA = "/eos/user/e/edursov/ship_data/"

def read_root_file(base_elem):
#     print(f"reading {base_elem}...")
    file = uproot.open(base_elem)
    Data_0 = pd.DataFrame({key: file['tree;1'][key].array(library="np") for key in file['tree;1'].keys()})
    return Data_0

def read_root_files_parallel(dir_name, fileName = "output_full.root"):
    data1 = EOS_DATA + dir_name
    print(f"{data1}")
#     return data1
    basePath = sorted(Path(data1).glob(f'**/{fileName}'))
    print("{} files to read in {}".format(len(basePath), data1))
    with mp.Pool(processes=mp.cpu_count()) as pool:
        Data = pool.map(read_root_file, basePath)
    return pd.concat(Data, ignore_index=True), len(basePath)

def read_configs(configs, fileName = "output_full.root"):
    Data = []
    nums = []
    for config in configs:
        extract_data, number_of_files = read_root_files_parallel(config, fileName)
        Data.append(extract_data)
        nums.append(number_of_files)
    return Data, nums


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
                go.Scatter(x=z[:half_position-6], y=x[:half_position-6], fill="toself", fillcolor=up_color, line_color=up_color, marker=dict(opacity=0), meta=dict(name="Up polarity"), showlegend = False),
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
def plot_tr_p_hists_full_1(Data_hist, figg, title, y_label, mult, config, row, col):

    FLUX = []
    planes = [0,1,2,7]
    query_all = ["P < 10", "P > 10 & P < 150", "P > 150"]

    for plane in planes:
        if plane != 7:
            cond_0 = "& x < 20 & x > -20 & y < 20 & y > -20"
        else:
            cond_0 = "& x < 200 & x > -200 & y < 300 & y > -300"
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

    def extract_sc_lengths(configs):
        SC_lens = []
        for config in configs:
            SC_lens.append(config[3]*2)
        return SC_lens
    def extract_muon_shield_length(configs):
        SC_lens = []
        for config in configs:
            SC_lens.append(sum(config[2:8])*2)
        return SC_lens
    def extract_gap(configs):
        gap = []
        for config in configs:
            gap.append(config[4]*2)
        return gap
    def extract_snd_rates(FLUX):
        rates = [sum(FLUX[i])/(40*40) for i in range(3)]
        return rates
    def extract_tr_rates(FLUX):
        return sum(FLUX[-1])

    data_out = [extract_sc_lengths([config])[0], extract_gap([config])[0]] + extract_snd_rates(FLUX) + [extract_tr_rates(FLUX)]
    print(data_out)
        
    

def plot_table(Data_hist, figg, title, y_label, mult, row, col):
    rates_40x40 = Data_hist.query("plane == 0 & x < 20 & x > -20 & y < 20 & y > -20").W.sum()*mult
    rates_80x80 = Data_hist.query("plane == 0 & x < 40 & x > -40 & y < 40 & y > -40").W.sum()*mult
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
                       ["%.2f" % rates_40x40, "%.2f" % rates_per_cm_40x40, "%.2f" % rates_per_day_40x40]], # 2nd column
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
    
def show_config(Data, legends, configs, y_label, is_sc, show_table, mult, out_folder = "default_folder"):
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
                plot_tr_p_hists_full_1(Data[j], fig, title = legends[j], y_label = y_label, mult = mult, config = config[j], row = j+1, col = 2)
        else:
            fig = make_subplots(rows=2, cols=2, subplot_titles=legends,
                                specs=[[{"type": "scatter"}, {"type": "histogram"}],
                                   [{"type": "scatter"}, {"type": "table"}]],
                               vertical_spacing = 0.05,
                               horizontal_spacing = 0.15)
            for i, shield in enumerate(configs):
                plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 0, fig, i+1, 1)
                plot_shield_from_verts_part(plot_arrays_from_params(shield, is_sc = is_sc), is_sc, 1, fig, i+2, 1)
            for j, filename in enumerate(legends):
                plot_tr_p_hists_full_1(Data[j], fig, title = legends[j], y_label = y_label, mult = mult, config = configs[j], row = j+1, col = 2)
                plot_table(Data[j], fig, title = legends[j], y_label = y_label, mult = mult, row = j+2, col = 2)
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
        fig.write_image(f"./{out_folder}/{legends[0]}.png")
        fig.write_image(f"./{out_folder}/{legends[0]}.pdf")
        # fig.show()



        

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
    fig.show()

def vis_all(Data, legends, configs, y_label = "Muons/spill", is_sc = True, show_table = False, mult = 1, out_folder = "default_folder"):
    for i in range(len(legends)):
        show_config([Data[i]], [legends[i]], [configs[i]], y_label, is_sc, show_table, mult, out_folder = out_folder)
        
if __name__ == '__main__':
    config_04032023_v0 = [70.0, 170.0, 0.0, 358.4735584780767, 50.0, 172.82, 212.54, 168.64, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 59.250000000000014, 7.81850649193742, 24.334789783051825, 11.56016586920779, 2.0, 2.0000000000000515, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 3.0, 32.0, 54.0, 24.0, 8.0, 8.0, 22.0, 32.0, 209.0, 35.0, 8.0, 13.0, 33.0, 77.0, 85.0, 241.0, 9.0, 26.0]
    config_05052023_v6 = [70.0, 170.0, 0.0, 353.0780575329521, 125.08255586355432, 184.8344375295139, 150.19262843951793, 186.81232063446174, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 42.272041375581644, 45.68879164565739, 72.18387587325509, 8.0, 27.006281622278333, 16.244833417370145, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 24.79612428119684, 48.76386379332487, 8.000000000000052, 104.73165886004907, 15.799123331055451, 16.779328771191132, 3.000000000000501, 100.0, 242.0, 242.0, 2.0000000000000475, 4.800402845273522, 3.0000000000001097, 100.0, 8.0, 172.7285434564396, 46.82853656724763, 2.0000000000006546] 
    config_05052023_v8 = [70.0, 170.0, 0.0, 309.38296961545626, 94.95830972105306, 166.8082001546308, 333.46867682763207, 95.38184368122768, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 45.74968505556718, 46.10466599404622, 8.0, 60.68600201786133, 16.00125977773132, 2.0, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 12.287238981286016, 44.88748281429583, 8.0, 240.1547709755534, 2.0, 13.782279021864408, 3.0, 100.0, 242.0, 8.0, 2.0, 2.0, 75.94187095948752, 3.0000000000000013, 242.0, 188.4836348070854, 2.000000000000054, 70.0]

    Data_v0, nums_v0 = read_configs(["SC_config_04032023_spill_07032023"])
    Data_v6, nums_v6 = read_configs([os.path.join("SC_full_opt_1", "config_05052023_v6_full_spill")])
    Data_v8, nums_v8 = read_configs([os.path.join("SC_full_opt_1", "config_05052023_v8_full_spill")])

    number_of_files = 68*30
    mult_v0 = number_of_files/nums_v0[0]
    mult_v6 = number_of_files/nums_v6[0]
    mult_v8 = number_of_files/nums_v8[0]

    vis_all(Data_v0, ["config_03042023_v0"], [config_04032023_v0], y_label = "Muons/spill", show_table = True, mult = mult_v0, out_folder = "Opt_07052023_full_spill")
    vis_all(Data_v6, ["config_05052023_v6"], [config_05052023_v6], y_label = "Muons/spill", show_table = True, mult = mult_v6, out_folder = "Opt_07052023_full_spill")
    vis_all(Data_v8, ["config_05052023_v8"], [config_05052023_v8], y_label = "Muons/spill", show_table = True, mult = mult_v8, out_folder = "Opt_07052023_full_spill")