"""
========================================================================================
QUANTITY SURVEYING & COST ESTIMATION (QS&CE) COMPUTATIONAL ANALYSIS
Project: 5-Marla (22.5' x 50') Single-Storey Residential House
Location: Paragon City Housing Scheme, Burki Road, Lahore Cantt, Pakistan
Course: CE-372 Quantity Surveying & Cost Estimation | Semester 6
Author: Muhammad Umer Basit (Civil Engineering Student)
NUST Institute of Civil Engineering (NICE), NUST, Islamabad
========================================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Reconfigure stdout for utf-8 safety on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Set aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI, Helvetica, Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

def analyze_boq_and_generate_figures(repo_dir: str):
    boq_excel = os.path.join(repo_dir, 'boq-and-cost-estimates', 'Bill-of-Quantities-Complete.xlsx')
    media_dir = os.path.join(repo_dir, 'media')
    os.makedirs(media_dir, exist_ok=True)

    print("================================================================================")
    print(" 🏗️ QUANTITY SURVEYING & BOQ COST BREAKDOWN (5-MARLA HOUSE, LAHORE)")
    print("================================================================================")

    # 1. Trade Cost Categorization
    trade_data = [
        {"Trade": "Masonry & Mortar", "Cost_PKR": 629446.41, "Color": "#c0392b", "Desc": "Foundation & superstructure brickwork (32,000 bricks)"},
        {"Trade": "Joinery & Glazing", "Cost_PKR": 564450.51, "Color": "#d35400", "Desc": "Teak doors (119 sft), bronze alum. windows, steel gate"},
        {"Trade": "Steel Reinforcement (BBS)", "Cost_PKR": 300907.67, "Color": "#2980b9", "Desc": "Grade 40 deformed bars (4,165.61 lb fabrication/fixing)"},
        {"Trade": "Finishes, Flooring & Plaster", "Cost_PKR": 247006.18, "Color": "#27ae60", "Desc": "Plaster (1:4), mosaic marble, tiles, weather shield"},
        {"Trade": "Plain & Reinforced Concrete", "Cost_PKR": 210324.54, "Color": "#7f8c8d", "Desc": "PCC 1:4:8 & RCC 1:2:4 footings, plinth & lintels (915.3 cft)"},
        {"Trade": "Insulation & Moisture Barrier", "Cost_PKR": 177891.85, "Color": "#8e44ad", "Desc": "DPC 1.5\", 2 coats hot bitumen, 2 layers XPS board"},
        {"Trade": "Earthwork & Sub-base Prep", "Cost_PKR": 26001.46, "Color": "#f39c12", "Desc": "Excavation (935.5 cft), backfill, 6\" sand & compacted earth"}
    ]

    df_trades = pd.DataFrame(trade_data)
    total_cost = df_trades["Cost_PKR"].sum()
    df_trades["Percentage"] = (df_trades["Cost_PKR"] / total_cost) * 100.0

    print("\nSummary of Construction Cost by Major Trades:")
    print("-" * 85)
    for _, row in df_trades.iterrows():
        print(f" {row['Trade']:<32} | PKR {row['Cost_PKR']:>12,.2f} | {row['Percentage']:>6.2f}% | {row['Desc']}")
    print("-" * 85)
    print(f" {'TOTAL BASE ESTIMATE (BOQ)':<32} | PKR {total_cost:>12,.2f} | 100.00%")
    print("-" * 85)

    # 2. Plot 1: Trade Cost Breakdown Donut Chart
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    wedges, texts, autotexts = ax.pie(
        df_trades["Cost_PKR"],
        labels=df_trades["Trade"],
        autopct='%1.1f%%',
        startangle=140,
        colors=df_trades["Color"],
        pctdistance=0.8,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.5),
        textprops=dict(fontsize=10, fontweight='semibold')
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9.5)
        autotext.set_weight('bold')

    # Center circle label
    ax.text(0, 0, f"TOTAL BOQ\nPKR 2.18M\n($22.5' x 50'$)",
            horizontalalignment='center', verticalalignment='center',
            fontsize=12, fontweight='bold', color='#333333')

    plt.title("5-Marla Residential House: Construction Cost Breakdown by Trade\nCE-372 Quantity Surveying & Cost Estimation | NUST NICE",
              fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    chart1_path = os.path.join(media_dir, "boq-cost-breakdown-trade.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"\n[Saved] BOQ Trade Breakdown Chart: {chart1_path}")

    # 3. Bar Bending Schedule (BBS) Steel Takeoff Accounting
    # Muhammad Umer Basit's specialized deliverable
    steel_schedule = [
        {"Element": "RCC Roof Slab (S1)", "Total_Length_ft": 5889.25, "Bar_Size": "#4 (0.5\")", "Weight_lb": 3934.02, "Weight_kg": 1784.44},
        {"Element": "RCC Lintel Beams", "Total_Length_ft": 287.50, "Bar_Size": "#4 & #3", "Weight_lb": 161.39, "Weight_kg": 73.21},
        {"Element": "RCC Beams (B1 & B2)", "Total_Length_ft": 77.08, "Bar_Size": "#4, #6 & #3", "Weight_lb": 140.23, "Weight_kg": 63.61},
        {"Element": "Columns & Stiffeners", "Total_Length_ft": 2907.92, "Bar_Size": "#3, #4 & #6", "Weight_lb": 1856.84, "Weight_kg": 842.25}
    ]
    df_steel = pd.DataFrame(steel_schedule)

    # 4. Plot 2: Steel Reinforcement Takeoff Distribution Bar Chart
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    y_pos = np.arange(len(df_steel))
    bars = ax.barh(y_pos, df_steel["Weight_lb"], color="#1f77b4", edgecolor="#333333", height=0.55, alpha=0.9)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_steel["Element"], fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel("Steel Weight (lbs)", fontsize=11, fontweight='bold', labelpad=10)
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    for bar, (_, row) in zip(bars, df_steel.iterrows()):
        w = bar.get_width()
        ax.text(w + 50, bar.get_y() + bar.get_height() / 2,
                f" {row['Weight_lb']:,.1f} lb ({row['Weight_kg']:,.1f} kg) [{row['Bar_Size']}]",
                va='center', ha='left', fontsize=9.5, fontweight='semibold', color='#222222')

    ax.set_xlim(0, max(df_steel["Weight_lb"]) * 1.35)
    plt.title("Structural Steel Takeoff & Bar Bending Schedule (BBS) by Member\nMuhammad Umer Basit (Lead Steel Estimator) | Grade-40 Deformed Bars",
              fontsize=11.5, fontweight='bold', pad=15)
    plt.tight_layout()
    chart2_path = os.path.join(media_dir, "steel-reinforcement-distribution-bbs.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"[Saved] Steel BBS Reinforcement Chart: {chart2_path}")

    print("\n================================================================================")
    print(" ✅ QUANTITY SURVEYING & COST AUDIT COMPLETE")
    print("================================================================================")

if __name__ == '__main__':
    repo_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    analyze_boq_and_generate_figures(repo_directory)
