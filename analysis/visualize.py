import warnings
warnings.filterwarnings('ignore')

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import WAREHOUSE_DB

def get_connection():
    return psycopg2.connect(**WAREHOUSE_DB)

def plot_salary_stacked_bar(conn):
    query = """
            SELECT job_group,
                   AVG(
                           CASE
                               WHEN salary_unit = 'USD' THEN min_salary * 25000
                               ELSE min_salary
                               END
                   ) / 1000000 AS avg_min_tr,
                   AVG(
                           CASE
                               WHEN salary_unit = 'USD' THEN max_salary * 25000
                               ELSE max_salary
                               END
                   ) / 1000000 AS avg_max_tr

            FROM jobs_cleaned
            WHERE min_salary IS NOT NULL
              AND max_salary IS NOT NULL
            GROUP BY job_group
            ORDER BY avg_max_tr DESC;
            """

    df_grouped = pd.read_sql_query(query, conn)
    df_grouped['diff'] = df_grouped['avg_max_tr'] - df_grouped['avg_min_tr']

    plt.figure(figsize=(12, 7))

    plt.bar(df_grouped['job_group'], df_grouped['avg_min_tr'], color='#3498db', label='Lương Min TB')
    plt.bar(df_grouped['job_group'], df_grouped['diff'], bottom=df_grouped['avg_min_tr'],
            color='#e74c3c', label='Khoảng Max TB')

    plt.xticks(rotation=45, ha='right')

    plt.ylabel('Triệu VNĐ')
    plt.title('Mức lương Trung bình (Min - Max) theo Nhóm ngành', fontsize=15, fontweight='bold')

    for i, val in enumerate(df_grouped['avg_max_tr']):
        plt.text(i, val + 0.5, f'{val:.1f}', ha='center', fontsize=9)

    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_vietnam_heatmap(conn):
    query = "SELECT city, COUNT(*) AS total_jobs FROM jobs_cleaned GROUP BY city"
    df = pd.read_sql_query(query, conn)

    val_toan_quoc = df[df['city'] == 'Toàn quốc']['total_jobs'].sum()
    df_filtered = df[~df['city'].isin(['Toàn quốc', 'Nước ngoài'])].copy()

    df_filtered['total_jobs'] = df_filtered['total_jobs'] + val_toan_quoc

    df_filtered = df_filtered.sort_values('total_jobs', ascending=False)

    heatmap_data = df_filtered.set_index('city')[['total_jobs']]

    plt.figure(figsize=(8, 12))

    sns.heatmap(heatmap_data, annot=True, fmt="g", cmap="YlOrRd",
                cbar_kws={'label': 'Số lượng công việc'})

    plt.title("MẬT ĐỘ TUYỂN DỤNG THEO TỈNH THÀNH", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Tỉnh / Thành phố")
    plt.xlabel("Thống kê số lượng")

    plt.tight_layout()
    plt.show()


def plot_job_trend_bar(conn):
    query = "SELECT job_group, COUNT(*) AS total FROM jobs_cleaned GROUP BY job_group ORDER BY total DESC"
    df = pd.read_sql_query(query, conn)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="total", y="job_group", hue="job_group", palette="magma", legend=False)

    plt.title("Xu hướng công nghệ", fontsize=15, fontweight='bold')
    plt.xlabel("Số lượng Jobs")
    plt.ylabel("Nhóm công việc")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    conn = None
    try:
        conn = get_connection()
        plot_salary_stacked_bar(conn)
        plot_vietnam_heatmap(conn)
        plot_job_trend_bar(conn)
        print("Finished visualizing data.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")