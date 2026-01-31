import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from config import WAREHOUSE_DB

def get_engine():
    conn_str = f"postgresql://{WAREHOUSE_DB['user']}:{WAREHOUSE_DB['password']}@{WAREHOUSE_DB['host']}:{WAREHOUSE_DB['port']}/{WAREHOUSE_DB['database']}"
    return create_engine(conn_str)

def plot_salary_stacked_bar(engine):
    query = """
            SELECT 
                job_group,
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

    df_grouped = pd.read_sql(query, engine)
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


def plot_vietnam_heatmap(engine):
    query = "SELECT city, COUNT(*) AS total_jobs FROM jobs_cleaned GROUP BY city"
    df = pd.read_sql(query, engine)

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


def plot_job_trend_bar(engine):
    query = "SELECT job_group, COUNT(*) AS total FROM jobs_cleaned GROUP BY job_group ORDER BY total DESC"
    df = pd.read_sql(query, engine)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="total", y="job_group", hue="job_group", palette="magma", legend=False)

    plt.title("Xu hướng công nghệ", fontsize=15, fontweight='bold')
    plt.xlabel("Số lượng Jobs")
    plt.ylabel("Nhóm công việc")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    try:
        engine = get_engine()
        plot_salary_stacked_bar(engine)
        plot_vietnam_heatmap(engine)
        plot_job_trend_bar(engine)
        print("Finished visualizing data.")
    except Exception as e:
        print(f"Error: {e}")