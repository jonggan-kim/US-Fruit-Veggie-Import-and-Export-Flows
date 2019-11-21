# Dependencies
import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
from flask import Flask, render_template, jsonify
from jinja2 import Template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Veggie_Fruit_DB.sqlite"
db = SQLAlchemy(app)

Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

FED = Base.classes.fruitexportdest
FEV = Base.classes.fruitexportval
FIS = Base.classes.fruitimportsource
FIV = Base.classes.fruitimportval
VED = Base.classes.veggieexportdest
VEV = Base.classes.veggieexportval
VIS = Base.classes.veggieimportsource
VIV = Base.classes.veggieimportval


# Create our session (link) from Python to the DB

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")
#route1
@app.route("/summary_edata")
def summary_edata_data():
    # 1 Generate Summary Export(for summary_edata route)
    fe_summary = db.session.query(FED.country,FED.yr17,FED.yr18).group_by(FED.country).order_by(FED.yr18.desc()).all()
    fe_summary_df = pd.DataFrame(fe_summary, columns=['country', 'yr17', 'yr18'])
    fe_summary_df['yr17'] = fe_summary_df['yr17'].str.replace(',', '')
    fe_summary_df['yr18'] = fe_summary_df['yr18'].str.replace(',', '')
    fe_summary_df=fe_summary_df.dropna(how="any")
    fe_summary_df["yr17"] = pd.to_numeric(fe_summary_df["yr17"])
    fe_summary_df["yr18"] = pd.to_numeric(fe_summary_df["yr18"])

    ve_summary = db.session.query(VED.country,VED.yr17,VED.yr18).group_by(VED.country).order_by(VED.yr18.desc()).all()
    ve_summary_df = pd.DataFrame(ve_summary, columns=['country', 'yr17', 'yr18'])
    ve_summary_df['yr17'] = ve_summary_df['yr17'].str.replace(',', '')
    ve_summary_df['yr18'] = ve_summary_df['yr18'].str.replace(',', '')
    ve_summary_df=ve_summary_df.dropna(how="any")
    ve_summary_df["yr17"] = pd.to_numeric(ve_summary_df["yr17"])
    ve_summary_df["yr18"] = pd.to_numeric(ve_summary_df["yr18"])
    esummary_frames = [ve_summary_df, fe_summary_df]
    summary_export = pd.concat(esummary_frames,ignore_index=False)
    summary_export = summary_export.sort_values(['yr17', 'yr18'], ascending=False)

    export_yr17sum=summary_export['yr17'].sum()
    export_yr18sum=summary_export['yr18'].sum()

    for i in summary_export:
        e_ms17=summary_export['yr17']/export_yr17sum*100

    for i in summary_export:
        e_ms18=summary_export['yr18']/export_yr18sum*100

    summary_export["MarketShare(2017)"]=e_ms17
    summary_export["MarketShare(2018)"]=e_ms18
    e_change = e_ms18-e_ms17
    summary_export["ChangeInMarketShare"]=e_change
    renamed_summary_export = summary_export.rename(columns={"country":"Country", "MS 2017":"MarketShare(2017)","MS 2018":"MarketShare(2018)", "Change in MS":"ChangeInMarketShare","yr17":"Value2017", "yr18":"Value2018"})
    summary_export = renamed_summary_export[["Country","MarketShare(2017)","MarketShare(2018)","ChangeInMarketShare", "Value2017", "Value2018"]]
    summary_export=summary_export.sort_values(['MarketShare(2018)'], ascending=False).head()
    Summary_Export = summary_export[["Country", "MarketShare(2017)", "MarketShare(2018)", "ChangeInMarketShare", "Value2017", "Value2018"]]
    Summary_Export["MarketShare(2017)"]= Summary_Export["MarketShare(2017)"].astype(int)
    Summary_Export["MarketShare(2018)"]= Summary_Export["MarketShare(2018)"].astype(int)
    Summary_Export["ChangeInMarketShare"]= Summary_Export["ChangeInMarketShare"].astype(int)

    summary_export_list = []

    Summary_Export = Summary_Export.reset_index(drop=True)
    ms17_list = Summary_Export["MarketShare(2017)"].tolist()
    ms18_list = Summary_Export["MarketShare(2018)"].tolist()
    mschange_list = Summary_Export["ChangeInMarketShare"].tolist()
    value_yr17 = Summary_Export["Value2017"].tolist()
    value_yr18 = Summary_Export["Value2018"].tolist()

    country_list = Summary_Export["Country"].tolist()
    for i in range(len(country_list)):
        summary_report_dict = {}
        summary_report_dict["Country"] = country_list[i]
        summary_report_dict["MS17"] = ms17_list[i]
        summary_report_dict["MS18"] = ms18_list[i]
        summary_report_dict["MSChange"] = mschange_list[i]
        summary_report_dict["Value2017"] = value_yr17[i]
        summary_report_dict["Value2018"] = value_yr18[i]

        summary_export_list.append(summary_report_dict)

    print(summary_export_list)
    return jsonify(summary_export_list)

# route2
@app.route("/top10_edata")
def top10_edata_data():   
    # route 2 Generate Top10 Export for @app.route("/top10_edata")

    ExportDataVeggie = db.session.query(VED.product,VED.yr18).\
    group_by(VED.product).order_by(VED.yr18.desc()).all()
    # # Save the query results as a Pandas DataFrame and set the index to the date column
    ve_data_df = pd.DataFrame(ExportDataVeggie, columns=['product', 'yr18'])
    # Sort the dataframe by date
    # all_import_data_df = all_import_data_df.sort_values("country")
    # precip_data_df.set_index(precip_data_df['date'], inplace=False)
    
    ve_data_df['yr18'] = ve_data_df['yr18'].str.replace(',', '')
    ve_data_df = ve_data_df.dropna(how="any")
    ve_data_df["yr18"] = pd.to_numeric(ve_data_df["yr18"])
    ve_data_df.sort_values(['yr18'], ascending=False).head()

    ExportDataFruit = db.session.query(FED.product,FED.yr18).\
    group_by(FED.product).order_by(FED.yr18.desc()).all()
    fe_data_df = pd.DataFrame(ExportDataFruit, columns=['product','yr18'])
    fe_data_df['yr18'] = fe_data_df['yr18'].str.replace(',', '')
    fe_data_df["yr18"] = pd.to_numeric(fe_data_df["yr18"])
    fe_data_df = fe_data_df.dropna(how="any")
    fe_data_df.sort_values(['yr18'], ascending=False)
    export_frames = [ve_data_df, fe_data_df]
    all_export = pd.concat(export_frames)
    all_export.sort_values(['yr18'], ascending=False).head()
    all_export_yr18sum=all_export['yr18'].sum()
    for i in all_export:
        eproduct_share=all_export["yr18"]/all_export_yr18sum*100
    all_export["Share"]=eproduct_share
    organized_all_export = all_export[["product","yr18","Share"]]
    org_top10_export = organized_all_export.sort_values(['Share'], ascending=False).head(10)
    top10_export = org_top10_export.rename(columns={"product":"Product","yr18":"Value2018", "Share":"Share"})
    top10_export.reset_index(inplace=True)
    Top10_Export= top10_export[["Product", "Value2018", "Share"]] 

    Top10_Export["Share"]= Top10_Export["Share"].astype(int)

    top10_export_list =[]
    # top10country_list = Top10_Export["Country"].tolist()
    top10product_list = Top10_Export["Product"].tolist()
    top10value_yr18 = Top10_Export["Value2018"].tolist()
    top10ms18_list = Top10_Export["Share"].tolist()

    for i in range(len(top10product_list)):
        top10_export_dict = {}
        top10_export_dict["Product"] = top10product_list[i]
        top10_export_dict["Value2018"] = top10value_yr18[i]
        top10_export_dict["Share"] = top10ms18_list[i]

        top10_export_list.append(top10_export_dict)

    print(top10_export_list)
    return jsonify(top10_export_list)
    

#  route3
@app.route("/bar_edata")
def bar_edata_data():  
    # 3 Generate Export Bar_Pie Chart data for # @app.route("/bar_edata")

    ExportDataVeggie = db.session.query(VED.product,VED.yr18).\
    group_by(VED.product).order_by(VED.yr18.desc()).all()
    # # Save the query results as a Pandas DataFrame and set the index to the date column
    ve_data_df = pd.DataFrame(ExportDataVeggie, columns=['product', 'yr18'])
    # Sort the dataframe by date
    # all_import_data_df = all_import_data_df.sort_values("country")
    # precip_data_df.set_index(precip_data_df['date'], inplace=False)
    
    ve_data_df['yr18'] = ve_data_df['yr18'].str.replace(',', '')
    ve_data_df = ve_data_df.dropna(how="any")
    ve_data_df["yr18"] = pd.to_numeric(ve_data_df["yr18"])
    ve_data_df.sort_values(['yr18'], ascending=False).head()

    ExportDataFruit = db.session.query(FED.product,FED.yr18).\
    group_by(FED.product).order_by(FED.yr18.desc()).all()
    fe_data_df = pd.DataFrame(ExportDataFruit, columns=['product','yr18'])
    fe_data_df['yr18'] = fe_data_df['yr18'].str.replace(',', '')
    fe_data_df["yr18"] = pd.to_numeric(fe_data_df["yr18"])
    fe_data_df = fe_data_df.dropna(how="any")
    fe_data_df.sort_values(['yr18'], ascending=False)
    export_frames = [ve_data_df, fe_data_df]
    all_export = pd.concat(export_frames)
    all_export.sort_values(['yr18'], ascending=False).head()
   
    organized_bar_export = all_export[["product","yr18"]]
    b_top10_export = organized_bar_export.sort_values(['yr18'], ascending=False).head(10)
    b_top10_export = b_top10_export.rename(columns={"product":"Product","yr18":"Value2018"})
    b_top10_export.reset_index(inplace=True)
    bTop10_Export= b_top10_export[["Product", "Value2018"]] 

    # Top10_Export["Share"]= Top10_Export["Share"].astype(int)

    top10_export_blist =[]
    # top10country_list = Top10_Export["Country"].tolist()
    top10product_blist = bTop10_Export["Product"].tolist()
    top10value_byr18 = bTop10_Export["Value2018"].tolist()

    for i in range(len(top10product_blist)):
        top10_export_bdict = {}
        top10_export_bdict["Product"] = top10product_blist[i]
        top10_export_bdict["Value2018"] = top10value_byr18[i]
        

        top10_export_blist.append(top10_export_bdict)


    data = {
           "bproduct": top10product_blist,
           "bvalue": top10value_byr18,
       }
    print(data)
    return jsonify(data)


#  route4
@app.route("/summary_idata")
def summary_idata_data():
    # 4 Generate Summary Import(for summary_idata route)
    fi_summary = db.session.query(FIS.country,FIS.yr17,FIS.yr18).group_by(FIS.country).order_by(FIS.yr18.desc()).all()
    fi_summary_df = pd.DataFrame(fi_summary, columns=['country', 'yr17', 'yr18'])
    fi_summary_df['yr17'] = fi_summary_df['yr17'].str.replace(',', '')
    fi_summary_df['yr18'] = fi_summary_df['yr18'].str.replace(',', '')
    fi_summary_df=fi_summary_df.dropna(how="any")
    fi_summary_df["yr17"] = pd.to_numeric(fi_summary_df["yr17"])
    fi_summary_df["yr18"] = pd.to_numeric(fi_summary_df["yr18"])

    vi_summary = db.session.query(VIS.country,VIS.yr17,VIS.yr18).group_by(VIS.country).order_by(VIS.yr18.desc()).all()
    vi_summary_df = pd.DataFrame(vi_summary, columns=['country', 'yr17', 'yr18'])
    vi_summary_df['yr17'] = vi_summary_df['yr17'].str.replace(',', '')
    vi_summary_df['yr18'] = vi_summary_df['yr18'].str.replace(',', '')
    vi_summary_df=vi_summary_df.dropna(how="any")
    vi_summary_df["yr17"] = pd.to_numeric(vi_summary_df["yr17"])
    vi_summary_df["yr18"] = pd.to_numeric(vi_summary_df["yr18"])
    isummary_frames = [vi_summary_df, fi_summary_df]
    summary_import = pd.concat(isummary_frames,ignore_index=False)
    summary_import = summary_import.sort_values(['yr17', 'yr18'], ascending=False)

    import_yr17sum=summary_import['yr17'].sum()
    import_yr18sum=summary_import['yr18'].sum()

    for i in summary_import:
        i_ms17=summary_import['yr17']/import_yr17sum*100

    for i in summary_import:
        i_ms18=summary_import['yr18']/import_yr18sum*100

    summary_import["MarketShare(2017)"]=i_ms17
    summary_import["MarketShare(2018)"]=i_ms18
    i_change = i_ms18-i_ms17
    summary_import["ChangeInMarketShare"]=i_change
    renamed_summary_import = summary_import.rename(columns={"country":"Country", "MS 2017":"MarketShare(2017)","MS 2018":"MarketShare(2018)", "Change in MS":"ChangeInMarketShare","yr17":"Value2017", "yr18":"Value2018"})
    summary_import = renamed_summary_import[["Country","MarketShare(2017)","MarketShare(2018)","ChangeInMarketShare", "Value2017", "Value2018"]]
    summary_import=summary_import.sort_values(['MarketShare(2018)'], ascending=False).head()
    Summary_Import = summary_import[["Country", "MarketShare(2017)", "MarketShare(2018)", "ChangeInMarketShare", "Value2017", "Value2018"]]
    Summary_Import["MarketShare(2017)"]= Summary_Import["MarketShare(2017)"].astype(int)
    Summary_Import["MarketShare(2018)"]= Summary_Import["MarketShare(2018)"].astype(int)
    Summary_Import["ChangeInMarketShare"]= Summary_Import["ChangeInMarketShare"].astype(int)

    summary_import_list = []

    Summary_Import = Summary_Import.reset_index(drop=True)
    ms17_ilist = Summary_Import["MarketShare(2017)"].tolist()
    ms18_ilist = Summary_Import["MarketShare(2018)"].tolist()
    mschange_ilist = Summary_Import["ChangeInMarketShare"].tolist()
    ivalue_yr17 = Summary_Import["Value2017"].tolist()
    ivalue_yr18 = Summary_Import["Value2018"].tolist()

    country_ilist = Summary_Import["Country"].tolist()
    for i in range(len(country_ilist)):
        summary_report_idict = {}
        summary_report_idict["Country"] = country_ilist[i]
        summary_report_idict["MS17"] = ms17_ilist[i]
        summary_report_idict["MS18"] = ms18_ilist[i]
        summary_report_idict["MSChange"] = mschange_ilist[i]
        summary_report_idict["Value2017"] = ivalue_yr17[i]
        summary_report_idict["Value2018"] = ivalue_yr18[i]

        summary_import_list.append(summary_report_idict)

    print(summary_import_list)
    return jsonify(summary_import_list)


#  route5
@app.route("/top10_idata")
def top10_idata_data():   
    # route 5 Generate Top10 Import for @app.route("/top10_idata")

    ImportDataVeggie = db.session.query(VIS.product,VIS.yr18).\
    group_by(VIS.product).order_by(VIS.yr18.desc()).all()
    # # Save the query results as a Pandas DataFrame and set the index to the date column
    vi_data_df = pd.DataFrame(ImportDataVeggie, columns=['product', 'yr18'])
    # Sort the dataframe by date
    # all_import_data_df = all_import_data_df.sort_values("country")
    # precip_data_df.set_index(precip_data_df['date'], inplace=False)
    
    vi_data_df['yr18'] = vi_data_df['yr18'].str.replace(',', '')
    vi_data_df = vi_data_df.dropna(how="any")
    vi_data_df["yr18"] = pd.to_numeric(vi_data_df["yr18"])
    vi_data_df.sort_values(['yr18'], ascending=False).head()

    ImportDataFruit = db.session.query(FIS.product,FIS.yr18).\
    group_by(FIS.product).order_by(FIS.yr18.desc()).all()
    fi_data_df = pd.DataFrame(ImportDataFruit, columns=['product','yr18'])
    fi_data_df['yr18'] = fi_data_df['yr18'].str.replace(',', '')
    fi_data_df["yr18"] = pd.to_numeric(fi_data_df["yr18"])
    fi_data_df = fi_data_df.dropna(how="any")
    fi_data_df.sort_values(['yr18'], ascending=False)
    import_frames = [vi_data_df, fi_data_df]
    all_import = pd.concat(import_frames)
    all_import.sort_values(['yr18'], ascending=False).head()
    all_import_yr18sum=all_import['yr18'].sum()
    for i in all_import:
        iproduct_share=all_import["yr18"]/all_import_yr18sum*100
    all_import["Share"]=iproduct_share
    organized_all_import = all_import[["product","yr18","Share"]]
    org_top10_import = organized_all_import.sort_values(['Share'], ascending=False).head(10)
    top10_import = org_top10_import.rename(columns={"product":"Product","yr18":"Value2018", "Share":"Share"})
    top10_import.reset_index(inplace=True)
    Top10_Import= top10_import[["Product", "Value2018", "Share"]] 

    Top10_Import["Share"]= Top10_Import["Share"].astype(int)

    top10_import_list =[]
    # top10country_list = Top10_Export["Country"].tolist()
    top10product_ilist = Top10_Import["Product"].tolist()
    top10value_iyr18 = Top10_Import["Value2018"].tolist()
    top10ms18_ilist = Top10_Import["Share"].tolist()

    for i in range(len(top10product_ilist)):
        top10_import_dict = {}
        top10_import_dict["Product"] = top10product_ilist[i]
        top10_import_dict["Value2018"] = top10value_iyr18[i]
        top10_import_dict["Share"] = top10ms18_ilist[i]

        top10_import_list.append(top10_import_dict)

    print(top10_import_list)
    return jsonify(top10_import_list)

# route 6
@app.route("/bar_idata")
def bar_idata_data():  
    # 6 Generate Import Bar_Pie Chart data for # @app.route("/bar_idata")

    ImportDataVeggie = db.session.query(VIS.product,VIS.yr18).\
    group_by(VIS.product).order_by(VIS.yr18.desc()).all()
    # # Save the query results as a Pandas DataFrame and set the index to the date column
    vi_data_df = pd.DataFrame(ImportDataVeggie, columns=['product', 'yr18'])
    # Sort the dataframe by date
    # all_import_data_df = all_import_data_df.sort_values("country")
    # precip_data_df.set_index(precip_data_df['date'], inplace=False)
    
    vi_data_df['yr18'] = vi_data_df['yr18'].str.replace(',', '')
    vi_data_df = vi_data_df.dropna(how="any")
    vi_data_df["yr18"] = pd.to_numeric(vi_data_df["yr18"])
    vi_data_df.sort_values(['yr18'], ascending=False).head()

    ImportDataFruit = db.session.query(FIS.product,FIS.yr18).\
    group_by(FIS.product).order_by(FIS.yr18.desc()).all()
    fi_data_df = pd.DataFrame(ImportDataFruit, columns=['product','yr18'])
    fi_data_df['yr18'] = fi_data_df['yr18'].str.replace(',', '')
    fi_data_df["yr18"] = pd.to_numeric(fi_data_df["yr18"])
    fi_data_df = fi_data_df.dropna(how="any")
    fi_data_df.sort_values(['yr18'], ascending=False)
    import_frames = [vi_data_df, fi_data_df]
    all_import = pd.concat(import_frames)
    all_import.sort_values(['yr18'], ascending=False).head()
   
    organized_bar_import = all_import[["product","yr18"]]
    b_top10_import = organized_bar_import.sort_values(['yr18'], ascending=False).head(10)
    b_top10_import = b_top10_import.rename(columns={"product":"Product","yr18":"Value2018"})
    b_top10_import.reset_index(inplace=True)
    bTop10_Import= b_top10_import[["Product", "Value2018"]] 

    # Top10_Export["Share"]= Top10_Export["Share"].astype(int)

    top10_import_blist =[]
    # top10country_list = Top10_Export["Country"].tolist()
    top10product_bilist = bTop10_Import["Product"].tolist()
    top10value_biyr18 = bTop10_Import["Value2018"].tolist()

    for i in range(len(top10product_bilist)):
        top10_import_bdict = {}
        top10_import_bdict["Product"] = top10product_bilist[i]
        top10_import_bdict["Value2018"] = top10value_biyr18[i]
        

        top10_import_blist.append(top10_import_bdict)


    data1 = {
           "bproduct": top10product_bilist,
           "bvalue": top10value_biyr18,
       }

    print(data1)
    return jsonify(data1)

@app.route("/veggienames")
def vegnames():
    """Return a list of sample names."""
    
    market_year = db.session.query(VED.product , VED.country , VED.share).all()
    mkt_yr_df = pd.DataFrame(market_year, columns = ["Product","Country","Share"])
    product_group = mkt_yr_df.groupby(["Product"]).count()
    product_list = product_group.index.values.tolist()
    product_list = product_list[1:]

    return jsonify(product_list)


@app.route("/veggieexp/<veggie>")
def veg_country(veggie):

    sel = [
        VED.product,
        VED.country,
        VED.share,
        VED.lat,
        VED.lon,
    ]
    veggie = VED.product
    results = db.session.query(*sel).filter(VED.product == veggie).all()
    veggie_list = []
    for result in results:
        veggie_country = {}
        veggie_country["Country"] = result[1]
        veggie_country["Type"] = "veggie"
        veggie_country["Share"] = float(result[2].replace('%',''))
        veggie_country["lat"] = result[3]
        veggie_country["lon"] = result[4]
        veggie_list.append(veggie_country)

    return jsonify(veggie_list)

@app.route("/fruitnames")
def fruitnames():
    """Return a list of sample names."""
    
    fruit_specific = db.session.query(FED.product , FED.country , FED.share).all()
    fruit_spec_df = pd.DataFrame(fruit_specific, columns = ["Product","Country","Share"])
    fruit_group = fruit_spec_df.groupby(["Product"]).count()
    fruit_overall = fruit_group.index.values.tolist()

    return jsonify(fruit_overall)


@app.route("/fruitexp/<fruit>")
def fruit_country(fruit):

    sel = [
        FED.product,
        FED.country,
        FED.share,
        FED.lat,
        FED.lon,
    ]
    fruit=FED.product
    results = db.session.query(*sel).filter(FED.product == fruit).all()
    fruit_list = []
    for result in results:
        fruit_country = {}
        fruit_country["Country"] = result[1]
        fruit_country["Type"] = "Fruit"
        fruit_country["Share"] = float(result[2].replace('%',''))
        fruit_country["lat"] = result[3]
        fruit_country["lon"] = result[4]
        fruit_list.append(fruit_country)

    return jsonify(fruit_list)



if __name__ == "__main__":
    app.run()



