# # --- Imports & Config ---
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# sns.set_context("talk")
# sns.set_style("whitegrid")
# plt.rcParams.update({
#     "figure.figsize": (9, 6),
#     "axes.titlesize": 16,
#     "axes.labelsize": 13,
#     "xtick.labelsize": 11,
#     "ytick.labelsize": 11
# })

# # --- Load data ---
# CSV_PATH = "assignment_3_dataset.csv"
# df = pd.read_csv(CSV_PATH)

# # --- Required columns & validation ---
# required = {
#     "lang", "z0t", "z1000t", "z1000mem",
#     "z1000rel", "m1000rel", "whours", "stmtL"
# }
# missing = required - set(df.columns)
# if missing:
#     raise ValueError(f"Missing required columns: {sorted(missing)}")

# # Optional: ensure 'lang' is categorical for consistent ordering
# df["lang"] = df["lang"].astype("category")

# # --- Derivations (safe) ---
# # Avoid divide-by-zero/infinite ratios
# df["scaling_ratio"] = np.where(df["z0t"] > 0, df["z1000t"] / df["z0t"], np.nan)

# # Long form for reliability comparison
# rel_long = df.melt(
#     id_vars="lang",
#     value_vars=["z1000rel", "m1000rel"],
#     var_name="test",
#     value_name="reliability"
# )

# # --- Small plotting helpers ---
# def boxplot(df_, x, y, title, xlabel=None, ylabel=None, order=None):
#     plt.figure()
#     sns.boxplot(data=df_, x=x, y=y, order=order)
#     plt.title(title)
#     plt.xlabel(xlabel or x)
#     plt.ylabel(ylabel or y)
#     plt.tight_layout()
#     plt.show()

# def barplot(df_, x, y, title, xlabel=None, ylabel=None, order=None, estimator=np.mean):
#     plt.figure()
#     sns.barplot(data=df_, x=x, y=y, order=order, estimator=estimator, errorbar="se")
#     plt.title(title)
#     plt.xlabel(xlabel or x)
#     plt.ylabel(ylabel or y)
#     plt.tight_layout()
#     plt.show()

# def scatter(df_, x, y, title, hue=None, xlabel=None, ylabel=None):
#     plt.figure()
#     sns.scatterplot(data=df_, x=x, y=y, hue=hue, alpha=0.85)
#     plt.title(title)
#     plt.xlabel(xlabel or x)
#     plt.ylabel(ylabel or y)
#     if hue:
#         plt.legend(title=hue, bbox_to_anchor=(1.02, 1), loc="upper left")
#     plt.tight_layout()
#     plt.show()

# def hist(df_, x, title, bins=20, xlabel=None, ylabel="Frequency"):
#     plt.figure()
#     sns.histplot(data=df_, x=x, bins=bins, kde=True)
#     plt.title(title)
#     plt.xlabel(xlabel or x)
#     plt.ylabel(ylabel)
#     plt.tight_layout()
#     plt.show()

# def corr_heatmap(df_num, title="Correlation Heatmap"):
#     plt.figure(figsize=(10, 7))
#     corr = df_num.corr(numeric_only=True)
#     sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=False)
#     plt.title(title)
#     plt.tight_layout()
#     plt.show()

# # Optional: consistent language order by median runtime (fastest to slowest)
# lang_order = (
#     df.groupby("lang")["z1000t"]
#       .median()
#       .sort_values()
#       .index
#       .tolist()
# )

# # --- Plots (one figure per analysis) ---

# # 1) Runtime (speed) by language
# boxplot(df, x="lang", y="z1000t",
#         title="Runtime (z1000t) by Programming Language",
#         ylabel="Minutes", order=lang_order)

# # 2) Startup time (baseline) by language
# boxplot(df, x="lang", y="z0t",
#         title="Startup Time (z0t) by Programming Language",
#         ylabel="Minutes", order=lang_order)

# # 3) Scalability / efficiency growth (ratio)
# boxplot(df, x="lang", y="scaling_ratio",
#         title="Scaling Ratio (z1000t / z0t) by Language",
#         ylabel="Ratio (higher = worse scaling)", order=lang_order)

# # 4) Memory usage by language
# barplot(df, x="lang", y="z1000mem",
#         title="Average Memory Usage (z1000mem) by Language",
#         ylabel="KB", order=lang_order, estimator=np.mean)

# # 5) Reliability across problem types (grouped bar)
# plt.figure()
# sns.barplot(data=rel_long, x="lang", y="reliability", hue="test", order=lang_order, errorbar="se")
# plt.title("Reliability by Language (z1000rel vs m1000rel)")
# plt.xlabel("Language")
# plt.ylabel("Reliability (%)")
# plt.legend(title="Test", bbox_to_anchor=(1.02, 1), loc="upper left")
# plt.tight_layout()
# plt.show()

# # 6) Code size vs runtime
# scatter(df, x="stmtL", y="z1000t",
#         hue="lang", title="Code Size (stmtL) vs Runtime (z1000t)",
#         xlabel="Statement Lines of Code", ylabel="Runtime (minutes)")

# # 7) Effort vs reliability
# scatter(df, x="whours", y="z1000rel",
#         hue="lang", title="Work Hours (whours) vs Reliability (z1000rel)",
#         xlabel="Work Hours", ylabel="Reliability (%)")

# # 8) Correlation heatmap (numeric features only)
# num_cols = ["z0t", "z1000t", "z1000mem", "z1000rel", "m1000rel", "whours", "stmtL", "scaling_ratio"]
# corr_heatmap(df[num_cols], title="Correlation Heatmap (Performance, Reliability, Effort)")

# # 9) Runtime vs memory trade-off
# scatter(df, x="z1000t", y="z1000mem",
#         hue="lang", title="Runtime (z1000t) vs Memory Usage (z1000mem)",
#         xlabel="Runtime (minutes)", ylabel="Memory (KB)")

# # 10) Distribution of work time
# hist(df, x="whours", title="Distribution of Work Hours (whours)", bins=18, xlabel="Work Hours")
