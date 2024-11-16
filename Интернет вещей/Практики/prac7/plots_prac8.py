import matplotlib.pyplot as plt
import pandas as pd


def draw_bar_plot(data: pd.DataFrame):
    df = data['motion']
    df_max = df.max()
    df_min = df.min()
    first = int((df_max - df_min) / 3 + df_min)
    second = int((df_max - df_min) / 3 + first)
    first_df = df.loc[df.between(df_min, first)]
    second_df = df.loc[df.between(first, second)]
    third_df = df.loc[df.between(second, df_max)]
    df_len = [len(first_df), len(second_df), len(third_df)]
    plt.bar([f'[{df_min};{first}]', f'[{first};{second}]', f'[{second};{df_max}]'], df_len)
    plt.xlabel('Интервалы показаний датчика движения')
    plt.ylabel('Частоты показаний')
    plt.show()


def draw_plot(data: pd.DataFrame):
    df = data['temperature']
    plt.plot(df)
    plt.ylabel('Показания температуры')
    plt.show()


def draw_pie_plot(data: pd.DataFrame):
    df = data['power']
    df_max = df.max()
    df_min = df.min()
    first = round((df_max - df_min) / 3 + df_min, 2)
    second = round((df_max - df_min) / 3 + first, 2)
    first_df = (df.loc[df.between(df_min, first)])
    second_df = df.loc[df.between(first, second)]
    third_df = df.loc[df.between(second, df_max)]
    df_len = [len(first_df), len(second_df), len(third_df)]
    plt.pie(df_len, labels=[f'[{df_min};{first}]', f'[{first};{second}]', f'[{second};{df_max}]'])
    plt.title('Показания датчика напряжения, В')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('data.csv')
    draw_bar_plot(df)
    draw_plot(df)
    draw_pie_plot(df)