
import branca
import folium
import pandas as pd
import streamlit as st
from folium import plugins
from streamlit_folium import folium_static


# 販売情報のCSVを取得し、ユーザが選択した条件に応じて抽出する
def extract_dataframe(store_df: pd.DataFrame, visible_flags: dict) -> pd.DataFrame:
    """ユーザが選択した条件に応じてDataFrameを抽出

    Args:
        store_df (pd.DataFrame): 抽出対象のDataFrame
        visible_flags (dict): 抽出条件が格納された辞書形式データ

    Returns:
        pd.DataFrame: 抽出されたDataFrame
    """

    # 条件にあわせて表示する店舗の情報を抽出
    visible_store_df = store_df.copy()
    if len(visible_flags) > 0:
        for flag in visible_flags:
            if flag == 'カスタムステンレスボトルセット販売中':
                visible_store_df = visible_store_df[visible_store_df['ステンレスボトルセット'] == '販売中'].reset_index(drop=True)
            elif flag == '店舗装飾実施中':
                visible_store_df = visible_store_df[visible_store_df['店舗装飾'] == '実施中'].reset_index(drop=True)

    return visible_store_df


# ポップアップに表示するHTMLテーブルを作成
def df2html(row: pd.core.series.Series) -> str:
    """DataFrameの1行ずつの情報をHTML形式のテーブルに変換

    Args:
        row (pd.core.series.Series): DataFrameの1行ずつの情報

    Returns:
        html: HTML形式でテーブルを表現した文字列
    """

    left_col_color = "#ffffff"
    right_col_color = "#ffffff"

    html = """<!DOCTYPE html>
        <html>
        <head>
        <h5 style="margin-bottom:10"; width="150px"><b>{}</b></h5>""".format(row['店舗名']) + """
        </head>
        <div style="height:120px; width:450px; overflow-x: scroll;">
        <table style="height: 100px; width: 470px;">
        <tbody>
        <tr>
        <td style="background-color: """+ left_col_color +""";"><span style="color: #000000;"><b>営業時間</b></span></td>
        <td style="width: 250px;background-color: """+ right_col_color +""";">{}</td>""".format(row['営業時間']  ) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_color +""";"><span style="color: #000000;"><b>電話番号</b></span></td>
        <td style="width: 250px;background-color: """+ right_col_color +""";">{}</td>""".format(row['電話番号']  ) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_color +""";"><span style="color: #000000;"><b>住所</b></span></td>
        <td style="width: 250px;background-color: """+ right_col_color +""";">{}</td>""".format(row['住所']  ) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_color +""";"><span style="color: #000000;"><b>店舗URL</b></span></td>
        <td style="width: 250px;background-color: """+ right_col_color +""";"><a href="{0}" target="_blank" rel="noopener noreferrer">{0}</a></td>""".format(row['店舗URL']) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_color +""";"><span style="color: #000000;"><b>Google Maps</b></span></td>
        <td style="width: 250px;background-color: """+ right_col_color +""";"><a href="https://www.google.com/maps?q={0},{1}&hl=ja" target="_blank" rel="noopener noreferrer">リンク</a></td>""".format(row['緯度'], row['経度']) + """
        </tr>
        </tbody>
        </table>
        </div>
        </html>
    """
    return html


# データを地図に渡す関数を作成する
def plot_tiles(df: pd.DataFrame, m: folium.plugins.marker_cluster.MarkerCluster) -> None:
    """DataFrameの情報をfoliumへ渡す

    Args:
        df (pd.DataFrame): 表示対象のGeoDataFrame
        m (folium.plugins.marker_cluster.MarkerCluster): FoliumのMarkerClusterオブジェト
    """
    # マーカーをプロット
    for i, row in df.iterrows():
        popup_html = df2html(row)
        iframe = branca.element.IFrame(html=popup_html, width=650, height=300)
        folium.Marker(
            location=[row['緯度'], row['経度']],
            popup=folium.Popup(folium.Html(popup_html, script=True), max_width=650),
            icon=folium.Icon(color="red", icon="cutlery"),
            clustered_marker=True
        ).add_to(m)


def main():
    # ページに関する設定
    st.set_page_config(
        page_title='【非公式】鬼頭明里のスガキヤだがや！ コラボ店舗マップ',
        page_icon='🗾',
        layout='wide'
    )

    # ページタイトル
    st.title('【非公式】鬼頭明里のスガキヤだがや！ コラボ店舗マップ')

    # 地図の初期設定
    folium_map = folium.Map(location=[35.311207, 137.050236], zoom_start=9)

    # マーカの表示設定にクラスタを適用
    marker_cluster = plugins.MarkerCluster().add_to(folium_map)

    # 表示する条件を選択
    st.sidebar.title('表示する条件を選択')

    visible_flags = {
        'カスタムステンレスボトルセット販売中': False,
        '店舗装飾実施中': False
    }
    selected_flags = [key for key in visible_flags.keys() if st.sidebar.checkbox(key)]

    # 店舗情報のデータを読み込む
    store_info_df = pd.read_csv('https://docs.google.com/spreadsheets/d/1GNjT4g3g1_J1u8TYYeKzl6F6bP7csZpByfY5QOuBUHM/export?format=csv')

    # ユーザの選択条件にあわせて表示する情報を抽出
    visible_store_df = extract_dataframe(store_info_df, selected_flags)

    # マーカークラスタのレイヤーを生成し、地図に追加
    plot_tiles(visible_store_df, marker_cluster)

    # 地図をフルスクリーンにするボタンの追加
    plugins.Fullscreen(
        position="topright",
        title="拡大する",
        title_cancel="元に戻す",
        force_separate_button=True
    ).add_to(folium_map)

    # 地図の表示
    folium_static(folium_map, width=1400, height=700)


if __name__ == "__main__":
    main()
